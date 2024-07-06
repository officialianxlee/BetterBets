import tkinter as tk
from tkinter import ttk
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import matplotlib.pyplot as plt
from nba import preprocess_nba_data
from model import train_models
from decisionmodel import evaluate_models

def run_prediction():
    league = league_var.get()
    player_name = player_name_entry.get()
    team = team_entry.get()
    stat = stat_var.get()
    projection = float(projection_entry.get())
    season_type = season_var.get()
    model_type = model_var.get()

    game_data, season_data = preprocess_nba_data(player_name, team, season_type)
    models, X_test, y_test, X_train, y_train = train_models(game_data, season_data, model_type)

    fig, text_output = evaluate_models(models, X_test, y_test, X_train, y_train, projection)

    # Display the plots
    canvas = FigureCanvasTkAgg(fig, master=window)
    canvas.draw()
    canvas.get_tk_widget().pack(side=tk.TOP, fill=tk.BOTH, expand=True)

    # Display the text output
    result_label.config(text=text_output)

window = tk.Tk()
window.title("Sports Betting Prediction")

# League input
tk.Label(window, text="League:").pack()
league_var = tk.StringVar(value="nba")
league_entry = tk.Entry(window, textvariable=league_var)
league_entry.pack()

# Player name input
tk.Label(window, text="Player Name:").pack()
player_name_entry = tk.Entry(window)
player_name_entry.pack()

# Team input
tk.Label(window, text="Team:").pack()
team_entry = tk.Entry(window)
team_entry.pack()

# Statistic input
tk.Label(window, text="Statistic:").pack()
stat_var = tk.StringVar(value="PTS")
stat_entry = tk.Entry(window, textvariable=stat_var)
stat_entry.pack()

# Projection input
tk.Label(window, text="Projection:").pack()
projection_entry = tk.Entry(window)
projection_entry.pack()

# Season type dropdown
tk.Label(window, text="Season Type:").pack()
season_var = tk.StringVar(value="regular")
season_dropdown = ttk.Combobox(window, textvariable=season_var, values=["regular", "playoffs"])
season_dropdown.pack()

# Model type dropdown
tk.Label(window, text="Model Type:").pack()
model_var = tk.StringVar(value="random_forest")
model_dropdown = ttk.Combobox(window, textvariable=model_var, values=["random_forest", "gradient_boosting", "svr", "xgboost", "catboost"])
model_dropdown.pack()

# Generate button
generate_button = tk.Button(window, text="Generate Statistic", command=run_prediction)
generate_button.pack()

# Result label
result_label = tk.Label(window, text="")
result_label.pack()

window.mainloop()
