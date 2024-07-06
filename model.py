import pandas as pd
import numpy as np
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestRegressor, GradientBoostingRegressor
from sklearn.svm import SVR
import catboost as cb
from sklearn.metrics import mean_squared_error, r2_score

def preprocess_and_combine(game_data, season_data):
    combined_data = pd.concat([game_data, season_data], axis=0)
    return combined_data

def train_model(X, y, model_type='random_forest'):
    if model_type == 'random_forest':
        model = RandomForestRegressor()
    elif model_type == 'weighted_moving_average':
        model = WeightedMovingAverage()
    elif model_type == 'gradient_boosting':
        model = GradientBoostingRegressor()
    elif model_type == 'svr':
        model = SVR()
    elif model_type == 'catboost':
        model = cb.CatBoostRegressor(verbose=0)
    else:
        raise ValueError("Invalid model type specified")

    model.fit(X, y)
    return model

def main(game_data, season_data, model_type):
    combined_data = preprocess_and_combine(game_data, season_data)
    target_stat = 'PTS'
    X = combined_data.drop(columns=[target_stat, 'Category'])
    y = combined_data[target_stat]

    X = X.apply(pd.to_numeric, errors='coerce').fillna(0)
    y = pd.to_numeric(y, errors='coerce').fillna(0).values.flatten()

    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)
    model = train_model(X_train, y_train, model_type=model_type)

    predictions = model.predict(X_test)
    mse = mean_squared_error(y_test, predictions)
    r2 = r2_score(y_test, predictions)
    print(f"{model_type.capitalize()} Model Evaluation - MSE: {mse}, R2: {r2}")

    return model, X_test, y_test, X_train, y_train

class WeightedMovingAverage:
    def __init__(self):
        self.weights = None
        self.y = None

    def fit(self, X, y):
        self.weights = np.arange(1, len(y) + 1)
        self.y = y

    def predict(self, X):
        if self.y is not None:
            weighted_average = np.average(self.y, weights=self.weights)
            return np.full((X.shape[0],), weighted_average)
        else:
            raise ValueError("The model has not been fitted yet.")
