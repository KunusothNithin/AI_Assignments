class State:
    goal_state = ['W', 'W', 'W', '_', 'E', 'E', 'E']

    def __init__(self, current_state):
        self.current_state = current_state

    def goalTest(self):
        return self.current_state == State.goal_state

    def moveGen(self):
        Children = []
        state = self.current_state
        empty = state.index('_')

        for i in [-2, -1, 1, 2]:
            new_pos = empty + i
            if 0 <= new_pos < len(state):
                new_state = state.copy()

                if i == -1 and state[empty - 1] == 'E':
                    new_state[empty], new_state[empty - 1] = new_state[empty - 1], '_'
                    Children.append(State(new_state))

                elif i == 1 and state[empty + 1] == 'W':
                    new_state[empty], new_state[empty + 1] = new_state[empty + 1], '_'
                    Children.append(State(new_state))

                elif i == -2 and state[empty - 2] == 'E' and state[empty - 1] == 'W':
                    new_state[empty], new_state[empty - 2] = new_state[empty - 2], '_'
                    Children.append(State(new_state))

                elif i == 2 and state[empty + 2] == 'W' and state[empty + 1] == 'E':
                    new_state[empty], new_state[empty + 2] = new_state[empty + 2], '_'
                    Children.append(State(new_state))

        return Children

    def __eq__(self, other):
        return isinstance(other, State) and self.current_state == other.current_state

    def __hash__(self):
        return hash(tuple(self.current_state))

    def __str__(self):
        return ''.join(self.current_state)

    def __repr__(self):
        return ''.join(self.current_state)


def reconstructPath(goal_node_pair, CLOSED):
    parent_map = {}
    for node, parent in CLOSED:
        parent_map[node] = parent

    path = []
    goal_node, parent = goal_node_pair
    path.append(goal_node)
    while parent is not None:
        path.append(parent)
        parent = parent_map[parent]

    return path


def removeSeen(children, OPEN, CLOSED):
    open_nodes = [node for node, parent in OPEN]
    closed_nodes = [node for node, parent in CLOSED]
    new_nodes = [c for c in children if c not in open_nodes and c not in closed_nodes]
    return new_nodes


def bfs(start):
    OPEN = [(start, None)]
    CLOSED = []
    while OPEN:
        node_pair = OPEN.pop(0)
        N, parent = node_pair

        if N.goalTest():
            path = reconstructPath(node_pair, CLOSED)
            path.reverse()
            print(" -> \n".join(map(str, path)))
            print(f"Steps: {len(path)-1}")
            return
        else:
            CLOSED.append(node_pair)
            children = N.moveGen()
            new_nodes = removeSeen(children, OPEN, CLOSED)
            new_pairs = [(node, N) for node in new_nodes]
            OPEN = OPEN + new_pairs
    print("No solution found.")
    return []


def dfs(start):
    OPEN = [(start, None)]
    CLOSED = []
    while OPEN:
        node_pair = OPEN.pop(0)
        N, parent = node_pair

        if N.goalTest():
            path = reconstructPath(node_pair, CLOSED)
            path.reverse()
            print(" -> \n".join(map(str, path)))
            print(f"Steps: {len(path)-1}")
            return
        else:
            CLOSED.append(node_pair)
            children = N.moveGen()
            new_nodes = removeSeen(children, OPEN, CLOSED)
            new_pairs = [(node, N) for node in new_nodes]
            OPEN = new_pairs + OPEN
    print("No solution found.")
    return []


# ✅ Test it
start_state = State(['E', 'E', 'E', '_', 'W', 'W', 'W'])

print("BFS")
bfs(start_state)

print("\nDFS")
dfs(start_state)
