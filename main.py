import tkinter as tk
from tkinter import ttk
from datascrapper import geturl
from datascrapper import scrape_statmuse
from nbbbba import clean_nba_data
from plot import plot_sports_stats

# Create the main window
root = tk.Tk()
root.title("Sports Statistics GUI")

# Create a label and dropdown for the league
league_label = tk.Label(root, text="League:")
league_label.grid(row=0, column=0)
league_var = tk.StringVar(value="NBA")
league_dropdown = ttk.Combobox(root, textvariable=league_var)
league_dropdown['values'] = ('NBA', 'NFL')
league_dropdown.grid(row=0, column=1)

# Create a label and text input for the player name
player_name_label = tk.Label(root, text="Player Name:")
player_name_label.grid(row=1, column=0)
player_name_entry = tk.Entry(root)
player_name_entry.grid(row=1, column=1)

# Create a label and text input for the team name
team_name_label = tk.Label(root, text="Team Name:")
team_name_label.grid(row=2, column=0)
team_name_entry = tk.Entry(root)
team_name_entry.grid(row=2, column=1)

# Create a label and dropdown for the time duration
time_duration_label = tk.Label(root, text="Time Duration:")
time_duration_label.grid(row=3, column=0)
time_duration_var = tk.StringVar(value="Last 5 Regular Games")
time_duration_dropdown = ttk.Combobox(root, textvariable=time_duration_var)
time_duration_dropdown['values'] = ('Last 5 Regular Games', 'Playoff Game Log')
time_duration_dropdown.grid(row=3, column=1)

# Create a label and dropdown for the statistic
statistic_label = tk.Label(root, text="Statistic:")
statistic_label.grid(row=4, column=0)
statistic_var = tk.StringVar(value="PTS")
statistic_dropdown = ttk.Combobox(root, textvariable=statistic_var)
statistic_dropdown['values'] = ('MIN', 'PTS', 'REB', 'AST', 'STL', 'BLK', 'FGM', 'FGA', '3PM', '3PA', 'FTM', 'FTA', 'OREB', 'DREB', 'TOV', 'PF', 'PTS + REB', 'PTS + AST', 'PTS + REB + AST', 'BLK + STL', 'REB + AST')
statistic_dropdown.grid(row=4, column=1)

# Create a label and text input for the projection
projection_label = tk.Label(root, text="Projection:")
projection_label.grid(row=5, column=0)
projection_entry = tk.Entry(root)
projection_entry.grid(row=5, column=1)


# Function to handle button click
def on_button_click():
    league = league_var.get()
    player_name = player_name_entry.get()
    team = team_name_entry.get()
    time_duration = time_duration_var.get()
    statistic = statistic_var.get()
    projection = float(projection_entry.get())

    url = geturl(league.lower(), player_name, team, time_duration)
    data = scrape_statmuse(url)

    if league == 'NBA':
        cleaned_data = clean_nba_data(data)
    # Add elif blocks for other leagues and their cleaning functions
    plot_sports_stats(cleaned_data, statistic, projection)


# Create a button to trigger data processing and plotting
button = tk.Button(root, text="Generate Plot", command=on_button_click)
button.grid(row=6, columnspan=2)

# Run the application
root.mainloop()
