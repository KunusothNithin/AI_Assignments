class State:
    times = {'Amogh': 5, 'Ameya': 10, 'GrandMaa': 20, 'GrandPaa': 25}

    def __init__(self, Amogh, Ameya, GrandMaa, GrandPaa, umbrella, time):
        self.Amogh = Amogh
        self.Ameya = Ameya
        self.GrandMaa = GrandMaa
        self.GrandPaa = GrandPaa
        self.umbrella = umbrella
        self.time = time

    def goalTest(self):
        return self.Amogh == self.Ameya == self.GrandMaa == self.GrandPaa == 'R' and self.time <= 60

    def getPeople(self):
        return {
            'Amogh': self.Amogh,
            'Ameya': self.Ameya,
            'GrandMaa': self.GrandMaa,
            'GrandPaa': self.GrandPaa
        }

    def moveGen(self):
        children = []
        people = self.getPeople()
        current_side_people = [p for p in people if people[p] == self.umbrella]
        new_side = 'R' if self.umbrella == 'L' else 'L'

        for i in range(len(current_side_people)):
            p1 = current_side_people[i]
            new_positions = people.copy()
            new_positions[p1] = new_side
            cost = State.times[p1]
            new_state = State(
                Amogh = new_positions['Amogh'],
                Ameya = new_positions['Ameya'],
                GrandMaa = new_positions['GrandMaa'],
                GrandPaa = new_positions['GrandPaa'],
                umbrella = new_side,
                time = self.time + cost
            )
            if new_state.time <= 60:
                children.append(new_state)

            for j in range(i + 1, len(current_side_people)):
                p2 = current_side_people[j]
                new_positions2 = people.copy()
                new_positions2[p1] = new_side
                new_positions2[p2] = new_side
                cost = max(State.times[p1], State.times[p2])
                new_state2 = State(
                    Amogh = new_positions2['Amogh'],
                    Ameya = new_positions2['Ameya'],
                    GrandMaa = new_positions2['GrandMaa'],
                    GrandPaa = new_positions2['GrandPaa'],
                    umbrella = new_side,
                    time = self.time + cost
                )
                if new_state2.time <= 60:
                    children.append(new_state2)

        return children

        children = []
        people = self.getPeople()
        current_side_people = [p for p in people if people[p] == self.umbrella]
        new_side = 'R' if self.umbrella == 'L' else 'L'

        for i in range(len(current_side_people)):
            # One person move
            p1 = current_side_people[i]
            new_positions = people.copy()
            new_positions[p1] = new_side
            cost = State.times[p1]
            new_state = State(
                Amogh = new_positions['Amogh'],
                Ameya = new_positions['Ameya'],
                GrandMaa = new_positions['GrandMaa'],
                GrandPaa = new_positions['GrandPaa'],
                umbrella = new_side,
                time = self.time + cost
            )
            if new_state.time <= 60:
                children.append(new_state)

            # Two person move
            for j in range(i + 1, len(current_side_people)):
                p2 = current_side_people[j]
                new_positions2 = people.copy()
                new_positions2[p1] = new_side
                new_positions2[p2] = new_side
                cost = max(State.times[p1], State.times[p2])
                new_state2 = State(
                    Amogh = new_positions2['Amogh'],
                    Ameya = new_positions2['Ameya'],
                    GrandMaa = new_positions2['GrandMaa'],
                    GrandPaa = new_positions2['GrandPaa'],
                    umbrella = new_side,
                    time = self.time + cost
                )
                if new_state2.time <= 60:
                    children.append(new_state2)

        return children

    def __str__(self):
        return f"Amogh:{self.Amogh} Ameya:{self.Ameya} GrandMaa:{self.GrandMaa} GrandPaa:{self.GrandPaa} Umbrella:{self.umbrella} Time:{self.time}\n"

    def __eq__(self, other):
        return (
            self.Amogh == other.Amogh and
            self.Ameya == other.Ameya and
            self.GrandMaa == other.GrandMaa and
            self.GrandPaa == other.GrandPaa and
            self.umbrella == other.umbrella
        )

    def __hash__(self):
        return hash((self.Amogh, self.Ameya, self.GrandMaa, self.GrandPaa, self.umbrella))


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


# BFS
def bfs(start):
    OPEN = [(start, None)]
    CLOSED = []
    while OPEN:
        node_pair = OPEN.pop(0)
        N, parent = node_pair

        if N.goalTest():
            path = reconstructPath(node_pair, CLOSED)
            path.reverse()
            print(" -> ".join(map(str, path)))
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


# DFS
def dfs(start):
    OPEN = [(start, None)]
    CLOSED = []
    while OPEN:
        node_pair = OPEN.pop(0)
        N, parent = node_pair

        if N.goalTest():
            path = reconstructPath(node_pair, CLOSED)
            path.reverse()
            print(" -> ".join(map(str, path)))
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


# Starting the Search
start_state = State('L', 'L', 'L', 'L', 'L', 0)
print("BFS Search")
bfs(start_state)
print("\nDFS Search")
dfs(start_state)
