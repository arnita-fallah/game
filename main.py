from re import match
from rich.console import Console
from rich.panel import Panel
from rich.table import Table
from time import perf_counter
from engine import Question, Match, ROUNDS, TIME_LIMIT, BONUS, SCORE
from game.storage import QuestionBank


console = Console()
questions = QuestionBank()

def show_menu():
    while True:

def ask(player, question, round_number):
    console.clear()
    console.print(
        Panel(
            f"[bold cyan]Round {round_number}[/bold cyan]\n\n"
            f"{question.text}",
            title="QUIZ GAME"
        )
    )

    for option in question.options:
        console.print(option)

    start_time = perf_counter()
    user_answer = input(f"\n{player}, your choice: ").strip().upper()
    elapsed = perf_counter() - start_time

    return user_answer, elapsed


def show_round_results(match, results, question):
    console.clear()
    console.print(
        Panel(
            f"[bold cyan]Round {match.rounds} Results[/bold cyan]\n\n"
            f"{question.text}",
            title="QUIZ GAME"
        )
    )

    for player in match.players:
        result = results[player]
        choice, elapsed = match.answer_of(player)

        if result.status == "correct":
            color = "green"
        elif result.status == "too_late":
            color = "yellow"
        else:
            color = "red"

        console.print(
            f"{player}: [bold {color}]{result.status}[/bold {color}] | "
            f"Score: +{result.score} | "
            f"Time: {elapsed:.2f}s"
        )

    console.print()
    for player in match.players:
        console.print(f"{player}: Total Score: {match.score_of(player)}")

    input("\nPress Enter to continue to the next round...")


def show_final_results(match):
    console.clear()
    console.print(
        Panel(
            "[bold cyan]Final Results[/bold cyan]",
            title="QUIZ GAME"
        )
    )

    for player in match.players:
        console.print(f"{player}: Total Score: {match.score_of(player)}")

    winner = match.winner()

    if winner is None:
        console.print(Panel("[bold yellow]It's a Draw![/bold yellow]"))
    else:
        console.print(Panel(f"[bold green]Winner: {winner}[/bold green]"))

        console.print(
            Panel(
                f"[bold green]Winner: {winner}[/bold green]"
            )
        )
def hand_over(player):
    console.clear()
    console.print(
        f"\n[bold magenta]Hand over to {player}![/bold magenta]"
    )
    input(f"{player}, press Enter when ready...")
def ask(player, question, round_number):
    console.clear()
    console.print(
        Panel(
            f"[bold cyan]Round {round_number}[/bold cyan]\n\n"
            f"{question.text}",
            title="QUIZ GAME"
        )
    )
    for letter, option in zip("ABCD", question.options):
        console.print(f"{letter}: {option}")
    start_time = perf_counter()
    user_answer = input(f"\n{player}, your choice: ").strip().upper()
    elapsed = perf_counter() - start_time
    return user_answer, elapsed
def show_round_results(match, results, question):
    console.clear()
    console.print(
        Panel(
            f"[bold cyan]Round {match.rounds} Results[/bold cyan]\n\n"
            f"{question.text}",
            title="QUIZ GAME"
        )
    )
    for player in match.players:
        result = results[player]
        choice , elapsed = match.answer_of(player)
        
        if result.status == "correct":
            console.print(
                f"{player}: [bold green]{result.status}[/bold green] | "
                f"Score: +{result.score} | "
                f"Time: {elapsed:.2f}s"
            )
        elif result.status == "too_late":
            console.print(
                f"{player}: [bold yellow]{result.status}[/bold yellow] | "
                f"Score: +{result.score} | "
                f"Time: {elapsed:.2f}s"
            )
        elif result.status == "incorrect":
            console.print(
                f"{player}: [bold red]{result.status}[/bold red] | "
                f"Score: +{result.score} | "
                f"Time: {elapsed:.2f}s"
            )
    for player in match.players:
        console.print(
            f"{player}: Total Score: {match.score_of(player)}"
        )
        
    input(f"\n{player}, press Enter to continue to the next round...")

def show_final_results(match):
    console.clear()
    console.print(
        Panel(
            "[bold cyan]Final Results[/bold cyan]",
            title="QUIZ GAME"
        )
    )
    for player in match.players:
        console.print(
            f"{player}: Total Score: {match.score_of(player)}"
        )
    winner = match.winner()
    if winner is None:
        console.print(
            Panel(
                "[bold yellow]It's a Draw![/bold yellow]"
            )
        )
    else:
        console.print(
            Panel(
                f"[bold green]Winner: {winner}[/bold green]"
            )
        )
console.print("[bold cyan]Welcome to the Quiz Game![/bold cyan]\n")
name1 = input("Enter name for Player 1: ").strip()
name2 = input("Enter name for Player 2: ").strip()
match = Match([name1, name2], questions.pick(5))
while not match.is_over():
    question = match.start_round()
    for index, player in enumerate(match.players):
        hand_over(player)
        choice, elapsed = ask(player, question, match.rounds)
        match.submit(player, choice, elapsed)
    results = match.results_round()
    show_round_results(match, results, question)
show_final_results(match)
