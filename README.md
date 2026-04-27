# 🎓 MIT Rank & Branch Predictor

> Predict your Manipal Entrance Test (MET) rank and eligible branches across Manipal, Bengaluru & Jaipur campuses — powered by a machine-learning model trained on 10 years of historical cutoff data.

[![Live Demo](https://img.shields.io/badge/🚀%20Live%20Demo-rank--predictor--nu.vercel.app-blue?style=for-the-badge)](https://rank-predictor-nu.vercel.app)
[![GitHub](https://img.shields.io/badge/GitHub-kausshikaagrawal%2Frank__predictor-181717?style=for-the-badge&logo=github)](https://github.com/kausshikaagrawal/rank_predictor)

---

## 🔗 Live Link

**[https://rank-predictor-nu.vercel.app](https://rank-predictor-nu.vercel.app)**

---

## ✨ Features

- 🤖 **ML-Powered Prediction** — XGBoost model (converted to pure Python) trained on real MET cutoff data
- 📊 **Branch Eligibility** — Shows eligible branches across all 3 Manipal campuses (Manipal, Bengaluru, Jaipur)
- 🎨 **Glassmorphism UI** — Modern dark-mode design with animated background blobs
- 💾 **MongoDB Logging** — Stores user predictions for analytics
- ⚡ **Serverless API** — Flask API deployed as a Vercel serverless function

---

## 🛠️ Tech Stack

| Layer | Technology |
|-------|-----------|
| Frontend | HTML, CSS (Glassmorphism), Vanilla JS |
| Backend | Python (Flask) |
| ML Model | XGBoost → Pure Python Decision Tree |
| Database | MongoDB Atlas |
| Hosting | Vercel (Serverless) |

---

## 📁 Project Structure

```
manipal-rank-predictor/
├── index.html          # Main UI
├── style.css           # Glassmorphism styling
├── script.js           # Frontend logic & API calls
├── data.json           # Historical cutoff data (10 years)
├── vercel.json         # Vercel routing config
└── api/
    ├── predict.py      # Flask serverless function
    ├── model_logic.py  # Pure Python XGBoost decision tree
    └── requirements.txt
```

---

## 🚀 Local Development

```bash
# Clone the repo
git clone https://github.com/kausshikaagrawal/rank_predictor.git
cd rank_predictor

# Install Python dependencies
pip install -r api/requirements.txt

# Set environment variable
echo "MONGODB_URI=your_mongo_uri" > .env

# Run Flask API
python api/predict.py

# Open index.html in browser (or use Live Server)
```

---

## 📈 How It Works

1. User enters their **MET Score** (out of 240) and **12th Board %**
2. The frontend calls `/api/predict` (Flask serverless function)
3. The ML model returns an **estimated rank**
4. The app filters `data.json` to show all **eligible branches** with closing ranks

---

*Built with ❤️ for MET aspirants. Data based on publicly available historical cutoffs.*
