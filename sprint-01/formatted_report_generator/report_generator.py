import os
from dotenv import load_dotenv
from anthropic import Anthropic
from datetime import date

load_dotenv()


def read_csv(file_path):
    with open(file_path, mode="r") as file:
        return file.read()


def generate_report():
    filename = "customer_interviews.csv"
    header = f"Date: {date.today()} \nFile: {filename}\n"
    raw_csv = read_csv(f"../inputs/{filename}")

    client = Anthropic(api_key=os.getenv("ANTHROPIC_API_KEY"))

    message = client.messages.create(
        max_tokens=1024,
        system="You are an expert at analyzing qualitative customer research. When given interview data, identify and summarize the most important recurring themes clearly and concisely.",
        messages=[
            {
                "role": "user",
                "content": f"""
                    Based on the provided data. Create a report that should have the following:

                    1. A header with the provided date and input filename
                    2. The top themes identified (numbered)
                    3. A one-sentence "what to do next" recommendation

                    header: {header}
                    raw-csv: {raw_csv}
                    """,
            }
        ],
        model=os.getenv("ANTHROPIC_API_MODEL"),
    )

    return message.content[0].text


def main():
    output_dir = os.path.join(os.path.dirname(__file__), "..", "outputs")
    os.makedirs(output_dir, exist_ok=True)

    output_file = f"interview_report_{date.today().strftime("%m_%d_%Y")}.txt"
    generated_report = generate_report()

    with open(os.path.join(output_dir, output_file), mode="w") as file:
        file.write(generated_report)


main()
