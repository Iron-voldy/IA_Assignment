# Member 3 – Q5 Corners Problem & Q6 Corners Heuristic

**Name:** Member3  |  **Student ID:** IT23516303  |  **Group:** Group_XX

## 1. What I did
- Designed `CornersProblem` (Q5) in `searchAgents.py`: start state, goal test, successors.
- Wrote `cornersHeuristic` (Q6).
- Reviewed Member 4's pull request (Q7).
- Full code: `Member3_Q5_Q6_code.py`

## 2. Q5 – State design
- **State = (position, visited)**, where `visited` is a tuple of 4 True/False flags, one per corner.
- Only what changes goes in the state. Walls never change, so they stay outside. The state is small and hashable (it can go in the `expanded` set).
- **Goal:** `all(visited)`.
- **Successors:** for each move that does not hit a wall, the new position, plus the flags with a corner ticked if Pac-Man lands on it. Each step costs 1.

```python
def getStartState(self):
    visited = tuple(self.startingPosition == c for c in self.corners)
    return (self.startingPosition, visited)

def isGoalState(self, state):
    return all(state[1])
```

## 3. Q6 – Heuristic
- **Relaxed problem:** pretend there are no walls.
- Try every order of the corners still left (at most 4! = 24) and return the shortest Manhattan tour.
- **Admissible:** walls only make walks longer, so the real cost is never less than this.
- **Consistent:** one step changes the tour length by at most 1.

```python
def cheapestTour(current, todo):
    if not todo:
        return 0
    return min(manhattan(current, c) + cheapestTour(c, [r for r in todo if r != c])
               for c in todo)
```

## 4. Results (autograder, 16 Oct 2026)
| | Layout | Path | Nodes | Autograder | Marks |
|---|---|---|---|---|---|
| Q5 (BFS) | mediumCorners | 106 | 1,966 | 3/3 | 8/8 |
| Q6 (A* + heuristic) | mediumCorners | 106 | **741** (≤ 1,200 for full marks) | 3/3 | 8/8 |

## 5. Run it
```bash
cd Group_Project/search
python autograder.py -q q5
python autograder.py -q q6
python pacman.py -l mediumCorners -p SearchAgent -a fn=bfs,prob=CornersProblem
python pacman.py -l mediumCorners -p AStarCornersAgent -z 0.5
```

## 6. Viva points
- Why the state holds visited flags and not the whole grid.
- Why tuples (hashable) and not lists.
- What a relaxed problem is and why it gives an admissible heuristic.
- Why the tour, and not just the nearest or farthest corner (tighter guess, fewer nodes).
