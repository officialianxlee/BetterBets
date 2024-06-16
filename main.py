# main.py
from datascraper import get_player_stats
from barchart import generate_bar_chart
from nba import process_nba_stats
import pandas as pd

player_name = "Luka Doncic"
stat_type = "reb"  # This can be "Points", "PTS", "Rebounds", "REB", etc.
team_name = "Boston Celtics"
projection = 30.5  # Example projection value

# User's choice for data display
choice = 'last_7_games'  # 'regular', 'playoffs', 'combined', 'last_7_games'

df, standardized_stat_type = process_nba_stats(player_name, stat_type, team_name, choice)

# Generate the bar chart based on the user's choice
if not df.empty:
    generate_bar_chart(df, player_name, standardized_stat_type, team_name, projection)
