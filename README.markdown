# Study Buddy Chatbot

## Overview

Study Buddy is a command-line Python chatbot designed to help students combat procrastination and maintain consistent study habits. It allows users to set daily study goals, receive motivational quotes, create and take flashcard quizzes, and set session-based reminders. The project incorporates a mock implementation of the Model Context Protocol (MCP) to simulate tool-based natural language processing, aligning with modern AI development practices.

This project was developed as part of an academic assignment, inspired by the need for a supportive "study buddy" for independent learners. It uses APIs for dynamic content and a modular design for maintainability.

## Features

- **Goal Setting**: Log and view daily study goals.
- **Motivational Quotes**: Fetch random quotes from the ZenQuotes API to inspire users.
- **Flashcard Quizzes**: Create custom flashcards or fetch trivia questions from the Open Trivia DB API.
- **Session-Based Reminders**: Set timers to receive study reminders during active sessions.
- **Mock MCP Integration**: Simulates MCP tool-calling for natural language input processing, reducing the need for custom NLP.

## Prerequisites

- Python 3.8 or higher
- Required Python packages:
  - `requests` (for API calls)
  - `pyyaml` (for flashcard storage)
- Internet connection (for API access)

## Installation

1. Clone the repository:

   ```bash
   git clone https://github.com/your-username/study-buddy.git
   cd study-buddy
   ```
2. Install dependencies:

   ```bash
   pip install requests pyyaml
   ```
3. Ensure the `flashcards.yaml` file is in the project directory (included in the repository).

## Usage

1. Run the chatbot:

   ```bash
   python study_buddy.py
   ```
2. Interact with the chatbot using the following commands:
   - `set_goal <goal>`: Set a study goal (e.g., `set_goal Study Python for 1 hour`).
   - `view_goals`: List all set goals.
   - `get_quote`: Fetch a motivational quote.
   - `add_flashcard Q: <question> A: <answer>`: Add a flashcard (e.g., `add_flashcard Q: What is Python? A: A programming language.`).
   - `take_quiz`: Take a quiz with stored flashcards.
   - `set_reminder <minutes>`: Set a reminder (e.g., `set_reminder 10` for 10 minutes).
   - `quit`: Exit the chatbot.
3. Use natural language inputs for mock MCP processing (e.g., `I need a quote` or `Give me a quiz`).

## Project Structure

- `study_buddy.py`: Main script containing the chatbot logic, command-line interface, and mock MCP implementation.
- `flashcards.yaml`: Stores user-created flashcards for persistence.
- `README.md`: Project documentation (this file).

## Technical Details

- **APIs Used**:
  - ZenQuotes API for motivational quotes.
  - Open Trivia DB API for trivia questions.
- **Mock MCP**: A simulated MCP system maps natural language inputs to tools (e.g., fetching quotes or trivia) using keyword-based intent detection. This aligns with the professor’s suggestion to leverage MCP for action mapping.
- **Persistence**: Flashcards are saved in a YAML file for simplicity and portability.
- **Reminders**: Implemented using Python’s `threading` module for non-blocking, session-based timers, addressing MCP’s scheduling limitations.

## Limitations and Future Improvements

- **Scheduling**: Reminders are session-based and stop if the app closes. Future versions could integrate desktop notifications (e.g., via `plyer`).
- **MCP Integration**: The current mock MCP could be replaced with the MCP Python SDK and an LLM like Claude for advanced NLP.
- **Quizzes**: Add scoring, multiple questions, or topic-specific flashcards.
- **UI**: Extend to a graphical interface (e.g., tkinter) or web app (e.g., Flask) for broader accessibility.

## Contributing

Contributions are welcome! Please fork the repository, create a new branch, and submit a pull request with your changes. Ensure your code follows the existing style and includes tests for new features.

## Credits

- Developed by Yash Samat
- Inspired by an academic project to support student productivity.
- Thanks to my professor for suggesting the MCP approach and providing feedback on project scope.

## License

This project is licensed under the MIT License. See the LICENSE file for details.