# Yatzy / Yahtzee — CLI Game with Expectimax AI

A complete command-line implementation of the Yahtzee/Yatzy-style dice game featuring an **Expectimax-based AI player**. The AI evaluates re-roll decisions using expected values (chance nodes) and chooses actions that maximize long-term score potential.

This repository is built to be:
- Fun to play in the terminal (nice dice rendering + readable scorecard)
- Easy to benchmark (run many games quickly)
- A clean reference project for Expectimax in a stochastic game

---

## Highlights

- **Full CLI game** (13 turns, scorecard categories, end-of-game total).
- **Expectimax AI player** that decides:
  - Which dice to hold and reroll (up to 2 rerolls)
  - Which category to fill at the end of the turn
- **Human mode** with optional AI advisor (AI suggests holds and/or category).
- **Benchmark mode** to evaluate performance across many simulated games.
- No heavy dependencies required (pure Python approach).

---

## How Yahtzee Works (Quick Rules)

Each game has **13 turns**.

In every turn:
1. Roll 5 dice.
2. You may reroll some dice up to **two times**.
3. After the final roll, you must choose **one** category on the scorecard and write the score there.
4. Each category can be used only once (if a turn goes badly, you can “burn” a category with 0).

Goal: maximize total points after 13 filled categories.

---

## Expectimax AI (Concept)

Unlike minimax (which assumes an adversary), Yahtzee is a game against **chance**. Expectimax models this by alternating:

- **MAX nodes**: the player chooses an action (which dice to hold).
- **CHANCE nodes**: the dice reroll outcome is random, so the node’s value is the **expected value** over all outcomes.

At a high level, the AI does:
1. Enumerate all hold masks (which dice to keep).
2. For each hold mask, compute expected score after rerolls.
3. Pick the hold mask with the best expected value.
4. At the end of the turn, choose a category using a scoring/evaluation heuristic.

This makes the AI “risk-aware”: it does not chase only the best single outcome, but instead prefers actions that are statistically strong.

---

## Getting Started

### Requirements
- Python **3.10+** (recommended 3.11+)

No extra libraries are required.

### Run the game
```bash
python main.py
