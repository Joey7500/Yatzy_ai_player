# 🎲 Yahtzee AI Player (Expectimax + Heuristics)

> Autonomous & assisted AI player for **Yahtzee** using the **Expectimax decision algorithm**  
> Implemented in **Python**, fully playable in **CLI**, with benchmarking support.

---

## 🧠 Project Overview

This project implements a fully functional **Yahtzee (Yatzy) game engine** with an advanced **AI player** based on the **Expectimax algorithm** — a variant of Minimax adapted for stochastic (random) games.

Yahtzee is a perfect example of a game where:
- **chance** (dice rolls) and  
- **strategy** (which dice to hold, which category to write)

are deeply intertwined.

The AI does **not** brute-force the entire game to the end.  
Instead, it:
- builds a **decision tree per turn**
- evaluates outcomes using **domain-specific heuristics**
- maximizes **expected value**, not guaranteed outcomes

---

## ✨ Features

- 🎮 **Playable CLI Yahtzee**
- 🤖 **Fully autonomous AI player**
- 🧑‍🏫 **Human mode with AI advisor**
- 🌳 **Expectimax decision tree**
- 🧮 **Heuristic-based leaf evaluation**
- 🚀 **Aggressive caching & optimization**
- 📊 **Benchmark mode (N simulated games)**
- 🧩 **Immutable scorecard design**
- 🧠 **Bitmask-based dice holding (fast & elegant)**

---

## 🕹️ Game Modes

1. **Human Player**
   - Manual play via terminal input

2. **Human + Advisor**
   - AI suggests:
     - which dice to hold
     - which category to write

3. **AI Autonomous Mode**
   - AI plays all 13 turns on its own
   - Prints decisions & scorecard evolution

4. **Benchmark Mode**
   - Runs **N games**
   - Outputs statistics:
     - average score
     - median
     - percentiles
     - min / max
     - standard deviation

---

## 🧠 AI Approach

### 🔁 Expectimax Algorithm

Classic Minimax does not work for Yahtzee — dice are not an adversary.

Instead, the game tree alternates between:

- **MAX nodes**
  - Player decisions (which dice to hold)
- **CHANCE nodes**
  - All possible dice roll outcomes  
  - Weighted by probability (expected value)

The tree structure per turn:
MAX (hold dice)
└── CHANCE (reroll)
└── MAX (hold dice)
└── CHANCE (reroll)
└── LEAF (heuristic evaluation)


Without optimization, the tree can reach **hundreds of millions of states**.

---

## ⚡ Optimizations

To make Expectimax feasible:

- 🔢 **5-bit hold masks** (0–31)
- 🧠 **LRU caching** of MAX & CHANCE nodes
- 🎲 **Precomputed roll outcomes**
- 🔁 **Sorted dice tuples** (state deduplication)
- 🧱 **Immutable scorecard** (safe caching)

---

## 🎯 Heuristics

Leaf nodes are evaluated using **game-aware heuristics**, not raw score.

Key strategic principles implemented:

### 🟡 Upper Section Bonus
- Bonus (35 pts) converted to **expected value**
- Probability-based, not binary
- AI actively protects **4s / 5s / 6s**

### 🛟 Chance as a Safety Net
- Penalized early if used too soon
- Saved for bad late-game rolls

### ❌ Smart Sacrificing
- Early game: avoid sacrificing rare categories
- Late game: sacrifice Yahtzee if statistically irrational

### ⏳ Phase-aware Strategy
- **Early game**: aggressive, high-risk
- **Mid game**: stabilize bonus & lower section
- **Late game**: defensive, minimize losses

---

## 📁 Project Structure
├── main.py # Entry point & menu
|
├── game.py # Game loop
|
├── players.py # Human & AI players
|
├── expectimax_turn.py # Expectimax implementation
|
├── heuristics.py # Strategic evaluation
|
├── scoring.py # Yahtzee scoring rules
|
├── scorecard.py # Immutable scorecard model
|
├── constants.py # Game constants & enums
|
└── benchmark.py # Statistics over N games


---

## 📊 Benchmark Results

**1000 simulated games**

- 📈 Average score: **224.31**
- 📊 Median: **219**
- 📉 Std deviation: **36.48**
- 🔻 Min: **128**
- 🔺 Max: **336**

Percentiles:
- 10% → 182
- 25% → 199
- 50% → 219
- 75% → 253
- 90% → 269

📚 Theoretical optimum ≈ **254.6**  
→ Results are considered **very strong**

---

## 🚀 How to Run


python main.py
Then select:
- game mode
- number of benchmark runs (if applicable)

---

## 🧪 Requirements

- Python **3.10+**
- No external dependencies

---

## 📚 References

- Expectimax / Expectiminimax
- Yahtzee official rules
- Python `functools.lru_cache`
- Game theory & decision trees

---

## 🏁 Final Notes

This project focuses on:
- clean architecture
- explainable AI decisions
- performance-aware design

It is intended as:
- a learning project in AI & game theory
- a demonstration of Expectimax in practice
- a playable, testable CLI game

⭐ If you like the project, feel free to star it!
