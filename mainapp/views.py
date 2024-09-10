import requests
from django.shortcuts import render, get_object_or_404
from django.core.paginator import Paginator

# Fetch all matches
import requests

def get_all_match_data():
    base_url = "https://rest.entitysport.com/v2/matches/"
    token = "ec471071441bb2ac538a0ff901abd249"
    per_page = 10
    total_pages = 21
    all_matches = []

    # Loop through all pages and fetch match data
    for page in range(1, total_pages + 1):
        response = requests.get(f"{base_url}?status=2&token={token}&per_page={per_page}&paged={page}")
        if response.status_code == 200:
            data = response.json()
            matches = data['response']['items']
            all_matches.extend(matches)
        else:
            print(f"Failed to fetch data for page {page}")
            break

    return all_matches


# View for paginated match data
def matches_view(request):
    match_data = get_all_match_data()  # Fetch all matches

    # Set up pagination (10 matches per page)
    paginator = Paginator(match_data, 10)  
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    return render(request, 'matches.html', {'page_obj': page_obj})

# Fetch squad data for a specific competition
def get_squad_data(competition_id):
    base_url = f"https://rest.entitysport.com/v2/competitions/{competition_id}/squads/"
    token = "ec471071441bb2ac538a0ff901abd249"
    response = requests.get(f"{base_url}?token={token}")
    
    if response.status_code == 200:
        data = response.json()
        squads = data['response']['squads']
        
        # Extract relevant information from the squad data
        formatted_squads = []
        for squad in squads:
            team = squad['team']
            players = squad['players']
            team_info = {
                'team_name': team['title'],
                'team_logo': team['logo_url'],
                'players': []
            }
            for player in players:
                player_info = {
                    'name': player['title'],
                    'playing_role': player.get('playing_role', 'N/A'),
                    'batting_style': player.get('batting_style', 'N/A'),
                    'bowling_style': player.get('bowling_style', 'N/A'),
                    'social_media': {
                        'facebook': player.get('facebook_profile', ''),
                        'twitter': player.get('twitter_profile', ''),
                        'instagram': player.get('instagram_profile', '')
                    }
                }
                team_info['players'].append(player_info)
            
            formatted_squads.append(team_info)
        
        return formatted_squads
    
    return []

# View to display squads for a specific competition
def squads_view(request, competition_id):
    squads = get_squad_data(competition_id)
    return render(request, 'squads.html', {'squads': squads, 'competition_id': competition_id})