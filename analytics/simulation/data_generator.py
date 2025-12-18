import random
import math
from datetime import datetime, timedelta

class DataGenerator:
    def __init__(self, max_pods=5, pod_scale_threshold=50):
        self.max_pods = max_pods
        self.pod_scale_threshold = pod_scale_threshold
        self.current_pod_count = 1
        self.simulation_time = 0.0  # Tempo in secondi dall'inizio simulazione
        
        # Parametri per pattern sinusoidale
        self.sine_period = 120  # Periodo completo: 2 minuti
        self.base_rps = 50      # RPS medio
        self.sine_amplitude = 20  # Oscillazione ±20 RPS
        
        # Parametri per spike
        self.spike_interval = 90   # Spike ogni 90 secondi
        self.spike_duration = 30   # Durata spike: 30 secondi
        self.spike_rps = 150       # RPS durante spike

    def _latency(self, in_flight, pods):
        return 50 + (in_flight / pods) * 0.75

    def _calculate_rps(self, time_seconds):
        """Calcola RPS basato su pattern sinusoidale + spike."""
        # Pattern sinusoidale base
        sine_value = math.sin(2 * math.pi * time_seconds / self.sine_period)
        base_rps = self.base_rps + (sine_value * self.sine_amplitude)
        
        # Controlla se siamo in uno spike
        time_in_cycle = time_seconds % self.spike_interval
        if time_in_cycle < self.spike_duration:
            # Durante spike: interpolazione tra base e spike
            spike_progress = time_in_cycle / self.spike_duration
            spike_factor = math.sin(spike_progress * math.pi)  # Curva smooth
            rps = base_rps + (self.spike_rps - base_rps) * spike_factor
        else:
            rps = base_rps
        
        # Aggiungi piccola variabilità
        rps = rps + random.uniform(-5, 5)
        
        return max(10, int(rps))  # Minimo 10 RPS

    def generate_minute_data(self):
        rps = self._calculate_rps(self.simulation_time)
        
        # Calcola requests_in_flight basato su RPS
        requests_in_flight = rps + random.randint(0, 30)
        
        latency_ms = self._latency(requests_in_flight, self.current_pod_count)
        
        # Logica scaling pods (graduale)
        if requests_in_flight > self.pod_scale_threshold * self.current_pod_count:
            self.current_pod_count = min(self.max_pods, self.current_pod_count + 1)
        elif requests_in_flight < self.pod_scale_threshold * (self.current_pod_count - 1):
            self.current_pod_count = max(1, self.current_pod_count - 1)
        
        return {
            "rps": rps,
            "requests_in_flight": requests_in_flight,
            "latency_ms": latency_ms,
            "pod_count": self.current_pod_count
        }

    def generate_request_data(self, timestamp, duration_seconds=60, start_time=None):
        if start_time is None:
            start_time = timestamp
        
        stats = self.generate_minute_data()
        rps, base_in_flight, pod_count = stats['rps'], stats['requests_in_flight'], stats['pod_count']
        
        base_interval_ms = (duration_seconds * 1000) / rps if rps > 0 else 1000
        
        rows = []
        current_offset_ms = 0.0
        
        for i in range(rps):
            jitter = random.uniform(0, min(base_interval_ms * 0.3, 20))
            current_offset_ms += jitter
            
            ts = timestamp + timedelta(milliseconds=current_offset_ms)
            
            rows.append({
                'request_id': format(hash((timestamp, i)) & 0xFFFFF, 'x'),
                'timestamp': (ts - start_time).total_seconds(),
                'latency_ms': round(max(10, self._latency(base_in_flight, pod_count) + random.gauss(0, self._latency(base_in_flight, pod_count) * 0.15)), 2),
                'requests_in_flight': max(0, base_in_flight + random.randint(-3, 3)),
                'pod_id': f"pod-{(i % pod_count) + 1}",
                'pod_count': pod_count,
                'success': random.random() > 0.01
            })
            
            current_offset_ms += base_interval_ms
        
        # Avanza il tempo di simulazione
        self.simulation_time += duration_seconds
        
        return rows