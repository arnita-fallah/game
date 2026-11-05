from rich.console import Console
from rich.panel import Panel
from rich.table import Table
from time import perf_counter

from engine_class import Question, Mach

console = Console()
questions = [
    Question(
        "What's the best CMS?",
        ["A: WordPress", "B: Joomla", "C: Drupal", "D: Headless"],
        "A"
    ),

    Question(
        "What's the best programming language?",
        ["A: Python", "B: JavaScript", "C: Java", "D: C++"],
        "A"
    ),

    Question(
        "What's the best database?",
        ["A: MySQL", "B: PostgreSQL", "C: MongoDB", "D: SQL"],
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
while True:

    if show_menu():

        try:

            player1 = input("Enter Player 1 name: ").strip()
            player2 = input("Enter Player 2 name: ").strip()

            match = Mach(
                player1,
                player2,
                questions
            )

            play_quiz(match)

            show_results(match)

        except ValueError as error:

            console.print(
                f"Error: {error}",
                style="red"
            )

    else:
        break
