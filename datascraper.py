import requests
from bs4 import BeautifulSoup
from datetime import datetime

def construct_base_url(league, player_name):
    """Constructs the base URL for scraping based on the league and player name."""
    base_url = f"https://www.statmuse.com/{league}/ask/{player_name}"
    return base_url

def construct_full_url(base_url, query, team=None):
    """Constructs the full URL for a specific query based on the base URL."""
    if team:
        return f"{base_url}-vs-{team}-{query}"
    else:
        return f"{base_url}-{query}"

def scrape_data(url):
    """Scrapes the table data from the given StatMuse URL."""
    response = requests.get(url)
    soup = BeautifulSoup(response.content, 'html.parser')

    table = soup.find('table')
    if not table:
        print(f"No table found at {url}")
        return []

    headers = [header.get_text(strip=True) for header in table.find_all('th')]
    rows = table.find_all('tr')
    data = [headers]

    for row in rows[1:]:
        cells = row.find_all('td')
        row_data = [cell.get_text(strip=True) for cell in cells]
        if any(cell.strip() for cell in row_data) and 'Total' not in row_data:
            data.append(row_data)

    return data

def filter_recent_seasons(data):
    """Filters the season averages to include only the two most recent seasons."""
    if not data or len(data) < 2:
        return data

    headers = data[0]
    filtered_data = [headers]

    # Parse the season data and filter for the most recent two seasons
    seasons = []
    for row in data[1:]:
        try:
            season = row[headers.index("SEASON")]
            games_played = int(row[headers.index("GP")])
            if season and games_played >= 0:
                year = int(season.split('-')[0])
                seasons.append((year, games_played, row))
        except (ValueError, IndexError):
            continue

    # Sort by the most recent season and filter
    seasons = sorted(seasons, key=lambda x: x[0], reverse=True)
    most_recent_seasons = seasons[:2]

    # Check if the most recent season has fewer than 10 games
    if len(most_recent_seasons) > 0 and most_recent_seasons[0][1] < 10:
        most_recent_seasons = seasons[1:3]

    for season in most_recent_seasons:
        filtered_data.append(season[2])

    return filtered_data

def get_player_stats(league, player_name, team):
    """Gets various statistics for a player."""
    base_url = construct_base_url(league, player_name)
    stats = {}

    # Last 5 games in general (including playoffs if applicable)
    general_url = construct_full_url(base_url, "last-5-games")
    stats["Last 5 games in general"] = scrape_data(general_url)

    # Last 5 regular season games against the team
    reg_season_url = construct_full_url(base_url, "last-5-games-vs", team)
    stats["Last 5 regular season games against team"] = scrape_data(reg_season_url)
    
    # Last 5 playoff games against the team
    playoff_url = construct_full_url(base_url, "last-5-playoff-games-vs", team)
    stats["Last 5 playoff games against team"] = scrape_data(playoff_url)

    # Home and away stats against the team (use data directly)
    home_team_url = construct_full_url(base_url, "home", team)
    home_team_data = scrape_data(home_team_url)
    stats["Home stats against team"] = home_team_data

    away_team_url = construct_full_url(base_url, "away", team)
    away_team_data = scrape_data(away_team_url)
    stats["Away stats against team"] = away_team_data
    
    # Current season average
    season_avg_url = construct_full_url(base_url, "current-season-averages")
    season_avg_data = scrape_data(season_avg_url)
    stats["Current season average"] = filter_recent_seasons(season_avg_data)

    # Home and away stats (regular season)
    home_reg_url = construct_full_url(base_url, "home-per-season")
    home_reg_data = scrape_data(home_reg_url)
    stats["Home stats (regular season)"] = filter_recent_seasons(home_reg_data)

    away_reg_url = construct_full_url(base_url, "away-per-season")
    away_reg_data = scrape_data(away_reg_url)
    stats["Away stats (regular season)"] = filter_recent_seasons(away_reg_data)

    return stats

# # Example usage
# league = "nba"
# player_name = "luka-doncic"
# team = "celtics"

# player_stats = get_player_stats(league, player_name, team)

# # Print the scraped data
# for key, value in player_stats.items():
#     print(f"{key}:")
#     for row in value:
#         print(row)
#     print()
