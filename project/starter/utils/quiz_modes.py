"""Quiz mode implementations using the Strategy pattern."""

import random
from abc import ABC, abstractmethod
from dataclasses import dataclass, field

from .data_loader import Card


@dataclass
class QuizState:
    """State tracking for a quiz session."""

    cards: list[Card]
    current_index: int = 0
    attempts: dict[int, int] = field(default_factory=dict)


class QuizMode(ABC):
    """Abstract base class for quiz modes."""

    def __init__(self, cards: list[Card]):
        """Initialize quiz mode.

        Args:
            cards: List of flashcards
        """
        self.state = QuizState(cards=cards)

    @abstractmethod
    def get_next_card(self) -> Card | None:
        """Get the next card to present to the user.

        Returns:
            The next Card, or None if quiz is complete
        """

    def mark_attempt(self, card_index: int) -> None:
        """Track an attempt for a card.

        Args:
            card_index: Index of the card attempted
        """
        self.state.attempts[card_index] = self.state.attempts.get(card_index, 0) + 1

    def is_complete(self) -> bool:
        """Check if all cards have been attempted at least once.

        Returns:
            True if the quiz should end
        """
        return False


class Sequential(QuizMode):
    """Quiz mode that presents cards in order."""

    def get_next_card(self) -> Card | None:
        """Get the next card in sequence."""
        if self.state.current_index >= len(self.state.cards):
            return None
        card = self.state.cards[self.state.current_index]
        self.state.current_index += 1
        return card


class Random(QuizMode):
    """Quiz mode that presents cards in random order."""

    def __init__(self, cards: list[Card]):
        """Initialize random mode and shuffle the deck."""
        super().__init__(cards)
        random.shuffle(self.state.cards)

    def get_next_card(self) -> Card | None:
        """Get the next card in random order."""
        if self.state.current_index >= len(self.state.cards):
            return None
        card = self.state.cards[self.state.current_index]
        self.state.current_index += 1
        return card


class Adaptive(QuizMode):
    """Quiz mode that prioritizes previously incorrect cards."""

    def __init__(self, cards: list[Card]):
        """Initialize adaptive mode."""
        super().__init__(cards)
        self.incorrect_indices: list[int] = []
        self.first_pass_complete: bool = False

    def get_next_card(self) -> Card | None:
        """Get the next card, prioritizing incorrect ones after first pass."""
        if not self.state.cards:
            return None

        if not self.first_pass_complete:
            if self.state.current_index >= len(self.state.cards):
                self.first_pass_complete = True
            else:
                card_index = self.state.current_index
                self.state.current_index += 1
                self.mark_attempt(card_index)
                return self.state.cards[card_index]

        if self.incorrect_indices:
            card_index = self.incorrect_indices.pop(0)
            self.mark_attempt(card_index)
            return self.state.cards[card_index]

        return None

    def mark_incorrect(self, card_index: int) -> None:
        """Mark a card as incorrect to be retried.

        Args:
            card_index: Index of the card that was answered incorrectly
        """
        if card_index not in self.incorrect_indices:
            self.incorrect_indices.append(card_index)


class QuizModeFactory:
    """Factory for creating quiz mode instances."""

    _modes: dict[str, type[QuizMode]] = {
        "sequential": Sequential,
        "random": Random,
        "adaptive": Adaptive,
    }

    @classmethod
    def create(cls, mode_name: str, cards: list[Card]) -> QuizMode:
        """Create a quiz mode instance.

        Args:
            mode_name: Name of the mode ('sequential', 'random', or 'adaptive')
            cards: List of flashcards

        Returns:
            A QuizMode instance

        Raises:
            ValueError: If the mode name is invalid
        """
        mode_name = mode_name.lower().strip()
        if mode_name not in cls._modes:
            valid = ", ".join(cls._modes.keys())
            raise ValueError(f"Invalid mode '{mode_name}'. Choose from: {valid}")

        return cls._modes[mode_name](cards)

    @classmethod
    def get_available_modes(cls) -> list[str]:
        """Get list of available mode names.

        Returns:
            List of mode names
        """
        return list(cls._modes.keys())
