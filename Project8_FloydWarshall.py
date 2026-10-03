"""
Project 8: All-Pairs Shortest Path Matrix Update (Floyd-Warshall)
Computes intermediate distance matrices and saves Visualization.png.
"""

import matplotlib.pyplot as plt

INF = 99999

def floyd_warshall(graph):
    v_count = len(graph)
    dist = [row[:] for row in graph]
    history = [(0, [row[:] for row in dist], [])]

    for k in range(v_count):
        updated = []
        for i in range(v_count):
            for j in range(v_count):
                if dist[i][k] + dist[k][j] < dist[i][j]:
                    dist[i][j] = dist[i][k] + dist[k][j]
                    updated.append((i, j))
        history.append((k + 1, [row[:] for row in dist], updated))
    return dist, history

def render_plot(history, output_file="Visualization.png"):
    steps = len(history)
    fig, axes = plt.subplots(1, steps, figsize=(3.8 * steps, 4.2))
    if steps == 1:
        axes = [axes]

    for idx, (step, mat, updated) in enumerate(history):
        ax = axes[idx]
        title = r"$D^{(0)}$ (Initial)" if step == 0 else rf"$D^{{({step})}}$ (via $V_{step}$)"
        ax.set_title(title, fontsize=11, fontweight="bold", pad=8)
        
        n = len(mat)
        ax.set_xlim(-0.5, n - 0.5)
        ax.set_ylim(n - 0.5, -0.5)
        ax.set_xticks(range(n))
        ax.set_yticks(range(n))
        ax.set_xticklabels([f"V{i+1}" for i in range(n)])
        ax.set_yticklabels([f"V{i+1}" for i in range(n)])
        ax.tick_params(left=False, bottom=False)

        for i in range(n):
            for j in range(n):
                val = mat[i][j]
                val_str = r"$\infty$" if val >= INF else str(val)
                is_upd = (i, j) in updated
                
                # Highlight relaxed cells in green, current intermediate vertex row/col in grey
                bg = "#c8e6c9" if is_upd else ("#f5f5f5" if step > 0 and (i == step - 1 or j == step - 1) else "white")
                ax.add_patch(plt.Rectangle((j - 0.5, i - 0.5), 1, 1, facecolor=bg, edgecolor="#999999", lw=0.8))
                ax.text(j, i, val_str, ha="center", va="center", fontsize=10, 
                        color="darkgreen" if is_upd else "black",
                        fontweight="bold" if is_upd else "normal")

    plt.suptitle("Floyd-Warshall Stepwise Distance Matrix Updates", fontsize=13, fontweight="bold", y=1.02)
    plt.tight_layout()
    plt.savefig(output_file, dpi=300, bbox_inches="tight")
    print(f"[OK] Generated: {output_file}")

if __name__ == "__main__":
    # Directed weighted graph representation
    graph = [
        [0, 3, INF, 7],
        [8, 0, 2, INF],
        [5, INF, 0, 1],
        [2, INF, INF, 0]
    ]
    _, history = floyd_warshall(graph)
    render_plot(history, output_file="Visualization.png")
