import csv


def read_csv_data(file_path):
    with open(file_path, 'r', encoding='utf-8') as file:
        csv_reader = csv.DictReader(file)
        data = list(csv_reader)

    # Przekształć wartości ID
    for i, row in enumerate(data):
        row['id'] = i + 1  # Zmieniamy ID na kolejne liczby naturalne

    return data
