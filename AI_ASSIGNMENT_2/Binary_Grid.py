import heapq
import math

# ---------- STATE CLASS ----------
class State:
    def __init__(self, x, y, g = 0, h = 0, parent = None):
        self.x = x
        self.y = y
        self.g = g              
        self.h = h              
        self.f = g + h          
        self.parent = parent    

    def __lt__(self, other):
        return self.f < other.f

    def __eq__(self, other):
        return self.x == other.x and self.y == other.y

    def __hash__(self):
        return hash((self.x, self.y))

    def get_pos(self):
        return (self.x, self.y)

    def distance_to(self, goal, method = "manhattan"):
        if method == "manhattan":
            return abs(self.x - goal[0]) + abs(self.y - goal[1])
        elif method == "euclidean":
            return math.sqrt((self.x - goal[0])**2 + (self.y - goal[1])**2)
        else:
            return 0


# ---------- PATH RECONSTRUCTION ----------
def reconstruct_path(state):
    path = []
    while state:
        path.append(state.get_pos())
        state = state.parent
    return path[::-1]


# ---------- BEST FIRST SEARCH ----------
def best_first_search(grid, start, goal, heuristic = "manhattan"):
    n = len(grid)
    start_state = State(*start)
    start_state.h = start_state.distance_to(goal, heuristic)
    start_state.f = start_state.h

    open_list = []
    heapq.heappush(open_list, start_state)
    closed = set()

    while open_list:
        current = heapq.heappop(open_list)

        if current.get_pos() == goal:
            return reconstruct_path(current)

        closed.add(current)

        # 8 possible moves
        for dx, dy in [(-1, -1), (-1, 0), (-1, 1),(0, -1),(0, 1),(1, -1),(1, 0),(1, 1)]:
            nx, ny = current.x + dx, current.y + dy
            if 0 <= nx < n and 0 <= ny < n and grid[nx][ny] == 0:
                neighbor = State(nx, ny, parent = current)
                neighbor.h = neighbor.distance_to(goal, heuristic)
                neighbor.f = neighbor.h  
                if neighbor not in closed:
                    heapq.heappush(open_list, neighbor)

    return []  


# ---------- A* SEARCH ----------
def a_star(grid, start, goal, heuristic="manhattan"):
    n = len(grid)
    start_state = State(*start)
    start_state.h = start_state.distance_to(goal, heuristic)
    start_state.f = start_state.g + start_state.h

    open_list = []
    heapq.heappush(open_list, start_state)
    closed = set()

    while open_list:
        current = heapq.heappop(open_list)

        if current.get_pos() == goal:
            return reconstruct_path(current)

        closed.add(current)

        for dx, dy in [(-1, -1), (-1, 0), (-1, 1),(0, -1),(0, 1),(1, -1),  (1, 0), (1, 1)]:
            nx, ny = current.x + dx, current.y + dy
            if 0 <= nx < n and 0 <= ny < n and grid[nx][ny] == 0:
                g_cost = current.g + 1  
                neighbor = State(nx, ny, g = g_cost, parent = current)
                neighbor.h = neighbor.distance_to(goal, heuristic)
                neighbor.f = neighbor.g + neighbor.h
                if neighbor not in closed:
                    heapq.heappush(open_list, neighbor)

    return []  



# Example input
grid1 = [[0, 1],
         [1, 0]]

grid2 = [[0, 0, 0],
         [1, 1, 0],
         [1, 1, 0]]

grid3 = [[1, 0, 0],
         [1, 1, 0],
         [1, 1, 0]]

test_cases = [grid1, grid2, grid3]

for idx, grid in enumerate(test_cases, 1):
    print(f"\nExample {idx}:")
    n = len(grid)
    start, goal = (0, 0), (n - 1, n - 1)

    bfs_path = best_first_search(grid, start, goal)
    astar_path = a_star(grid, start, goal)

    if bfs_path:
        print("Best First Search : length:", len(bfs_path), ", Path:", bfs_path)
    else:
        print("Best First Search : length: -1")

    if astar_path:
        print("A* Search : length:", len(astar_path), ", Path:",astar_path)
    else:
        print("A* Search : length: -1")
