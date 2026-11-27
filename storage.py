import json
from engine import ROUNDS, Question
import random
from pathlib import Path
from tempfile import NamedTemporaryFile
from typing import Optional
QUESTION_PATH="question.json"
LEADERBOARD_PATH = Path(__file__).resolve().with_name("leaderboard.json")

class QuestionBank:
    def __init__(self,path=QUESTION_PATH):
        with open(path,encoding="utf-8") as f:
            raw=json.load(f)
        self._questions=[]
        for item in raw:
            if "text" in item:
                text_key, options_key, answer_key = "text", "options", "correct"
            else:
                text_key, options_key, answer_key = "question", "choices", "answer"
            self._questions.append(
                Question(
                    item[text_key],
                    item[options_key],
                    item[answer_key].strip().upper()
                )
            )
    def count(self):
        return len(self._questions)
    def pick (self,n=ROUNDS):
        """Pick n random questions from the bank."""
        if self.count()<n:
            raise ValueError(f"Not enough questions in the bank. Required: {n}, available: {self.count()}.")
        return random.sample(self._questions,n)
class Leaderboard:
    def __init__(self, path=LEADERBOARD_PATH):
        self._path = Path(path)
        try:
            content = self._path.read_text(encoding="utf-8")
        except FileNotFoundError:
            content = ""
        self._data = json.loads(content) if content.strip() else {}

    def is_empty(self):
        return not self._data

    def record(self, winner: Optional[str], player1, player2, score1, score2):
        """Record a completed match; None indicates a draw."""
        if player1 == player2:
            raise ValueError("Player names must be different.")
        if winner is not None and winner not in (player1, player2):
            raise ValueError("The winner must be one of the players.")

        updated = self._data.copy()
        for player, score in ((player1, score1), (player2, score2)):
            totals = updated.get(player, {"score": 0, "wins": 0, "draws": 0}).copy()
            totals["score"] += score
            totals["wins"] += int(winner == player)
            totals["draws"] += int(winner is None)
            updated[player] = totals

        previous = self._data
        self._data = updated
        try:
            self._save()
        except OSError:
            self._data = previous
            raise

    def top(self, n=5):
        """Return (player, totals) pairs ordered by score, wins, and name."""
        ranked = sorted(
            self._data.items(),
            key=lambda entry: (-entry[1]["score"], -entry[1]["wins"], entry[0]),
        )
        return [(player, totals.copy()) for player, totals in ranked[:max(0, n)]]

    def _save(self):
        file = NamedTemporaryFile(
            mode="w", encoding="utf-8", dir=self._path.parent, delete=False
        )
        temporary = Path(file.name)
        try:
            with file:
                json.dump(self._data, file, ensure_ascii=False, indent=2)
                file.write("\n")
            temporary.replace(self._path)
        finally:
            temporary.unlink(missing_ok=True)
