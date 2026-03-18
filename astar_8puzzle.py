import heapq

GOAL_STATE = (1, 2, 3,
              4, 5, 6,
              7, 8, 0)

def heuristic(state):
    distance = 0
    for i, tile in enumerate(state):
        if tile != 0:
            goal_index = GOAL_STATE.index(tile)
            current_row, current_col = i // 3, i % 3
            goal_row,    goal_col    = goal_index // 3, goal_index % 3
            distance += abs(current_row - goal_row) + abs(current_col - goal_col)
    return distance

def get_successors(state):
    successors = []
    blank_index = state.index(0)
    row, col = blank_index // 3, blank_index % 3

    moves = [
        (-1, 0, "UP"),
        ( 1, 0, "DOWN"),
        ( 0,-1, "LEFT"),
        ( 0, 1, "RIGHT")
    ]

    for dr, dc, direction in moves:
        new_row, new_col = row + dr, col + dc
        if 0 <= new_row < 3 and 0 <= new_col < 3:
            new_index = new_row * 3 + new_col
            new_state = list(state)
            new_state[blank_index], new_state[new_index] = \
                new_state[new_index], new_state[blank_index]
            successors.append((tuple(new_state), direction))

    return successors

def display_state(state, move=None, step=None, f=None, g=None, h=None):
    if step == 0:
        print("\n  [ INITIAL STATE ]")
    elif move and step is not None:
        arrow = {"UP": "⬆", "DOWN": "⬇", "LEFT": "⬅", "RIGHT": "➡"}.get(move, move)
        print(f"\n  [ Step {step:02d} ]  Blank moves {arrow} {move}")

    print("  +-----------+")
    for i in range(3):
        row = state[i*3 : i*3+3]
        print("  |  " + "  ".join(str(t) if t != 0 else "*" for t in row) + "  |")
    print("  +-----------+")

    if f is not None:
        print(f"  f(n)={f}  g(n)={g}  h(n)={h}")

def get_user_input():
    print("\n" + "=" * 52)
    print("      GOAL-BASED INTELLIGENT AGENT")
    print("         8-Puzzle Solver via A*")
    print("=" * 52)
    print("""
  HOW IT WORKS:
  - You provide a shuffled puzzle
  - The agent finds the OPTIMAL solution
  - Using f(n) = g(n) + h(n) at every step

  RULES:
  - Enter 9 unique digits (0 to 8)
  - 0 = blank tile (*)
  - Separate numbers with spaces

  GOAL STATE THE AGENT AIMS FOR:
  +-----------+
  |  1  2  3  |
  |  4  5  6  |
  |  7  8  *  |
  +-----------+
    """)
    print("  Press Enter to use built-in example.\n")

    while True:
        user_input = input("  Enter puzzle >> ").strip()

        if user_input == "":
            initial = [1, 2, 3, 4, 0, 6, 7, 5, 8]
            print("\n  Using default: 1 2 3 4 0 6 7 5 8")
            return initial

        nums = user_input.split()

        if len(nums) != 9:
            print("  [!] Error: Enter exactly 9 numbers. Try again.")
            continue

        try:
            initial = list(map(int, nums))
        except ValueError:
            print("  [!] Error: Only integers allowed. Try again.")
            continue

        if sorted(initial) != list(range(9)):
            print("  [!] Error: Must contain digits 0-8 each exactly once. Try again.")
            continue

        return initial

def is_solvable(state):
    tiles = [t for t in state if t != 0]
    inversions = 0
    for i in range(len(tiles)):
        for j in range(i + 1, len(tiles)):
            if tiles[i] > tiles[j]:
                inversions += 1
    return inversions % 2 == 0

def a_star(initial_state):
    initial_state = tuple(initial_state)

    if initial_state == GOAL_STATE:
        return [initial_state], [], 0, 0

    h0 = heuristic(initial_state)
    open_list = []
    heapq.heappush(open_list, (h0, 0, initial_state, [initial_state], []))

    visited = set()
    nodes_explored = 0

    while open_list:
        f, g, current_state, path_states, path_moves = heapq.heappop(open_list)

        if current_state in visited:
            continue
        visited.add(current_state)
        nodes_explored += 1

        if current_state == GOAL_STATE:
            return path_states, path_moves, g, nodes_explored

        for successor_state, move in get_successors(current_state):
            if successor_state not in visited:
                g_new = g + 1
                h_new = heuristic(successor_state)
                f_new = g_new + h_new
                heapq.heappush(
                    open_list,
                    (f_new, g_new, successor_state,
                     path_states + [successor_state],
                     path_moves  + [move])
                )

    return [], [], 0, nodes_explored

class GoalBasedPuzzleAgent:
    """
    Goal-Based Intelligent Agent for 8-Puzzle.
    - Perceives the environment (puzzle state)
    - Has a defined goal state
    - Plans using A* with f(n) = g(n) + h(n)
    - Selects best state at every step
    - Displays full solution path and cost analysis
    """

    def __init__(self, initial_state):
        self.initial_state = tuple(initial_state)
        self.goal_state    = GOAL_STATE

    def perceive(self):
        return self.initial_state

    def is_goal(self, state):
        return state == self.goal_state

    def act(self):
        current_state = self.perceive()

        h0 = heuristic(current_state)
        display_state(current_state, step=0, f=h0, g=0, h=h0)

        if self.is_goal(current_state):
            print("\n  Already at goal state! No moves needed.")
            return

        if not is_solvable(current_state):
            print("\n  [✘] This puzzle is UNSOLVABLE.")
            print("  Tip: Swap any two tiles to make it solvable.")
            return

        print("\n  Agent thinking... running A* search")
        print("  " + "-" * 40)

        result = a_star(current_state)
        path_states, path_moves, total_cost, nodes_explored = result

        if not path_states:
            print("  Agent failed to find a solution.")
            return

        print("\n" + "=" * 52)
        print("  SOLUTION PATH")
        print("=" * 52)

        for step, (state, move) in enumerate(zip(path_states[1:], path_moves), start=1):
            g = step
            h = heuristic(state)
            f = g + h
            display_state(state, move=move, step=step, f=f, g=g, h=h)

        print("\n" + "=" * 52)
        print("  [✔] GOAL STATE REACHED!")
        print("=" * 52)

        print(f"""
  PERFORMANCE ANALYSIS
  {'-' * 35}
  Total Moves (Optimal Cost)  : {total_cost}
  Total Nodes Explored        : {nodes_explored}
  Initial h(n)                : {heuristic(self.initial_state)}
  Final   h(n)                : 0  (goal reached)

  HOW AGENT ENSURED OPTIMAL DECISIONS:
  - Expanded node with lowest f(n) each step
  - h(n) = Manhattan Distance (admissible)
  - Never overestimated cost to goal
  - Guaranteed shortest path via A*
        """)
        print("=" * 52)

if __name__ == "__main__":
    initial = get_user_input()
    agent = GoalBasedPuzzleAgent(initial)
    agent.act()