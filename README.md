# All-Pairs Shortest Path Matrix Update (Floyd-Warshall)

## Description
This project implements the Floyd-Warshall dynamic programming algorithm to compute all-pairs shortest paths on a directed weighted graph. It tracks intermediate distance matrices $D^{(k)}$ to demonstrate state transitions and subproblem relaxation.

## Algorithm
```text
Algorithm FloydWarshall(W, n):
    // Input: Weight matrix W of size n x n
    // Output: All-pairs shortest distance matrix D

    D^(0) = W
    for k = 1 to n do:
        for i = 1 to n do:
            for j = 1 to n do:
                D^(k)[i][j] = min(D^(k-1)[i][j], D^(k-1)[i][k] + D^(k-1)[k][j])
    return D^(n)
```

## Prompt Used
"Show iterative updates of distance matrix in Floyd-Warshall algorithm."

## Output
![Floyd-Warshall Matrix Updates](Visualization.png)

## Learning Outcome
- Understood optimal substructure in graph problems via dynamic programming.
- Visualized vertex relaxation across iterative state matrices.
- Practiced modular Git commit workflows and documentation.
