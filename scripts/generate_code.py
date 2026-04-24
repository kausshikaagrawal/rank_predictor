import numpy as np
import pandas as pd
from sklearn.tree import DecisionTreeRegressor
import m2cgen as m2c
import os

# 1. Generate Synthetic Data
np.random.seed(42)
num_samples = 5000 # reduced sample size slightly to keep code size small

met_scores = np.random.normal(loc=110, scale=40, size=num_samples)
met_scores = np.clip(met_scores, 0, 240)
board_percentages = np.random.normal(loc=85, scale=10, size=num_samples)
board_percentages = np.clip(board_percentages, 50, 100)

combined_score = 0.5 * (met_scores / 240 * 100) + 0.5 * board_percentages

def estimate_rank_from_combined(score):
    if score >= 95: return np.random.uniform(1, 100)
    elif score >= 90: return np.random.uniform(101, 1000)
    elif score >= 85: return np.random.uniform(1001, 3500)
    elif score >= 80: return np.random.uniform(3501, 8000)
    elif score >= 75: return np.random.uniform(8001, 14000)
    elif score >= 70: return np.random.uniform(14001, 22000)
    elif score >= 60: return np.random.uniform(22001, 35000)
    else: return np.random.uniform(35001, 45000)

v_estimate = np.vectorize(estimate_rank_from_combined)
ranks = v_estimate(combined_score)
noise = np.random.normal(0, 200, size=num_samples)
ranks = np.clip(ranks + noise, 1, 45000)

df = pd.DataFrame({'met_score': met_scores, 'board_percentage': board_percentages, 'rank': ranks})
X = df[['met_score', 'board_percentage']]
y = df['rank']

# 2. Train Decision Tree Model
print("Training Decision Tree model...")
# Keep max_depth reasonable so the generated Python code isn't megabytes in size
model = DecisionTreeRegressor(max_depth=8, random_state=42)
model.fit(X, y)

# 3. Generate native Python code
print("Generating pure Python code...")
code = m2c.export_to_python(model)

# 4. Save to model_logic.py
current_dir = os.path.dirname(os.path.abspath(__file__))
api_dir = os.path.join(current_dir, '..', 'api')
output_path = os.path.join(api_dir, 'model_logic.py')

with open(output_path, 'w') as f:
    f.write(code)

print(f"Native Python logic saved successfully to {output_path}")
