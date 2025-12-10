#!/usr/bin/env python3
"""
scripts/generate_sim_data.py

Genera CSV sintetici per:
 - api_requests.csv
 - pod_events.csv
 - metrics.csv

Uso:
  python scripts/generate_sim_data.py --days 1 --outdir data --seed 42
"""

import argparse
import os
from datetime import datetime, timedelta, timezone
import random
import uuid

import numpy as np
import pandas as pd

# ---------- Config defaults ----------
DEFAULT_OUTDIR = "data"
DEFAULT_DAYS = 1
METRICS_RES_SEC = 10  # sample ogni 10 secondi
BASE_RATE_PER_SEC = 5  # richieste base per secondo (tasso lambda)
SPIKE_PROB_PER_HOUR = 0.5  # probabilità di spike ogni ora
SEED = 42

ENDPOINTS = [
    ("/api/v1/devices", "GET"),
    ("/api/v1/devices", "POST"),
    ("/api/v1/data", "GET"),
    ("/api/v1/data", "POST"),
    ("/api/v1/auth", "POST"),
]

# ---------- Helpers ----------
def iso(ts: datetime):
    return ts.astimezone(timezone.utc).isoformat().replace("+00:00", "Z")

# ---------- Generators ----------
def generate_request_stream(start: datetime, end: datetime, base_rate=BASE_RATE_PER_SEC,
                            spike_prob_hour=SPIKE_PROB_PER_HOUR, seed=SEED):
    """
    Genera una lista di richieste con timestamp, endpoint, method, status, latency_ms, bytes.
    Usa un Poisson process con occasionali spike cluster.
    """
    rng = np.random.default_rng(seed)
    t = start
    requests = []

    total_seconds = int((end - start).total_seconds())
    for sec in range(total_seconds):
        # modulazione oraria: picco diurno semplice (sinus)
        hour_of_day = (start + timedelta(seconds=sec)).hour
        diurnal = 1.0 + 0.6 * np.sin((hour_of_day / 24.0) * 2 * np.pi)

        # occasional spike (cluster): se triggered, aumentiamo il lambda in quell'ora
        if rng.random() < (spike_prob_hour / 3600.0):  # convert hour prob to per-second small chance
            # crea un breve burst durato 10-60s
            burst_len = rng.integers(10, 61)
            burst_multiplier = rng.uniform(5, 20)
            for b in range(burst_len):
                lam = base_rate * diurnal * burst_multiplier
                k = rng.poisson(lam)
                ts = start + timedelta(seconds=sec + b)
                for i in range(k):
                    ep, method = random.choice(ENDPOINTS)
                    status = rng.choice([200, 201, 400, 401, 500], p=[0.88, 0.03, 0.04, 0.02, 0.03])
                    latency = max(1.0, rng.lognormal(mean=3.0, sigma=0.8))  # ms-ish scale
                    size = int(max(100, rng.normal(800, 600)))
                    requests.append({
                        "timestamp": iso(ts),
                        "endpoint": ep,
                        "method": method,
                        "status": int(status),
                        "latency_ms": float(latency),
                        "bytes": int(size)
                    })
            # skip ahead burst_len seconds
            continue

        lam = base_rate * diurnal
        k = rng.poisson(lam)
        ts = start + timedelta(seconds=sec)
        for i in range(k):
            ep, method = random.choice(ENDPOINTS)
            status = rng.choice([200, 201, 400, 401, 500], p=[0.9, 0.03, 0.03, 0.02, 0.02])
            latency = max(1.0, rng.lognormal(mean=3.1, sigma=0.6))
            # add slight correlation: higher latency when lam high
            latency *= (1.0 + min(2.0, lam / (base_rate * 2.0)))
            size = int(max(100, rng.normal(900, 500)))
            requests.append({
                "timestamp": iso(ts),
                "endpoint": ep,
                "method": method,
                "status": int(status),
                "latency_ms": float(latency),
                "bytes": int(size)
            })

    df = pd.DataFrame(requests)
    return df

def generate_metric_series(start: datetime, end: datetime, pods, res_seconds=METRICS_RES_SEC, seed=SEED+1):
    """
    Genera metriche regolari ogni res_seconds per ogni pod:
    - cpu_core_usage: in cores (es 0.1-2.0)
    - memory_mb
    - requests_in_flight: numero stimato correlato al rate
    """
    rng = np.random.default_rng(seed)
    timestamps = list(pd.date_range(start, end, freq=f"{res_seconds}S", tz=timezone.utc))
    rows = []
    # keep a memory baseline per pod
    pod_mem_baseline = {p: rng.integers(200, 700) for p in pods}  # MB
    for ts in timestamps:
        # basic global load factor (simulate diurnal)
        hour = ts.hour
        diurnal = 1.0 + 0.6 * np.sin((hour / 24.0) * 2 * np.pi)
        for p in pods:
            # CPU proportional to diurnal + some pod-specific noise
            cpu = max(0.01, rng.normal(0.2 * diurnal, 0.05))
            # memory has slow drift
            pod_mem_baseline[p] += rng.normal(0, 1.0)
            mem = max(50.0, pod_mem_baseline[p] + rng.normal(0, 10.0) + 50.0 * (cpu - 0.2))
            req_in_flight = max(0, int(rng.poisson(1.0 * diurnal * cpu * 20)))
            rows.append({
                "timestamp": iso(ts.to_pydatetime()),
                "pod_id": p,
                "cpu_cores": float(round(cpu, 3)),
                "memory_mb": float(round(mem, 2)),
                "requests_in_flight": int(req_in_flight)
            })
    df = pd.DataFrame(rows)
    return df

def simulate_scaling(start: datetime, end: datetime, initial_replicas=3,
                     min_replicas=1, max_replicas=10, cooldown_sec=60, seed=SEED+2):
    """
    Simula eventi di scaling basandosi su una regola semplice:
    - ogni minute controlla "simulated load" e scala di conseguenza.
    Restituisce dataframe di eventi con reason.
    """
    rng = np.random.default_rng(seed)
    ts = start
    replicas = initial_replicas
    last_scale_time = start - timedelta(seconds=cooldown_sec)
    events = []
    minute = timedelta(seconds=60)
    while ts <= end:
        # stima di load: sample casuale + orario
        hour = ts.hour
        diurnal = 1.0 + 0.6 * np.sin((hour / 24.0) * 2 * np.pi)
        estimated_rps = BASE_RATE_PER_SEC * diurnal * (1 + rng.normal(0, 0.1))
        per_pod = estimated_rps / max(1, replicas)
        replicas_before = replicas
        scaled = False
        reason = ""
        # simply: target replicas proportional to rps
        target = int(np.clip(np.ceil(estimated_rps / 10.0), min_replicas, max_replicas))
        if target > replicas and (ts - last_scale_time).total_seconds() >= cooldown_sec:
            replicas = min(max_replicas, replicas + 1)
            scaled = True
            reason = f"scale_up_target={target}"
            last_scale_time = ts
        elif target < replicas and (ts - last_scale_time).total_seconds() >= cooldown_sec:
            replicas = max(min_replicas, replicas - 1)
            scaled = True
            reason = f"scale_down_target={target}"
            last_scale_time = ts

        if scaled:
            events.append({
                "timestamp": iso(ts),
                "pod_id": f"pod-{rng.integers(1000,9999)}",
                "action": "scale_up" if replicas > replicas_before else "scale_down",
                "replicas_before": int(replicas_before),
                "replicas_after": int(replicas),
                "reason": reason
            })
        ts += minute
    df = pd.DataFrame(events)
    return df

# ---------- Main ----------
def main(args):
    random.seed(args.seed)
    np.random.seed(args.seed)

    start = datetime.now(timezone.utc)
    end = start + timedelta(days=args.days)

    os.makedirs(args.outdir, exist_ok=True)

    print(f"[info] Generating requests from {start.isoformat()} to {end.isoformat()} ...")
    req_df = generate_request_stream(start, end, base_rate=args.base_rate, spike_prob_hour=args.spike_prob_hour, seed=args.seed)
    req_path = os.path.join(args.outdir, "api_requests.csv")
    req_df.to_csv(req_path, index=False)
    print(f"[info] Wrote {len(req_df)} requests to {req_path}")

    # simple pods list (based on initial replicas)
    initial_replicas = args.initial_replicas
    pods = [f"pod-{i+1}" for i in range(initial_replicas)]

    print("[info] Generating metrics series ...")
    metrics_df = generate_metric_series(start, end, pods, res_seconds=args.metrics_res_sec, seed=args.seed+1)
    metrics_path = os.path.join(args.outdir, "metrics.csv")
    metrics_df.to_csv(metrics_path, index=False)
    print(f"[info] Wrote {len(metrics_df)} metric rows to {metrics_path}")

    print("[info] Simulating scaling events ...")
    pod_events_df = simulate_scaling(start, end, initial_replicas=initial_replicas,
                                     min_replicas=args.min_replicas, max_replicas=args.max_replicas,
                                     cooldown_sec=args.cooldown_sec, seed=args.seed+2)
    events_path = os.path.join(args.outdir, "pod_events.csv")
    pod_events_df.to_csv(events_path, index=False)
    print(f"[info] Wrote {len(pod_events_df)} pod events to {events_path}")

if __name__ == "__main__":
    p = argparse.ArgumentParser()
    p.add_argument("--days", type=int, default=DEFAULT_DAYS, help="numero di giorni da simulare")
    p.add_argument("--outdir", type=str, default=DEFAULT_OUTDIR, help="cartella di output")
    p.add_argument("--seed", type=int, default=SEED, help="seed per riproducibilità")
    p.add_argument("--base-rate", type=float, default=BASE_RATE_PER_SEC, help="tasso base req/sec")
    p.add_argument("--spike-prob-hour", type=float, default=SPIKE_PROB_PER_HOUR, help="probabilità di spike per ora")
    p.add_argument("--metrics-res-sec", type=int, default=METRICS_RES_SEC, help="risoluzione (s) per metriche")
    p.add_argument("--initial-replicas", type=int, default=3)
    p.add_argument("--min-replicas", type=int, default=1)
    p.add_argument("--max-replicas", type=int, default=10)
    p.add_argument("--cooldown-sec", type=int, default=60)
    args = p.parse_args()
    main(args)
