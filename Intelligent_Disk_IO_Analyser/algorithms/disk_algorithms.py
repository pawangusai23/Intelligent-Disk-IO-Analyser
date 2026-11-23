
def run_algorithm(name, requests, head, disk_size, direction):

    left = sorted(x for x in requests if x < head)
    right = sorted(x for x in requests if x >= head)

    if name == "FCFS":
        order = list(requests)
        path = [head] + order

    elif name == "SSTF":
        pending = list(requests)
        order = []
        current = head

        while pending:
            nearest = min(
                pending,
                key=lambda x: (abs(x - current), x)
            )
            order.append(nearest)
            pending.remove(nearest)
            current = nearest

        path = [head] + order

    elif name == "SCAN":
        if direction == "right":
            order = right + list(reversed(left))
            path = [head] + right

            if left:
                path += [disk_size - 1] + list(reversed(left))
        else:
            order = list(reversed(left)) + right
            path = [head] + list(reversed(left))

            if right:
                path += [0] + right

    elif name == "C-SCAN":
        if direction == "right":
            order = right + left
            path = [head] + right

            if left:
                path += [disk_size - 1, 0] + left
        else:
            order = list(reversed(left)) + list(reversed(right))
            path = [head] + list(reversed(left))

            if right:
                path += [0, disk_size - 1] + list(reversed(right))

    elif name == "LOOK":
        if direction == "right":
            order = right + list(reversed(left))
        else:
            order = list(reversed(left)) + right

        path = [head] + order

    elif name == "C-LOOK":
        if direction == "right":
            order = right + left
        else:
            order = list(reversed(left)) + list(reversed(right))

        path = [head] + order

    else:
        raise ValueError(f"Unknown algorithm: {name}")

    return {
        "algorithm": name,
        "service_order": order,
        "movement_path": path
    }
