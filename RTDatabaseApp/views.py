import requests
from django.core.paginator import Paginator
from django.shortcuts import render, Http404
from .utils import read_csv_data

def temple_list(request):
    csv_data = read_csv_data('data/RT_DATA2.CSV')

    query = request.GET.get('q', '')
    if query:
        csv_data = [row for row in csv_data if query.lower() in row['name'].lower()]

    paginator = Paginator(csv_data, 20)  # Paginate with 10 items per page
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    return render(request, 'temple_list.html', {'page_obj': page_obj, 'query': query})

def temple_detail(request, temple_id):
    csv_data = read_csv_data('data/RT_DATA2.CSV')
    temple = next((row for row in csv_data if row['id'] == str(temple_id)), None)
    if temple is None:
        raise Http404("Świątynia nie została znaleziona")

    wikipedia_image_url = get_wikipedia_image_url(temple['wikipedia'])
    return render(request, 'temple_detail.html', {'temple': temple, 'wikipedia_image_url': wikipedia_image_url})

def get_wikipedia_image_url(page_title):
    url = f"https://en.wikipedia.org/w/api.php"
    params = {
        'action': 'query',
        'titles': page_title,
        'prop': 'pageimages',
        'format': 'json',
        'pithumbsize': 500,
    }
    response = requests.get(url, params=params).json()
    pages = response.get('query', {}).get('pages', {})
    for page_id, page_data in pages.items():
        thumbnail = page_data.get('thumbnail', {})
        return thumbnail.get('source')
    return None