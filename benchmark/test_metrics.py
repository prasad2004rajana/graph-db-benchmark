from metrics import calculate_latency_metrics


latencies = [
    10, 12, 11, 15, 13,
    20, 18, 14, 16, 12
]

result = calculate_latency_metrics(latencies)

print("Benchmark metrics:")
print(f"Min:  {result['min_ms']:.2f} ms")
print(f"Max:  {result['max_ms']:.2f} ms")
print(f"Mean: {result['mean_ms']:.2f} ms")
print(f"P50:  {result['p50_ms']:.2f} ms")
print(f"P95:  {result['p95_ms']:.2f} ms")