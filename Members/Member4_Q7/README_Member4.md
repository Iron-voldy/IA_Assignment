# Member 4 - Q7 Food Heuristic (+ integration, report & Git lead)

**Name:** Member4  |  **Student ID:** IT23516404  |  **Group:** Group_XX

## What I was responsible for
Designed the heuristic for eating all the dots, and integrated/tested the final two files and prepared the submission package.

## Files / functions I edited
- `searchAgents.py` -> `foodHeuristic` (Q7)
- Full code: `Member4_Q7_code.py`
- Integration: final `search.py` + `searchAgents.py`, `Submission/Group_XX_Code.zip`, `Report/`

## How it works
- `h(state)` = **maze distance from Pacman to the farthest remaining food dot** (real shortest path with walls, computed by the provided `mazeDistance` BFS).
- **Admissible**: to eat every dot Pacman must at least reach the farthest one. **Consistent**: maze distance obeys the triangle inequality, so h(n) <= 1 + h(n') for a unit step.
- **Efficiency**: every pairwise distance is memoised in `problem.heuristicInfo['distCache']`, so each BFS runs once.
- Returns 0 when no food is left.

## Results (autograder, local run)
- Q7: PASS, **4137 nodes expanded** on trickySearch (needs <=9000 for full marks), optimal cost 60 -> 8/8 marks

## How to run / verify
```
cd Group_Project/search
python autograder.py -q q7
python autograder.py --no-graphics
python pacman.py -l trickySearch -p AStarFoodSearchAgent
```

## Viva cheat-sheet (be ready to answer these)
- Why farthest-food maze distance rather than Manhattan? Why not the sum of distances (inadmissible)?
- Prove admissibility and consistency.
- What does heuristicInfo do, and why cache?
- Explain the whole pipeline: which file, which class, which algorithm for each Qn.

## Team workflow
- Branch: work on your own feature branch, open a pull request into `main`.
- You review the pull request of **Member 1 (Q1-Q2)** and run their autograder question yourself.
- Before the viva, read ALL four code files and be able to explain every question.

## My Git work (commit each step separately, with your own account)
Suggested commits: "Add farthest-dot maze-distance heuristic (Q7)", "Cache distances in heuristicInfo", "Add report and submission zip". Also merge/PR review of the others' branches.

## AI usage
Claude Code (Sonnet 5) generated the first version of the whole project; I read, ran and reviewed the code. Exact prompts are listed in Section 8 of the report.
