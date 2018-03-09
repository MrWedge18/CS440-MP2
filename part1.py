import numpy as np
import heapq

default_goal_state = ["AEDCA", "BEACD", "BABCE", "DADBD", "BECBD"]

factory_dist = np.array([[   0, 1064,  673, 1401, 277],
                         [1064,    0,  958, 1934, 337],
                         [ 673,  958,    0, 1001, 399],
                         [1401, 1934, 1001,    0, 387],
                         [ 277,  337,  399,  387,   0]])

# Current state/node for A* search in part 1
# parent     - parent state
# total_dist - total distance of current path
# num_stops  - total number of stops of current path
# factory    - current factory
# goal_state - goal state of current search
# ws         - list of the current state of the widgets
class State:
    def __init__(self, factory, goal_state=[], parent=None):
        if parent is None:
            self.parent = None
            self.total_dist = 0
            self.num_stops = 0
            self.factory = factory
            self.goal_state = goal_state
            self.ws = new_ws(["", "", "", "", ""], factory, goal_state)
        else:
            self.parent = parent
            self.total_dist = parent.total_dist + distance(parent.factory, factory)
            if factory != parent.factory:
                self.num_stops = parent.num_stops
            else:
                self.num_stops = parent.num_stops + 1
            self.factory = factory
            self.goal_state = parent.goal_state
            self.ws = new_ws(parent.ws, factory, parent.goal_state)

# Build the widgets
# ws      - current state of widgets
# factory - current factory
# goal    - goal state of widgets
def new_ws(ws, factory, goal):
    new = list(ws)
    for i in range(len(ws)):
        w = ws[i]
        g = goal[i]
        if len(w) != len(g):
            if factory == g[len(w)]:
                new[i] = ws[i] + g[len(w)]

    return new

# Translates widget parts to numbers
def translate(c):
    if c == "A":
        return 0
    if c == "B":
        return 1
    if c == "C":
        return 2
    if c == "D":
        return 3
    if c == "E":
        return 4

    return -1 # error

# Translates numbers to widget parts
def rev_translate(i):
    if i == 0:
        return "A"
    if i == 1:
        return "B"
    if i == 2:
        return "C"
    if i == 3:
        return "D"
    if i == 4:
        return "E"

    return "Z" # error

# Distance between two factories
def distance(a, b):
    x = translate(a)
    y = translate(b)

    return factory_dist[x][y]

# Calculates total distance traveled
# ws - current state of the widgets
def total_distance(ws):
    dist = [0, 0, 0, 0, 0]
    count = 0
    for w in ws:
        for i in range(len(w) - 1):
            dist[count] += distance(w[i], w[i+1])
        count += 1

    print dist

# Heuristic for A* search of least distance
# Calculates the greates remaining distance for the widgets
# Returns this max distance + current path cost
def distance_heuristic(state):
    max_dist = 0
    ws = state.ws
    goal = state.goal_state

    for i in range(5):
        w = ws[i]
        g = goal[i]
        dist = 0
        
        for j in range(len(w)-1, len(g)-1):
            dist += distance(g[j], g[j+1])

        if dist > max_dist:
            max_dist = dist

    return max_dist + state.total_dist

# Checks if we're at goal state
# state - current state
# goal  - goal state
def check_goal(state, goal):
    ws = state.ws
    for i in range(5):
        if ws[i] != goal[i]:
            return False

    return True

# Builds and returns a string of the path taken
def build_path(state):
    if state.parent is None:
        return state.factory

    return build_path(state.parent) + state.factory

# A* search to minimize distance
def ayyy_dist(goal=default_goal_state):

    frontier = []
    front2 = set([])

    for i in range(5):
        state = State(rev_translate(i), goal)

        heapq.heappush(frontier, (distance_heuristic(state), state))
        front2.add(state)

    step = 0

    while len(frontier) > 0:
        tup = heapq.heappop(frontier)
        state = tup[1]

        print(step)
        step += 1
        
        if check_goal(state, goal):
            print("distance:" + str(state.total_dist))
            print("path: " + build_path(state))
            return state

        for i in range(5):
            new_state = State(rev_translate(i), parent=state)

            heapq.heappush(frontier, (distance_heuristic(new_state), new_state))
            front2.add(new_state)
