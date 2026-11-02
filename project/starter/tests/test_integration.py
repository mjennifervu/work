"""Integration tests for the full quiz application."""

import json
import pytest
from utils.data_loader import load_flashcards
from utils.quiz_modes import QuizModeFactory
from utils.quiz_engine import QuizEngine


@pytest.fixture
def sample_json_file(tmp_path):
    """Create a temporary JSON file with sample flashcards."""
    file_path = tmp_path / "test_cards.json"
    data = [
        {"front": "What is 2+2?", "back": "4"},
        {"front": "What is the capital of France?", "back": "Paris"},
        {"front": "What is Python?", "back": "A programming language"},
    ]
    file_path.write_text(json.dumps(data))
    return str(file_path)


class TestFullQuizSession:
    """Test a complete quiz session."""

    def test_full_session_sequential_all_correct(self, sample_json_file):
        """Test a complete sequential quiz with all correct answers."""
        cards = load_flashcards(sample_json_file)
        mode = QuizModeFactory.create("sequential", cards)
        engine = QuizEngine(mode)

        engine.start_quiz()
        engine.submit_answer("4")
        engine.get_next_card()
        engine.submit_answer("Paris")
        engine.get_next_card()
        engine.submit_answer("A programming language")

        results = engine.get_results()
        assert results.total_questions == 3
        assert results.correct_count == 3
        assert results.incorrect_count == 0
        assert results.accuracy_percent == 100.0
        assert len(results.missed_cards) == 0

    def test_full_session_with_errors(self, sample_json_file):
        """Test a complete quiz with some incorrect answers."""
        cards = load_flashcards(sample_json_file)
        mode = QuizModeFactory.create("sequential", cards)
        engine = QuizEngine(mode)

        engine.start_quiz()
        engine.submit_answer("5")
        engine.get_next_card()
        engine.submit_answer("Paris")
        engine.get_next_card()
        engine.submit_answer("Wrong")

        results = engine.get_results()
        assert results.total_questions == 3
        assert results.correct_count == 1
        assert results.incorrect_count == 2
        assert results.accuracy_percent == pytest.approx(33.33, rel=0.1)
        assert len(results.missed_cards) == 2

    def test_full_session_random_mode(self, sample_json_file):
        """Test a complete quiz in random mode."""
        cards = load_flashcards(sample_json_file)
        mode = QuizModeFactory.create("random", cards)
        engine = QuizEngine(mode)

        presented_cards = []
        card = engine.start_quiz()

        while card:
            presented_cards.append(card.front)
            if "2+2" in card.front:
                engine.submit_answer("4")
            elif "France" in card.front:
                engine.submit_answer("Paris")
            else:
                engine.submit_answer("A programming language")

            card = engine.get_next_card()

        results = engine.get_results()
        assert results.total_questions == 3
        assert results.correct_count == 3

    def test_full_session_adaptive_mode_retries(self, sample_json_file):
        """Test adaptive mode retries incorrect cards after first pass."""
        cards = load_flashcards(sample_json_file)
        mode = QuizModeFactory.create("adaptive", cards)
        engine = QuizEngine(mode)

        # First pass - go through all cards
        engine.start_quiz()
        engine.submit_answer("Wrong")  # Card 0 (2+2) - incorrect
        engine.get_next_card()
        engine.submit_answer("Paris")  # Card 1 - correct
        engine.get_next_card()
        engine.submit_answer("A programming language")  # Card 2 - correct

        # After first pass, should retry the incorrect card
        next_card = engine.get_next_card()
        assert next_card is not None
        assert "2+2" in next_card.front

        engine.submit_answer("4")  # Now correct

        results = engine.get_results()
        assert results.total_questions == 4
        assert results.correct_count == 3
        assert results.incorrect_count == 1

    def test_load_and_quiz_object_format(self, tmp_path):
        """Test loading and quizzing with object format JSON."""
        file_path = tmp_path / "cards.json"
        data = {
            "cards": [
                {"front": "Q1", "back": "A1"},
                {"front": "Q2", "back": "A2"},
            ]
        }
        file_path.write_text(json.dumps(data))

        cards = load_flashcards(str(file_path))
        mode = QuizModeFactory.create("sequential", cards)
        engine = QuizEngine(mode)

        engine.start_quiz()
        engine.submit_answer("A1")
        engine.get_next_card()
        engine.submit_answer("A2")

        results = engine.get_results()
        assert results.total_questions == 2
        assert results.correct_count == 2


class TestQuizWithDifferentModes:
    """Test quiz behavior with different modes."""

    def test_sequential_vs_random_order(self, sample_json_file):
        """Test that sequential and random modes produce different orders."""
        cards = load_flashcards(sample_json_file)

        seq_mode = QuizModeFactory.create("sequential", cards)
        seq_order = []
        card = seq_mode.get_next_card()
        while card:
            seq_order.append(card.front)
            card = seq_mode.get_next_card()

        random_mode = QuizModeFactory.create("random", cards)
        random_order = []
        card = random_mode.get_next_card()
        while card:
            random_order.append(card.front)
            card = random_mode.get_next_card()

        assert len(seq_order) == len(random_order) == 3
        assert set(seq_order) == set(random_order)

    def test_multiple_quizzes_independence(self, sample_json_file):
        """Test that multiple quiz sessions are independent."""
        cards = load_flashcards(sample_json_file)

        mode1 = QuizModeFactory.create("adaptive", cards)
        engine1 = QuizEngine(mode1)

        mode2 = QuizModeFactory.create("adaptive", cards)
        engine2 = QuizEngine(mode2)

        engine1.start_quiz()
        engine1.submit_answer("Wrong")  # Incorrect answer to first card

        engine2.start_quiz()
        engine2.submit_answer("4")  # Correct answer to first card

        assert len(engine1.responses) == len(engine2.responses) == 1
        assert engine1.responses[0]["is_correct"] is False
        assert engine2.responses[0]["is_correct"] is True
