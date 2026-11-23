
def calculate_metrics(result, seek_time_per_cylinder=0.1, direction="right"):
    """
    Calculate disk scheduling performance metrics.

    seek_time_per_cylinder is an illustrative configurable
    estimate in milliseconds per cylinder.
    """

    path = result["movement_path"]
    algorithm = result["algorithm"]
    service_order = result["service_order"]

    if not path:
        raise ValueError("Movement path cannot be empty")

    # Calculate movement between consecutive head positions
    movements = [
        abs(path[i] - path[i - 1])
        for i in range(1, len(path))
    ]

    total_movement = sum(movements)

    request_count = len(service_order)

    average_movement = (
        total_movement / request_count
        if request_count > 0 else 0
    )

    # Determine actual direction changes
    deltas = [
        path[i] - path[i - 1]
        for i in range(1, len(path))
    ]

    # Remove circular wrap transitions.
    if algorithm in ("C-SCAN", "C-LOOK"):
        if direction == "right":
            deltas = [d for d in deltas if d >= 0]
        else:
            deltas = [d for d in deltas if d <= 0]

    nonzero_directions = [
        1 if d > 0 else -1
        for d in deltas if d != 0
    ]

    direction_changes = sum(
        nonzero_directions[i] != nonzero_directions[i - 1]
        for i in range(1, len(nonzero_directions))
    )

    estimated_seek_time = (
        total_movement * seek_time_per_cylinder
    )

    return {
        "algorithm": algorithm,
        "total_head_movement": total_movement,
        "average_head_movement": round(average_movement, 2),
        "direction_changes": direction_changes,
        "requests_serviced": request_count,
        "estimated_seek_time_ms": round(estimated_seek_time, 2)
    }
