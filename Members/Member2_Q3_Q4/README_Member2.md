# Member 2 - Q3 Uniform Cost Search & Q4 A* Search

**Name:** Member2  |  **Student ID:** IT23516202  |  **Group:** Group_XX

## What I was responsible for
Implemented the cost-sensitive (informed) searches.

## Files / functions I edited
- `search.py` -> `uniformCostSearch(problem)` (Q3)
- `search.py` -> `aStarSearch(problem, heuristic)` (Q4)
- Full code: `Member2_Q3_Q4_code.py`

## How it works
- **UCS** uses `util.PriorityQueue`, priority = accumulated cost g(n). The fringe entry is `(state, path, cost)`. The goal is tested when a node is *popped*, which guarantees the cheapest path even with varying step costs (StayEastSearchAgent / StayWestSearchAgent use exponential cost functions).
- **A*** is UCS with priority f(n) = g(n) + h(n). `nullHeuristic` (h=0) makes it identical to UCS. With an admissible + consistent h it stays optimal and expands fewer nodes (checked with `manhattanHeuristic` on bigMaze).

## Results (autograder, local run)
- Q3: PASS -> 3/3 marks
- Q4: PASS (A* with Manhattan finds optimal cost 210 on bigMaze, expanding fewer nodes than UCS) -> 3/3 marks

## How to run / verify
```
cd Group_Project/search
python autograder.py -q q3
python autograder.py -q q4
python pacman.py -l mediumMaze -p SearchAgent -a fn=ucs
python pacman.py -l bigMaze -z .5 -p SearchAgent -a fn=astar,heuristic=manhattanHeuristic
```

## Viva cheat-sheet (be ready to answer these)
- UCS vs BFS vs Dijkstra?
- Why is the goal test done at pop time for UCS/A*?
- Define admissible and consistent. Which one does graph-search A* need for optimality?
- What does A* do with nullHeuristic? With a perfect heuristic?

## Team workflow
- Branch: work on your own feature branch, open a pull request into `main`.
- You review the pull request of **Member 3 (Q5-Q6)** and run their autograder question yourself.
- Before the viva, read ALL four code files and be able to explain every question.

## My Git work (commit each step separately, with your own account)
Suggested commits: "Add UCS with priority queue (Q3)", "Add A* search (Q4)", "Handle heuristic(successor) in A* push", "Refactor / comment UCS & A*".

## AI usage
Claude Code (Sonnet 5) generated the first version of the whole project; I read, ran and reviewed the code. Exact prompts are listed in Section 8 of the report.
