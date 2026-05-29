import os
import anthropic

from dotenv import load_dotenv
from anthropic import Anthropic

load_dotenv()


def stream_response(client):
    prompt = {
        "role": "user",
        "content": "Explain how the internet works in depth.",
    }
    try:
        with client.messages.stream(
            max_tokens=1024,
            messages=[prompt],
            model=os.getenv("ANTHROPIC_API_MODEL", "claude-opus-4-6"),
        ) as stream:
            for text in stream.text_stream:
                print(text, end="", flush=True)
            print()
    except anthropic.APIError as e:
        print(f"An API error occurred: {e}")


def main():
    if not os.getenv("ANTHROPIC_API_KEY"):
        print("Please provide API key.")
        return

    client = Anthropic(api_key=os.getenv("ANTHROPIC_API_KEY"))
    stream_response(client)


if __name__ == "__main__":
    main()
