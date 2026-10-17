# Member 1 – Q1 Depth First Search & Q2 Breadth First Search

**Name:** Member1  |  **Student ID:** IT23516101  |  **Group:** Group_XX

## 1. What I did
- Wrote `depthFirstSearch` (Q1) and `breadthFirstSearch` (Q2) in `search.py`.
- Built the graph-search loop that UCS, A* and every later question reuse.
- Reviewed Member 2's pull request (Q3–Q4).
- Full code: `Member1_Q1_Q2_code.py`

## 2. The shared loop (graph search)
1. Put the start state on the **fringe** (the to-do list) with an empty path.
2. Take one entry out. If it is the goal, return its path.
3. If the state is not in `expanded`, add it there and push every neighbour with `path + [action]`.
4. Repeat until the fringe is empty (then return `[]`).

The `expanded` set is what makes it **graph search**: no state is opened twice, so it can't loop forever.

## 3. Q1 – DFS
```python
fringe = util.Stack()
fringe.push((problem.getStartState(), []))
expanded = set()
while not fringe.isEmpty():
    state, path = fringe.pop()
    if problem.isGoalState(state):
        return path
    if state not in expanded:
        expanded.add(state)
        for successor, action, _ in problem.getSuccessors(state):
            if successor not in expanded:
                fringe.push((successor, path + [action]))
return []
```
- **Stack = last in, first out** → always opens the newest place → dives deep.
- **Complete** on a finite maze, **not optimal**: it returns the first path it finds.

## 4. Q2 – BFS
- Same code, with `util.Queue()` instead of `util.Stack()`.
- **Queue = first in, first out** → opens all places 1 step away, then 2, then 3...
- Every step costs 1, so the first path to reach the goal is the **shortest** one (optimal).
- Uses more memory and opens more places than DFS.
- Member 4's `mazeDistance` (Q7) and Member 3's corners problem (Q5) both run on this BFS.

## 5. Results (autograder, 16 Oct 2026)
| | Layout | Path length | Nodes expanded | Autograder | Marks |
|---|---|---|---|---|---|
| Q1 DFS | mediumMaze | 130 | 146 | 3/3 | 4/4 |
| Q2 BFS | mediumMaze | 68 | 269 | 3/3 | 4/4 |

## 6. Run it
```bash
cd Group_Project/search
python autograder.py -q q1
python autograder.py -q q2
python pacman.py -l mediumMaze -p SearchAgent -a fn=dfs
python pacman.py -l mediumMaze -p SearchAgent -a fn=bfs
```

## 7. Viva points
- Stack vs queue: why DFS dives and BFS spreads.
- Why BFS is optimal only when every step costs the same.
- Graph search vs tree search: the `expanded` set.
- Why we check `isGoalState` when we **pop**, not when we push.
- Why we must use `util.Stack` / `util.Queue` and not Python lists.
