# barchart.py
import pandas as pd
import matplotlib.pyplot as plt

def generate_bar_chart(df, player_name, stat_type, team_name, projection):
    # Ensure the DataFrame is not empty
    if df.empty:
        print("The DataFrame is empty. No chart will be generated.")
        return
    
    # Extract the relevant columns
    dates = df['DATE']
    stat_values = df[stat_type]

    # Determine the colors of the bars
    colors = ['green' if value > projection else 'red' if value < projection else 'gray' for value in stat_values]

    # Plot the bar chart
    plt.figure(figsize=(10, 6))
    bars = plt.bar(dates, stat_values, color=colors)
    plt.axhline(y=projection, color='blue', linestyle='--', label=f'Projection: {projection}')
    plt.xlabel('Date of the Game')
    plt.ylabel(stat_type.capitalize())
    plt.title(f'{player_name} vs {team_name} - {stat_type.capitalize()}')
    plt.xticks(rotation=45)
    plt.tight_layout()
    plt.legend()

    # Display the plot
    plt.show()

# # Example usage (for testing purposes only, remove or comment out when using in other scripts)
# if __name__ == "__main__":
#     # Sample DataFrame for testing
#     data = {
#         'DATE': ['2021-01-01', '2021-01-02', '2021-01-03'],
#         'PTS': [30, 25, 40]
#     }
#     df = pd.DataFrame(data)
#     generate_bar_chart(df, 'Luka Doncic', 'PTS', 'Boston Celtics', 30.5)
