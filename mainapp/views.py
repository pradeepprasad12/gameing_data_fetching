import requests
from django.shortcuts import render

# Fetch data from the API
def get_match_data():
    base_url = "https://rest.entitysport.com/v2/matches/"
    token = "ec471071441bb2ac538a0ff901abd249"
    total_pages = 2  # Limit to 2 pages to keep the data manageable

    all_matches = []

    for page in range(1, total_pages + 1):
        response = requests.get(f"{base_url}?status=2&token={token}&per_page=10&paged={page}")
        if response.status_code == 200:
            data = response.json()
            matches = data['response']['items']
            all_matches.extend(matches)

    return all_matches

# Create a view for displaying matches
def matches_view(request):
    matches = get_match_data()
    return render(request, 'matches.html', {'matches': matches})
