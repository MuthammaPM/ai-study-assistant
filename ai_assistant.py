import os
import time
from pathlib import Path
from google import genai

# Gemini API configuration
API_KEY = os.getenv("GEMINI_API_KEY")
MODEL = os.getenv("GEMINI_MODEL", "gemini-3.1-flash-lite")

if not API_KEY:
    raise SystemExit(
        "API key not found. Set GEMINI_API_KEY and try again."
    )

client = genai.Client(api_key=API_KEY)


def ask_gemini(prompt):
    """Send a prompt to Gemini with automatic retries."""
    for attempt in range(3):
        try:
            response = client.models.generate_content(
                model=MODEL,
                contents=prompt,
            )
            return response.text or "No answer was returned."

        except Exception as error:
            error_message = str(error)

            # Retry temporary server overload errors
            if "503" in error_message and attempt < 2:
                wait_seconds = 5 * (attempt + 1)
                print(
                    f"\nGemini is busy. Retrying in "
                    f"{wait_seconds} seconds..."
                )
                time.sleep(wait_seconds)
            else:
                raise


def chat():
    """Answer study questions."""
    question = input("Ask your question: ").strip()

    if not question:
        print("Please enter a question.")
        return

    try:
        prompt = (
            "You are a helpful AI Study Assistant. "
            "Explain concepts in simple language with examples.\n\n"
            + question
        )

        answer = ask_gemini(prompt)

        print("\nAI Answer:\n")
        print(answer)

    except Exception as error:
        print("\nCould not get an answer from Gemini.")
        print("Error:", error)


def summarize():
    """Summarize a text file."""
    filename = input(
        "Enter text filename (e.g. test.txt): "
    ).strip()

    path = Path(filename)

    if not path.is_file():
        print(
            "File not found. Save the text file "
            "in your project folder."
        )
        return

    try:
        text = path.read_text(encoding="utf-8")

        if not text.strip():
            print("The file is empty.")
            return

        prompt = (
            "Summarize these study notes using headings "
            "and simple bullet points:\n\n" + text
        )

        answer = ask_gemini(prompt)

        print("\nSummary:\n")
        print(answer)

    except Exception as error:
        print("\nCould not summarize the file.")
        print("Error:", error)


def explain_code():
    """Explain code entered by the user."""
    print("Paste the code you want explained.")
    print("When finished, type END on a new line.")

    lines = []

    while True:
        line = input()

        if line.strip().upper() == "END":
            break

        lines.append(line)

    code = "\n".join(lines).strip()

    if not code:
        print("No code was entered.")
        return

    try:
        prompt = (
            "You are a programming tutor. Explain the following "
            "code in simple language. Describe what it does, "
            "explain important lines, and show the expected output "
            "if possible. Do not execute the code.\n\n"
            + code
        )

        answer = ask_gemini(prompt)

        print("\nCode Explanation:\n")
        print(answer)

    except Exception as error:
        print("\nCould not explain the code.")
        print("Error:", error)


def main():
    """Display the main menu."""
    while True:
        print("\n=== AI Study Assistant ===")
        print("1. Chat")
        print("2. Summarize a text file")
        print("3. Explain this code")
        print("4. Exit")

        choice = input("Choose an option: ").strip()

        if choice == "1":
            chat()

        elif choice == "2":
            summarize()

        elif choice == "3":
            explain_code()

        elif choice == "4":
            print("Thank you for using AI Study Assistant!")
            break

        else:
            print(
                "Invalid choice. Please enter 1, 2, 3, or 4."
            )


if __name__ == "__main__":
    main()