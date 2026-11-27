class Question:
    def __init__(self, text, options, correct):
        self._text = text
        self._options = options
        self._correct = correct

    @property
    def text(self):
        return self._text
    @property
    def correct(self):
        return self._correct
    @property
    def options(self):
        return self._options
    def is_correct(self, answer):
        return answer.strip().upper() == self._correct
    def create_text(self):
        return self._options["ABCD".index(self._correct)]
ROUNDS = 3
TIME_LIMIT = 30
BONUS = 3
SCORE = 10
class Match:
    def __init__(self, players, questions):
        if len(set(players)) < len(players):
            raise ValueError("Player names must be different.")
        if len(questions) < ROUNDS:
            raise ValueError(f"At least {ROUNDS} questions are required.")
        self._players = list(players)
        self._questions = list(questions)
        self._score = {player: 0 for player in self._players}
        self._round = 0
        self._answers = {}
    
    @property
    def players(self):
        return self._players
    @property
    def rounds(self):
        return self._round
    def score_of(self, player):
        if player not in self._players:
            raise ValueError(f"{player} is not a valid player.")
        return self._score[player]
    def answer_of(self, player):
        if player not in self._players:
            raise ValueError(f"{player} is not a valid player.")
        return self._answers[player]
    def start_round(self):
        if self._round >= ROUNDS:
            raise ValueError("All rounds have been played.")
        self._round += 1
        self._answers = {}
        return self._questions[self._round - 1]
    def submit(self, player, choice, elapsed):
        self._answers[player] = (choice, elapsed)
    def is_over(self):
        return self._round >= ROUNDS
    def winner(self):
        player1, player2 = self._players
        if self._score[player1] > self._score[player2]:
            return player1
        if self._score[player1] == self._score[player2]:
            return None
        return player2
    def results_round(self):
        question = self._questions[self._round - 1]
        results = {}
        correct_players = []
        for player in self._players:
            choice, elapsed = self._answers[player]
            if elapsed > TIME_LIMIT:
                results[player] = RoundResult("too_late", 0)
            elif question.is_correct(choice):
                results[player] = RoundResult("correct", SCORE)
                correct_players.append(player)
            else:
                results[player] = RoundResult("incorrect", 0)
        if correct_players:
            fast=correct_players[0]
            for player in correct_players:
                if self._answers[player][1] < self._answers[fast][1]:
                    fast = player
            results[fast] = RoundResult("correct", SCORE + BONUS)
        for player in self._players:
            self._score[player] += results[player].score
        return results
class RoundResult:
    def __init__(self, status, score):
        self._status = status
        self._score = score
    @property
    def status(self):
        return self._status
    @property
    def score(self):
        return self._score
    def add_bonus(self, bonus):
        self._score += bonus
