# Member 3 - Q5 CornersProblem & Q6 Corners Heuristic

**Name:** Member3  |  **Student ID:** IT23516303  |  **Group:** Group_XX

## What I was responsible for
Designed the state representation for the corners problem and its heuristic.

## Files / functions I edited
- `searchAgents.py` -> `CornersProblem.getStartState`, `isGoalState`, `getSuccessors` (Q5)
- `searchAgents.py` -> `cornersHeuristic` (Q6)
- Full code: `Member3_Q5_Q6_code.py`

## How it works
- **State** = `(position, visitedCorners)` where `visitedCorners` is a tuple of 4 booleans aligned with `self.corners`. Small and hashable; no walls or GameState stored.
- **Goal**: `all(visitedCorners)`. **Successors**: for each legal non-wall move, mark the corner visited if the new position equals it; step cost 1.
- **Heuristic**: relax the problem by removing walls; return the cheapest tour (Manhattan distances, brute-force over <= 4! orders) from Pacman through all unvisited corners. It is the exact optimum of a relaxed problem -> admissible, and consistent (one real step changes it by at most 1). Returns 0 at goals, never negative.

## Results (autograder, local run)
- Q5: PASS -> 8/8 marks
- Q6: PASS, **741 nodes expanded** on mediumCorners (needs <=1200 for full marks), optimal path length 106 -> 8/8 marks

## How to run / verify
```
cd Group_Project/search
python autograder.py -q q5
python autograder.py -q q6
python pacman.py -l mediumCorners -p AStarCornersAgent -z 0.5
```

## Viva cheat-sheet (be ready to answer these)
- Why not store the food grid or walls in the state? How big is the state space (positions x 2^4)?
- Prove the heuristic is admissible and consistent.
- What is a relaxed problem? Why is a max of Manhattan distances weaker than the tour?
- Why is returning 0 at a goal required?

## Team workflow
- Branch: work on your own feature branch, open a pull request into `main`.
- You review the pull request of **Member 4 (Q7)** and run their autograder question yourself.
- Before the viva, read ALL four code files and be able to explain every question.

## My Git work (commit each step separately, with your own account)
Suggested commits: "Add corners state representation (Q5)", "Implement getSuccessors with visited corners", "Add Manhattan-tour corners heuristic (Q6)", "Tune/comment heuristic".

## AI usage
Claude Code (Sonnet 5) generated the first version of the whole project; I read, ran and reviewed the code. Exact prompts are listed in Section 8 of the report.
