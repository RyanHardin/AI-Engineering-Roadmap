import os
import anthropic  # error type references

from dotenv import load_dotenv
from anthropic import Anthropic  # client class

load_dotenv()

CSV_FILE_PATH = "../inputs/customer_interviews.csv"


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


def interview_chat(claude_client):
    try:
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

        messages = call_claude(claude_client, message_history)

        if messages is None:
            return

        print(f"\n{messages.content[0].text}")

        chat_open = True

        while chat_open:
            user_input = input("\nEnter your response (or 'quit' to exit): ")
            user_message = {"role": "user", "content": user_input}

            if user_input == "quit" or user_input == "exit":
                chat_open = False
                print("\nEnding session. Goodbye!")
                continue

            message_history.append(user_message)
            new_message = call_claude(claude_client, message_history)

            assistant_message = {
                "role": "assistant",
                "content": new_message.content[0].text,
            }
            message_history.append(assistant_message)

            print(f"\n{assistant_message['content']}")
    except anthropic.APIConnectionError:
        print("The server could not be reached")
    except anthropic.APIStatusError as e:
        print(f"API Error {e.staus_code}: {e.message}")
    except anthropic.RateLimitError:
        print("Rate limit hit.")


def main():
    if not os.getenv("ANTHROPIC_API_KEY"):
        print("Please provide ANTHROPIC_API_KEY")
        return

    try:
        client = Anthropic(api_key=os.getenv("ANTHROPIC_API_KEY"))
        interview_chat(client)
    except anthropic.APIConnectionError:
        print("The server could not be reached")
    except anthropic.AuthenticationError:
        print("Invalid API key.")


main()
