import json
from game.engine import ROUNDS, Question
import random
from pathlib import Path
QUESTION_PATH="question.json"
LEADERBOARD_PATH="leaderboard.json"

class QuestionBank:
    def __init__(self,path=QUESTION_PATH):
        with open(path,encoding="utf-8") as f:
            raw=json.load(f)
        self._questions=[]
        for item in raw:
            self._questions.append(
                Question(
                    item["question"],
                    item["choices"],
                    item["answer"]
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
    def __init__(self,path=LEADERBOARD_PATH):
        self._path=Path(path)
        self._data={}
        if self._path.exists():
            with open(self._path,encoding="utf-8") as f:
                self._data=json.load(f)
    # def is_empty(self):
    #     pass
    # def record(self,player,score):
    #     pass
    # def _save(self):
    #     pass
