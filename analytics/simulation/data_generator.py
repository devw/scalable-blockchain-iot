import random
from datetime import datetime, timedelta

class DataGenerator:
    def __init__(self, max_pods=5, pod_scale_threshold=50):
        """
        max_pods: maximum number of pods allowed
        pod_scale_threshold: requests_in_flight threshold to trigger scaling
        """
        self.max_pods = max_pods
        self.pod_scale_threshold = pod_scale_threshold
        self.current_pod_count = 1

    def generate_minute_data(self):
        """
        Generate a single timestamp data point with:
        - rps: requests per second
        - requests_in_flight: number of active requests
        - latency_ms: simulated latency in ms
        - pod_count: number of pods needed
        """
        # Simulate RPS and requests in flight with randomness
        rps = random.randint(50, 150)                # base traffic + random
        requests_in_flight = rps + random.randint(0, 50)  # occasional spikes

        # Simple latency model: increases with requests_in_flight
        latency_ms = 50 + requests_in_flight * 0.75

        # Scaling logic
        if requests_in_flight > self.pod_scale_threshold:
            self.current_pod_count = min(self.max_pods, self.current_pod_count + 1)
        else:
            # Optional: scale down slowly
            self.current_pod_count = max(1, self.current_pod_count - 1)

        return {
            "rps": rps,
            "requests_in_flight": requests_in_flight,
            "latency_ms": latency_ms,
            "pod_count": self.current_pod_count
        }

    def generate_request_data(self, timestamp, duration_seconds=60):
        """
        Generate individual request records for a time window.
        
        Args:
            timestamp (datetime): Start time for this window
            duration_seconds (int): Length of window (default 60 for 1 minute)
            
        Returns:
            list of dict: Individual request records
        """
        requests = []
        
        # Get aggregated metrics for this minute (reuse existing logic)
        minute_stats = self.generate_minute_data()
        
        rps = minute_stats['rps']
        base_latency = minute_stats['latency_ms']
        base_in_flight = minute_stats['requests_in_flight']
        pod_count = minute_stats['pod_count']
        
        # Generate individual requests for this minute
        num_requests = rps  # requests in this 1-second window (will be called 60 times)
        
        for i in range(num_requests):
            # Spread requests across the second with some jitter
            offset_ms = (i / num_requests * 1000) + random.uniform(-50, 50)
            offset_ms = max(0, min(999, offset_ms))  # Keep within 0-999ms
            
            request_timestamp = timestamp + timedelta(milliseconds=offset_ms)
            
            # Add realistic variance to latency (±15% standard deviation)
            latency_variance = random.gauss(0, base_latency * 0.15)
            latency = max(10, base_latency + latency_variance)  # Min 10ms
            
            # Add small variance to in-flight requests
            in_flight_variance = random.randint(-3, 3)
            in_flight = max(0, base_in_flight + in_flight_variance)
            
            # Assign to a pod (round-robin style)
            pod_id = f"pod-{(i % pod_count) + 1}"
            
            # 1% error rate (can be adjusted)
            success = random.random() > 0.01
            
            requests.append({
                'request_id': f"req_{int(request_timestamp.timestamp() * 1000000)}",
                'timestamp': request_timestamp.isoformat(),
                'latency_ms': round(latency, 2),
                'requests_in_flight': in_flight,
                'pod_id': pod_id,
                'success': success
            })
        
        return requests

