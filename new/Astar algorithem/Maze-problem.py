from collections import deque

class MazeGraph:
    def __init__(self, rows, cols, maze):
        self.rows = rows
        self.cols = cols
        self.maze = maze
        self.adj = self.create_adjacency_matrix()

    def create_adjacency_matrix(self):
        adj = [[0 for _ in range(self.rows * self.cols)] for _ in range(self.rows * self.cols)]

        for i in range(self.rows):
            for j in range(self.cols):
                if self.maze[i][j] != '%':
                    current_node = i * self.cols + j

                    # Check and add neighbors (up, down, left, right)
                    for x, y in [(i-1, j), (i+1, j), (i, j-1), (i, j+1)]:
                        if 0 <= x < self.rows and 0 <= y < self.cols and self.maze[x][y] != '%':
                            neighbor_node = x * self.cols + y
                            adj[current_node][neighbor_node] = 1

        return adj

    def bfs(self, start, goal):
        visited = [False] * (self.rows * self.cols)
        parent = [-1] * (self.rows * self.cols)
        queue = deque([start])
        visited[start] = True

        while queue:
            current_node = queue.popleft()

            for neighbor in range(self.rows * self.cols):
                if self.adj[current_node][neighbor] == 1 and not visited[neighbor]:
                    queue.append(neighbor)
                    visited[neighbor] = True
                    parent[neighbor] = current_node

                    if neighbor == goal:
                        return self.construct_path(parent, start, goal)

        return None  # No path found

    def construct_path(self, parent, start, goal):
        path = []
        current_node = goal

        while current_node != -1:
            path.append(current_node)
            current_node = parent[current_node]

        return path[::-1]

    def get_directions(self, path):
        directions = []
        for i in range(len(path) - 1):
            current_node = path[i]
            next_node = path[i + 1]
            current_i, current_j = divmod(current_node, self.cols)
            next_i, next_j = divmod(next_node, self.cols)

            if current_i < next_i:
                directions.append("Down")
            elif current_i > next_i:
                directions.append("Up")
            elif current_j < next_j:
                directions.append("Right")
            elif current_j > next_j:
                directions.append("Left")

        return directions

# Example usage:
# rows, cols = 5, 5
# maze = [
#     "% % % % G",
#     "- - % % -",
#     "% - % - -",
#     "% % - - %",
#     "S - - % -"
# ]
# rows, cols = 8, 6
# maze=[
# "%%%%%%",
# "S--%--",
# "%-%%--",
# "%--%-%",
# "%%-%%G",
# "%--%%-",
# "%---%-",
# "%%%---"
# ]
rows, cols = 12, 10
maze=[
   "%---%---%G",
"---%------",
"%--%-%%---",
"---%---%-%",
"---%-%--%-",
"--%-%--%--",
"-%----%---",
"---%-%----",
"-%--%-----",
"--%%------",
"%-%-------",
"-S--------"
]
maze_without_spaces = [row.replace(" ", "") for row in maze]

maze_graph = MazeGraph(rows, cols, maze_without_spaces)

# Find the starting and goal positions
for i in range(rows):
    for j in range(cols):
        if maze_without_spaces[i][j] == "S":
            start_node = i * cols + j
        elif maze_without_spaces[i][j] == "G":
            goal_node = i * cols + j

# Find the path from 'S' to 'G'
path = maze_graph.bfs(start_node, goal_node)

if path:
    print("Path from 'S' to 'G':", path)
    directions = maze_graph.get_directions(path)
    print("Directions:", directions)
else:
    print("No path found from 'S' to 'G'")
