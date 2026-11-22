# Mini-Courier Planner — DAA Capstone

**Course:** Design & Analysis of Algorithms (ETCCDA302)  
**Programme:** B.Tech CSE & Specializations  
**University:** K.R. Mangalam University, Gurugram, Haryana

## 1. Project overview
This Python prototype plans a courier trip. It sorts parcels by priority and deadline, chooses a valuable set of parcels within vehicle capacity, finds shortest paths in a road graph, and creates an approximate delivery tour.

## 2. Algorithms used
1. **Merge Sort:** orders parcels by decreasing priority; ties are ordered by earlier deadline.
2. **0/1 Knapsack using Dynamic Programming:** maximizes total parcel value without exceeding vehicle capacity.
3. **Dijkstra's Algorithm:** finds shortest paths between graph nodes using non-negative road distances.
4. **Nearest-Neighbor TSP Approximation:** repeatedly visits the closest unvisited delivery point and returns to the depot when reachable.

## 3. Folder structure
```
Mini_Courier_Planner/
│── main.py
│── README.md
│── Capstone_Report.docx
│── data/
│   └── sample_data.json
└── results/
    ├── sample_output.txt
    └── runtime_chart.png
```

## 4. Requirements
- Python 3.8 or later
- No third-party packages are required to run `main.py`.
- `matplotlib` is only required if you want to recreate the runtime chart.

## 5. How to run
1. Extract the ZIP file.
2. Open the `Mini_Courier_Planner` folder in VS Code or a terminal.
3. Run:
   ```
   python main.py
   ```
4. The program prints sorted parcels, selected parcels, packing value, route, route distance, and observed execution times.
5. The captured sample run is available at `results/sample_output.txt`.

## 6. Input data format
Edit `data/sample_data.json`.
- `depot`: starting/ending graph node.
- `vehicle_capacity`: maximum total parcel weight.
- `parcels`: list of parcels with `id`, `priority`, `deadline`, `weight`, `value`, and `destination`.
- `graph`: weighted adjacency list. Each edge should be listed in both directions for an undirected road network.

## 7. Complexity analysis
Let `n` be the number of parcels, `W` the vehicle capacity, `V` the number of graph vertices, and `E` the number of graph edges.
- Merge Sort: **O(n log n)** time and **O(n)** auxiliary space.
- 0/1 Knapsack DP: **O(nW)** time and **O(nW)** space for the displayed DP table.
- Dijkstra with a binary heap: **O((V + E) log V)** time and **O(V)** auxiliary space.
- Nearest-neighbor route: at most `n` Dijkstra runs, approximately **O(n(V + E) log V)** time; the TSP approximation is heuristic and does not guarantee the optimal tour.

## 8. Testing and performance
The program runs the sample dataset and benchmarks Merge Sort and Knapsack DP for 10, 20, 40, 80, and 120 parcels. Runtime depends on the computer and Python environment. The chart in `results/runtime_chart.png` is generated from the recorded run; do not expect identical values on another machine.

## 9. Limitations and future improvements
- The nearest-neighbor method gives a fast approximate route, not a guaranteed optimal TSP route.
- The graph is a small static road network; real road traffic and live distances are not included.
- Knapsack uses integer weight capacity.
- Future work can add live maps, time windows, multiple vehicles, and more advanced route optimization.

## 10. Submission checklist
- Source code: `main.py`
- Sample dataset: `data/sample_data.json`
- Sample output: `results/sample_output.txt`
- Runtime chart: `results/runtime_chart.png`
- Full report: `Capstone_Report.docx`
