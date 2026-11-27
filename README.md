# Quiz Game

A Python quiz game for two players sharing one terminal. Take turns answering timed multiple-choice questions and see how your score ranks across matches. The terminal interface uses [Rich](https://github.com/Textualize/rich).

## Features

- Three rounds with randomly selected multiple-choice questions
- A handover prompt between turns and a 30-second limit per answer
- Round results, running scores, and a final winner or draw
- A leaderboard that displays up to five players and saves scores across runs

## Project Structure

```
game/
├── main.py           # Terminal interface and match flow
├── engine.py         # Questions, match rules, and scoring
├── storage.py        # Question loading and leaderboard storage
├── question.json     # Question bank
├── leaderboard.json  # Saved scores, wins, and draws
└── README.md
```

## Requirements

- Python 3.9+
- [rich](https://pypi.org/project/rich/)

## Installation and Launch

Run these commands on Linux or macOS.

```bash
git clone --branch mahdi https://github.com/arnita-fallah/game.git
cd game
python3 -m venv .venv
source .venv/bin/activate
python -m pip install rich
python main.py
```

On Windows PowerShell, use `python -m venv .venv` to create the environment and
`.\.venv\Scripts\Activate.ps1` to activate it.

For an existing checkout, run `python main.py` with the virtual environment active
from the directory that contains both `main.py` and `question.json`.

## How to Play

1. Enter a different name for each player.
2. Each round, a question is shown to each player in turn. Type `A`, `B`, `C`, or `D` and press Enter.
3. After both players answer, the round results and total scores are shown. Press Enter to continue.
4. After the final round, the game displays the winner or a draw, followed by the leaderboard.

### Scoring

- A correct answer within 30 seconds earns 10 points.
- The fastest correct answer earns 3 extra points. If only one player answers correctly in time, that player gets the bonus.
- Incorrect answers and answers submitted after 30 seconds earn 0 points.

### Leaderboard

Each completed match updates both players' cumulative scores and records a win
for the winner or a draw for both players. Scores are saved in `leaderboard.json`
next to the game files. Rankings use total score first, then wins, then player name.
Use the same spelling each time to add to your existing record.

## Adding Your Own Questions

Add a question object to the JSON array in `question.json`. List the four
options in A–D order and put the answer letter in `correct`.

```json
{
  "text": "What is the capital of Japan?",
  "options": ["Seoul", "Tokyo", "Beijing", "Bangkok"],
  "correct": "B"
}
```

Keep at least five questions in the file. The launcher samples five from the
bank and uses three in a standard match.

## Configuration

The round count (`ROUNDS`), time limit in seconds (`TIME_LIMIT`), and points
(`SCORE` and `BONUS`) are defined in `engine.py`. For a match with more than five
rounds, increase the sample size in `main.py` and add enough questions to the bank.

