from re import match
from rich.console import Console
from rich.panel import Panel
from rich.table import Table
from time import perf_counter

from engine import Question, Match, ROUNDS, TIME_LIMIT, BONUS, SCORE

console = Console()
questions = [
    Question(
        "What's the best CMS?",
        ["WordPress", "Joomla", "Drupal", "Headless"],
        "A"
    ),

    Question(
        "What's the best programming language?",
        ["Python", "JavaScript", "Java", "C++"],
        "A"
    ),

    Question(
        "What's the best database?",
        ["MySQL", "PostgreSQL", "MongoDB", "SQL"],
        "B"
    ),
]


def show_menu():

    while True:

        user_input = input(
            "Do you want to start the quiz?(yes/no) "
        ).strip().lower()

        if user_input == "yes":
            return True

        elif user_input == "no":

            console.print(
                "Exiting the quiz. Goodbye!",
                style="yellow on black"
            )

            return False

        else:

            console.print(
                "Invalid input. Please enter yes or no.",
                style="red on white"
            )

def play_quiz(match):

    while not match.is_over():

        question = match.start_round()

        console.print(
            Panel(
                f"[bold cyan]Round {match.rounds}[/bold cyan]\n\n"
                f"{question.text}",
                title="QUIZ GAME"
            )
        )

        for option in question.options:
            console.print(option)
        for player in match.players:

            console.print(
                f"\n[bold yellow]{player}'s turn[/bold yellow]"
            )

            start_time = perf_counter()

            user_answer = input("Your choice: ").strip().upper()

            elapsed = perf_counter() - start_time

            match.submit(player, user_answer, elapsed)
        results = match.results_round()
        
        for player in match.players:

            result = results[player]

            console.print(
                f"{player}: {result.status} | "
                f"Score: +{result.score}"
            )
        console.print("\n[bold cyan]Current Scores[/bold cyan]")

        for player in match.players:

            console.print(
                f"{player}: {match.score_of(player)}"
            )
def show_results(match):

    table = Table(title="FINAL RESULTS")

    table.add_column("Player", style="cyan")
    table.add_column("Score", justify="center")

    for player in match.players:

        table.add_row(
            player,
            str(match.score_of(player))
        )

    console.print(table)

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
match = Match([name1, name2], questions)
while not match.is_over():
    question = match.start_round()
    for index, player in enumerate(match.players):
        hand_over(player)
        choice, elapsed = ask(player, question, match.rounds)
        match.submit(player, choice, elapsed)
    results = match.results_round()
    show_round_results(match, results, question)
show_final_results(match)