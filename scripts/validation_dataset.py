# This script creates a validation data set of games 650-700 in the 17/18-season. 
# Season averages are calculated for each team up until the game being played. These averages
# replace actual stats in games 650-700 and are saved with the outcome. 

import pandas as pd
import numpy as np
import csv

def team_average(team_name, game_number):
    """ 
    Calculates average performance of a team up until a certain game.
    Requires a team_name (string) and a game_number (int).
    Returns a list of average statistics for team.
    """

    # Get games up until game_number.
    validation_df = df[:game_number]

    # Find all games played at home by team and select their stats. 
    home_games = validation_df.loc[validation_df['home_team'] == team_name].iloc[:, 2:14]
    
    # Find all games played away by team and select their stats. 
    away_games = validation_df.loc[validation_df['away_team'] == team_name].iloc[:, 14:-2]
    
    # Calculate average statistics for team.
    averages = np.divide(home_games.mean().values + away_games.mean().values,2).tolist()
    
    return averages

# Load training data set.
df = pd.read_csv("training_dataset.csv")

# Collect average statistics of teams in the validation games and write to csv. 
with open("validation_dataset.csv", "w", newline='') as outfile:
    
    filewriter = csv.writer(outfile, delimiter=',', quoting=csv.QUOTE_MINIMAL)

    # Iterate over validation games 651-701.
    for game in range(651, 701):

        validation_game = df[game:game+1]
        
        home_team_name = validation_game['home_team'].tolist()[0]
        
        away_team_name = validation_game['away_team'].tolist()[0]
        
        outcome = validation_game['outcome'].tolist()[0]
        
        # Calculate team averages up until current game. 
        home_team_averages = team_average(home_team_name, game)
        away_team_averages = team_average(away_team_name, game)
    
        validation_vector = home_team_averages + away_team_averages + [outcome]
        
        # Write to statistics to csv.
        filewriter.writerow(validation_vector)