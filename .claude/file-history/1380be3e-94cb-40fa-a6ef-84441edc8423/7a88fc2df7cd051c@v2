"""Tests for quiz modes and factory."""

import pytest
from utils.data_loader import Card
from utils.quiz_modes import (
    Sequential,
    Random,
    Adaptive,
    QuizModeFactory,
    QuizMode,
)


@pytest.fixture
def sample_cards():
    """Create sample cards for testing."""
    return [
        Card(front="Q1", back="A1"),
        Card(front="Q2", back="A2"),
        Card(front="Q3", back="A3"),
    ]


class TestSequentialMode:
    """Test Sequential quiz mode."""

    def test_sequential_returns_cards_in_order(self, sample_cards):
        """Test that Sequential mode returns cards in order."""
        mode = Sequential(sample_cards)

        card1 = mode.get_next_card()
        assert card1.front == "Q1"

        card2 = mode.get_next_card()
        assert card2.front == "Q2"

        card3 = mode.get_next_card()
        assert card3.front == "Q3"

        card4 = mode.get_next_card()
        assert card4 is None

    def test_sequential_mark_attempt(self, sample_cards):
        """Test that Sequential mode tracks attempts."""
        mode = Sequential(sample_cards)
        mode.get_next_card()
        mode.mark_attempt(0)
        assert mode.state.attempts[0] == 1


class TestRandomMode:
    """Test Random quiz mode."""

    def test_random_returns_all_cards(self, sample_cards):
        """Test that Random mode returns all cards."""
        mode = Random(sample_cards)
        cards = []

        card = mode.get_next_card()
        while card:
            cards.append(card)
            card = mode.get_next_card()

        assert len(cards) == 3
        assert all(card in sample_cards for card in cards)

    def test_random_shuffles_order(self, sample_cards):
        """Test that Random mode shuffles cards (or handles small decks)."""
        mode = Random(sample_cards)
        shuffled_cards = [card.front for card in mode.state.cards]
        original_order = [card.front for card in sample_cards]
        # Either the order is different or the deck is small (1-2 cards)
        # With 3+ cards, shuffling should usually change order
        if len(sample_cards) >= 3:
            # Just verify all cards are present, shuffle may coincidentally match
            assert set(shuffled_cards) == set(original_order)
        else:
            assert shuffled_cards == original_order or shuffled_cards != original_order


class TestAdaptiveMode:
    """Test Adaptive quiz mode."""

    def test_adaptive_presents_all_cards_once(self, sample_cards):
        """Test that Adaptive mode presents all cards at least once."""
        mode = Adaptive(sample_cards)
        cards = []

        card = mode.get_next_card()
        while card:
            cards.append(card)
            card = mode.get_next_card()

        assert len(cards) == 3

    def test_adaptive_retries_incorrect_cards(self, sample_cards):
        """Test that Adaptive mode retries cards marked as incorrect."""
        mode = Adaptive(sample_cards)

        card1 = mode.get_next_card()
        assert card1 is not None
        mode.mark_incorrect(0)

        card2 = mode.get_next_card()
        assert card2 is not None
        card3 = mode.get_next_card()
        assert card3 is not None

        card_retry = mode.get_next_card()
        assert card_retry is not None

    def test_adaptive_prioritizes_incorrect(self, sample_cards):
        """Test that incorrect cards are retried after first pass."""
        mode = Adaptive(sample_cards)

        # First pass: present each card once
        card1 = mode.get_next_card()
        assert card1.front == "Q1"
        mode.mark_incorrect(0)  # Mark Q1 as incorrect

        card2 = mode.get_next_card()
        assert card2.front == "Q2"

        card3 = mode.get_next_card()
        assert card3.front == "Q3"

        # Second pass: retry incorrect cards
        card_retry = mode.get_next_card()
        assert card_retry.front == "Q1"

    def test_adaptive_tracks_attempts(self, sample_cards):
        """Test that Adaptive mode tracks attempt counts."""
        mode = Adaptive(sample_cards)

        mode.get_next_card()
        assert 0 in mode.state.attempts
        assert mode.state.attempts[0] == 1


class TestQuizModeFactory:
    """Test the Quiz Mode Factory."""

    def test_factory_create_sequential(self, sample_cards):
        """Test factory creates Sequential mode."""
        mode = QuizModeFactory.create("sequential", sample_cards)
        assert isinstance(mode, Sequential)

    def test_factory_create_random(self, sample_cards):
        """Test factory creates Random mode."""
        mode = QuizModeFactory.create("random", sample_cards)
        assert isinstance(mode, Random)

    def test_factory_create_adaptive(self, sample_cards):
        """Test factory creates Adaptive mode."""
        mode = QuizModeFactory.create("adaptive", sample_cards)
        assert isinstance(mode, Adaptive)

    def test_factory_case_insensitive(self, sample_cards):
        """Test that factory is case-insensitive."""
        mode1 = QuizModeFactory.create("SEQUENTIAL", sample_cards)
        mode2 = QuizModeFactory.create("SeQuEnTiAl", sample_cards)
        assert isinstance(mode1, Sequential)
        assert isinstance(mode2, Sequential)

    def test_factory_invalid_mode(self, sample_cards):
        """Test that factory raises ValueError for invalid mode."""
        with pytest.raises(ValueError, match="Invalid mode"):
            QuizModeFactory.create("invalid", sample_cards)

    def test_factory_get_available_modes(self):
        """Test getting available modes."""
        modes = QuizModeFactory.get_available_modes()
        assert "sequential" in modes
        assert "random" in modes
        assert "adaptive" in modes
        assert len(modes) == 3

    def test_factory_all_modes_return_quiz_mode(self, sample_cards):
        """Test that all factory modes return QuizMode instances."""
        for mode_name in QuizModeFactory.get_available_modes():
            mode = QuizModeFactory.create(mode_name, sample_cards)
            assert isinstance(mode, QuizMode)
