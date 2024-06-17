# nba.py
from datascraper import get_player_stats, get_last_7_games
import pandas as pd

# Define the mapping of user-friendly stat types to actual column names
stat_type_mapping = {
    'points': 'PTS',
    'pts': 'PTS',
    'rebounds': 'REB',
    'reb': 'REB',
    'assists': 'AST',
    'ast': 'AST',
    'steals': 'STL',
    'stl': 'STL',
    'blocks': 'BLK',
    'blk': 'BLK',
    'field goals made': 'FGM',
    'fgm': 'FGM',
    'field goals attempted': 'FGA',
    'fga': 'FGA',
    'three points made': '3PM',
    '3pm': '3PM',
    'three points attempted': '3PA',
    '3pa': '3PA',
    'free throws made': 'FTM',
    'ftm': 'FTM',
    'free throws attempted': 'FTA',
    'fta': 'FTA',
    'offensive rebounds': 'OREB',
    'oreb': 'OREB',
    'defensive rebounds': 'DREB',
    'dreb': 'DREB',
    'turnovers': 'TOV',
    'tov': 'TOV',
    'pointsandrebound': ['PTS', 'REB'],
    'pointsandassists': ['PTS', 'AST'],
    'pointsreboundsassists': ['PTS', 'REB', 'AST'],
    'blocksandsteals': ['BLK', 'STL'],
    'reboundsandassists': ['REB', 'AST']
}

def process_nba_stats(player_name, stat_type, team_name, choice):
    league = 'nba'
    stat_type_key = stat_type.lower().replace(' ', '').replace(',', '').replace('+', '')
    stat_type_mapped = stat_type_mapping.get(stat_type_key, stat_type_key)  # Standardize the stat_type input
    
    if choice == 'regular':
        df = get_player_stats(player_name, stat_type_key, team_name, league, playoffs=False)
    elif choice == 'playoffs':
        df = get_player_stats(player_name, stat_type_key, team_name, league, playoffs=True)
    elif choice == 'combined':
        regular_season_df = get_player_stats(player_name, stat_type_key, team_name, league, playoffs=False)
        playoff_df = get_player_stats(player_name, stat_type_key, team_name, league, playoffs=True)
        if not regular_season_df.empty and not playoff_df.empty:
            df = pd.concat([regular_season_df, playoff_df], ignore_index=True)
        elif not regular_season_df.empty:
            df = regular_season_df
        elif not playoff_df.empty:
            df = playoff_df
        else:
            df = pd.DataFrame()
    elif choice == 'last_7_games':
        df = get_last_7_games(player_name, stat_type_key, league)
    else:
        df = pd.DataFrame()

    if df.empty:
        return df, stat_type
    
    # Define the index mapping
    index_mapping = {
        'NAME': 1,
        'DATE': 2,
        'PTS': 3,
        'REB': 4,
        'AST': 5,
        'STL': 6,
        'BLK': 7,
        'FGM': 8,
        'FGA': 9,
        '3PM': 10,
        '3PA': 11,
        'FTM': 12,
        'FTA': 13,
        'OREB': 14,
        'DREB': 15,
        'TOV': 16
    }
    
    # Invert the mapping to use indices for selection
    index_to_column = {v: k for k, v in index_mapping.items()}
    columns_to_keep = [index_to_column[i] for i in sorted(index_to_column.keys())]
    
    # Select desired columns by their names
    if not df.empty:
        df = df.loc[:, columns_to_keep]
        df.loc[:, 'NAME'] = df['NAME'].astype(str)
        df.loc[:, 'DATE'] = df['DATE'].astype(str)
        
        # Handle combined statistics
        if isinstance(stat_type_mapped, list):
            combined_stat_name = ' + '.join(stat_type_mapped)
            df[combined_stat_name] = df[stat_type_mapped].sum(axis=1)
            stat_type_mapped = combined_stat_name
    
    return df, stat_type_mapped

# Example usage (for testing purposes only, remove or comment out when using in other scripts)
if __name__ == "__main__":
    player_name = "Luka Doncic"
    stat_type = "Points and Assists"
    team_name = "Boston Celtics"
    choice = 'regular'  # 'regular', 'playoffs', 'combined', 'last_7_games'
    df, stat_type = process_nba_stats(player_name, stat_type, team_name, choice)
    print("Stats:")
    print(df)
