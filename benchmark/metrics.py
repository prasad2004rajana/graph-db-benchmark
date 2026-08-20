import statistics


def percentile(values, percentile):
    if not values:
        return None

    sorted_values = sorted(values)

    index = (len(sorted_values) - 1) * percentile / 100
    lower = int(index)
    upper = min(lower + 1, len(sorted_values) - 1)

    weight = index - lower

    return (
        sorted_values[lower]
        + weight * (sorted_values[upper] - sorted_values[lower])
    )


def calculate_latency_metrics(latencies):
    return {
        "min_ms": min(latencies),
        "max_ms": max(latencies),
        "mean_ms": statistics.mean(latencies),
        "p50_ms": percentile(latencies, 50),
        "p95_ms": percentile(latencies, 95),
    }