# Member 4 – Q7 Food Heuristic (+ team lead)

**Name:** Member4  |  **Student ID:** IT23516404  |  **Group:** Group_XX

## 1. What I did

| Task | Where |
|---|---|
| Wrote the heuristic for eating every dot (Q7) | `searchAgents.py` → `foodHeuristic` |
| Saved (cached) maze distances so each one is worked out only once | `problem.heuristicInfo['distCache']` |
| Merged all four members' code into the final two files | `search.py`, `searchAgents.py` |
| Ran the full autograder and saved the logs | `Group_Project/autograder_logs/` |
| Built the report and the submission zip | `Report/`, `Submission/Group_XX_Code.zip` |
| Recorded the replays and built the presentation | `Presentation/` |
| Reviewed Member 1's pull request (Q1–Q2) | GitHub PR |

Full code: `Member4_Q7_code.py`

## 2. The problem (Q7)

- Pac-Man must eat **every dot** in the maze using as few steps as possible.
- **State** = `(position, foodGrid)`: where Pac-Man is, plus a True/False grid showing which dots are left.
- **Goal** = no dots left.
- We solve it with Member 2's **A\*** search. A* needs a **heuristic**: a guess of how many steps are still needed.
- A better guess means A* opens fewer states and finishes faster. A guess that is **too high** can make A* return a wrong (longer) path, and gets 0 marks.

## 3. My solution in one line

> **h(state) = the real maze distance from Pac-Man to the farthest dot that is still left.**

```python
position, foodGrid = state
food = foodGrid.asList()
if not food:
    return 0                       # all dots eaten -> nothing left to do
cache = problem.heuristicInfo.setdefault('distCache', {})

def dist(a, b):
    key = (a, b)
    if key not in cache:           # run each BFS only once
        cache[key] = mazeDistance(a, b, problem.startingGameState)
    return cache[key]

return max(dist(position, f) for f in food)
```

**Line by line**
1. Split the state into Pac-Man's position and the food grid.
2. Turn the grid into a list of dot coordinates.
3. No dots left means we are at the goal, so the guess is 0.
4. Get (or create) a dictionary that lives for the whole search, used as a cache.
5. `dist(a, b)` returns the real number of steps from `a` to `b`. If it is not in the cache yet, it runs `mazeDistance`, which runs **Member 1's BFS**, and stores the answer.
6. Return the largest distance, i.e. the distance to the farthest dot.

## 4. Theory, in simple English

### 4.1 What A* does
- A* gives every state a score **f(n) = g(n) + h(n)**.
  - **g(n)** = steps already taken (known for sure).
  - **h(n)** = guess of steps still needed (the heuristic).
- It always opens the state with the **smallest f** first.
- If h is a good guess, A* goes straight toward the goal and opens few states.
- With h = 0 it becomes UCS and opens everything around it.

### 4.2 Admissible: the guess is never too high
- Rule: **h(n) ≤ the real cheapest cost from n to the goal.**
- **Why mine is admissible:** to eat *all* dots, Pac-Man must at some point stand on the farthest dot. Walking there takes at least the maze distance to it. So the real answer is **at least** my guess. It can never be too high.
- **Why it matters:** if the guess were too high, A* could skip the real best path because it "looks" expensive, and return a longer one.

### 4.3 Consistent: the guess drops smoothly
- Rule: **h(n) ≤ cost(n → n′) + h(n′)**. Here every step costs 1, so **h(n) ≤ 1 + h(n′)**.
- **Why mine is consistent:** one step moves Pac-Man one square. The maze distance to any dot can change by at most 1 (triangle inequality: going via the next square can't be more than 1 step shorter). So the farthest-dot distance also changes by at most 1 per step. If a dot is eaten, the max is taken over fewer dots, which can only make h smaller when it already followed the rule. The rule still holds.
- **Why it matters:** with a consistent heuristic, the first time A* opens a state it has already found the cheapest way there. That lets our **graph search** (never open a state twice) stay optimal.
- Consistent always implies admissible (h(goal) = 0, then add up the step rule along the best path).

### 4.4 Why maze distance and not Manhattan distance?
- **Manhattan distance** = |x1 − x2| + |y1 − y2|. It ignores walls.
- In a maze, walls force long detours, so Manhattan is often far too low. It is still admissible, but a weak guess.
- **Maze distance** = the real number of steps around walls (found with BFS). Still never too high, but much closer to the truth.
- Result on `trickySearch`: **4,137** nodes with maze distance vs **9,551** with Manhattan.

### 4.5 Why not add up the distances to all dots?
- Pac-Man eats many dots in one walk, so the sum counts the same steps many times.
- Example: Pac-Man at square 0, dots at squares 1 and 2 in a straight line.
  - Real cost = **2** steps.
  - Sum = 1 + 2 = **3** → too high → **not admissible**.
  - Farthest dot = **2** → exact.

### 4.6 Relaxed problem (where the idea comes from)
- A good way to design a heuristic is to **relax** the problem: remove a rule and solve the easier version exactly.
- My relaxation: "Pac-Man only needs to reach the **one** farthest dot." The answer to the easier problem is always ≤ the real answer, so it is admissible by design.
- Member 3 used the same idea in Q6 (relaxation: no walls).

### 4.7 Why the cache (`heuristicInfo`)?
- A* calls the heuristic **for every state it adds**, thousands of times.
- Each `mazeDistance` is a full BFS. Doing it again and again is slow.
- `problem.heuristicInfo` is a dictionary the problem keeps for the whole search. I store each `(from, to)` distance the first time it is computed, and reuse it after that. This is called **memoisation**.
- Measured on `trickySearch`: **708** BFS runs with the cache vs **44,947** without; **0.57 s** vs **6.1 s**. Same answer, same 4,137 nodes.

## 5. Results

### Autograder (`python autograder.py -q q7`, run 16 Oct 2026)
```
*** PASS: test_cases\q7\food_heuristic_1.test   ... (17 small tests, all PASS)
*** PASS: test_cases\q7\food_heuristic_grade_tricky.test
***     expanded nodes: 4137
***     thresholds: [15000, 12000, 9000, 7000]
### Question q7: 5/4 ###
```
- Under 9,000 nodes → full marks (**8/8**). Under 7,000 → one bonus autograder point.
- Path cost **60** = optimal (same as UCS).

### Comparison I ran (all with our A* on `trickySearch`)
| Heuristic | Nodes expanded | Admissible? |
|---|---|---|
| None (h = 0, same as UCS) | 16,688 | yes |
| Number of dots left | 12,517 | yes |
| Farthest dot, Manhattan | 9,551 | yes |
| **Farthest dot, maze distance (ours)** | **4,137** | **yes** |
| Sum of Manhattan distances | 5,423 | **no**, can guess too high |

All of them happened to find the 60-step path here. Only the admissible ones are *guaranteed* to.

## 6. How my part uses everyone else's

```
Member 1  BFS ─────────────► mazeDistance() ─► my dist() ─┐
Member 2  A* ◄─────────────────────────────── my foodHeuristic
Member 3  idea of a relaxed-problem heuristic (Q6) ───────┘
```

## 7. How to run / show it

```bash
cd Group_Project/search
python autograder.py -q q7                                  # grade Q7
python pacman.py -l trickySearch -p AStarFoodSearchAgent    # watch Pac-Man eat every dot
python autograder.py --no-graphics                          # grade everything
```

From the repo root:
```bash
python Presentation/compare_food_heuristics.py   # prints the heuristic comparison table + cache test
python Presentation/run_member_demos.py 4        # opens the game window for my part (Q7)
python Presentation/run_member_demos.py all      # every member's part, Q1 -> Q7
```
Node counts are always the same. Times change from computer to computer.

## 8. Viva questions I should answer

| Question | Short answer |
|---|---|
| What is your heuristic? | Maze distance from Pac-Man to the farthest dot left. |
| Why is it admissible? | Pac-Man must reach that dot, which costs at least that many steps. |
| Why is it consistent? | One step changes any maze distance by at most 1. |
| Why not sum the distances? | One walk eats many dots, so the sum counts steps twice and can guess too high. |
| Why not Manhattan? | It ignores walls, so it's a weaker guess: 9,551 nodes vs 4,137. |
| What does `heuristicInfo` do? | A dictionary that lasts the whole search. I cache distances in it so each BFS runs once. |
| What does `mazeDistance` use? | Member 1's `breadthFirstSearch` on a `PositionSearchProblem`. |
| What happens with no food left? | Return 0, since the state is a goal. |
| What if the heuristic were inadmissible? | A* could return a longer path, and the autograder gives 0. |
| Which file and function for each question? | Q1–Q4 in `search.py`, Q5–Q7 in `searchAgents.py` (see the main README). |

## 9. Team workflow
- Worked on branch `Hasindu`, merged into `main`.
- Reviewed Member 1's pull request and ran `autograder.py -q q1` and `-q q2` myself.

## 10. AI usage
Claude Code generated the first version of the project. I read, ran, tested and reviewed the code, and ran the heuristic comparison myself. Exact prompts are in Section 8 of the report.
