"""Tests for the data loader module."""

import json
import pytest
from utils.data_loader import load_flashcards, Card, _parse_json_data


class TestLoadFlashcardsArray:
    """Test loading flashcards in array format."""

    def test_load_valid_flashcards_array(self, tmp_path):
        """Test loading a valid array format JSON file."""
        file_path = tmp_path / "cards.json"
        data = [
            {"front": "Question 1", "back": "Answer 1"},
            {"front": "Question 2", "back": "Answer 2"},
        ]
        file_path.write_text(json.dumps(data))

        cards = load_flashcards(str(file_path))

        assert len(cards) == 2
        assert cards[0].front == "Question 1"
        assert cards[0].back == "Answer 1"
        assert cards[1].front == "Question 2"
        assert cards[1].back == "Answer 2"

    def test_load_valid_flashcards_object_format(self, tmp_path):
        """Test loading a valid object format JSON file."""
        file_path = tmp_path / "cards.json"
        data = {
            "cards": [
                {"front": "Q1", "back": "A1"},
                {"front": "Q2", "back": "A2"},
            ]
        }
        file_path.write_text(json.dumps(data))

        cards = load_flashcards(str(file_path))

        assert len(cards) == 2
        assert cards[0].front == "Q1"
        assert cards[0].back == "A1"


class TestLoadFlashcardsErrors:
    """Test error handling in data loader."""

    def test_load_missing_file(self):
        """Test that missing file raises FileNotFoundError."""
        with pytest.raises(FileNotFoundError):
            load_flashcards("nonexistent.json")

    def test_load_invalid_json(self, tmp_path):
        """Test that malformed JSON raises ValueError."""
        file_path = tmp_path / "invalid.json"
        file_path.write_text("{this is not valid json")

        with pytest.raises(ValueError, match="Invalid JSON"):
            load_flashcards(str(file_path))

    def test_load_missing_cards_key(self, tmp_path):
        """Test that object format without 'cards' key raises ValueError."""
        file_path = tmp_path / "cards.json"
        data = {"data": [{"front": "Q", "back": "A"}]}
        file_path.write_text(json.dumps(data))

        with pytest.raises(ValueError, match="'cards' key"):
            load_flashcards(str(file_path))

    def test_load_missing_front_field(self, tmp_path):
        """Test that cards missing 'front' field raise ValueError."""
        file_path = tmp_path / "cards.json"
        data = [{"back": "Answer"}]
        file_path.write_text(json.dumps(data))

        with pytest.raises(ValueError, match="'front'"):
            load_flashcards(str(file_path))

    def test_load_missing_back_field(self, tmp_path):
        """Test that cards missing 'back' field raise ValueError."""
        file_path = tmp_path / "cards.json"
        data = [{"front": "Question"}]
        file_path.write_text(json.dumps(data))

        with pytest.raises(ValueError, match="'back'"):
            load_flashcards(str(file_path))

    def test_load_empty_cards_list(self, tmp_path):
        """Test that empty cards list raises ValueError."""
        file_path = tmp_path / "cards.json"
        file_path.write_text(json.dumps([]))

        with pytest.raises(ValueError, match="No cards found"):
            load_flashcards(str(file_path))

    def test_load_empty_front_or_back(self, tmp_path):
        """Test that cards with empty front or back raise ValueError."""
        file_path = tmp_path / "cards.json"
        data = [{"front": "", "back": "Answer"}]
        file_path.write_text(json.dumps(data))

        with pytest.raises(ValueError, match="empty"):
            load_flashcards(str(file_path))

    def test_load_invalid_root_type(self, tmp_path):
        """Test that invalid root type raises ValueError."""
        file_path = tmp_path / "cards.json"
        file_path.write_text(json.dumps("invalid"))

        with pytest.raises(ValueError, match="array or object"):
            load_flashcards(str(file_path))


class TestParseJsonData:
    """Test JSON data parsing."""

    def test_parse_array_format(self):
        """Test parsing array format."""
        data = [
            {"front": "Q1", "back": "A1"},
            {"front": "Q2", "back": "A2"},
        ]
        cards = _parse_json_data(data)
        assert len(cards) == 2
        assert isinstance(cards[0], Card)

    def test_parse_object_format(self):
        """Test parsing object format."""
        data = {"cards": [{"front": "Q1", "back": "A1"}]}
        cards = _parse_json_data(data)
        assert len(cards) == 1
        assert cards[0].front == "Q1"

    def test_parse_strips_whitespace(self):
        """Test that front and back values are stripped."""
        data = [{"front": "  Q1  ", "back": "  A1  "}]
        cards = _parse_json_data(data)
        assert cards[0].front == "Q1"
        assert cards[0].back == "A1"

    def test_parse_converts_to_string(self):
        """Test that values are converted to strings."""
        data = [{"front": 123, "back": 456}]
        cards = _parse_json_data(data)
        assert cards[0].front == "123"
        assert cards[0].back == "456"


class TestCardDataclass:
    """Test the Card dataclass."""

    def test_card_creation(self):
        """Test creating a Card instance."""
        card = Card(front="Question", back="Answer")
        assert card.front == "Question"
        assert card.back == "Answer"

    def test_card_equality(self):
        """Test Card equality."""
        card1 = Card(front="Q", back="A")
        card2 = Card(front="Q", back="A")
        card3 = Card(front="Q", back="B")
        assert card1 == card2
        assert card1 != card3
