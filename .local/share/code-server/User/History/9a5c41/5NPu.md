# Prompts Log

This file documents the prompts used for guiding Claude through building the Flashcard Quizzer. For detailed analysis and notes on prompt interactions, refer to docs/ai_edit_log.md

---

## 1. Requirements set up

**Prompt**
In this project, your goal is to engineer with AI-generated code to build a production-ready Command Line Interface (CLI) application: The Flashcard Quizzer. 
You must produce an application that meets the following criteria:

1. Functional Requirements (What the app does)
Data Ingestion:
The app must load flashcards from a JSON file.
It must validate the JSON structure. If the file is missing or malformed, the app should crash gracefully with a helpful error message, not a stack trace.
• Requirement: The app must support JSON input in two formats:
1. Array Format: A simple list of objects [{"front": "...", "back": "..."}].
2. Object Format: A wrapper object {"cards": [...]}.
Error Handling: If the JSON is malformed or missing fields, the app must catch the error and print a friendly message (no raw Python tracebacks).
The Quiz Loop:
Present the "Front" of the card to the user.
Accept text input for the answer.
Compare input to the "Back" of the card (case-insensitive).
Provide immediate feedback (Correct/Incorrect).
Quiz Modes:
Sequential: Go through cards from 1 to N.
Random: Shuffle the deck.
Adaptive: This is the challenge feature. The app should prioritize cards the user previously got wrong.
Session Stats:
At the end of a quiz, show a summary table: Total Questions, Accuracy %, and a list of terms the user missed.
2. Technical Requirements
Architecture:
The code must be modular. Do not submit a single main.py file. Separation of concerns is required (e.g., data_loader.py, quiz_engine.py, ui.py).
Design Patterns:
Use the Strategy Pattern for the Quiz Modes.
Why? Because Sequential, Random, and Adaptive are different algorithms for the same task (selecting the next card). This allows you to easily add a "Spaced Repetition" mode later without rewriting the whole app.
Implement a QuizMode abstract base class. Then create three classes - Sequential, Random, and Adaptive - that inherit from it. Use a Factory Pattern to select the correct mode based on user input.
Type Safety:
All functions must have Python Type Hints.
Testing:
The project must include a test suite (using pytest).
You need at least 80% code coverage including
A. Data Loader Tests (test_flashcard_loader.py)
• test_load_valid_flashcards_array: Does it load a list correctly?
• test_load_invalid_json: Does it gracefully handle bad syntax?
• test_load_missing_required_field: Does it reject cards without a "Back"?
B. Quiz Logic Tests (test_quiz_modes.py)
• test_quiz_mode_factory: Does the factory return the correct class object?
• test_adaptive_mode_behavior: Does it actually repeat incorrect questions?
C. Integration Tests (test_integration.py)
test_full_session: Simulate a user answering 3 questions and checking the final stats calculation.
CLI
• Use argparse to handle flags like -f (file), -m (mode), and --stats.
• Display text colors (Green for correct, Red for incorrect).
• Allow the user to type "exit" or press Ctrl+C to quit gracefully without errors.
QC
• environment: python 3.10+
• before saying app is done, run pytest and flake8 and make sure they are clean
• flake8 must report zero linting errors
Deliverables
• modular source code
• a prompts.md prompt log documenting what was asked for at each step
• Completed ai_edit_log.md with at least 5 detailed AI interaction examples
• Final project report using the provided template in docs/report_template.md (1000-1500 words)
• Updated README.md with current setup instructions and feature descriptions
• Test coverage report demonstrating >80% coverage
• Code quality verification (all linting tools should pass without errors)

Do not write the code yet. Give the module plan first

**Outcome:**


---

## 2. Module Planning and Architecture

**Prompt:**
Based on the requirements, create a detailed module plan for the Flashcard Quizzer application before implementing any code. The plan should outline:
- Core modules with clear responsibilities (data_loader, quiz_modes, quiz_engine, ui, main)
- Design patterns (Strategy for quiz modes, Factory for mode selection)
- Data structures (Card dataclass, QuizState, QuizResult)
- Test structure (test files organized by component)

**Outcome:**
Created a comprehensive module architecture plan with:
- Modular separation of concerns across 5 core modules
- Clear dependencies between modules
- Strategy pattern for quiz modes (Sequential, Random, Adaptive)
- Factory pattern for mode instantiation
- Comprehensive test organization with >80% target coverage

---

## 3. Data Layer Implementation

**Prompt:**
Implement the data_loader.py module that:
- Loads flashcards from JSON files
- Supports both array and object formats
- Validates JSON structure with friendly error messages
- Handles missing files and malformed JSON gracefully
- Returns a list of Card dataclass objects

**Outcome:**
Implemented utils/data_loader.py with:
- Card dataclass for type-safe card representation
- load_flashcards() function supporting both JSON formats
- Comprehensive validation with user-friendly error messages
- 96% code coverage with 16 test cases covering all error scenarios

---

## 4. Quiz Mode Design Patterns

**Prompt:**
Implement the quiz_modes.py module with:
- QuizMode abstract base class defining the interface
- Sequential mode (cards in order)
- Random mode (shuffled order)
- Adaptive mode (prioritizes incorrect cards after first pass)
- QuizModeFactory for creating mode instances by name
- Type hints throughout

**Outcome:**
Implemented utils/quiz_modes.py with:
- Abstract base class with clear contract for subclasses
- Three concrete implementations using Strategy pattern
- Factory pattern for mode instantiation
- QuizState dataclass for tracking quiz progress
- 97% code coverage with 15 test cases
- Adaptive mode correctly retries incorrect cards after first pass

---

## 5. Quiz Engine and Session Management

**Prompt:**
Implement the quiz_engine.py module that:
- Manages quiz sessions using any QuizMode
- Tracks user responses and correctness
- Calculates statistics (accuracy %, missed cards)
- Marks incorrect cards for adaptive mode retries
- Returns QuizResult dataclass with final stats

**Outcome:**
Implemented utils/quiz_engine.py with:
- QuizEngine class managing the quiz flow
- QuizResult dataclass with accuracy calculation
- Response tracking and missed card collection
- Integration with adaptive mode for retry logic
- 98% code coverage with 16 test cases

---

## 6. Terminal UI and Formatting

**Prompt:**
Implement the ui.py module that:
- Displays flashcard questions with formatting
- Shows correct/incorrect feedback with colors (green/red)
- Displays final stats in a formatted table
- Handles user input prompts
- Displays error messages and welcome message

**Outcome:**
Implemented utils/ui.py with:
- Colors class with ANSI color codes
- Functions for displaying cards, feedback, results, and messages
- Terminal-friendly formatting with bold and colored text
- 95% code coverage with 9 test cases

---

## 7. CLI Entry Point

**Prompt:**
Implement the main.py entry point with:
- argparse configuration for -f (file), -m (mode), --stats flags
- Quiz loop orchestration
- Graceful error handling and Ctrl+C support
- Integration of all modules

**Outcome:**
Implemented main.py with:
- argparse setup with descriptive help messages
- Main quiz loop using QuizEngine
- Graceful handling of KeyboardInterrupt
- "exit" command support
- Error handling with user-friendly messages
- Results display with statistics

---

## 8. Comprehensive Test Suite

**Prompt:**
Implement a comprehensive test suite with:
- test_data_loader.py: JSON loading and validation tests
- test_quiz_modes.py: Strategy pattern and factory tests
- test_quiz_engine.py: Quiz logic and statistics tests
- test_ui.py: Output formatting and display tests
- test_integration.py: End-to-end quiz scenarios
- Target >80% code coverage

**Outcome:**
Implemented 66 tests with 97% code coverage:
- 16 tests for data loading (malformed JSON, missing fields, etc.)
- 15 tests for quiz modes (all three modes, factory)
- 16 tests for quiz engine (answer tracking, stats, adaptive mode)
- 9 tests for UI components (formatting, display)
- 7 tests for integration (full quiz sessions, mode independence)
- All tests pass, zero warnings

---

## 9. Code Quality and Testing

**Prompt:**
Verify code quality by:
- Running pytest with coverage reporting (target >80%)
- Running flake8 for linting (zero errors)
- Running mypy for type checking
- Testing CLI with actual flashcard files
- Testing error handling with invalid inputs

**Outcome:**
Achieved production-ready code quality:
- 66 tests passing with 97% coverage (well above 80% target)
- 0 flake8 linting errors (clean code)
- 0 mypy type checking errors (type-safe)
- CLI tested with sample data files (working correctly)
- Error handling verified (graceful failures with helpful messages)

---

## 10. Application Testing and Verification

**Prompt:**
Test the complete application with:
- Sample JSON files (glossary.json, python_basics.json)
- All quiz modes (sequential, random, adaptive)
- Both JSON formats (array and object)
- Error scenarios (missing file, malformed JSON)
- Complete quiz sessions showing stats

**Outcome:**
Verified complete functionality:
- Sequential mode: presents cards in order
- Random mode: shuffles and presents cards
- Adaptive mode: retries incorrect cards after first pass
- Both JSON formats: loads correctly with full validation
- Error handling: displays friendly messages without stack traces
- Statistics: shows accuracy %, correct/incorrect counts, and missed terms
- Colors: green for correct, red for incorrect feedback
- Ctrl+C handling: graceful exit without errors

---

## 5. Testing

**Prompt**


**Outcome:**

---

## 6. Rubric check

**Prompt**


**Outcome:**

