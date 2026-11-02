"""Core quiz engine for running quiz sessions."""

from dataclasses import dataclass, field

from .data_loader import Card
from .quiz_modes import QuizMode, Adaptive


@dataclass
class QuizResult:
    """Results from a quiz session."""

    total_questions: int
    correct_count: int
    incorrect_count: int
    missed_cards: list[Card] = field(default_factory=list)

    @property
    def accuracy_percent(self) -> float:
        """Calculate accuracy percentage.

        Returns:
            Accuracy as a percentage (0-100)
        """
        if self.total_questions == 0:
            return 0.0
        return (self.correct_count / self.total_questions) * 100


class QuizEngine:
    """Engine for running a quiz session."""

    def __init__(self, quiz_mode: QuizMode):
        """Initialize the quiz engine.

        Args:
            quiz_mode: A QuizMode instance (Sequential, Random, or Adaptive)
        """
        self.quiz_mode = quiz_mode
        self.current_card: Card | None = None
        self.current_card_index: int | None = None
        self.responses: list[dict] = []
        self.missed_card_indices: set[int] = set()

    def start_quiz(self) -> Card | None:
        """Start the quiz and get the first card.

        Returns:
            The first Card to present, or None if there are no cards
        """
        self.current_card = self.quiz_mode.get_next_card()
        return self.current_card

    def submit_answer(self, user_answer: str) -> bool:
        """Submit an answer for the current card.

        Args:
            user_answer: User's text response

        Returns:
            True if the answer is correct, False otherwise
        """
        if self.current_card is None:
            raise RuntimeError("No card is currently active")

        is_correct = self._check_answer(self.current_card.back, user_answer)

        self.responses.append({
            "card": self.current_card,
            "user_answer": user_answer,
            "is_correct": is_correct,
        })

        if not is_correct:
            self.missed_card_indices.add(len(self.responses) - 1)
            if isinstance(self.quiz_mode, Adaptive):
                card_index = self._find_card_index(self.current_card)
                if card_index is not None:
                    self.quiz_mode.mark_incorrect(card_index)

        return is_correct

    def get_next_card(self) -> Card | None:
        """Get the next card in the quiz.

        Returns:
            The next Card to present, or None if the quiz is complete
        """
        self.current_card = self.quiz_mode.get_next_card()
        return self.current_card

    def get_results(self) -> QuizResult:
        """Get the quiz results.

        Returns:
            QuizResult containing statistics
        """
        total = len(self.responses)
        correct = sum(1 for r in self.responses if r["is_correct"])
        incorrect = total - correct

        missed_cards = []
        seen = set()
        for response in self.responses:
            if not response["is_correct"]:
                card = response["card"]
                card_id = (card.front, card.back)
                if card_id not in seen:
                    missed_cards.append(card)
                    seen.add(card_id)

        return QuizResult(
            total_questions=total,
            correct_count=correct,
            incorrect_count=incorrect,
            missed_cards=missed_cards,
        )

    def _check_answer(self, correct_answer: str, user_answer: str) -> bool:
        """Check if a user's answer is correct (case-insensitive).

        Args:
            correct_answer: The correct answer from the card
            user_answer: The user's input

        Returns:
            True if the answer matches (case-insensitive)
        """
        return correct_answer.lower().strip() == user_answer.lower().strip()

    def _find_card_index(self, card: Card) -> int | None:
        """Find the index of a card in the quiz mode's cards.

        Args:
            card: The card to find

        Returns:
            The card's index, or None if not found
        """
        for i, c in enumerate(self.quiz_mode.state.cards):
            if c.front == card.front and c.back == card.back:
                return i
        return None
