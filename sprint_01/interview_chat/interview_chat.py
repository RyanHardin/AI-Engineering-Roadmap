import os
import anthropic  # error type references

from dotenv import load_dotenv
from anthropic import Anthropic  # client class

load_dotenv()

CSV_FILE_PATH = os.path.join(
    os.path.dirname(__file__), "../inputs/customer_interviews.csv"
)


def read_csv(file_path):
    with open(file_path, mode="r") as file:
        return file.read()


def call_claude(claude_client, message_history):
    response = claude_client.messages.create(
        max_tokens=1024,
        system="You are an expert at analyzing qualitative customer research. When given interview data, identify and summarize the most important recurring themes clearly and concisely.",
        messages=message_history,
        model=os.getenv("ANTHROPIC_API_MODEL", "claude-opus-4-5"),
    )
    return response


def load_interview_data(claude_client):
    raw_csv = read_csv(CSV_FILE_PATH)
    message_history = [
        {
            "role": "user",
            "content": f"""
            Give a brief summary of the provided report.       
            raw csv: {raw_csv}
        """,
        }
    ]
    try:
        response = call_claude(claude_client, message_history)
    except anthropic.AuthenticationError:
        print("Invalid API key")
        return
    except anthropic.APIConnectionError:
        print("The server could not be reached.")
        return
    except anthropic.APIStatusError as error:
        print(f"API Error {error.status_code}: {error.message}")
        return

    return response, message_history


def run_chat_loop(claude_client, message_history):
    while True:
        user_input = input("\nEnter your response (or 'quit' to exit): ")

        if user_input == "quit" or user_input == "exit":
            print("\nEnding session. Goodbye!")
            break

        if user_input.strip() == "":
            print("Please enter a valid message.")
            continue

        user_message = {"role": "user", "content": user_input}
        message_history.append(user_message)

        try:
            new_message = call_claude(claude_client, message_history)
        except anthropic.APIConnectionError:
            print("The server could not be reached")
            message_history.pop()
            continue
        except anthropic.RateLimitError:
            print("Rate limit hit.")
            message_history.pop()
            continue

        assistant_message = {
            "role": "assistant",
            "content": new_message.content[0].text,
        }
        message_history.append(assistant_message)

        print(f"\n{assistant_message['content']}")


def interview_chat(claude_client):
    result = load_interview_data(claude_client)

    if result is None:
        return

    messages, message_history = result
    print(f"\n{messages.content[0].text}")

    run_chat_loop(claude_client, message_history)


def main():
    if not os.getenv("ANTHROPIC_API_KEY"):
        print("Please provide ANTHROPIC_API_KEY")
        return

    client = Anthropic(api_key=os.getenv("ANTHROPIC_API_KEY"))
    interview_chat(client)


main()
