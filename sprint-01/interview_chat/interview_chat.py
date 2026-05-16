import os
from dotenv import load_dotenv
from anthropic import Anthropic

load_dotenv()

CSV_FILE_PATH = "../inputs/customer_interviews.csv"


def read_csv(file_path):
    with open(file_path, mode="r") as file:
        return file.read()


def call_claude(claude_client, message_history):
    return claude_client.messages.create(
        max_tokens=1024,
        system="You are an expert at analyzing qualitative customer research. When given interview data, identify and summarize the most important recurring themes clearly and concisely.",
        messages=message_history,
        model=os.getenv("ANTHROPIC_API_MODEL", "claude-opus-4-5"),
    )


def interview_chat(claude_client):

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

    print(f"\n{messages.content[0].text}")

    chat_open = True

    while chat_open:
        user_input = input("\nEnter your response (or 'quit' to exit): ")
        user_message = {"role": "user", "content": user_input}

        if user_input == "quit":
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


def main():
    client = Anthropic(api_key=os.getenv("ANTHROPIC_API_KEY"))
    interview_chat(client)


main()
