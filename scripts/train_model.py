import numpy as np
import pandas as pd
from xgboost import XGBRegressor
import pickle
import os

# 1. Generate Synthetic Data
np.random.seed(42)

# Generate 10,000 realistic student profiles
num_samples = 10000

# MET scores usually follow a normal-ish distribution skewed towards the lower end
met_scores = np.random.normal(loc=110, scale=40, size=num_samples)
met_scores = np.clip(met_scores, 0, 240) # Ensure between 0 and 240

# Board percentages usually skewed towards the higher end
board_percentages = np.random.normal(loc=85, scale=10, size=num_samples)
board_percentages = np.clip(board_percentages, 50, 100) # Ensure between 50 and 100

# Calculate combined score based on MAHE's 50-50 formula
# MET score out of 240 converted to percentage -> (met/240)*100
# Total percentage = 0.5 * (met/240)*100 + 0.5 * board
combined_score = 0.5 * (met_scores / 240 * 100) + 0.5 * board_percentages

# Define a function to roughly map combined score to historical ranks
# A score of 95+ -> top 100, 90+ -> top 1000, etc.
def estimate_rank_from_combined(score):
    if score >= 95:
        return np.random.uniform(1, 100)
    elif score >= 90:
        return np.random.uniform(101, 1000)
    elif score >= 85:
        return np.random.uniform(1001, 3500)
    elif score >= 80:
        return np.random.uniform(3501, 8000)
    elif score >= 75:
        return np.random.uniform(8001, 14000)
    elif score >= 70:
        return np.random.uniform(14001, 22000)
    elif score >= 60:
        return np.random.uniform(22001, 35000)
    else:
        return np.random.uniform(35001, 45000)

# Vectorize the function
v_estimate = np.vectorize(estimate_rank_from_combined)
ranks = v_estimate(combined_score)

# Add some random noise to simulate real-world variance
noise = np.random.normal(0, 200, size=num_samples)
ranks = np.clip(ranks + noise, 1, 45000)

df = pd.DataFrame({
    'met_score': met_scores,
    'board_percentage': board_percentages,
    'rank': ranks
})

X = df[['met_score', 'board_percentage']]
y = df['rank']

# 2. Train XGBoost Model
print("Training XGBoost model...")
model = XGBRegressor(n_estimators=100, max_depth=5, learning_rate=0.1, random_state=42)
model.fit(X, y)

# 3. Save the Model
current_dir = os.path.dirname(os.path.abspath(__file__))
model_path = os.path.join(current_dir, 'model.json')
model.save_model(model_path)

print(f"Model saved successfully to {model_path}")
