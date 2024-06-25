import matplotlib.pyplot as plt
import numpy as np
from datetime import datetime
import requests
from PIL import Image
from io import BytesIO
from matplotlib.offsetbox import OffsetImage, AnnotationBbox

def get_team_logo(team_abbr):
    url = f"https://a.espncdn.com/i/teamlogos/nba/500/{team_abbr}.png"
    response = requests.get(url)
    if response.status_code == 200:
        img = Image.open(BytesIO(response.content))
        return img
    else:
        print(f"Error fetching logo for {team_abbr}: {response.status_code}")
        return None

def plot_sports_stats(data, statistic, parameter, quantitative):
    plt.style.use('https://github.com/dhaitz/matplotlib-stylesheets/raw/master/pitayasmoothie-dark.mplstyle')

    # Extract header and find the index of the specified parameter
    header = data[0]
    index_to_extract = header.index(parameter)

    # Extracting dates, the specified parameter's values, and team abbreviations
    dates = [datetime.strptime(game[header.index('DATE')], '%m/%d/%Y') for game in data[1:] if game[header.index('DATE')]]
    values = [float(game[index_to_extract]) for game in data[1:] if game[index_to_extract]]
    team_abbrs = [game[header.index('TM')] for game in data[1:] if game[header.index('TM')]]

    # Sorting dates, values, and team abbreviations based on dates
    sorted_dates, sorted_values, sorted_team_abbrs = zip(*sorted(zip(dates, values, team_abbrs)))

    x_values = list(range(len(sorted_dates)))

    # Plotting the bar chart
    plt.figure(figsize=(12, 8))

    colors = ['green' if value >= quantitative else 'red' for value in sorted_values]

    bars = plt.bar(x_values, sorted_values, width=0.6, color=colors)
    # Plot the quantitative line
    plt.axhline(y=quantitative, color='purple', linestyle='-.', label='Quantitative Line')

    plt.xlabel('Date')
    plt.ylabel(parameter)
    plt.title(f'{parameter} Over Time')
    plt.xticks(x_values, [date.strftime('%b %d, %Y') for date in sorted_dates], rotation=45, ha='right')
    plt.legend()
    plt.grid(False)
    plt.tight_layout()

    # Adding data labels and team logos on top of each bar
    for i, bar in enumerate(bars):
        yval = bar.get_height()
        plt.text(bar.get_x() + bar.get_width() / 2, yval + 1, yval, ha='center', va='bottom', fontsize=10, color='white')

        # Add the team logo to each bar (optional, if applicable and logos are available)
        # team_logo = get_team_logo(sorted_team_abbrs[i])
        # if team_logo:
        #     imagebox = OffsetImage(team_logo, zoom=0.05)
        #     imagebox.image.axes = plt.gca()

        #     ab = AnnotationBbox(imagebox, (bar.get_x() + bar.get_width() / 2, yval - 2),  # Adjust the position to be slightly below the number
        #                         frameon=False, box_alignment=(0.5, 0))
        #     plt.gca().add_artist(ab)

    plt.show()

# Example usage:
# data = [
#     ['NAME', 'DATE', 'TM', 'OPP', 'PARAM'],
#     ['Player1', '6/18/2024', 'Team1', 'Opponent1', '5'],
#     ['Player2', '6/19/2024', 'Team2', 'Opponent2', '3'],
#     # Add more rows as needed...
# ]
# plot_sports_stats(data, 'statistic', 'PARAM', 4.0)
