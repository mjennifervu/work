"""Tests for UI components."""

import pytest
from utils.data_loader import Card
from utils.quiz_engine import QuizResult
from utils.ui import (
    display_card,
    display_feedback,
    display_results,
    display_welcome,
    display_error,
    Colors,
)


@pytest.fixture
def capture_output(capsys):
    """Fixture to capture printed output."""
    return capsys


class TestColorConstants:
    """Test color constants."""

    def test_color_codes_exist(self):
        """Test that color codes are defined."""
        assert Colors.GREEN
        assert Colors.RED
        assert Colors.BLUE
        assert Colors.YELLOW
        assert Colors.RESET
        assert Colors.BOLD


class TestDisplayCard:
    """Test card display function."""

    def test_display_card_output(self, capture_output):
        """Test that display_card outputs the card."""
        card = Card(front="Test Question", back="Test Answer")
        display_card(card, 1, 5)

        out, _ = capture_output.readouterr()
        assert "Test Question" in out
        assert "Question 1/5" in out

    def test_display_card_numbering(self, capture_output):
        """Test that card numbering is correct."""
        card = Card(front="Q", back="A")
        display_card(card, 3, 10)

        out, _ = capture_output.readouterr()
        assert "Question 3/10" in out


class TestDisplayFeedback:
    """Test feedback display function."""

    def test_display_correct_feedback(self, capture_output):
        """Test feedback for correct answer."""
        display_feedback(True, "Correct Answer")

        out, _ = capture_output.readouterr()
        assert "Correct" in out

    def test_display_incorrect_feedback(self, capture_output):
        """Test feedback for incorrect answer."""
        display_feedback(False, "Correct Answer")

        out, _ = capture_output.readouterr()
        assert "Incorrect" in out
        assert "Correct Answer" in out


class TestDisplayResults:
    """Test results display function."""

    def test_display_results_output(self, capture_output):
        """Test that results are displayed."""
        results = QuizResult(
            total_questions=10,
            correct_count=8,
            incorrect_count=2,
            missed_cards=[
                Card(front="Q1", back="A1"),
                Card(front="Q2", back="A2"),
            ],
        )
        display_results(results)

        out, _ = capture_output.readouterr()
        assert "Quiz Complete" in out
        assert "Total Questions: 10" in out
        assert "Correct: 8" in out
        assert "Incorrect: 2" in out

    def test_display_results_accuracy(self, capture_output):
        """Test that accuracy percentage is displayed."""
        results = QuizResult(
            total_questions=10,
            correct_count=7,
            incorrect_count=3,
        )
        display_results(results)

        out, _ = capture_output.readouterr()
        assert "70" in out

    def test_display_results_missed_cards(self, capture_output):
        """Test that missed cards are displayed."""
        card1 = Card(front="Question 1", back="Answer 1")
        card2 = Card(front="Question 2", back="Answer 2")
        results = QuizResult(
            total_questions=2,
            correct_count=0,
            incorrect_count=2,
            missed_cards=[card1, card2],
        )
        display_results(results)

        out, _ = capture_output.readouterr()
        assert "Terms You Missed" in out
        assert "Question 1" in out
        assert "Question 2" in out

    def test_display_results_no_missed_cards(self, capture_output):
        """Test results display when no cards were missed."""
        results = QuizResult(
            total_questions=3,
            correct_count=3,
            incorrect_count=0,
            missed_cards=[],
        )
        display_results(results)

        out, _ = capture_output.readouterr()
        assert "Quiz Complete" in out


class TestDisplayWelcome:
    """Test welcome message display."""

    def test_display_welcome_output(self, capture_output):
        """Test that welcome message is displayed."""
        display_welcome()

        out, _ = capture_output.readouterr()
        assert "Welcome" in out
        assert "Flashcard Quizzer" in out
        assert "exit" in out


class TestDisplayError:
    """Test error message display."""

    def test_display_error_output(self, capture_output):
        """Test that error message is displayed."""
        display_error("Test error message")

        out, _ = capture_output.readouterr()
        assert "Error" in out
        assert "Test error message" in out
