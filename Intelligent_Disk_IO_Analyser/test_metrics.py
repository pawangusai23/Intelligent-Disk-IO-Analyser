
from algorithms.disk_algorithms import run_algorithm
from core.metrics import calculate_metrics

requests = [98, 183, 37, 122, 14, 124, 65, 67]

algorithms = [
    "FCFS",
    "SSTF",
    "SCAN",
    "C-SCAN",
    "LOOK",
    "C-LOOK"
]

print("\nDISK I/O PERFORMANCE ANALYSIS")
print("=" * 55)

for name in algorithms:

    result = run_algorithm(
        name=name,
        requests=requests,
        head=53,
        disk_size=200,
        direction="right"
    )

    metrics = calculate_metrics(
        result,
        seek_time_per_cylinder=0.1,
        direction="right"
    )

    print(f"\nAlgorithm: {name}")
    print("-" * 35)

    for key, value in metrics.items():
        print(f"{key}: {value}")

print("\nAnalysis completed successfully.")
