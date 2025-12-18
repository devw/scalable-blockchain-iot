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

    def generate_request_data(self, timestamp, duration_seconds=60):
        stats = self.generate_minute_data()
        rps, base_in_flight, pod_count = stats['rps'], stats['requests_in_flight'], stats['pod_count']
        
        return [
            {
                'request_id': format(hash(ts := timestamp + timedelta(milliseconds=max(0, min(999, (i/rps*1000) + random.uniform(-50, 50))))) & 0xFFFFF, 'x'),
                'timestamp': (ts - timestamp).total_seconds(),
                'latency_ms': round(max(10, self._latency(base_in_flight, pod_count) + random.gauss(0, self._latency(base_in_flight, pod_count) * 0.15)), 2),
                'requests_in_flight': max(0, base_in_flight + random.randint(-3, 3)),
                'pod_id': f"pod-{(i % pod_count) + 1}",
                'pod_count': pod_count,
                'success': random.random() > 0.01
            }
            for i in range(rps)
        ]