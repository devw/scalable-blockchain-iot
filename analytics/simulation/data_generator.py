import random
from datetime import datetime, timedelta

class DataGenerator:
    def __init__(self, max_pods=5, pod_scale_threshold=50):
        self.max_pods, self.pod_scale_threshold, self.current_pod_count = max_pods, pod_scale_threshold, 1

    def _latency(self, in_flight, pods): return 50 + (in_flight / pods) * 0.75

    def generate_minute_data(self):
        rps, in_flight = random.randint(50, 150), lambda r: r + random.randint(0, 50)
        requests_in_flight = in_flight(rps)
        latency_ms = self._latency(requests_in_flight, self.current_pod_count)
        self.current_pod_count = min(self.max_pods, self.current_pod_count + 1) if requests_in_flight > self.pod_scale_threshold else max(1, self.current_pod_count - 1)
        return {"rps": rps, "requests_in_flight": requests_in_flight, "latency_ms": latency_ms, "pod_count": self.current_pod_count}

    def generate_request_data(self, timestamp, duration_seconds=60, start_time=None):
        # Se start_time non è fornito, usa timestamp come riferimento (backward compatibility)
        if start_time is None:
            start_time = timestamp
        
        stats = self.generate_minute_data()
        rps, base_in_flight, pod_count = stats['rps'], stats['requests_in_flight'], stats['pod_count']
        
        # Calcola l'intervallo base tra richieste
        base_interval_ms = (duration_seconds * 1000) / rps
        
        rows = []
        current_offset_ms = 0.0
        
        for i in range(rps):
            # Aggiungi variabilità casuale mantenendo monotonia
            jitter = random.uniform(0, min(base_interval_ms * 0.3, 20))
            current_offset_ms += jitter
            
            ts = timestamp + timedelta(milliseconds=current_offset_ms)
            
            rows.append({
                'request_id': format(hash((timestamp, i)) & 0xFFFFF, 'x'),
                'timestamp': (ts - start_time).total_seconds(),  # ← Usa start_time invece di timestamp
                'latency_ms': round(max(10, self._latency(base_in_flight, pod_count) + random.gauss(0, self._latency(base_in_flight, pod_count) * 0.15)), 2),
                'requests_in_flight': max(0, base_in_flight + random.randint(-3, 3)),
                'pod_id': f"pod-{(i % pod_count) + 1}",
                'pod_count': pod_count,
                'success': random.random() > 0.01
            })
            
            # Avanza al prossimo intervallo base
            current_offset_ms += base_interval_ms
        
        return rows