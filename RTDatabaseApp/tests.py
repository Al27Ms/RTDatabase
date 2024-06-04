from django.test import TestCase

# Create your tests here.
import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'RTDatabase.settings')
django.setup()

# Teraz możesz importować modele i uruchamiać testy
from RTDatabaseApp.models import RomanTemple

# Import modelu RomanTemple
from RTDatabaseApp.models import RomanTemple

# Sprawdzenie, czy istnieje rekord o identyfikatorze 1
try:
    temple = RomanTemple.objects.get(id=1)
    print("Świątynia o ID 1 istnieje.")
except RomanTemple.DoesNotExist:
    print("Świątynia o ID 1 nie istnieje.")





