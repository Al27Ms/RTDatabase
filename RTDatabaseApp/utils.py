import csv
from googleapiclient.discovery import build
from RTDatabase import settings

def read_csv_data(file_path, encoding='utf-8'):
    """
    Reads CSV data from the given file path and returns a list of dictionaries,
    each representing a row in the CSV file. Adds an 'id' field to each row.
    """
    updated_data = []
    try:
        with open(file_path, 'r', encoding=encoding) as file:
            csv_reader = csv.DictReader(file)
            for idx, row in enumerate(csv_reader, start=1):
                row['id'] = str(idx)
                updated_data.append(row)
    except FileNotFoundError:
        print(f"Error: The file {file_path} was not found.")
    except Exception as e:
        print(f"An error occurred while reading the CSV file: {e}")

    return updated_data

def fetch_google_images(query, num_images=3):
    """
    Fetches image URLs from Google Custom Search based on the given query.

    Args:
        query (str): The search query.
        num_images (int): The number of image URLs to fetch.

    Returns:
        list: A list of image URLs.
    """
    api_key = settings.GOOGLE_API_KEY
    custom_search_engine_id = settings.GOOGLE_SEARCH_ID

    try:
        # Build the API client object
        service = build("customsearch", "v1", developerKey=api_key)

        # Call the `list` method on the custom search engine
        result = service.cse().list(
            q=query,
            cx=custom_search_engine_id,
            searchType='image',
            num=num_images
        ).execute()

        # Extract image URLs from the search results
        image_links = [item['link'] for item in result.get('items', [])]

        return image_links
    except Exception as e:
        print(f"An error occurred while fetching images from Google: {e}")
        return []
