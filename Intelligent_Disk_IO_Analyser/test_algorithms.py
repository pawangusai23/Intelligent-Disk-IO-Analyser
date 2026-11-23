
from algorithms.disk_algorithms import run_algorithm

requests = [98, 183, 37, 122, 14, 124, 65, 67]

for name in [
    "FCFS",
    "SSTF",
    "SCAN",
    "C-SCAN",
    "LOOK",
    "C-LOOK"
]:
    result = run_algorithm(
        name=name,
        requests=requests,
        head=53,
        disk_size=200,
        direction="right"
    )

    print("\nAlgorithm:", name)
    print("Service order:", result["service_order"])
    print("Movement path:", result["movement_path"])
