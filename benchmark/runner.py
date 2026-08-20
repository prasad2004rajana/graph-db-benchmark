import time

from metrics import calculate_latency_metrics


def benchmark_operation(operation, runs=100):
    latencies = []

    # Warm-up
    for _ in range(10):
        operation()

    # Measurement
    for _ in range(runs):
        start = time.perf_counter()

        operation()

        end = time.perf_counter()

        latency_ms = (end - start) * 1000
        latencies.append(latency_ms)

    return calculate_latency_metrics(latencies)