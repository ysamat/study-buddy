import cmd
import requests
import yaml
import json
from typing import Dict, Callable
import random
import threading
import time

def fetch_quote() -> str:
    """Fetch a random motivational quote from ZenQuotes API."""
    try:
        response = requests.get("https://zenquotes.io/api/random")
        response.raise_for_status()
        data = response.json()
        quote = data[0]['q']
        author = data[0]['a']
        return f"{quote} - {author}"
    except requests.RequestException:
        return "Sorry, couldn't fetch a quote right now. Try again later!"

def fetch_trivia() -> str:
    """Fetch a random trivia question from Open Trivia DB."""
    try:
        response = requests.get("https://opentdb.com/api.php?amount=1&type=multiple")
        response.raise_for_status()
        data = response.json()
        question = data['results'][0]['question']
        correct_answer = data['results'][0]['correct_answer']
        return f"Question: {question}\nCorrect Answer: {correct_answer}"
    except requests.RequestException:
        return "Sorry, couldn't fetch a trivia question right now. Try again later!"

# Mock MCP tool definition
TOOLS = {
    "fetch_quote": {
        "description": "Fetch a motivational quote to inspire the user.",
        "function": fetch_quote
    },
    "fetch_trivia": {
        "description": "Fetch a random trivia question for a quiz.",
        "function": fetch_trivia
    }
}

class MockMCP:
    """Simulate MCP tool-calling behavior."""
    def process_input(self, user_input: str) -> str:
        """Map user input to a tool or command."""
        user_input = user_input.lower().strip()
        
        if "quote" in user_input or "motivate" in user_input or "inspire" in user_input:
            tool = TOOLS.get("fetch_quote")
            return tool["function"]()
        elif "trivia" in user_input or "quiz" in user_input or "question" in user_input:
            tool = TOOLS.get("fetch_trivia")
            return tool["function"]()
        elif "goal" in user_input:
            return "Try 'set_goal <your goal>' to set a study goal!"
        elif "view" in user_input or "list" in user_input:
            return "Try 'view_goals' to see your goals!"
        elif "remind" in user_input:
            return "Try 'set_reminder <minutes>' to set a reminder!"
        else:
            return f"Sorry, I didn't understand: '{user_input}'. Try 'set_goal', 'view_goals', 'get_quote', 'add_flashcard', 'take_quiz', 'set_reminder', or ask for a 'quote' or 'quiz'."

class StudyBuddy(cmd.Cmd):
    intro = "Welcome to your Study Buddy! Type 'help' for commands or 'quit' to exit."
    prompt = "(StudyBuddy) "

    def __init__(self):
        super().__init__()
        self.goals = []  # Store user goals
        self.flashcards = []  # Store flashcards
        self.mcp = MockMCP()  # Mock MCP integration
        self.load_flashcards()

    def load_flashcards(self):
        """Load flashcards from a YAML file."""
        try:
            with open("flashcards.yaml", "r") as f:
                data = yaml.safe_load(f)
                self.flashcards = data.get("flashcards", []) if data else []
        except FileNotFoundError:
            self.flashcards = []

    def save_flashcards(self):
        """Save flashcards to a YAML file."""
        with open("flashcards.yaml", "w") as f:
            yaml.safe_dump({"flashcards": self.flashcards}, f)

    def set_reminder(self, minutes: int):
        """Set a reminder to print a message after specified minutes."""
        def reminder_task():
            time.sleep(minutes * 60)
            print("\nReminder: Time to check on your study goals! Keep it up!")
        
        threading.Thread(target=reminder_task, daemon=True).start()
        print(f"Reminder set for {minutes} minute(s).")

    def do_set_goal(self, arg):
        """Set a study goal for today."""
        if arg:
            self.goals.append(arg)
            print(f"Goal set: {arg}")
        else:
            print("Please specify a goal, e.g., 'set_goal Study Python for 1 hour'")

    def do_view_goals(self, arg):
        """View all set goals."""
        if self.goals:
            print("Your goals:")
            for i, goal in enumerate(self.goals, 1):
                print(f"{i}. {goal}")
        else:
            print("No goals set yet.")

    def do_get_quote(self, arg):
        """Fetch a motivational quote."""
        quote = fetch_quote()
        print(f"Here's some motivation: {quote}")

    def do_add_flashcard(self, arg):
        """Add a flashcard, e.g., 'add_flashcard Q: What is Python? A: A programming language.'"""
        try:
            question, answer = arg.split(" A: ", 1)
            question = question.replace("Q: ", "").strip()
            self.flashcards.append({"question": question, "answer": answer.strip()})
            self.save_flashcards()
            print(f"Flashcard added: Q: {question} A: {answer}")
        except ValueError:
            print("Please use format: 'add_flashcard Q: <question> A: <answer>'")

    def do_take_quiz(self, arg):
        """Take a quiz with stored flashcards."""
        if not self.flashcards:
            print("No flashcards available. Add some with 'add_flashcard' or try 'quiz' for a trivia question.")
            return
        
        card = random.choice(self.flashcards)
        print(f"Question: {card['question']}")
        user_answer = input("Your answer: ").strip()
        if user_answer.lower() == card['answer'].lower():
            print("Correct! Great job!")
        else:
            print(f"Sorry, the correct answer was: {card['answer']}")

    def do_set_reminder(self, arg):
        """Set a reminder, e.g., 'set_reminder 10' for 10 minutes."""
        try:
            minutes = int(arg)
            if minutes <= 0:
                print("Please specify a positive number of minutes.")
                return
            self.set_reminder(minutes)
        except ValueError:
            print("Please specify a number of minutes, e.g., 'set_reminder 10'.")

    def do_quit(self, arg):
        """Exit the Study Buddy."""
        print("Goodbye! Keep studying!")
        return True

    def default(self, line):
        """Handle unknown commands via mock MCP."""
        response = self.mcp.process_input(line)
        print(response)

if __name__ == "__main__":
    StudyBuddy().cmdloop()