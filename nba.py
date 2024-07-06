import pandas as pd
import numpy as np
from datascraper import get_player_stats

# Define column mappings for different stat categories
column_mappings = {
    "Last 5 games in general": {
        'PTS': 'PTS', 'REB': 'REB', 'AST': 'AST', 'STL': 'STL', 'BLK': 'BLK',
        'FGM': 'FGM', 'FGA': 'FGA', '3PM': '3PM', '3PA': '3PA',
        'FTM': 'FTM', 'FTA': 'FTA', 'OREB': 'OREB', 'DREB': 'DREB', 'TOV': 'TOV'
    },
    "Last 5 regular season games against team": {
        'PTS': 'PTS', 'REB': 'REB', 'AST': 'AST', 'STL': 'STL', 'BLK': 'BLK',
        'FGM': 'FGM', 'FGA': 'FGA', '3PM': '3PM', '3PA': '3PA',
        'FTM': 'FTM', 'FTA': 'FTA', 'OREB': 'OREB', 'DREB': 'DREB', 'TOV': 'TOV'
    },
    "Last 5 playoff games against team": {
        'PTS': 'PTS', 'REB': 'REB', 'AST': 'AST', 'STL': 'STL', 'BLK': 'BLK',
        'FGM': 'FGM', 'FGA': 'FGA', '3PM': '3PM', '3PA': '3PA',
        'FTM': 'FTM', 'FTA': 'FTA', 'OREB': 'OREB', 'DREB': 'DREB', 'TOV': 'TOV'
    },
    "Home stats against team": {
        'PTS': 'PTS', 'REB': 'REB', 'AST': 'AST', 'STL': 'STL', 'BLK': 'BLK',
        'FGM': 'FGM', 'FGA': 'FGA', '3PM': '3PM', '3PA': '3PA',
        'FTM': 'FTM', 'FTA': 'FTA', 'OREB': 'OREB', 'DREB': 'DREB', 'TOV': 'TOV'
    },
    "Away stats against team": {
        'PTS': 'PTS', 'REB': 'REB', 'AST': 'AST', 'STL': 'STL', 'BLK': 'BLK',
        'FGM': 'FGM', 'FGA': 'FGA', '3PM': '3PM', '3PA': '3PA',
        'FTM': 'FTM', 'FTA': 'FTA', 'OREB': 'OREB', 'DREB': 'DREB', 'TOV': 'TOV'
    },
    "Current season average": {
        'PPG': 'PTS', 'RPG': 'REB', 'APG': 'AST', 'SPG': 'STL', 'BPG': 'BLK',
        'FGM': 'FGM', 'FGA': 'FGA', '3PM': '3PM', '3PA': '3PA',
        'FTM': 'FTM', 'FTA': 'FTA', 'OREB': 'OREB', 'DREB': 'DREB', 'TPG': 'TOV'
    },
    "Home stats (regular season)": {
        'PPG': 'PTS', 'RPG': 'REB', 'APG': 'AST', 'SPG': 'STL', 'BPG': 'BLK',
        'FGM': 'FGM', 'FGA': 'FGA', '3PM': '3PM', '3PA': '3PA',
        'FTM': 'FTM', 'FTA': 'FTA', 'OREB': 'OREB', 'DREB': 'DREB', 'TPG': 'TOV'
    },
    "Away stats (regular season)": {
        'PPG': 'PTS', 'RPG': 'REB', 'APG': 'AST', 'SPG': 'STL', 'BPG': 'BLK',
        'FGM': 'FGM', 'FGA': 'FGA', '3PM': '3PM', '3PA': '3PA',
        'FTM': 'FTM', 'FTA': 'FTA', 'OREB': 'OREB', 'DREB': 'DREB', 'TPG': 'TOV'
    }
}

# List of season-related stat categories
season_related_categories = [
    "Current season average", 
    "Home stats (regular season)", 
    "Away stats (regular season)"
]

def clean_nba_data(data, column_mapping, is_season_avg=False):
    """
    Cleans NBA data by keeping specified columns and adding calculated columns.
    
    Parameters:
    data (list of list): Raw data from StatMuse.
    column_mapping (dict): Mapping from raw column names to standardized names.
    is_season_avg (bool): Flag to indicate if the data is season averages.
    
    Returns:
    pd.DataFrame: Cleaned and processed DataFrame.
    """
    header = data[0]
    indices_to_keep = {raw: header.index(raw) for raw in column_mapping.keys() if raw in header}

    cleaned_rows = []
    for row in data[1:]:
        if row and 'Average' not in row:
            try:
                cleaned_row = {column_mapping[raw]: float(row[idx]) if row[idx] else 0.0 for raw, idx in indices_to_keep.items()}
                
                # Extract values to calculate new columns
                pts = cleaned_row.get('PTS', 0.0)
                reb = cleaned_row.get('REB', 0.0)
                ast = cleaned_row.get('AST', 0.0)
                blk = cleaned_row.get('BLK', 0.0)
                stl = cleaned_row.get('STL', 0.0)

                # Calculate new columns
                cleaned_row['PTS + REB'] = pts + reb
                cleaned_row['PTS + AST'] = pts + ast
                cleaned_row['PTS + REB + AST'] = pts + reb + ast
                cleaned_row['BLK + STL'] = blk + stl
                cleaned_row['REB + AST'] = reb + ast

                cleaned_rows.append(cleaned_row)
            except ValueError:
                continue

    # Create DataFrame
    df = pd.DataFrame(cleaned_rows)
    
    # Adjust column names for season averages
    if is_season_avg:
        df.columns = [col.replace("PPG", "PTS").replace("RPG", "REB").replace("APG", "AST").replace("SPG", "STL").replace("BPG", "BLK").replace("TPG", "TOV") for col in df.columns]
    
    return df

def preprocess_nba_data(player_name, team, season_type):
    """
    Fetches, cleans, and preprocesses NBA player data for the given player and team.
    
    Parameters:
    player_name (str): The name of the player.
    team (str): The opposing team.
    season_type (str): Either "Regular Season" or "Playoffs".
    
    Returns:
    pd.DataFrame: Preprocessed data ready for model training.
    """
    league = "nba"
    player_stats = get_player_stats(league, player_name, team)
    
    game_data_frames = []
    season_data_frames = []

    for stat_category, stats_data in player_stats.items():
        if season_type == "Regular Season" and stat_category == "Last 5 playoff games against team":
            continue

        print(f"Processing: {stat_category}")
        column_mapping = column_mappings.get(stat_category, {})
        if stat_category in season_related_categories:
            cleaned_data = clean_nba_data(stats_data, column_mapping, is_season_avg=True)
            cleaned_data['Category'] = stat_category
            season_data_frames.append(cleaned_data)
        else:
            cleaned_data = clean_nba_data(stats_data, column_mapping)
            cleaned_data['Category'] = stat_category
            game_data_frames.append(cleaned_data)
    
    game_combined_df = pd.concat(game_data_frames, ignore_index=True)
    season_combined_df = pd.concat(season_data_frames, ignore_index=True)

    return game_combined_df, season_combined_df