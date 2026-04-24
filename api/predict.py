from flask import Flask, request, jsonify
import os
import numpy as np
from datetime import datetime
from pymongo import MongoClient
import xgboost as xgb

app = Flask(__name__)

# Load the trained XGBoost model natively to save Vercel bundle size
current_dir = os.path.dirname(os.path.abspath(__file__))
model_path = os.path.join(current_dir, 'model.json')

model = xgb.XGBRegressor()
try:
    model.load_model(model_path)
except Exception as e:
    print(f"Error loading model: {e}")

# MongoDB Setup
MONGO_URI = os.environ.get('MONGODB_URI')
client = None
db = None
users_collection = None

if MONGO_URI:
    try:
        client = MongoClient(MONGO_URI, serverSelectionTimeoutMS=5000)
        db = client['manipal_predictor']
        users_collection = db['users']
        print("MongoDB connected successfully.")
    except Exception as e:
        print(f"MongoDB connection error: {e}")
else:
    print("Warning: MONGODB_URI environment variable not set. Database logging is disabled.")

@app.route('/api/predict', methods=['POST'])
def predict_rank():
    if model is None:
        return jsonify({'error': 'Model not loaded properly.'}), 500

    data = request.get_json()
    
    if not data or 'met_score' not in data or 'board_percentage' not in data:
        return jsonify({'error': 'Invalid request. Please provide met_score and board_percentage.'}), 400
        
    name = data.get('name', 'Anonymous')
    email = data.get('email', 'No Email')

    try:
        met_score = float(data['met_score'])
        board_percentage = float(data['board_percentage'])
        
        # Validate inputs
        if not (0 <= met_score <= 240):
            return jsonify({'error': 'MET score must be between 0 and 240.'}), 400
        if not (0 <= board_percentage <= 100):
            return jsonify({'error': 'Board percentage must be between 0 and 100.'}), 400
            
        # Prepare feature vector
        features = np.array([[met_score, board_percentage]])
        
        # Predict
        predicted_rank = model.predict(features)[0]
        
        # Ensure rank is within realistic bounds (1 to 45000)
        predicted_rank = max(1, int(predicted_rank))
        predicted_rank = min(45000, predicted_rank)
        
        # Save to MongoDB
        if users_collection is not None:
            try:
                user_record = {
                    "name": name,
                    "email": email,
                    "met_score": met_score,
                    "board_percentage": board_percentage,
                    "predicted_rank": predicted_rank,
                    "created_at": datetime.utcnow()
                }
                users_collection.insert_one(user_record)
            except Exception as db_error:
                print(f"Database error: {db_error}")
                # We don't fail the prediction if DB fails, just log it.
        
        return jsonify({
            'predicted_rank': predicted_rank,
            'message': 'Prediction successful.'
        })
        
    except ValueError:
        return jsonify({'error': 'Invalid input types. Please provide numbers.'}), 400
    except Exception as e:
        return jsonify({'error': str(e)}), 500

# Vercel needs the app instance
if __name__ == '__main__':
    app.run(debug=True)
