import numpy as np
from sklearn.calibration import calibration_curve
import matplotlib.pyplot as plt
import joblib
import pandas as pd
from sklearn.metrics import mean_squared_error, r2_score

def load_model_and_data(model_file, X_test_file, y_test_file, X_train_file, y_train_file):
    model = joblib.load(model_file)
    X_test = pd.read_csv(X_test_file)
    y_test = pd.read_csv(y_test_file).values.flatten()
    X_train = pd.read_csv(X_train_file)
    y_train = pd.read_csv(y_train_file).values.flatten()
    return model, X_test, y_test, X_train, y_train

def evaluate_calibration(model, X, y, projection):
    y_binary = (y > projection).astype(int)
    pred_prob = (model.predict(X) > projection).astype(float)

    prob_true, prob_pred = calibration_curve(y_binary, pred_prob, n_bins=10)

    plt.figure(figsize=(14, 6))

    plt.subplot(1, 2, 1)
    plt.plot(prob_pred, prob_true, marker='o', linewidth=1, label='Calibration curve')
    plt.plot([0, 1], [0, 1], linestyle='--', color='gray', label='Perfectly calibrated')
    plt.xlabel('Predicted probability')
    plt.ylabel('True probability')
    plt.title('Calibration plot')
    plt.legend()

    residuals = y - model.predict(X)
    plt.subplot(1, 2, 2)
    plt.hist(residuals, bins=10, edgecolor='black', alpha=0.7)
    plt.xlabel('Residuals')
    plt.ylabel('Frequency')
    plt.title('Residuals distribution')

    plt.tight_layout()
    plt.show()

def predict_and_decide_with_probability(model, X, projection, X_train, y_train):
    X = np.array(X).reshape(1, -1)
    predicted_value = model.predict(X)[0]
    
    residuals = y_train - model.predict(X_train)
    std_residuals = np.std(residuals)
    
    ci_lower = predicted_value - 1.96 * std_residuals
    ci_upper = predicted_value + 1.96 * std_residuals
    
    over_prob = min(max(1 - (np.abs(predicted_value - projection) / std_residuals), 0), 1)
    under_prob = 1 - over_prob
    
    decision = 'over' if predicted_value > projection else 'under'
    confidence = over_prob * 100 if decision == 'over' else under_prob * 100
    
    if confidence > 100:
        confidence = 100
    elif confidence < 0:
        confidence = 0
    
    return predicted_value, decision, ci_lower, ci_upper, confidence

if __name__ == "__main__":
    # Define the model types and their corresponding model files
    model_types = ['random_forest', 'gradient_boosting', 'svr', 'xgboost', 'catboost']
    model_files = [f'trained_{model_type}_model.pkl' for model_type in model_types]

    X_test_file = 'X_test.csv'
    y_test_file = 'y_test.csv'
    X_train_file = 'X_train.csv'
    y_train_file = 'y_train.csv'

    projection = 32.5

    for model_file, model_type in zip(model_files, model_types):
        model, X_test, y_test, X_train, y_train = load_model_and_data(model_file, X_test_file, y_test_file, X_train_file, y_train_file)
        X = X_test
        y = y_test

        evaluate_calibration(model, X, y, projection)

        example_input = X_test.iloc[0].to_numpy()
        predicted_value, decision, ci_lower, ci_upper, confidence = predict_and_decide_with_probability(model, example_input, projection, X_train, y_train)
        print(f"{model_type.capitalize()} - Predicted Value: {predicted_value}, Decision: {decision}, Confidence Interval: ({ci_lower}, {ci_upper}), Confidence: {confidence:.2f}%")
