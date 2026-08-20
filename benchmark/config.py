from pathlib import Path

# Project root
BASE_DIR = Path(__file__).resolve().parent.parent

# Dataset
DATASET_PATH = BASE_DIR / "dataset" / "cit-HepPh.txt.gz"

# Results
RESULTS_DIR = BASE_DIR / "results"

# Benchmark settings
WARMUP_RUNS = 10
MEASURED_RUNS = 100

# Concurrency levels
CONCURRENCY_LEVELS = [1, 5, 10, 25]

# Dataset information from SNAP
DATASET_NAME = "cit-HepPh"