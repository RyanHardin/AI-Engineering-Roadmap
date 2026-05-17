import os
from dotenv import load_dotenv
from anthropic import Anthropic

load_dotenv()


def read_csv(file_path):
    with open(file_path, mode="r") as file:
        return file.read()


def main():
    raw_csv = read_csv("../inputs/customer_interviews.csv")
    client = Anthropic(api_key=os.getenv("ANTHROPIC_API_KEY"))

    message = client.messages.create(
        max_tokens=1024,
        system="You are an expert at analyzing qualitative customer research. When given interview data, identify and summarize the most important recurring themes clearly and concisely.",
        messages=[
            {
                "role": "user",
                "content": f"Here is data from customer interviews:\n\n{raw_csv}\n\nPlease identify the top 5 pain point themes. For each theme, provide a short title and a 1-2 sentence description.",
            }
        ],
        model=os.getenv("ANTHROPIC_API_MODEL"),
    )

    print(message.content[0].text)


main()
