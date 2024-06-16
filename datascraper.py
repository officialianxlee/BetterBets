# datascraper.py
import requests
from bs4 import BeautifulSoup
import pandas as pd
from io import StringIO

def get_player_stats(player_name, stat_type, team_name, league, playoffs=False):
    query = f"{player_name} {stat_type} vs {team_name}"
    if playoffs:
        query += " playoffs"
    url = f"https://www.statmuse.com/{league}/ask/{query.replace(' ', '-')}"
    response = requests.get(url)
    if response.status_code != 200:
        print(f"Failed to retrieve data: {response.status_code}")
        return pd.DataFrame()
    
    soup = BeautifulSoup(response.text, 'html.parser')
    table = soup.find('table')

    if not table:
        print("Table not found")
        return pd.DataFrame()
    
    table_html = StringIO(str(table))
    df = pd.read_html(table_html)[0]
    
    return df

def get_last_7_games(player_name, stat_type, league):
    query = f"{player_name} last 7 games {stat_type}"
    url = f"https://www.statmuse.com/{league}/ask/{query.replace(' ', '-')}"
    response = requests.get(url)
    if response.status_code != 200:
        print(f"Failed to retrieve data: {response.status_code}")
        return pd.DataFrame()
    
    soup = BeautifulSoup(response.text, 'html.parser')
    table = soup.find('table')

    if not table:
        print("Table not found")
        return pd.DataFrame()
    
    table_html = StringIO(str(table))
    df = pd.read_html(table_html)[0]
    
    return df
