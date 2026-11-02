# Prompts Log

This file documents the prompts used for guiding Claude through building the Flashcard Quizzer. For detailed analysis and notes on prompt interactions, refer to docs/ai_edit_log.md

---

## 1. Requirements set up

**Prompt**
In this project, your goal is to engineer with AI-generated code to build a production-ready Command Line Interface (CLI) application: The Flashcard Quizzer. 
You must produce an application that meets the following criteria.

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
Checks
• 
Deliverables
• source code that is modular
• tests/ directory with tests and coverage report showing >= 80%
• a README.md with stepup instructions and feature descriptions
• 

**Outcome:**

---

## 2. Data Layer and Validation

**Prompt**


**Outcome:**

---

## 3. Core Logic and Design Patterns

**Prompt**


**Outcome:**

---

## 4. CLI and Interation

**Prompt**


**Outcome:**

---

## 5. Testing

**Prompt**


**Outcome:**

---

## 6. Rubric check

**Prompt**


**Outcome:**

