
from algorithms.disk_algorithms import run_algorithm
from core.metrics import calculate_metrics
from core.recommender import recommend_algorithm

requests = [98, 183, 37, 122, 14, 124, 65, 67]

algorithms = [
    "FCFS",
    "SSTF",
    "SCAN",
    "C-SCAN",
    "LOOK",
    "C-LOOK"
]

all_metrics = []

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

    all_metrics.append(metrics)


# Test minimum movement recommendation
print("\nMINIMUM MOVEMENT RECOMMENDATION")
print("=" * 50)

minimum_result = recommend_algorithm(
    all_metrics,
    objective="minimum_movement"
)

print("Recommended:", minimum_result["recommended_algorithm"])
print("Reason:", minimum_result["reason"])

# Test balanced recommendation
print("\nBALANCED RECOMMENDATION")
print("=" * 50)

balanced_result = recommend_algorithm(
    all_metrics,
    objective="balanced"
)

print("Recommended:", balanced_result["recommended_algorithm"])
print("Reason:", balanced_result["reason"])

print("\nALGORITHM RANKINGS")
print("=" * 50)

for rank, item in enumerate(
    balanced_result["rankings"], start=1
):
    print(
        f"{rank}. {item['algorithm']} | "
        f"Movement: {item['total_head_movement']} | "
        f"Direction changes: {item['direction_changes']} | "
        f"Score: {item['score']}"
    )

print("\nWARNINGS")

for warning in balanced_result["warnings"]:
    print("-", warning)

print("\nRecommendation analysis completed.")