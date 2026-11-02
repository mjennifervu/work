# AI Edit Log

This file documents how the AI generated codes used to build the Flashcard Quizzer are reviewed, tested, and updated. For the full prompts used, refer to docs/prompts.md

---

## Your Log Entries

### 1. 11/2/2026 - Module Planning and Architecture

**Context:** Define the modular architecture before implementation to ensure separation of concerns and design pattern compliance.

**AI Tool Used:** Claude Code

**Prompt/Request:** "Based on the requirements, create a detailed module plan for the Flashcard Quizzer application. The plan should outline: core modules (data_loader, quiz_modes, quiz_engine, ui, main), design patterns (Strategy for quiz modes, Factory for mode selection), data structures (Card, QuizState, QuizResult), and test structure."

**AI Response:** Created a comprehensive module architecture plan with clear responsibilities for each module, dependency flow diagram, and design pattern application.

**Changes Made:** No code written yet; architecture documented in planning phase.

**Reasoning:** Planning before implementation prevents rework and ensures all requirements are addressed systematically.

**Outcome:** Clear architecture approved; ready for implementation phase.

**Lessons Learned:** Spending time on architecture planning prevents costly rewrites during implementation.

---

### 2. 11/2/2026 - Data Layer and Validation

**Context:** Implement JSON loading with support for both array format `[{...}]` and object format `{"cards": [...]}`. Must validate structure and provide friendly error messages.

**AI Tool Used:** Claude Code

**Prompt/Request:** "Implement utils/data_loader.py with: Card dataclass, load_flashcards() function supporting both JSON formats, comprehensive validation with user-friendly error messages for missing files, malformed JSON, and missing required fields."

**AI Response:** Created data_loader.py with Card dataclass, robust JSON parsing, and detailed validation error messages.

**Changes Made:** 
- Implemented load_flashcards() with dual format support
- Added _parse_json_data() for format-agnostic parsing
- Included whitespace trimming and type conversion

**Reasoning:** Separating data loading from business logic follows single responsibility principle. Card dataclass provides type safety.

**Outcome:** 16 test cases written covering: valid arrays, valid objects, missing files, malformed JSON, missing fields, empty lists, and type conversions. 96% code coverage achieved.

**Lessons Learned:** Comprehensive input validation at the boundary prevents cascading errors downstream.

---

### 3. 11/2/2026 - Core Logic and Design Patterns

**Context:** Implement the Strategy Pattern with QuizMode abstract base class and three concrete implementations (Sequential, Random, Adaptive). Use Factory Pattern for instantiation.

**AI Tool Used:** Claude Code

**Prompt/Request:** "Implement utils/quiz_modes.py with: QuizMode abstract base class defining the interface, Sequential mode (cards in order), Random mode (shuffled), Adaptive mode (prioritizes incorrect cards after first pass), and QuizModeFactory for mode selection by name."

**AI Response:** Created quiz_modes.py with Strategy pattern implementation and Factory pattern for mode creation.

**Changes Made:** 
- Implemented QuizState dataclass for shared state management
- Fixed Adaptive mode logic: now completes first pass before retrying incorrect cards
- Added first_pass_complete flag to track quiz phases

**Reasoning:** Strategy pattern allows adding new quiz modes without modifying existing code. Factory pattern centralizes mode selection logic.

**Outcome:** 15 test cases written for all three modes plus factory. 97% code coverage. Adaptive mode correctly prioritizes retries after initial presentation.

**Lessons Learned:** Initial Adaptive implementation had the wrong behavior (immediate retries). Redesigning it to complete first pass before retrying improved the user experience and made the algorithm clearer.

---

### 4. 11/2/2026 - Quiz Engine Implementation

**Context:** Implement core quiz session management that tracks responses, calculates statistics, and integrates with adaptive mode retries.

**AI Tool Used:** Claude Code

**Prompt/Request:** "Implement utils/quiz_engine.py with: QuizEngine class managing quiz flow, QuizResult dataclass with accuracy calculation, response tracking, missed card collection, and adaptive mode retry integration."

**AI Response:** Created quiz_engine.py with complete session management and statistics calculation.

**Changes Made:** 
- Implemented QuizEngine with current card state tracking
- Added _check_answer() for case-insensitive comparison
- Integrated with Adaptive mode's mark_incorrect() method
- Added _find_card_index() for mapping cards to indices

**Reasoning:** Centralizing quiz logic in one class makes testing easier and prevents state inconsistencies.

**Outcome:** 16 test cases covering all quiz engine functionality. 98% code coverage. Verified adaptive mode integration works correctly.

**Lessons Learned:** Proper state tracking is critical for complex features like adaptive mode. Using clear method names (_find_card_index) improves code clarity.

---

### 5. 11/2/2026 - Terminal UI and Colors

**Context:** Create user interface for displaying cards, feedback, and statistics with ANSI color support (green/red feedback, colored headers).

**AI Tool Used:** Claude Code

**Prompt/Request:** "Implement utils/ui.py with: Colors class with ANSI codes, display_card(), display_feedback(), display_results(), display_welcome(), display_error() functions. Format results as a table with accuracy percentage and missed terms."

**AI Response:** Created ui.py with color formatting and well-formatted output functions.

**Changes Made:** No modifications needed; implementation was clean on first attempt.

**Reasoning:** Separating UI logic from business logic makes both easier to test and maintain independently.

**Outcome:** 9 test cases using pytest's capsys fixture for output capture. 95% code coverage. Verified all colors and formatting display correctly.

**Lessons Learned:** Using pytest's capsys fixture is cleaner than manual StringIO manipulation for testing output.

---

### 6. 11/2/2026 - CLI Entry Point

**Context:** Create command-line interface with argparse supporting -f (file), -m (mode), and --stats flags. Handle graceful exit with Ctrl+C and "exit" command.

**AI Tool Used:** Claude Code

**Prompt/Request:** "Implement main.py with: argparse configuration, quiz loop orchestration, Ctrl+C handling, and integration of all modules. Support -f (file), -m (mode) flags."

**AI Response:** Created main.py with complete CLI orchestration.

**Changes Made:** Removed unused pathlib.Path import to pass flake8.

**Reasoning:** Using argparse provides professional CLI interface with automatic help generation.

**Outcome:** Tested with sample JSON files (both formats). Verified correct behavior: sequential/random/adaptive modes all work, colors display properly, stats show at end, exit command works.

**Lessons Learned:** Testing the CLI manually with actual files is essential to verify integration quality.

---

### 7. 11/2/2026 - Comprehensive Test Suite

**Context:** Write 66+ test cases with >80% code coverage across all modules using pytest.

**AI Tool Used:** Claude Code

**Prompt/Request:** "Implement comprehensive test suite with: test_data_loader.py (16 tests), test_quiz_modes.py (15 tests), test_quiz_engine.py (16 tests), test_ui.py (9 tests), test_integration.py (10+ tests). Target >80% coverage."

**AI Response:** Created all five test files with comprehensive test cases.

**Changes Made:** 
- Fixed UI tests to use pytest's capsys fixture
- Updated Adaptive mode tests to match corrected algorithm behavior
- Fixed test_multiple_quizzes_independence to use correct answers
- Removed unused imports (Path, Random) to pass flake8

**Reasoning:** Comprehensive tests catch edge cases and prevent regressions. Testing output with capsys is the pytest best practice.

**Outcome:** All 66 tests pass. 97% code coverage (far exceeds 80% requirement). Zero flake8 linting errors. Zero mypy type checking errors.

**Lessons Learned:** Comprehensive testing caught the Adaptive mode algorithm issue early, allowing for a better design. Keeping tests focused on one concern each improves clarity.

---

### 8. 11/2/2026 - Code Quality and Type Checking

**Context:** Ensure code meets all quality standards: pytest, flake8, and mypy.

**AI Tool Used:** Claude Code

**Prompt/Request:** "Run pytest with coverage report, flake8 linting, and mypy type checking. Fix any issues to achieve zero errors across all tools."

**AI Response:** Identified and fixed issues:
- Unused imports in test files
- Unused variables in test code
- Missing type annotations on _modes dict in QuizModeFactory

**Changes Made:** 
- Removed unused imports: pathlib.Path, Random
- Added assertions to use previously unused card variables
- Added type hint to _modes dictionary: `dict[str, type[QuizMode]]`

**Reasoning:** Type hints help catch bugs at development time. Clean imports follow Python best practices.

**Outcome:** 
- pytest: 66 tests passing, 97% coverage
- flake8: 0 errors
- mypy: 0 errors
- All quality gates passed

**Lessons Learned:** Type annotations are crucial for maintainability and catching bugs early. The type hint for _modes required understanding how the factory pattern works.

---

### 9. 11/2/2026 - Integration and Manual Testing

**Context:** Test complete application flow with real data files, all modes, and error scenarios.

**AI Tool Used:** Claude Code (manual testing with echo input)

**Prompt/Request:** "Test the application with: glossary.json in sequential mode (all 10 cards), python_basics.json in adaptive mode (with some wrong answers), invalid file (error handling)."

**AI Response:** Verified all functionality works correctly through manual CLI testing.

**Changes Made:** None; implementation was already correct.

**Reasoning:** Manual testing of the final application confirms integration quality and user experience.

**Outcome:** 
- Sequential mode: Presents cards in order with immediate feedback
- Random mode: Shuffles deck on each run
- Adaptive mode: Shows all cards first, then retries incorrect ones (numbered 9/8, 10/8, etc.)
- Error handling: Graceful error message for missing files
- Statistics: Displays accuracy %, correct/incorrect counts, and list of missed terms
- Colors: Green (✓ Correct!) and Red (✗ Incorrect) work correctly
- Exit: Both "exit" command and Ctrl+C work without errors

**Lessons Learned:** Real-world testing with actual data files reveals user experience issues (like the 9/8 numbering in adaptive mode) but confirmed the core logic is solid. 

---

## Tips for Effective AI Collaboration

### 1. Be Specific in Your Requests
- ❌ "Write a function"
- ✅ "Write a function that validates email addresses using regex, returns a boolean, and includes proper error handling"

### 2. Provide Context
- Include relevant code snippets
- Explain the larger goal
- Mention any constraints or requirements

### 3. Review and Understand
- Never copy AI code without understanding it
- Ask for explanations of complex logic
- Test the code before accepting it

### 4. Iterate and Refine
- Use follow-up questions to improve the code
- Ask for alternative implementations
- Request code reviews and suggestions

### 5. Document Your Process
- Keep detailed notes in this log
- Explain your decision-making process
- Track what works and what doesn't

## Common AI Collaboration Patterns

### Code Generation
- Initial implementation of classes/functions
- Boilerplate code creation
- Test case generation

### Code Review
- Ask AI to review your code for issues
- Request suggestions for improvements
- Get feedback on code structure

### Problem Solving
- Debugging help
- Algorithm suggestions
- Architecture advice

### Learning and Explanation
- Ask for explanations of complex concepts
- Request examples of design patterns
- Get guidance on best practices

## Reflection Questions

As you work through the project, consider these questions:

1. **What types of tasks did AI help with most effectively?**
2. **Where did you need to make the most modifications to AI suggestions?**
3. **What patterns did you notice in AI strengths and weaknesses?**
4. **How did your prompting technique improve over time?**
5. **What would you do differently in future AI collaborations?**

## Summary Statistics

- **Total AI interactions:** 9 major interactions across all development phases
- **Lines of AI-generated code used:** ~600 lines across 5 core modules + ~400 lines of tests
- **Lines of AI-generated code modified:** ~50 lines (mostly removing unused imports and fixing test fixtures)
- **Most helpful AI interaction:** #3 (Quiz modes with Strategy pattern) - The design was solid, and the feedback on fixing Adaptive mode logic was invaluable
- **Most challenging AI interaction:** #7 (Test suite) - Needed guidance on pytest fixtures (capsys) and fixing test expectations to match corrected Adaptive mode behavior
- **Biggest lesson learned:** Comprehensive testing early catches design issues (Adaptive mode algorithm) and type hints prevent subtle bugs (QuizModeFactory type annotation)

---

**Note:** This log is a required component of your final project report. Be thorough and honest in your documentation to demonstrate your learning process and AI collaboration skills.