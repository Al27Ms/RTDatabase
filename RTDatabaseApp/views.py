import os
import requests
from django.core.paginator import Paginator
from django.shortcuts import render, Http404
from django.conf import settings
from .utils import read_csv_data, fetch_google_images
from functools import lru_cache

def index(request):
    """
    Handles the view for the index page.
    """
    return render(request, 'index.html')

def map_view(request):
    """
    Handles the view for the map page.
    """
    return render(request, 'map.html')

def info_view(request):
    """
    Handles the view for the info page.
    """
    return render(request, 'info.html')

@lru_cache(maxsize=1)
def get_csv_data(file_path):
    """
    Reads CSV data from the given file path with caching to improve performance.
    """
    return read_csv_data(file_path)

def temple_list(request):
    """
    Handles the view for the list of temples.
    Retrieves and filters the CSV data based on the query parameter.
    Paginates the results and renders the 'temple_list' template.
    """
    # Get CSV data with caching
    csv_data = get_csv_data('data/RT_DATA.CSV')

    # Get query parameter and filter data
    query = request.GET.get('q', '').lower()
    if query:
        csv_data = [row for row in csv_data if query in row['name'].lower()]

    # Paginate the filtered data
    paginator = Paginator(csv_data, 20)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    # Render the template with paginated data
    return render(request, 'temple_list.html', {'page_obj': page_obj, 'query': query})

def temple_detail(request, temple_id):
    """
    Handles the view for the detail of a specific temple.
    Retrieves the temple data by ID, fetches images from Wikipedia and Google,
    and renders the 'temple_detail' template.
    """
    # Get CSV data with caching
    csv_data = get_csv_data('data/RT_DATA.CSV')

    # Find the temple by ID
    temple = next((row for row in csv_data if row['id'] == str(temple_id)), None)
    if temple is None:
        raise Http404("The temple was not found.")

    # Get Wikipedia image URL or default image if not found
    wikipedia_image_url = get_wikipedia_image_url(temple['wikipedia'])

    # Construct the search query for Google Images
    temple_name = f"{temple['name']} {temple['location']}, {temple['modernplace']}, {temple['country']}"
    temple_images = fetch_google_images(temple_name)

    # Prepare context data for the template
    context = {
        'temple': temple,
        'wikipedia_image_url': wikipedia_image_url,
        'temple_images': temple_images,
        'GOOGLE_MAPS_API_KEY': settings.GOOGLE_API_KEY
    }

    # Render the template with context data
    return render(request, 'temple_detail.html', context)

def get_wikipedia_image_url(page_title):
    """
    Fetches the image URL from Wikipedia for the given page title.
    Returns the image URL if found, otherwise returns None.
    """
    url = "https://en.wikipedia.org/w/api.php"
    params = {
        'action': 'query',
        'titles': page_title,
        'prop': 'pageimages',
        'format': 'json',
        'pithumbsize': 500,
    }
    try:
        response = requests.get(url, params=params)
        response.raise_for_status()
        data = response.json()
        pages = data.get('query', {}).get('pages', {})
        for page_data in pages.values():
            thumbnail = page_data.get('thumbnail', {})
            if thumbnail:
                return thumbnail.get('source')
    except requests.exceptions.RequestException as e:
        print(f"Error fetching Wikipedia image: {e}")
    return None

def map_view(request):
    """
    Handles the view for the map page.
    Retrieves temple data from the CSV file and provides it to the map template.
    """
    csv_data = get_csv_data('data/RT_DATA.CSV')
    temples = [
        {
            'id': temple['id'],
            'name': temple['name'],
            'latitude': temple['latitude'],
            'longitude': temple['longitude']
        }
        for temple in csv_data
        if temple['latitude'] and temple['longitude']
    ]

    context = {
        'temples': temples,
        'GOOGLE_MAPS_API_KEY': settings.GOOGLE_API_KEY
    }
    return render(request, 'map.html', context)

def info_view(request):
    """
    Handles the view for the info page.
    Provides a list of attribute definitions for the template.
    """
    context = {
        'attributes': [
            {'name': 'id', 'definition': 'Unique internal ID number, starting at 1000001 to avoid issues with leading zeroes.'},
            {'name': 'name', 'definition': 'Common name of the temple, if any, typically in English.'},
            {'name': 'dedicatee', 'definition': 'Divinity/-ies to whom the temple was dedicated, typically in English, using Roman (not Greek) version.'},
            {'name': 'type', 'definition': 'Type of structure (temple, mithraeum, etc). Almost all are temples.'},
            {'name': 'location', 'definition': 'Name of locale in which the temple is found, whether ancient or modern, smaller than a city or whatever is listed in ancient/modern place. For example, Campus Martius in Rome.'},
            {'name': 'setting', 'definition': 'Geographical context for the structure, e.g., forum, acropolis.'},
            {'name': 'modernplace', 'definition': 'Modern name for the place in which the temple was found.'},
            {'name': 'ancientplace', 'definition': 'Ancient name for the place in which the temple was found.'},
            {'name': 'pleiadesplace', 'definition': 'Pleiades ID for the place in which the temple was found. Not to be confused with field "pleiades" which is the Pleiades entry that is the same as the database entry.'},
            {'name': 'country', 'definition': 'Modern country in which the temple was found.'},
            {'name': 'latitude', 'definition': 'Latitude of the location of the temple. Right now these all presume the exact location is known, that is, there’s no indication of accuracy.'},
            {'name': 'longitude', 'definition': 'Longitude of the location of the temple. Right now these all presume the exact location is known, that is, there’s no indication of accuracy.'},
            {'name': 'orientation', 'definition': 'Orientation in degrees (1-360°) of the temple, where 0/360° is north. These were mostly obtained from Google maps, though some are taken from published plans.'},
            {'name': 'compass', 'definition': 'Conversion of orientation into one of eight directions (N, NE, E, etc).'},
            {'name': 'vowed', 'definition': 'Year of vow for the building of the temple. Mainly applies to ones in the city of Rome. Negative numbers for BCE.'},
            {'name': 'date', 'definition': 'Date (often descriptive, e.g., “early 1st c. BCE”) of the dedication/start of the temple.'},
            {'name': 'startdateearly', 'definition': 'Date for the early side of the start-date range.'},
            {'name': 'startdatelate', 'definition': 'Date for the late side of the start-date range.'},
            {'name': 'century', 'definition': 'Century of start of temple’s use with negative number for BCE.'},
            {'name': 'enddate', 'definition': 'Date for the end of temple’s use with negative number for BCE.'},
            {'name': 'preceded', 'definition': 'ID of temple that preceded the one in question. Not much used yet.'},
            {'name': 'succeeded', 'definition': 'ID of temple that replaced the one in question. Not much used yet.'},
            {'name': 'sex', 'definition': 'Sex of the divinity to whom the temple is dedicated, including “both”. '},
            {'name': 'dedicationday', 'definition': 'Calendar date for the dedication of the temple. Mainly applies to the city of Rome.'},
            {'name': 'deitytype', 'definition': 'Description of the nature of the deity with multiple values possible. Allowed values are: god, hero, concept, city, emperor, family.'},
            {'name': 'culture', 'definition': 'Culture to which the temple belonged, broadly speaking. For example, Greek or Roman.'},
            {'name': 'style', 'definition': 'Architectural type of the temple.'},
            {'name': 'extant', 'definition': 'Is the temple still in existence, even if fragmentary?'},
            {'name': 'source', 'definition': 'Other database or project that was the original source for this entry.'},
            {'name': 'meetings', 'definition': 'Did the Roman senate meet in the temple. Only applies to ones in the city of Rome.'},
            {'name': 'note', 'definition': 'Pertinent note.'},
            {'name': 'vici', 'definition': 'Vici.org ID for the temple.'},
            {'name': 'pleiades', 'definition': 'Pleiades ID for the temple.'},
            {'name': 'dare', 'definition': 'DARE ID for the temple (defunct?).'},
            {'name': 'arachne', 'definition': 'DAIR’s Arachne ID for the temple.'},
            {'name': 'livius', 'definition': 'Livius ID for the temple.'},
            {'name': 'wikipedia', 'definition': 'Wikipedia article for the temple.'},
            {'name': 'wikidata', 'definition': 'Wikidata ID for the temple.'},
            {'name': 'digitalromanforum', 'definition': 'Digital Roman Forum ID for the temple.'},
            {'name': 'digitalesforumromanum', 'definition': 'Digitales Forum Romanam ID for the temple.'},
            {'name': 'trismegistos', 'definition': 'Trismegistos ID for the temple.'},
            {'name': 'ads', 'definition': 'Archeological Data Service ID for the temple (British).'},
            {'name': 'cona', 'definition': 'Getty Cultural Objects Names Authority ID for the temple.'},
            {'name': 'topostext', 'definition': 'ID for the temple.'},
            {'name': 'sls', 'definition': 'Heritage Gazetteer of Libya ID for the temple.'},
            {'name': 'url', 'definition': 'External URL for the temple.'},
            {'name': 'checked', 'definition': 'Whether I looked at the evidence for the temple to confirm its existence.'},
        ]
    }
    return render(request, 'info.html', context)
