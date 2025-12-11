import random

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
