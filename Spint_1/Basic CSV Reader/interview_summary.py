import csv

def interview_summary(interview_data_path):
    contacts = 0
    completed = 0
    scheduled = 0
    not_contacted = 0
    willing_to_pay = 0

    with open(interview_data_path, 'r') as file:
        reader = csv.DictReader(file)
        for item in reader:
            contacts += 1
            if item['interview_status'] == 'completed':
                completed += 1
            elif item['interview_status'] == 'scheduled':
                scheduled += 1
            elif item['interview_status'] == 'not_contacted':
                not_contacted += 1
            if item['willing_to_pay'] == 'yes':
                willing_to_pay += 1

    print(f"Total contacts: {contacts}")
    print(f"Completed interviews: {completed}")
    print(f"Scheduled interviews: {scheduled}")
    print(f"Not contacted: {not_contacted}")
    print(f"Willing to pay (yes): {willing_to_pay}")

interview_summary('customer_interviews.csv')