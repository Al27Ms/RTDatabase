# RTDatabase Project

## Project Description

RTDatabase is a Django project designed to manage a database of Roman temples. The application allows users to browse a list of temples, view detailed information about individual temples, and locate them on a map. The project utilizes Django ORM to manage data stored in a CSV file and integrates external APIs such as Google Maps and Google Images.

## Features

### List of Features:
- **Temple List:** Browse a list of Roman temples with filtering and pagination capabilities.
- **Temple Detail:** Display detailed information about a selected temple, including images fetched from Google Images and its location on Google Maps.
- **Map View:** View all temples on an interactive map using the Google Maps API.
- **Info View:** Display information about attributes available in the database, such as ID, name, dedication, type, location, date, culture, etc.

## Technologies Used

- **Python 3.x**
- **Django 3.x:** Web framework for building web applications in Python.
- **Google Maps API:** Used for displaying temple locations on maps.
- **Google Images API:** Used for fetching temple images.
- **Git:** Version control system.
- **GitHub:** Repository hosting and project management.

### Getting Started

1. **Clone the repository:**

   ```bash
   git clone https://github.com/Al27Ms/RTDatabase.git
   cd RTDatabase
   ```

2. **Install dependencies:**

```bash
pip install -r requirements.txt
```

3. **Set up environment variables:**

- Create a .env file in the root directory.

- Add your Google Maps API key and other necessary API keys:

```bash
makefile
GOOGLE_API_KEY=your_google_api_key
GOOGLE_SEARCH_API_KEY=your_google_search_api_key
```
4. **Run the development server:**

```bash
python manage.py runserver
```
The application will be accessible at http://localhost:8000.
