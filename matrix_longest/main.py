import numpy as np
import matplotlib.pyplot as plt
import matplotlib.colors as mcolors
from matplotlib.patches import Rectangle

def input_matrix(rows, cols):
    matrix = np.zeros((rows, cols), dtype=int)
    print("Enter the matrix values row by row:")
    for i in range(rows):
        while True:
            try:
                row_values = list(map(int, input(f"Row {i+1} (space-separated values): ").strip().split()))
                if len(row_values) != cols:
                    print(f"Please enter exactly {cols} values.")
                    continue
                matrix[i] = row_values
                break
            except ValueError:
                print("Invalid input. Please enter integer values only.")
    return matrix

def longest_path(matrix):
    rows, cols = matrix.shape
    dp = np.zeros_like(matrix)
    path = np.zeros_like(matrix, dtype=object)
    
    def dfs(x, y):
        if dp[x, y] != 0:
            return dp[x, y]
        
        longest = 0
        longest_path = []
        
        for dx, dy in [(-1, 0), (1, 0), (0, -1), (0, 1)]:
            nx, ny = x + dx, y + dy
            if 0 <= nx < rows and 0 <= ny < cols and matrix[nx, ny] > matrix[x, y]:
                candidate_length = dfs(nx, ny)
                if candidate_length > longest:
                    longest = candidate_length
                    longest_path = path[nx, ny]
        
        dp[x, y] = longest + 1
        path[x, y] = [f'({x},{y})'] + longest_path
        return dp[x, y]

    max_length = 0
    max_path = []

    for i in range(rows):
        for j in range(cols):
            current_length = dfs(i, j)
            if current_length > max_length:
                max_length = current_length
                max_path = path[i, j]

    return max_length, max_path

def visualize_matrix(matrix, longest_path):
    fig, ax = plt.subplots(figsize=(8, 8))
    cmap = plt.get_cmap('viridis', np.max(matrix))
    norm = mcolors.Normalize(vmin=np.min(matrix), vmax=np.max(matrix))

    cax = ax.matshow(matrix, cmap=cmap, norm=norm)
    plt.colorbar(cax)

    for (i, j) in np.ndindex(matrix.shape):
        plt.text(j, i, f'{matrix[i, j]}', va='center', ha='center')

    for (x, y) in longest_path:
        rect = Rectangle((y - 0.5, x - 0.5), 1, 1, linewidth=2, edgecolor='r', facecolor='none')
        ax.add_patch(rect)

    plt.title("Matrix with Longest Path")
    plt.xticks(range(matrix.shape[1]))
    plt.yticks(range(matrix.shape[0]))
    plt.show()

def main():
    # Get matrix dimensions from user
    rows = int(input("Enter the number of rows: ").strip())
    cols = int(input("Enter the number of columns: ").strip())

    # Input matrix values from user
    matrix = input_matrix(rows, cols)
    print("Generated Matrix:")
    print(matrix)

    # Find longest path
    length, path = longest_path(matrix)
    print("\nLongest Path Length:", length)
    print("Longest Path:", path)

    # Convert path coordinates to (row, column) format
    path_coords = [tuple(map(int, pos.strip('()').split(','))) for pos in path]

    # Visualize matrix with longest path
    visualize_matrix(matrix, path_coords)

if __name__ == "__main__":
    main()
