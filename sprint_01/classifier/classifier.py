import os
import csv
import json
import anthropic

from dotenv import load_dotenv
from anthropic import Anthropic

load_dotenv()


def read_csv(relative_file_path):
    file_path = os.path.join(os.path.dirname(__file__), relative_file_path)

    try:
        with open(file_path, mode="r") as file:
            return file.read()
    except FileNotFoundError:
        print(f"Unable to locate the file at: {file_path}")
        return


def call_claude(client):
    raw_csv = read_csv("../inputs/customer_interviews.csv")

    if not raw_csv:
        return

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

    try:
        response = client.messages.create(
            max_tokens=4096,
            system="You are an expert at analyzing qualitative customer research. When given interview data, you need to look through each row and classify that data.",
            messages=prompt,
            model=os.getenv("ANTHROPIC_API_MODEL", "claude-opus-4-5"),
        )
    except anthropic.AuthenticationError:
        print("Invalid API key")
        return
    except anthropic.APIConnectionError:
        print("Unable to establish connection to server.")
        return
    except anthropic.APIStatusError as e:
        print(f"{e.status_code} status code was received with message: {e.message}")
        return
    except anthropic.APIError as e:
        print(f"An error occurred: {e}")
        return

    try:
        raw_json = json.loads(response.content[0].text)
    except json.JSONDecodeError as e:
        print(f"An error occurred while parsing JSON: {e}")
        print(response.content[0].text)
        return

    parse_and_write_csv(raw_json)


def parse_and_write_csv(json_data):
    if not json_data:
        print("No data to write to CSV.")
        return

    output_file = "interviews_classified.csv"
    output_dir = os.path.join(os.path.dirname(__file__), "..", "outputs")
    os.makedirs(output_dir, exist_ok=True)

    try:
        with open(os.path.join(output_dir, output_file), mode="w", newline="") as file:
            field_names = json_data[0].keys()
            writer = csv.DictWriter(file, fieldnames=field_names)
            writer.writeheader()
            writer.writerows(json_data)
    except IOError as e:
        print(f"An error occurred while writing the CSV file: {e}")
        print(f"Data that failed to write: {json_data}")
        return

    print("File for classified interviews successfully created.")


def main():
    if not os.getenv("ANTHROPIC_API_KEY"):
        print("Please provide API key.")
        return

    client = Anthropic(api_key=os.getenv("ANTHROPIC_API_KEY"))

    call_claude(client)


main()
