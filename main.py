"""
Mini-Courier Planner
Design and Analysis of Algorithms (ETCCDA302)
Algorithms: Merge Sort, 0/1 Knapsack (Dynamic Programming),
Dijkstra's Shortest Path, and Nearest-Neighbor TSP Approximation.
"""

import json
import heapq
import time
import random
from pathlib import Path

ROOT = Path(__file__).resolve().parent


def merge_sort_parcels(parcels):
    """Sort by higher priority first, then earlier deadline."""
    if len(parcels) <= 1:
        return parcels[:]

    mid = len(parcels) // 2
    left = merge_sort_parcels(parcels[:mid])
    right = merge_sort_parcels(parcels[mid:])

    result = []
    i = j = 0
    while i < len(left) and j < len(right):
        a = left[i]
        b = right[j]
        # Higher priority comes first. If equal, earlier deadline comes first.
        if (a["priority"] > b["priority"] or
                (a["priority"] == b["priority"] and
                 a["deadline"] <= b["deadline"])):
            result.append(a)
            i += 1
        else:
            result.append(b)
            j += 1

    result.extend(left[i:])
    result.extend(right[j:])
    return result


def knapsack_dp(parcels, capacity):
    """Return maximum-value parcel selection using 0/1 Knapsack DP."""
    n = len(parcels)
    dp = [[0 for _ in range(capacity + 1)] for _ in range(n + 1)]

    for i in range(1, n + 1):
        weight = parcels[i - 1]["weight"]
        value = parcels[i - 1]["value"]
        for cap in range(capacity + 1):
            dp[i][cap] = dp[i - 1][cap]
            if weight <= cap:
                take = value + dp[i - 1][cap - weight]
                if take > dp[i][cap]:
                    dp[i][cap] = take

    selected = []
    cap = capacity
    for i in range(n, 0, -1):
        if dp[i][cap] != dp[i - 1][cap]:
            selected.append(parcels[i - 1])
            cap -= parcels[i - 1]["weight"]

    selected.reverse()
    return selected, dp[n][capacity], dp


def dijkstra(graph, start):
    """Find shortest distances and paths from start to every reachable node."""
    distances = {node: float("inf") for node in graph}
    previous = {node: None for node in graph}
    distances[start] = 0
    priority_queue = [(0, start)]

    while priority_queue:
        current_distance, current = heapq.heappop(priority_queue)
        if current_distance != distances[current]:
            continue

        for neighbor, weight in graph[current].items():
            new_distance = current_distance + weight
            if new_distance < distances[neighbor]:
                distances[neighbor] = new_distance
                previous[neighbor] = current
                heapq.heappush(priority_queue, (new_distance, neighbor))

    return distances, previous


def get_path(previous, start, end):
    """Rebuild a shortest path using Dijkstra's previous-node map."""
    path = []
    current = end
    while current is not None:
        path.append(current)
        current = previous[current]
    path.reverse()
    if not path or path[0] != start:
        return []
    return path


def nearest_neighbor_tsp(graph, start, destinations):
    """
    Approximate a delivery tour. At each step choose the nearest unvisited
    destination using Dijkstra shortest-path distance.
    """
    remaining = list(dict.fromkeys(destinations))
    if start in remaining:
        remaining.remove(start)

    route = [start]
    total_distance = 0
    current = start
    route_legs = []

    while remaining:
        distances, previous = dijkstra(graph, current)
        reachable = [node for node in remaining if distances.get(node, float("inf")) < float("inf")]
        if not reachable:
            break

        next_node = min(reachable, key=lambda node: distances[node])
        leg_distance = distances[next_node]
        leg_path = get_path(previous, current, next_node)
        route_legs.append({"from": current, "to": next_node,
                           "path": leg_path, "distance": leg_distance})
        total_distance += leg_distance
        route.append(next_node)
        remaining.remove(next_node)
        current = next_node

    # Return to depot to complete the tour when possible.
    distances, previous = dijkstra(graph, current)
    if start in distances and distances[start] < float("inf") and current != start:
        leg_path = get_path(previous, current, start)
        route_legs.append({"from": current, "to": start,
                           "path": leg_path, "distance": distances[start]})
        total_distance += distances[start]
        route.append(start)

    return route, total_distance, route_legs


def load_data():
    file_path = ROOT / "data" / "sample_data.json"
    with open(file_path, "r", encoding="utf-8") as file:
        return json.load(file)


def run_planner(show=True):
    data = load_data()
    parcels = data["parcels"]
    graph = data["graph"]
    capacity = data["vehicle_capacity"]
    depot = data["depot"]

    start = time.perf_counter()
    sorted_parcels = merge_sort_parcels(parcels)
    sort_time = time.perf_counter() - start

    start = time.perf_counter()
    selected, total_value, dp_table = knapsack_dp(sorted_parcels, capacity)
    knapsack_time = time.perf_counter() - start

    destinations = [parcel["destination"] for parcel in selected]
    start = time.perf_counter()
    route, route_distance, legs = nearest_neighbor_tsp(graph, depot, destinations)
    route_time = time.perf_counter() - start

    result = {
        "sorted_parcels": sorted_parcels,
        "selected_parcels": selected,
        "total_value": total_value,
        "total_weight": sum(p["weight"] for p in selected),
        "capacity": capacity,
        "route": route,
        "route_distance": route_distance,
        "route_legs": legs,
        "timings_seconds": {
            "merge_sort": sort_time,
            "knapsack_dp": knapsack_time,
            "route_planning": route_time
        }
    }

    if show:
        print("\n========== MINI-COURIER PLANNER ==========")
        print("\n1. PARCELS SORTED BY PRIORITY / DEADLINE")
        for p in sorted_parcels:
            print(f'{p["id"]}: priority={p["priority"]}, deadline={p["deadline"]}, '
                  f'weight={p["weight"]}, value={p["value"]}, destination={p["destination"]}')

        print("\n2. OPTIMAL PACKING PLAN (0/1 KNAPSACK)")
        for p in selected:
            print(f'{p["id"]} -> weight {p["weight"]}, value {p["value"]}')
        print(f'Total weight: {result["total_weight"]}/{capacity}')
        print(f'Total value: {total_value}')

        print("\n3. DELIVERY ROUTE")
        print(" -> ".join(route))
        print(f"Total route distance: {route_distance}")
        for leg in legs:
            print(f'{leg["from"]} to {leg["to"]}: '
                  f'{" -> ".join(leg["path"])} (distance {leg["distance"]})')

        print("\n4. OBSERVED EXECUTION TIMES")
        for name, value in result["timings_seconds"].items():
            print(f"{name}: {value:.8f} seconds")
        print("==========================================\n")

    return result


def benchmark():
    """Measure the sorting and knapsack components for increasing input sizes."""
    sizes = [10, 20, 40, 80, 120]
    sort_times = []
    dp_times = []
    for size in sizes:
        parcels = []
        for i in range(size):
            parcels.append({
                "id": f"P{i}", "priority": random.randint(1, 5),
                "deadline": random.randint(1, 30),
                "weight": random.randint(1, 10),
                "value": random.randint(10, 100),
                "destination": "A"
            })

        start = time.perf_counter()
        merge_sort_parcels(parcels)
        sort_times.append(time.perf_counter() - start)

        # Keep capacity fixed to isolate the effect of increasing parcel count.
        start = time.perf_counter()
        knapsack_dp(parcels, 50)
        dp_times.append(time.perf_counter() - start)

    return sizes, sort_times, dp_times


if __name__ == "__main__":
    run_planner()
    sizes, sort_times, dp_times = benchmark()
    print("Benchmark (parcel count, merge-sort seconds, knapsack seconds):")
    for i in range(len(sizes)):
        print(f"{sizes[i]}, {sort_times[i]:.8f}, {dp_times[i]:.8f}")
