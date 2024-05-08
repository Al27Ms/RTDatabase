from django.shortcuts import render
from django.core.paginator import Paginator
from .utils import read_csv_data  # Import funkcji do czytania danych z pliku CSV

def index(request):
    # Odczytaj dane z pliku CSV
    csv_data = read_csv_data('data/RT_DATA.CSV')

    # Paginacja danych
    paginator = Paginator(csv_data, 25)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    return render(request, 'index.html', {'page_obj': page_obj})
