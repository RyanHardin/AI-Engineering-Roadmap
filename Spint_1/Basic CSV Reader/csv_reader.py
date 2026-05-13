import csv

def read_csv_by_rows(file_path):
    with open(file_path, 'r') as file:
        reader = csv.reader(file)
        data = []
        for row in reader:
            data.append(row)
    return data

print(read_csv_by_rows('customer_interviews.csv'))

def read_csv_by_columns(file_path):
    with open(file_path, 'r') as file:
        reader = csv.DictReader(file)
        scheduled = []
        for row in reader:
            if(row['interview_status'] == 'scheduled'):
                scheduled.append(row['name'])
    return scheduled

print(read_csv_by_columns('customer_interviews.csv'))