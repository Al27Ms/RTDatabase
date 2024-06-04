import csv

def read_csv_data(file_path, encoding='utf-8'):
    updated_data = []
    with open(file_path, 'r', encoding=encoding) as file:
        csv_reader = csv.DictReader(file)
        for idx, row in enumerate(csv_reader, start=1):
            row['id'] = str(idx)
            updated_data.append(row)

    return updated_data
