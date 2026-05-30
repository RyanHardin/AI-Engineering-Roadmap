import os
import anthropic
import csv
import json

from dotenv import load_dotenv

load_dotenv()


def read_csv(relative_file_path):
    print(f"Attempting to read file at: {relative_file_path}")
    file_path = os.path.join(os.path.dirname(__file__), relative_file_path)

    try:
        with open(file_path, mode="r") as file:
            return file.read()
    except FileNotFoundError as e:
        print(f"Unable to locate file at {file_path}")
        return


def call_claude(client, raw_csv):

    prompt = [
        {
            "role": "user",
            "content": f"""
            Take a look at the provided file, analyze the feedback, and output the same table with the addition of the following keys:
            
            1. category (report writing/scheduling/client communication/ etc.),
            2. severity (high, medium, or low)
            3. software opportunity (Yes or No)

            raw csv: {raw_csv}
        """,
        }
    ]
    try:
        print("Sending prompt to Claude API...")
        message = client.messages.create(
            max_tokens=2048,
            messages=prompt,
            model=os.getenv("ANTHROPIC_API_MODEL", "claude-opus-4-6"),
            output_config={
                "format": {
                    "type": "json_schema",
                    "schema": {
                        "type": "array",
                        "items": {
                            "type": "object",
                            "additionalProperties": False,
                            "properties": {
                                "name": {"type": "string"},
                                "email": {"type": "string"},
                                "company": {"type": "string"},
                                "role": {"type": "string"},
                                "interview_status": {"type": "string"},
                                "pain_point": {"type": "string"},
                                "willing_to_pay": {"type": "string"},
                                "category": {"type": "string"},
                                "severity": {"type": "string"},
                                "software_opportunity": {"type": "string"},
                            },
                            "required": [
                                "name",
                                "email",
                                "company",
                                "role",
                                "interview_status",
                                "pain_point",
                                "willing_to_pay",
                                "category",
                                "severity",
                                "software_opportunity",
                            ],
                        },
                    },
                }
            },
        )
    except anthropic.APIError as e:
        print("Error creating message:", e)
        return

    return json.loads(message.content[0].text)


def generate_report(client):
    print("\nReading raw csv data...")
    raw_csv = read_csv("../inputs/customer_interviews.csv")

    if not raw_csv:
        return

    print("\nCalling Claude API...")
    raw_json = call_claude(client, raw_csv)

    if not raw_json:
        return

    print("\nGenerating report...")

    output_file = "classified_output.csv"
    output_dir = os.path.join(os.path.dirname(__file__), "..", "outputs")
    os.makedirs(output_dir, exist_ok=True)

    try:
        with open(os.path.join(output_dir, output_file), mode="w", newline="") as file:
            field_names = raw_json[0].keys()
            writer = csv.DictWriter(file, fieldnames=field_names)
            writer.writeheader()
            writer.writerows(raw_json)
    except Exception as e:
        print("Error writing CSV file:", e)
        return

    print("File for classified interviews successfully created.")


def main():
    if not os.getenv("ANTHROPIC_API_KEY"):
        print("Please provide API key for access.")
        return
    print("\nCreating Anthropic client...")
    client = anthropic.Anthropic(api_key=os.getenv("ANTHROPIC_API_KEY"))
    generate_report(client)


if __name__ == "__main__":
    main()
