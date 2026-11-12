from time import perf_counter

from rich.console import Console
from rich.panel import Panel

from engine import Question, Match

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


def hand_over(player):
    console.clear()
    console.print(f"\n[bold magenta]Hand over to {player}![/bold magenta]")
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


def main():
    console.print("[bold cyan]Welcome to the Quiz Game![/bold cyan]\n")
    name1 = input("Enter name for Player 1: ").strip()
    name2 = input("Enter name for Player 2: ").strip()

    match = Match([name1, name2], questions)

    while not match.is_over():
        question = match.start_round()

        for player in match.players:
            hand_over(player)
            choice, elapsed = ask(player, question, match.rounds)
            match.submit(player, choice, elapsed)

        results = match.results_round()
        show_round_results(match, results, question)

    show_final_results(match)


if __name__ == "__main__":
    main()