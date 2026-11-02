"""Tests for the quiz engine."""

import pytest
from utils.data_loader import Card
from utils.quiz_modes import Sequential, Adaptive
from utils.quiz_engine import QuizEngine, QuizResult


@pytest.fixture
def sample_cards():
    """Create sample cards for testing."""
    return [
        Card(front="Q1", back="A1"),
        Card(front="Q2", back="A2"),
        Card(front="Q3", back="A3"),
    ]


@pytest.fixture
def quiz_engine(sample_cards):
    """Create a quiz engine with sample cards."""
    mode = Sequential(sample_cards)
    return QuizEngine(mode)


class TestQuizEngineBasics:
    """Test basic quiz engine functionality."""

    def test_start_quiz(self, quiz_engine):
        """Test starting a quiz."""
        card = quiz_engine.start_quiz()
        assert card is not None
        assert card.front == "Q1"

    def test_get_next_card(self, quiz_engine):
        """Test getting the next card."""
        quiz_engine.start_quiz()
        card = quiz_engine.get_next_card()
        assert card.front == "Q2"

    def test_no_more_cards(self, quiz_engine):
        """Test that None is returned when no more cards."""
        quiz_engine.start_quiz()
        quiz_engine.get_next_card()
        quiz_engine.get_next_card()
        card = quiz_engine.get_next_card()
        assert card is None


class TestAnswerSubmission:
    """Test submitting answers."""

    def test_correct_answer(self, quiz_engine):
        """Test submitting a correct answer."""
        quiz_engine.start_quiz()
        is_correct = quiz_engine.submit_answer("A1")
        assert is_correct is True

    def test_incorrect_answer(self, quiz_engine):
        """Test submitting an incorrect answer."""
        quiz_engine.start_quiz()
        is_correct = quiz_engine.submit_answer("Wrong")
        assert is_correct is False

    def test_case_insensitive_answer(self, quiz_engine):
        """Test that answer checking is case-insensitive."""
        quiz_engine.start_quiz()
        assert quiz_engine.submit_answer("a1") is True
        quiz_engine.get_next_card()
        assert quiz_engine.submit_answer("A2") is True

    def test_whitespace_handling(self, quiz_engine):
        """Test that whitespace is handled correctly."""
        quiz_engine.start_quiz()
        assert quiz_engine.submit_answer("  A1  ") is True

    def test_submit_without_card_raises_error(self, quiz_engine):
        """Test that submitting without a card raises an error."""
        with pytest.raises(RuntimeError):
            quiz_engine.submit_answer("answer")


class TestResponseTracking:
    """Test response tracking."""

    def test_responses_are_recorded(self, quiz_engine):
        """Test that responses are recorded."""
        quiz_engine.start_quiz()
        quiz_engine.submit_answer("A1")
        quiz_engine.get_next_card()
        quiz_engine.submit_answer("Wrong")

        assert len(quiz_engine.responses) == 2
        assert quiz_engine.responses[0]["is_correct"] is True
        assert quiz_engine.responses[1]["is_correct"] is False

    def test_missed_card_indices_tracked(self, quiz_engine):
        """Test that missed card indices are tracked."""
        quiz_engine.start_quiz()
        quiz_engine.submit_answer("Wrong")
        assert 0 in quiz_engine.missed_card_indices


class TestQuizResults:
    """Test quiz results calculation."""

    def test_results_all_correct(self, quiz_engine):
        """Test results when all answers are correct."""
        quiz_engine.start_quiz()
        quiz_engine.submit_answer("A1")
        quiz_engine.get_next_card()
        quiz_engine.submit_answer("A2")
        quiz_engine.get_next_card()
        quiz_engine.submit_answer("A3")

        results = quiz_engine.get_results()
        assert results.total_questions == 3
        assert results.correct_count == 3
        assert results.incorrect_count == 0
        assert results.accuracy_percent == 100.0

    def test_results_all_incorrect(self, quiz_engine):
        """Test results when all answers are incorrect."""
        quiz_engine.start_quiz()
        quiz_engine.submit_answer("Wrong1")
        quiz_engine.get_next_card()
        quiz_engine.submit_answer("Wrong2")
        quiz_engine.get_next_card()
        quiz_engine.submit_answer("Wrong3")

        results = quiz_engine.get_results()
        assert results.total_questions == 3
        assert results.correct_count == 0
        assert results.incorrect_count == 3
        assert results.accuracy_percent == 0.0

    def test_results_partial_correct(self, quiz_engine):
        """Test results with mixed correct/incorrect."""
        quiz_engine.start_quiz()
        quiz_engine.submit_answer("A1")
        quiz_engine.get_next_card()
        quiz_engine.submit_answer("Wrong")
        quiz_engine.get_next_card()
        quiz_engine.submit_answer("A3")

        results = quiz_engine.get_results()
        assert results.total_questions == 3
        assert results.correct_count == 2
        assert results.incorrect_count == 1
        assert results.accuracy_percent == pytest.approx(66.67, rel=0.1)

    def test_missed_cards_list(self, quiz_engine):
        """Test that missed cards are recorded."""
        quiz_engine.start_quiz()
        quiz_engine.submit_answer("A1")
        quiz_engine.get_next_card()
        quiz_engine.submit_answer("Wrong")
        quiz_engine.get_next_card()
        quiz_engine.submit_answer("A3")

        results = quiz_engine.get_results()
        assert len(results.missed_cards) == 1
        assert results.missed_cards[0].front == "Q2"


class TestQuizResultDataclass:
    """Test QuizResult dataclass."""

    def test_accuracy_percent_calculation(self):
        """Test accuracy percentage calculation."""
        result = QuizResult(
            total_questions=4,
            correct_count=3,
            incorrect_count=1,
        )
        assert result.accuracy_percent == 75.0

    def test_accuracy_percent_zero_questions(self):
        """Test accuracy with zero questions."""
        result = QuizResult(
            total_questions=0,
            correct_count=0,
            incorrect_count=0,
        )
        assert result.accuracy_percent == 0.0


class TestAdaptiveModeIntegration:
    """Test adaptive mode with quiz engine."""

    def test_adaptive_mode_retries_incorrect(self, sample_cards):
        """Test that adaptive mode retries incorrect cards after first pass."""
        mode = Adaptive(sample_cards)
        engine = QuizEngine(mode)

        # First pass through all cards
        engine.start_quiz()
        engine.submit_answer("Wrong")  # Q1 incorrect

        engine.get_next_card()
        engine.submit_answer("A2")  # Q2 correct

        engine.get_next_card()
        engine.submit_answer("A3")  # Q3 correct

        # After first pass, should retry Q1
        next_card = engine.get_next_card()
        assert next_card.front == "Q1"
