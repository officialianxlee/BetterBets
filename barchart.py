#BAR CHART
import matplotlib.pyplot as plt
import numpy as np
from datetime import datetime
import requests
from PIL import Image
from io import BytesIO
from matplotlib.offsetbox import OffsetImage, AnnotationBbox
import matplotlib.pyplot as plt


def get_team_logo(team_abbr):
    url = f"https://a.espncdn.com/i/teamlogos/nba/500/{team_abbr}.png"
    response = requests.get(url)
    if response.status_code == 200:
        img = Image.open(BytesIO(response.content))
        return img
    else:
        print(f"Error fetching logo for {team_abbr}: {response.status_code}")
        return None

def plot_sports_stats(data, parameter, projection):
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

    # Calculate the mean of the values
    mean_value = np.mean(sorted_values)

    # Plotting the bar chart
    plt.figure(figsize=(12, 8))

    colors = ['green' if value >= mean_value else 'red' for value in sorted_values]

    bars = plt.bar(x_values, sorted_values, width=0.6, color=colors)
    plt.axhline(y=mean_value, color='blue', linestyle='--', label=f'Average {parameter}')
    # Plot the projection line
    plt.axhline(y=projection, color='purple', linestyle='-.', label='Projection')

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
data = [
    ['', '', 'NAME', 'DATE', 'TM', '', 'OPP', 'CMP', 'ATT', 'PCT', 'YDS', 'AVG', 'TD', 'INT', 'RATE', 'TD%', 'INT%', 'SCK', 'SCKY'],
    ['1', '', 'Tom BradyT. Brady', '11/30/2014', 'NE', '@', 'GB', '22', '35', '62.9', '245', '7.0', '2', '0', '102.7', '5.7', '0.0', '1', '9'],
    ['2', '', 'Tom BradyT. Brady', '11/4/2018', 'NE', 'vs', 'GB', '22', '35', '62.9', '294', '8.4', '1', '0', '99.0', '2.9', '0.0', '2', '21'],
    ['3', '', 'Tom BradyT. Brady', '10/18/2020', 'TB', 'vs', 'GB', '17', '27', '63.0', '166', '6.1', '2', '0', '104.9', '7.4', '0.0', '0', '0'],
    ['4', '', 'Tom BradyT. Brady', '1/24/2021', 'TB', '@', 'GB', '20', '36', '55.6', '280', '7.8', '3', '3', '73.8', '8.3', '8.3', '1', '5'],
    ['5', '', 'Tom BradyT. Brady', '9/25/2022', 'TB', 'vs', 'GB', '31', '42', '73.8', '271', '6.5', '1', '0', '98.4', '2.4', '0.0', '3', '20'],
    ['', '', 'Average', '', '', '', '', '22.4', '35.0', '64.0', '251.2', '7.2', '1.8', '0.6', '95.3', '5.1', '1.7', '1.4', '11.0']
]

plot_sports_stats(data, 'TD', 10)

lebron_james_career = geturl("nba", "lebron-james", "", "playoff-game-log")
lj = scrape_statmuse(lebron_james_career)
v = clean_nba_data(lj)
plot_sports_stats(v, 'PTS', 10)
