import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.linear_model import LinearRegression
from sklearn.ensemble import RandomForestRegressor, GradientBoostingRegressor
from sklearn.svm import SVR
import xgboost as xgb
import lightgbm as lgb
import catboost as cb
from sklearn.metrics import mean_squared_error, r2_score
import joblib

# Load data function
def load_data(game_data_file, season_data_file):
    game_data = pd.read_csv(game_data_file)
    season_data = pd.read_csv(season_data_file)
    return game_data, season_data

# Preprocess and combine data function
def preprocess_and_combine(game_data, season_data):
    combined_data = pd.concat([game_data, season_data], axis=0)
    return combined_data

# Model training function
def train_model(X, y, model_type='random_forest'):
    if model_type == 'random_forest':
        model = RandomForestRegressor()
    elif model_type == 'gradient_boosting':
        model = GradientBoostingRegressor()
    elif model_type == 'svr':
        model = SVR()
    elif model_type == 'xgboost':
        model = xgb.XGBRegressor()
    elif model_type == 'catboost':
        model = cb.CatBoostRegressor(verbose=0)
    else:
        raise ValueError("Invalid model type specified")

    model.fit(X, y)
    return model

# Example usage
if __name__ == "__main__":
    game_data_file = 'preprocessed_nba_game_datav3.csv'
    season_data_file = 'preprocessed_nba_season_datav3.csv'
    game_data, season_data = load_data(game_data_file, season_data_file)

    combined_data = preprocess_and_combine(game_data, season_data)

    target_stat = 'PTS'
    X = combined_data.drop(columns=[target_stat, 'Category'])
    y = combined_data[target_stat]

    X = X.apply(pd.to_numeric, errors='coerce').fillna(0)
    y = pd.to_numeric(y, errors='coerce').fillna(0).values.flatten()

    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

    model_types = ['random_forest', 'gradient_boosting', 'svr', 'xgboost', 'catboost']
    for model_type in model_types:
        model = train_model(X_train, y_train, model_type=model_type)

        joblib.dump(model, f'trained_{model_type}_model.pkl')

        predictions = model.predict(X_test)
        mse = mean_squared_error(y_test, predictions)
        r2 = r2_score(y_test, predictions)
        print(f"{model_type.capitalize()} Model Evaluation - MSE: {mse}, R2: {r2}")

        player_projection = 32.5
        example_input = X_test.iloc[0].to_numpy()
        predicted_value = model.predict(example_input.reshape(1, -1))[0]
        print(f"{model_type.capitalize()} Predicted Value: {predicted_value}")

    # Save the training and test sets to CSV files
    X_train.to_csv('X_train.csv', index=False)
    X_test.to_csv('X_test.csv', index=False)
    pd.DataFrame(y_train, columns=[target_stat]).to_csv('y_train.csv', index=False)
    pd.DataFrame(y_test, columns=[target_stat]).to_csv('y_test.csv', index=False)
