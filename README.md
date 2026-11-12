# Quiz Game

A two-player, turn-based quiz game for the terminal, written in Python with [Rich](https://github.com/Textualize/rich) for a colorful console UI.

Players take turns answering multiple-choice questions on the same computer. Each answer is timed, scores are calculated per round, and a winner is announced at the end.

## Features

- Two players on one machine, with a "hand over" screen between turns so nobody sees the other's answer
- Multiple-choice questions (A–D)
- Timed answers: each response is measured and scored (correct, incorrect, or too late)
- Round-by-round results and running totals
- Final results screen with the winner, or a draw
- Clean separation between the game logic (`engine.py`) and the interface (`main.py`)

## Project Structure

```
game/
├── main.py      # Terminal interface: screens, input, output
├── engine.py    # Game logic: Question, Match, scoring rules
└── README.md
```

## Requirements

- Python 3.9+
- [rich](https://pypi.org/project/rich/)

## Installation

```bash
git clone <your-repo-url>
cd game

python -m venv .venv

# Windows (PowerShell)
.venv\Scripts\Activate.ps1
# macOS / Linux
source .venv/bin/activate

pip install rich
```

## Usage

```bash
python main.py
```

1. Enter a name for Player 1 and Player 2.
2. Each round, a question is shown to each player in turn. Type `A`, `B`, `C`, or `D` and press Enter.
3. After both players answer, the round results and total scores are shown. Press Enter to continue.
4. When all rounds are done, the final scores and the winner are displayed.

## Adding Your Own Questions

Questions are defined in the `questions` list in `main.py`:

```python
Question(
    "What's the best database?",
    ["A: MySQL", "B: PostgreSQL", "C: MongoDB", "D: SQL"],
    "B"   # correct answer
)
```

Add as many `Question(...)` entries as you like.

## Configuration

Game settings such as the number of rounds, the time limit per answer, and the scoring values are defined in `engine.py`.

## Possible Improvements

- Load questions from a JSON file
- Randomize question and option order
- Support more than two players
- Add difficulty levels and categories
- Save a high-score table

## License

Add a license of your choice (for example MIT).
