
def recommend_algorithm(metrics_list, objective="balanced"):
    """
    Rank disk scheduling algorithms using performance metrics.

    Objectives:
    1. minimum_movement
    2. balanced
    """

    if not metrics_list:
        raise ValueError("No performance metrics provided")

    movement_values = [
        item["total_head_movement"]
        for item in metrics_list
    ]

    direction_values = [
        item["direction_changes"]
        for item in metrics_list
    ]

    min_movement = min(movement_values)
    max_movement = max(movement_values)

    min_direction = min(direction_values)
    max_direction = max(direction_values)

    movement_range = max_movement - min_movement
    direction_range = max_direction - min_direction

    rankings = []

    for item in metrics_list:

        movement = item["total_head_movement"]
        changes = item["direction_changes"]

        # Normalize movement: lower is better
        movement_score = (
            (movement - min_movement) / movement_range
            if movement_range else 0
        )

        # Normalize direction changes: lower is better
        direction_score = (
            (changes - min_direction) / direction_range
            if direction_range else 0
        )

        if objective == "minimum_movement":
            final_score = movement_score * 100

        elif objective == "balanced":
            final_score = (
                movement_score * 0.85 +
                direction_score * 0.15
            ) * 100

        else:
            raise ValueError("Unknown recommendation objective")

        rankings.append({
            "algorithm": item["algorithm"],
            "total_head_movement": movement,
            "direction_changes": changes,
            "score": round(final_score, 2)
        })

    # Lower score indicates better performance
    rankings.sort(
        key=lambda x: (
            x["score"],
            x["total_head_movement"],
            x["algorithm"]
        )
    )

    best = rankings[0]

    if objective == "minimum_movement":
        reason = (
            "Selected because it has the lowest total "
            "disk head movement."
        )
    else:
        reason = (
            "Selected using a weighted comparison of "
            "head movement (85%) and direction changes (15%)."
        )

    warnings = []

    if best["algorithm"] == "SSTF":
        warnings.append(
            "SSTF may cause starvation of requests that "
            "remain far from the disk head."
        )

    warnings.append(
        "This recommendation is based on a static request "
        "queue and does not measure actual waiting-time fairness."
    )

    return {
        "recommended_algorithm": best["algorithm"],
        "objective": objective,
        "reason": reason,
        "recommended_score": best["score"],
        "rankings": rankings,
        "warnings": warnings
    }
