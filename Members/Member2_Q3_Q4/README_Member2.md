# Member 2 – Q3 Uniform Cost Search & Q4 A* Search

**Name:** Member2  |  **Student ID:** IT23516202  |  **Group:** Group_XX

## 1. What I did
- Wrote `uniformCostSearch` (Q3) and `aStarSearch` (Q4) in `search.py`.
- Reused Member 1's loop and changed the fringe to a **priority queue**.
- Reviewed Member 3's pull request (Q5–Q6).
- Full code: `Member2_Q3_Q4_code.py`

## 2. Q3 – UCS
```python
fringe = util.PriorityQueue()
fringe.push((problem.getStartState(), [], 0), 0)
expanded = set()
while not fringe.isEmpty():
    state, path, cost = fringe.pop()
    if problem.isGoalState(state):
        return path
    if state not in expanded:
        expanded.add(state)
        for successor, action, stepCost in problem.getSuccessors(state):
            if successor not in expanded:
                newCost = cost + stepCost
                fringe.push((successor, path + [action], newCost), newCost)
return []
```
- Priority = **g**, the total cost of the path so far. The cheapest path comes out first.
- Goal test when a node is **taken out**: by then no cheaper path is left, so the answer is optimal.
- Works when steps have different costs (e.g. `mediumDottedMaze`, where the east is cheap).

## 3. Q4 – A*
- Same as UCS, but priority = **g + h** (cost so far + guess of cost left).
- `h = nullHeuristic` (always 0) makes it exactly UCS.
- With `manhattanHeuristic` on bigMaze: same 210-step path, **549** nodes instead of **620**.
- Optimal when h is **admissible** (never too high) and, for graph search, **consistent**.
- Members 3 and 4 pass their heuristics into this function.

## 4. Results (autograder, 16 Oct 2026)
| | Test | Result | Marks |
|---|---|---|---|
| Q3 UCS | 11 tests incl. `ucs_5_goalAtDequeue` | 3/3 | 4/4 |
| Q4 A* | `astar_2_manhattan`: length 68, 221 nodes | 3/3 | 4/4 |

## 5. Run it
```bash
cd Group_Project/search
python autograder.py -q q3
python autograder.py -q q4
python pacman.py -l mediumDottedMaze -p StayEastSearchAgent
python pacman.py -l bigMaze -z .5 -p SearchAgent -a fn=astar,heuristic=manhattanHeuristic
```

## 6. Viva points
- Difference between UCS and BFS (costs vs steps).
- Why goal test on pop, not on push (`goalAtDequeue` test).
- f = g + h, and what admissible / consistent mean.
- Why A* with Manhattan opens fewer nodes than UCS.
