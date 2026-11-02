"""Load and validate flashcards from JSON files."""

import json
from dataclasses import dataclass
from pathlib import Path
from typing import Any


@dataclass
class Card:
    """A single flashcard with front and back sides."""

    front: str
    back: str


def load_flashcards(file_path: str) -> list[Card]:
    """Load flashcards from a JSON file.

    Supports two JSON formats:
    1. Array format: [{"front": "...", "back": "..."}]
    2. Object format: {"cards": [{"front": "...", "back": "..."}]}

    Args:
        file_path: Path to the JSON file

    Returns:
        List of Card objects

    Raises:
        FileNotFoundError: If the file doesn't exist
        ValueError: If JSON is malformed or missing required fields
    """
    path = Path(file_path)

    if not path.exists():
        raise FileNotFoundError(f"Flashcard file not found: {file_path}")

    try:
        with open(path, "r", encoding="utf-8") as f:
            data = json.load(f)
    except json.JSONDecodeError as e:
        raise ValueError(f"Invalid JSON in {file_path}: {e}")

    cards = _parse_json_data(data)
    return cards


def _parse_json_data(data: Any) -> list[Card]:
    """Parse JSON data into a list of Card objects.

    Args:
        data: Parsed JSON data (dict or list)

    Returns:
        List of Card objects

    Raises:
        ValueError: If data structure is invalid
    """
    if isinstance(data, dict):
        if "cards" not in data:
            raise ValueError("Object format requires a 'cards' key")
        cards_data = data["cards"]
    elif isinstance(data, list):
        cards_data = data
    else:
        raise ValueError("JSON must be an array or object with a 'cards' key")

    if not isinstance(cards_data, list):
        raise ValueError("Cards data must be a list")

    if not cards_data:
        raise ValueError("No cards found in the JSON file")

    cards = []
    for i, card_data in enumerate(cards_data):
        if not isinstance(card_data, dict):
            raise ValueError(f"Card {i} is not a dictionary")

        if "front" not in card_data:
            raise ValueError(f"Card {i} is missing the 'front' field")

        if "back" not in card_data:
            raise ValueError(f"Card {i} is missing the 'back' field")

        front = str(card_data["front"]).strip()
        back = str(card_data["back"]).strip()

        if not front or not back:
            raise ValueError(f"Card {i} has empty 'front' or 'back' field")

        cards.append(Card(front=front, back=back))

    return cards
