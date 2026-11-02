# Flashcard Quizzer

A command-line application that loads flashcards from JSON files and quizzes you in sequential, random, or adaptive mode. Built with Python 3.10+ using design patterns (Strategy, Factory) and comprehensive test coverage (97%).

## Features

- **Three Quiz Modes:**
  - **Sequential**: Present cards in order (1 to N)
  - **Random**: Shuffle the deck and present in random order
  - **Adaptive**: Show all cards once, then retry incorrect cards (prioritizes learning)

- **Flexible JSON Input:**
  - Array format: `[{"front": "...", "back": "..."}]`
  - Object format: `{"cards": [...]}`
  - Validates structure with friendly error messages

- **Interactive Quiz Experience:**
  - Case-insensitive answer checking
  - Immediate colored feedback (✓ green for correct, ✗ red for incorrect)
  - Session statistics showing accuracy %, correct/incorrect counts
  - List of terms you missed for targeted review

- **Production-Ready Code:**
  - Modular architecture with clear separation of concerns
  - Type hints throughout for code safety
  - 97% test coverage with 66 comprehensive tests
  - Zero linting errors (flake8) and type checking errors (mypy)
  - Graceful error handling and user-friendly messages

## Project Structure

```
starter/
├── main.py                     # CLI entry point with argparse
├── utils/
│   ├── data_loader.py          # JSON loading and validation
│   ├── quiz_modes.py           # Strategy pattern: Sequential/Random/Adaptive
│   ├── quiz_engine.py          # Core quiz session management
│   └── ui.py                   # Terminal UI with color formatting
├── data/                       # Sample flashcard decks
│   ├── glossary.json           # Technical terms (array format)
│   └── python_basics.json      # Python keywords (object format)
├── tests/                      # Comprehensive pytest suite
│   ├── test_data_loader.py     # JSON loading tests (16 tests)
│   ├── test_quiz_modes.py      # Strategy pattern tests (15 tests)
│   ├── test_quiz_engine.py     # Quiz logic tests (16 tests)
│   ├── test_ui.py              # Display formatting tests (9 tests)
│   └── test_integration.py     # End-to-end tests (10 tests)
├── docs/
│   ├── prompts.md              # AI development process documentation
│   ├── ai_edit_log.md          # Detailed AI interactions and decisions
│   └── report_template.md      # Final project report
└── requirements.txt            # Development dependencies
```

## Installation

### In the provided workspace:
```bash
cd /voc/work/project/starter
python -m pip install -r requirements.txt
```

### On your own computer:
```bash
python3 -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
python -m pip install -r requirements.txt
```

## Usage

### Basic examples:

```bash
# Show help
python main.py --help

# Sequential mode (recommended for learning a new topic)
python main.py -f data/glossary.json -m sequential

# Random mode (shuffle for variety)
python main.py -f data/python_basics.json -m random

# Adaptive mode (focus on cards you miss)
python main.py -f data/glossary.json -m adaptive

# Short flags
python main.py --file data/python_basics.json --mode adaptive
```

### During a quiz:
- Type your answer and press Enter
- Type `exit` to quit at any time
- Press Ctrl+C to exit gracefully

### Example quiz output:
```
Welcome to Flashcard Quizzer!
Type 'exit' or press Ctrl+C to quit at any time.

[Question 1/10]
Front: What is an API?

Your answer: Application Programming Interface
✓ Correct!

[Question 2/10]
Front: What is a CDN?

Your answer: Content Delivery Network
✓ Correct!

...

==================================================
Quiz Complete!
==================================================

Statistics:
  Total Questions: 10
  Correct: 9 (90.0%)
  Incorrect: 1

Terms You Missed:
  • VPN: Virtual Private Network

==================================================
```

## Design Patterns

### Strategy Pattern (Quiz Modes)
Different quiz algorithms (Sequential, Random, Adaptive) implement the same QuizMode interface, allowing new modes to be added without modifying existing code.

### Factory Pattern (Mode Selection)
The `QuizModeFactory` centralizes mode instantiation, providing a clean API for selecting quiz modes by name.

### Dataclasses
Type-safe data structures for Card, QuizState, and QuizResult ensure data integrity throughout the application.

## Code Quality

The application meets production-ready standards:

```bash
# Run all tests with coverage
python -m pytest tests/ --cov=utils --cov-report=html

# Check code formatting
python -m black --check .

# Lint for style issues
python -m flake8 .

# Type checking
python -m mypy .
```

### Quality Metrics:
- **Test Coverage:** 97% (66 tests, >80% required)
- **Linting:** 0 errors (flake8)
- **Type Checking:** 0 errors (mypy)
- **Code Style:** Consistent (black-compatible)

## Architecture Overview

### Data Flow:
1. **User starts quiz** → `main.py` loads arguments
2. **Load flashcards** → `data_loader.py` validates and parses JSON
3. **Create quiz session** → `quiz_engine.py` initializes with chosen mode
4. **Present and track answers** → `ui.py` displays cards, `quiz_engine.py` scores
5. **Calculate and display stats** → `ui.py` shows results with colors

### Mode Behavior:

**Sequential Mode:**
```
1. Present cards 1, 2, 3...N in order
2. Show stats
```

**Random Mode:**
```
1. Shuffle deck
2. Present cards in shuffled order
3. Show stats
```

**Adaptive Mode:**
```
1. Present all cards 1...N (first pass)
   - Track incorrect cards
2. After first pass, retry incorrect cards
3. Show stats (question count includes retries)
```

## Testing Strategy

The test suite covers:

1. **Data Loading** - Valid/invalid JSON, both formats, error handling
2. **Quiz Modes** - All three modes work correctly, factory pattern functions
3. **Quiz Engine** - Answer tracking, stats calculation, adaptive mode logic
4. **UI Display** - Formatting, colors, output content
5. **Integration** - Full quiz sessions with different modes and outcomes

Run tests with: `python -m pytest tests/ -v`

## Sample Flashcard Decks

### glossary.json (Array Format)
10 technical terms with definitions. Good for testing with large decks.

### python_basics.json (Object Format)
8 Python keywords and built-in functions. Good for quick full quiz tests.

Add your own decks to the `data/` folder in either JSON format.

## Lessons Learned

### Key Insights from Development:

1. **Design Before Code** - Spending time on architecture (module plan) prevented rework
2. **Comprehensive Testing** - 97% test coverage caught design issues (e.g., Adaptive mode algorithm) early
3. **Type Hints Matter** - Added type annotation to factory's `_modes` dict caught subtle bugs in mypy
4. **Separation of Concerns** - Clean module boundaries made testing individual components straightforward
5. **User Experience** - Real-world testing with actual data revealed UI improvements (e.g., question numbering in adaptive mode)

## Future Enhancements

Possible improvements for future versions:

- **Spaced Repetition Mode** - Use `QuizModeFactory` to add new mode without changing existing code
- **Statistics Tracking** - Store results to track long-term learning progress
- **Difficulty Levels** - Hide definitions initially, show on second try
- **CSV Import** - Support other data formats beyond JSON
- **Web Interface** - Use same quiz engine with a Flask/FastAPI frontend

## License

[License](../../LICENSE.txt)
