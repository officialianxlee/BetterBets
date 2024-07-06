import tkinter as tk
from tkinter import ttk
from nba import preprocess_nba_data
from model import main as train_main
from decisionmodel import evaluate_models
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import pandas as pd

def run_prediction():
    league = league_entry.get()
    player_name = player_name_entry.get()
    team = team_entry.get()
    stat = stat_entry.get()
    projection = float(projection_entry.get())
    season_type = season_type_var.get()
    model_type = model_type_var.get()

    game_data, season_data = preprocess_nba_data(player_name, team, season_type)
    model, X_test, y_test, X_train, y_train = train_main(game_data, season_data, model_type)

    fig, results = evaluate_models({model_type: model}, X_test, y_test, X_train, y_train, projection)
    
    text_output = "\n".join([f"{result['model_type']} - Predicted Value: {result['predicted_value']}, Decision: {result['decision']}, Confidence Interval: {result['confidence_interval']}, Hit Probability: {result['hit_probability']:.2f}%, Confidence: {result['hit_probability']:.2f}% ± {result['confidence_range']:.2f}" for result in results])
    result_label.config(text=text_output)
    
    # Display the plots in the Tkinter window
    for widget in plot_frame.winfo_children():
        widget.destroy()
    
    canvas = FigureCanvasTkAgg(fig, master=plot_frame)
    canvas.draw()
    canvas.get_tk_widget().pack()

app = tk.Tk()
app.title("Sports Betting Prediction")

tk.Label(app, text="League").grid(row=0, column=0)
league_entry = tk.Entry(app)
league_entry.grid(row=0, column=1)

tk.Label(app, text="Player Name").grid(row=1, column=0)
player_name_entry = tk.Entry(app)
player_name_entry.grid(row=1, column=1)

tk.Label(app, text="Team Against").grid(row=2, column=0)
team_entry = tk.Entry(app)
team_entry.grid(row=2, column=1)

tk.Label(app, text="Statistic").grid(row=3, column=0)
stat_entry = tk.Entry(app)
stat_entry.grid(row=3, column=1)

tk.Label(app, text="Projection").grid(row=4, column=0)
projection_entry = tk.Entry(app)
projection_entry.grid(row=4, column=1)

season_type_var = tk.StringVar(value="Regular Season")
tk.Label(app, text="Season Type").grid(row=5, column=0)
season_type_menu = ttk.Combobox(app, textvariable=season_type_var, values=["Regular Season", "Playoffs"])
season_type_menu.grid(row=5, column=1)

model_type_var = tk.StringVar(value="random_forest")
tk.Label(app, text="Model Type").grid(row=6, column=0)
model_type_menu = ttk.Combobox(app, textvariable=model_type_var, values=["random_forest", "weighted_moving_average", "svr", "catboost","gradient_boosting"])
model_type_menu.grid(row=6, column=1)

tk.Button(app, text="Generate Statistic", command=run_prediction).grid(row=7, column=0, columnspan=2)

result_label = tk.Label(app, text="", wraplength=400)
result_label.grid(row=8, column=0, columnspan=2)

plot_frame = tk.Frame(app)
plot_frame.grid(row=9, column=0, columnspan=2)

app.mainloop()
