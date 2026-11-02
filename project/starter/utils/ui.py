"""Terminal UI for the Flashcard Quizzer."""

from .data_loader import Card
from .quiz_engine import QuizResult


class Colors:
    """ANSI color codes for terminal output."""

    GREEN = "\033[92m"
    RED = "\033[91m"
    BLUE = "\033[94m"
    YELLOW = "\033[93m"
    RESET = "\033[0m"
    BOLD = "\033[1m"


def display_card(card: Card, card_number: int, total_cards: int) -> None:
    """Display a flashcard to the user.

    Args:
        card: The Card object to display
        card_number: Current question number
        total_cards: Total number of cards
    """
    print(f"\n{Colors.BLUE}[Question {card_number}/{total_cards}]{Colors.RESET}")
    print(f"{Colors.BOLD}Front:{Colors.RESET} {card.front}")


def get_user_answer() -> str:
    """Prompt the user for an answer.

    Returns:
        The user's answer (or special commands like 'exit')
    """
    answer = input(f"\n{Colors.BOLD}Your answer:{Colors.RESET} ")
    return answer


def display_feedback(is_correct: bool, correct_answer: str) -> None:
    """Display feedback on the user's answer.

    Args:
        is_correct: Whether the answer was correct
        correct_answer: The correct answer from the card
    """
    if is_correct:
        print(f"{Colors.GREEN}✓ Correct!{Colors.RESET}")
    else:
        print(f"{Colors.RED}✗ Incorrect{Colors.RESET}")
        print(f"{Colors.BOLD}Correct answer:{Colors.RESET} {correct_answer}")


def display_results(results: QuizResult) -> None:
    """Display quiz results in a formatted table.

    Args:
        results: QuizResult object with statistics
    """
    print(f"\n{Colors.BOLD}{'='*50}{Colors.RESET}")
    print(f"{Colors.BOLD}Quiz Complete!{Colors.RESET}")
    print(f"{Colors.BOLD}{'='*50}{Colors.RESET}\n")

    print(f"{Colors.BOLD}Statistics:{Colors.RESET}")
    print(f"  Total Questions: {results.total_questions}")
    print(
        f"  Correct: {results.correct_count} "
        f"({Colors.GREEN}{results.accuracy_percent:.1f}%{Colors.RESET})"
    )
    print(f"  Incorrect: {results.incorrect_count}")

    if results.missed_cards:
        print(f"\n{Colors.BOLD}Terms You Missed:{Colors.RESET}")
        for card in results.missed_cards:
            print(f"  • {Colors.RED}{card.front}{Colors.RESET}: {card.back}")

    print(f"\n{Colors.BOLD}{'='*50}{Colors.RESET}\n")


def display_welcome() -> None:
    """Display welcome message."""
    print(f"\n{Colors.BOLD}Welcome to Flashcard Quizzer!{Colors.RESET}")
    print("Type 'exit' or press Ctrl+C to quit at any time.\n")


def display_error(message: str) -> None:
    """Display an error message.

    Args:
        message: The error message to display
    """
    print(f"{Colors.RED}Error: {message}{Colors.RESET}")
