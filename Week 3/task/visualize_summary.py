#!/usr/bin/env python3

"""
Usage:
    python visualize_summary.py output.json
    python visualize_summary.py output.json --save report.png

Speedup Definition:
    speedup = dijkstra_time / algorithm_time

Higher speedup is better.

Why Nodes Explored Matter:
    Runtime can vary depending on machine load and background
    processes, but nodes explored directly measures the amount
    of search work performed.

    A good heuristic should significantly reduce the number
    of expanded nodes while preserving optimality.

Expected Observation:
    Dijkstra explores the largest search space.

    A* Euclidean explores fewer nodes than Dijkstra.

    A* Manhattan usually performs best on 4-connected grids
    because the heuristic closely matches the true remaining
    path cost.

Json Input Format:
    {
        "meta": {...},
        "results": [
            {
                "id": 1,
                "dijkstra": {
                    "time_ms": ...,
                    "nodes_explored": ...
                },
                "astar_euclidean": {
                    "time_ms": ...,
                    "nodes_explored": ...
                },
                "astar_manhattan": {
                    "time_ms": ...,
                    "nodes_explored": ...
                }
            }
        ]
    }

Output:
    • Summary figure (PNG)
    • Terminal report containing aggregate statistics
"""

import json
import argparse
import numpy as np
import matplotlib.pyplot as plt


def main():
    # --------------------------------------------------
    # Command Line Arguments
    # --------------------------------------------------
    parser = argparse.ArgumentParser(
        description="Visualize A* vs Dijkstra performance summary"
    )

    parser.add_argument(
        "json_file",
        help="Path to output.json"
    )

    parser.add_argument(
        "--save",
        default="performance_summary.png",
        help="Output image filename"
    )

    args = parser.parse_args()

    # --------------------------------------------------
    # Load JSON Results
    # --------------------------------------------------
    with open(args.json_file, "r") as f:
        data = json.load(f)

    results = data["results"]

    if len(results) == 0:
        raise ValueError("No results found in output.json")

    algorithms = {
        "Dijkstra": {
            "times": [],
            "nodes": []
        },
        "A* Euclidean": {
            "times": [],
            "nodes": []
        },
        "A* Manhattan": {
            "times": [],
            "nodes": []
        }
    }

    # --------------------------------------------------
    # Parse Results
    # --------------------------------------------------
    for r in results:
        algorithms["Dijkstra"]["times"].append(
            r["dijkstra"]["time_ms"]
        )
        algorithms["Dijkstra"]["nodes"].append(
            r["dijkstra"]["nodes_explored"]
        )

        algorithms["A* Euclidean"]["times"].append(
            r["astar_euclidean"]["time_ms"]
        )
        algorithms["A* Euclidean"]["nodes"].append(
            r["astar_euclidean"]["nodes_explored"]
        )

        algorithms["A* Manhattan"]["times"].append(
            r["astar_manhattan"]["time_ms"]
        )
        algorithms["A* Manhattan"]["nodes"].append(
            r["astar_manhattan"]["nodes_explored"]
        )

    names = list(algorithms.keys())

    # --------------------------------------------------
    # Aggregate Metrics
    # --------------------------------------------------
    avg_times = [
        np.mean(algorithms[name]["times"])
        for name in names
    ]

    median_times = [
        np.median(algorithms[name]["times"])
        for name in names
    ]

    avg_nodes = [
        np.mean(algorithms[name]["nodes"])
        for name in names
    ]

    median_nodes = [
        np.median(algorithms[name]["nodes"])
        for name in names
    ]

    total_nodes = [
        np.sum(algorithms[name]["nodes"])
        for name in names
    ]

    # --------------------------------------------------
    # Speedup Calculation
    # --------------------------------------------------
    dijkstra_times = np.array(
        algorithms["Dijkstra"]["times"]
    )

    euclidean_times = np.array(
        algorithms["A* Euclidean"]["times"]
    )

    manhattan_times = np.array(
        algorithms["A* Manhattan"]["times"]
    )

    euclidean_speedup = np.mean(
        dijkstra_times / np.maximum(euclidean_times, 1e-9)
    )

    manhattan_speedup = np.mean(
        dijkstra_times / np.maximum(manhattan_times, 1e-9)
    )

    speedups = [
        1.0,
        euclidean_speedup,
        manhattan_speedup
    ]

    # --------------------------------------------------
    # Plot Summary Figure
    # --------------------------------------------------
    fig, axs = plt.subplots(2, 2, figsize=(14, 9))

    # Average Runtime
    axs[0, 0].bar(names, avg_times)
    axs[0, 0].set_title("Average Runtime")
    axs[0, 0].set_ylabel("Milliseconds")

    # Average Nodes
    axs[0, 1].bar(names, avg_nodes)
    axs[0, 1].set_title("Average Nodes Explored")
    axs[0, 1].set_ylabel("Nodes")

    # Median Runtime
    axs[1, 0].bar(names, median_times)
    axs[1, 0].set_title("Median Runtime")
    axs[1, 0].set_ylabel("Milliseconds")

    # Speedup
    axs[1, 1].bar(names, speedups)
    axs[1, 1].set_title("Average Speedup vs Dijkstra")
    axs[1, 1].set_ylabel("× Speedup")

    plt.suptitle(
        f"A* Search Performance Summary ({len(results)} Queries)",
        fontsize=16
    )

    plt.tight_layout()

    plt.savefig(
        args.save,
        dpi=300,
        bbox_inches="tight"
    )

    print(f"\nSaved figure to: {args.save}")

    # --------------------------------------------------
    # Terminal Report
    # --------------------------------------------------
    print("\n" + "=" * 60)
    print("PERFORMANCE SUMMARY")
    print("=" * 60)

    for i, name in enumerate(names):
        print(f"\n{name}")
        print("-" * len(name))
        print(f"Average Runtime      : {avg_times[i]:.4f} ms")
        print(f"Median Runtime       : {median_times[i]:.4f} ms")
        print(f"Average Nodes        : {avg_nodes[i]:.2f}")
        print(f"Median Nodes         : {median_nodes[i]:.2f}")
        print(f"Total Nodes          : {total_nodes[i]}")
        print(f"Average Speedup      : {speedups[i]:.2f}x")

    print("\n" + "=" * 60)

    # --------------------------------------------------
    # Optional Ranking
    # --------------------------------------------------
    print("\nAlgorithm Ranking (by Average Runtime):")

    ranking = sorted(
        zip(names, avg_times),
        key=lambda x: x[1]
    )

    for idx, (name, avg_time) in enumerate(ranking, start=1):
        print(f"{idx}. {name:<15} {avg_time:.4f} ms")

    plt.show()


if __name__ == "__main__":
    main()