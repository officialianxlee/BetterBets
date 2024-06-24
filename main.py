import tkinter as tk
from tkinter import ttk
import importlib
from barchart import plot_sports_stats
from datascraper import geturl, scrape_statmuse
from nba import clean_nba_data
from nhl import clean_nhl_data

# Create the main window
root = tk.Tk()
root.title("Sports Statistics GUI")

# Create a label and dropdown for the league
league_label = tk.Label(root, text="League:")
league_label.grid(row=0, column=0)
league_var = tk.StringVar(value="NBA")
league_dropdown = ttk.Combobox(root, textvariable=league_var)
league_dropdown['values'] = ('NBA', 'NFL', 'NHL')
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

# Create a label and dropdown for the position (only for NHL)
position_label = tk.Label(root, text="Position:")
position_label.grid(row=4, column=0)
position_var = tk.StringVar(value="Player")
position_dropdown = ttk.Combobox(root, textvariable=position_var)
position_dropdown['values'] = ('Player', 'Goalie')
position_dropdown.grid(row=4, column=1)
position_label.grid_remove()
position_dropdown.grid_remove()

# Create a label and dropdown for the statistic
statistic_label = tk.Label(root, text="Statistic:")
statistic_label.grid(row=5, column=0)
statistic_var = tk.StringVar(value="PTS")
statistic_dropdown = ttk.Combobox(root, textvariable=statistic_var)
statistic_dropdown.grid(row=5, column=1)

# Create a label and text input for the projection
projection_label = tk.Label(root, text="Projection:")
projection_label.grid(row=6, column=0)
projection_entry = tk.Entry(root)
projection_entry.grid(row=6, column=1)

def update_statistic_options(*args):
    league = league_var.get()
    if league == 'NHL':
        position_label.grid()
        position_dropdown.grid()
        position = position_var.get().lower()
    else:
        position_label.grid_remove()
        position_dropdown.grid_remove()
        position = 'player'
    
    try:
        module = importlib.import_module(league.lower())
        if league == 'NHL':
            if position == 'goalie':
                get_statistics = getattr(module, f'get_{league.lower()}_goalie_statistics')
            else:
                get_statistics = getattr(module, f'get_{league.lower()}_player_statistics')
        else:
            get_statistics = getattr(module, f'get_{league.lower()}_statistics')
        stat_options = get_statistics()
        statistic_var.set(stat_options[0])
        statistic_dropdown['values'] = stat_options
    except ImportError:
        print(f"Module for {league} not found.")
    except AttributeError:
        print(f"Function to get statistics for {league} not found.")

# Update statistic options when the league or position changes
league_var.trace('w', update_statistic_options)
position_var.trace('w', update_statistic_options)

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
    elif league == 'NHL':
        position = position_var.get().lower()
        cleaned_data = clean_nhl_data(data, position)
    # Add elif blocks for other leagues and their cleaning functions
    
    plot_sports_stats(cleaned_data, statistic, projection)

# Create a button to trigger data processing and plotting
button = tk.Button(root, text="Generate Plot", command=on_button_click)
button.grid(row=7, columnspan=2)

# Initial update to set the correct statistic options
update_statistic_options()

# Run the application
root.mainloop()
