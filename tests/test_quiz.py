import json
import subprocess
import sys
import unittest
from pathlib import Path
from shutil import copyfile
from tempfile import TemporaryDirectory

from engine import BONUS, ROUNDS, SCORE, TIME_LIMIT, Match, Question
from storage import Leaderboard, QuestionBank


PROJECT_DIR = Path(__file__).resolve().parent.parent


class QuizTests(unittest.TestCase):
    def test_bundled_question_bank_loads(self):
        bank = QuestionBank(PROJECT_DIR / "question.json")
        self.assertGreaterEqual(bank.count(), max(ROUNDS, 5))
        for question in bank.pick(bank.count()):
            self.assertEqual(len(question.options), 4)
            self.assertIn(question.correct, ("A", "B", "C", "D"))
            self.assertTrue(question.is_correct(question.correct.lower()))

    def test_round_applies_speed_bonus_and_time_limit(self):
        question = Question("Which letter?", ["A", "B", "C", "D"], "A")
        match = Match(["Alice", "Bob"], [question] * ROUNDS)
        match.start_round()
        match.submit("Alice", "A", 2)
        match.submit("Bob", "A", 1)
        results = match.results_round()
        self.assertEqual(results["Alice"].score, SCORE)
        self.assertEqual(results["Bob"].score, SCORE + BONUS)

        match.start_round()
        match.submit("Alice", "A", TIME_LIMIT + 1)
        match.submit("Bob", "B", 1)
        results = match.results_round()
        self.assertEqual(results["Alice"].status, "too_late")
        self.assertEqual(results["Bob"].status, "incorrect")
        self.assertEqual(results["Alice"].score, 0)
        self.assertEqual(results["Bob"].score, 0)
        self.assertEqual(match.winner(), "Bob")

    def test_leaderboard_saves_scores_and_draws(self):
        with TemporaryDirectory() as directory:
            path = Path(directory) / "leaderboard.json"
            board = Leaderboard(path)
            self.assertTrue(board.is_empty())
            board.record("Alice", "Alice", "Bob", 13, 0)
            board.record(None, "Alice", "Bob", 10, 10)
            self.assertEqual(
                Leaderboard(path).top(1),
                [("Alice", {"score": 23, "wins": 1, "draws": 1})],
            )

    def test_command_line_match_displays_and_saves_leaderboard(self):
        with TemporaryDirectory() as directory:
            project = Path(directory)
            for filename in ("main.py", "storage.py", "engine.py", "question.json"):
                copyfile(PROJECT_DIR / filename, project / filename)

            answers = "Alice\nBob\n" + "\nx\n\nx\n\n" * ROUNDS
            result = subprocess.run(
                [sys.executable, "-B", "main.py"],
                cwd=project,
                input=answers,
                text=True,
                capture_output=True,
                timeout=15,
            )
            self.assertEqual(result.returncode, 0, result.stderr)
            self.assertIn("Final Results", result.stdout)
            self.assertIn("LEADERBOARD", result.stdout)
            saved = json.loads((project / "leaderboard.json").read_text(encoding="utf-8"))
            self.assertEqual(saved["Alice"], {"score": 0, "wins": 0, "draws": 1})
            self.assertEqual(saved["Bob"], {"score": 0, "wins": 0, "draws": 1})
