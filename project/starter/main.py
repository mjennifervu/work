"""Entry point for the Flashcard Quizzer CLI."""

import argparse
import sys

from utils.data_loader import load_flashcards
from utils.quiz_modes import QuizModeFactory
from utils.quiz_engine import QuizEngine
from utils.ui import (
    display_card,
    get_user_answer,
    display_feedback,
    display_results,
    display_welcome,
    display_error,
)


def parse_arguments() -> argparse.Namespace:
    """Parse command-line arguments.

    Returns:
        Parsed arguments
    """
    parser = argparse.ArgumentParser(
        description="Flashcard Quizzer - Learn with interactive flashcards",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="Examples:\n"
               "  python main.py -f data/glossary.json -m sequential\n"
               "  python main.py -f data/python_basics.json -m random --stats",
    )

    parser.add_argument(
        "-f",
        "--file",
        required=True,
        help="Path to the JSON file containing flashcards",
    )

    parser.add_argument(
        "-m",
        "--mode",
        default="sequential",
        choices=["sequential", "random", "adaptive"],
        help="Quiz mode (default: sequential)",
    )

    parser.add_argument(
        "--stats",
        action="store_true",
        help="Display statistics at the end of the quiz",
    )

    return parser.parse_args()


def run_quiz() -> None:
    """Run the flashcard quiz application."""
    args = parse_arguments()

    try:
        cards = load_flashcards(args.file)
    except (FileNotFoundError, ValueError) as e:
        display_error(str(e))
        sys.exit(1)

    quiz_mode = QuizModeFactory.create(args.mode, cards)
    engine = QuizEngine(quiz_mode)

    display_welcome()

    card_number = 0
    total_cards = len(cards)

    try:
        card = engine.start_quiz()

        while card is not None:
            card_number += 1
            display_card(card, card_number, total_cards)

            user_answer = get_user_answer()

            if user_answer.lower() == "exit":
                print("\nQuiz ended. Goodbye!")
                sys.exit(0)

            is_correct = engine.submit_answer(user_answer)
            display_feedback(is_correct, card.back)

            card = engine.get_next_card()

        results = engine.get_results()
        display_results(results)

    except KeyboardInterrupt:
        print("\n\nQuiz interrupted. Goodbye!")
        sys.exit(0)


if __name__ == "__main__":
    run_quiz()
