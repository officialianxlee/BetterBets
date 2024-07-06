import numpy as np
from sklearn.calibration import calibration_curve
import matplotlib.pyplot as plt
import pandas as pd

def sigmoid(x):
    return 1 / (1 + np.exp(-x))

def evaluate_calibration(model, X, y, projection):
    y_binary = (y > projection).astype(int)
    pred_prob = sigmoid(model.predict(X) - projection)  # Probability of hitting the projection

    prob_true, prob_pred = calibration_curve(y_binary, pred_prob, n_bins=10)

    fig, ax = plt.subplots(1, 2, figsize=(14, 6))

    ax[0].plot(prob_pred, prob_true, marker='o', linewidth=1, label='Calibration curve')
    ax[0].plot([0, 1], [0, 1], linestyle='--', color='gray', label='Perfectly calibrated')
    ax[0].set_xlabel('Predicted probability')
    ax[0].set_ylabel('True probability')
    ax[0].set_title('Calibration plot')
    ax[0].legend()

    residuals = y - model.predict(X)
    ax[1].hist(residuals, bins=10, edgecolor='black', alpha=0.7)
    ax[1].set_xlabel('Residuals')
    ax[1].set_ylabel('Frequency')
    ax[1].set_title('Residuals distribution')

    plt.tight_layout()
    return fig

def predict_and_decide_with_probability(model, X, projection, X_train, y_train):
    X = np.array(X).reshape(1, -1)
    predicted_value = model.predict(X)[0]
    
    residuals = y_train - model.predict(X_train)
    std_residuals = np.std(residuals)
    n = len(X_train)
    
    # Calculate the confidence interval
    ci_lower = predicted_value - 1.96 * (std_residuals / np.sqrt(n))
    ci_upper = predicted_value + 1.96 * (std_residuals / np.sqrt(n))
    
    # Compute hit probability using sigmoid function
    hit_prob = sigmoid(predicted_value - projection) * 100

    decision = 'over' if predicted_value > projection else 'under'
    confidence_range = 1.96 * (std_residuals / np.sqrt(n))
    
    return predicted_value, decision, ci_lower, ci_upper, hit_prob, confidence_range

def evaluate_models(models, X_test, y_test, X_train, y_train, projection):
    results = []
    fig = None
    for model_type, model in models.items():
        print(f"Evaluating {model_type.capitalize()} model...")
        fig = evaluate_calibration(model, X_test, y_test, projection)

        example_input = X_test.iloc[0].to_numpy()
        predicted_value, decision, ci_lower, ci_upper, hit_prob, confidence_range = predict_and_decide_with_probability(model, example_input, projection, X_train, y_train)
        result = {
            "model_type": model_type.capitalize(),
            "predicted_value": predicted_value,
            "decision": decision,
            "confidence_interval": (ci_lower, ci_upper),
            "hit_probability": hit_prob,
            "confidence_range": confidence_range
        }
        results.append(result)
        print(f"{model_type.capitalize()} - Predicted Value: {predicted_value}, Decision: {decision}, Confidence Interval: ({ci_lower}, {ci_upper}), Hit Probability: {hit_prob:.2f}%, Confidence: {hit_prob:.2f}% ± {confidence_range:.2f}")
    
    return fig, results
