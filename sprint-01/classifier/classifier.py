import os
import csv
import json
from dotenv import load_dotenv
from anthropic import Anthropic

load_dotenv()


def read_csv(file_path):
    with open(file_path, mode="r") as file:
        return file.read()


def call_claude():
    raw_csv = read_csv("../inputs/customer_interviews.csv")
    client = Anthropic(api_key=os.getenv("ANTHROPIC_API_KEY"))
    prompt = [
        {
            "role": "user",
            "content": f"""
        Look at this csv file and add on 3 new labels for each response. Return the data back in JSON format no explanation, 
        no markdown, no code fences. Just the JSON.
        
        Labels:
        Category (report writing, scheduling, client communication, etc.)
        Severity (ex. high, medium, or low)
        Software Opportunity (ex. Yes or No)

        raw csv: {raw_csv}
        """,
        }
    ]

    response = client.messages.create(
        max_tokens=4096,
        system="You are an expert at analyzing qualitative customer research. When given interview data, you need to look through each row and classify that data.",
        messages=prompt,
        model=os.getenv("ANTHROPIC_API_MODEL", "claude-opus-4-5"),
    )

    raw_json = json.loads(response.content[0].text)
    parse_and_write_csv(raw_json)


def parse_and_write_csv(json_data):
    output_file = "interviews_classified.csv"
    output_dir = os.path.join(os.path.dirname(__file__), "..", "outputs")
    os.makedirs(output_dir, exist_ok=True)

    with open(os.path.join(output_dir, output_file), mode="w", newline="") as file:
        fieldNames = json_data[0].keys()
        writer = csv.DictWriter(file, fieldnames=fieldNames)
        writer.writeheader()
        writer.writerows(json_data)

    print("File for classified interviews successfully created.")


def main():
    call_claude()


main()
