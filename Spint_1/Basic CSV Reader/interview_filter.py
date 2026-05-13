import csv

def filter_interviews(interview_data_path, status_filter):
    filtered_interviews = []

    with open(interview_data_path, 'r') as file:
        reader = csv.DictReader(file)
        for item in reader:
            if item['interview_status'] == status_filter:
                filtered_interviews.append(item)

    return filtered_interviews

def create_filtered_csv(filtered_interviews, output_path):
    if not filtered_interviews:
        print("No interviews match the specified status filter.")
        return
    
    with open(output_path, 'w', newline='') as file:
        writer = csv.DictWriter(file, fieldnames=filtered_interviews[0].keys())
        writer.writeheader() # Extracting headers from the first dictionary
        writer.writerows(filtered_interviews) # Writing all filtered values to the new CSV file

filtered_data = filter_interviews('customer_interviews.csv', 'completed')
create_filtered_csv(filtered_data, 'completed_interviews.csv')