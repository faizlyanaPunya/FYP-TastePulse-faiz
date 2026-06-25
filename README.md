# TastePulse 📊 
### Northern Malaysia Food Tourism Sentiment Analysis Dashboard

TastePulse is an AI-powered sentiment analysis dashboard designed for **Majlis Perbandaran Kubang Pasu (MPKP)** to monitor, analyze, and generate actionable insights from food tourism reviews in Northern Malaysia.

🔗 **Live Application:** [fyp-tastepulse-faiz.streamlit.app](https://fyp-tastepulse-faiz.streamlit.app/)

---

## 📋 Table of Contents
1. [How to Use the Dashboard](#-how-to-use-the-dashboard)
2. [Dataset Requirements](#-dataset-requirements)
3. [Features](#-features)
4. [Local Setup & Installation](#-local-setup--installation)

---

## 🚀 How to Use the Dashboard

To start exploring insights, follow these simple steps once you open the app:

1. **Upload the Dataset:**
   - Locate the sidebar on the left.
   - Click **Browse files** and upload your sentiment CSV file (see [Dataset Requirements](#-dataset-requirements) below).
2. **Select & Train Models:**
   - Choose which machine learning models you want to train (e.g., **Multinomial Naive Bayes** and/or **LSTM**).
   - Click the **"Train Models"** button.
   - Once training is complete, the dashboard will load the test data (20% split) for all insights.
3. **Explore Dashboard Tabs:**
   - **📊 Overview:** View general sentiment distribution, health scores, and metrics.
   - **📈 Time Series:** Track how sentiment evolves over time.
   - **☁️ Word Cloud:** Visualize the most common terms found in reviews.
   - **📱 Social & Influencers:** Analyze platform-specific reaches and top influencers.
   - **💡 Initiatives:** Check recommended municipal actions based on sentiment feedback.
   - **🗺️ Map Area:** View geographical sentiment distributions across Kubang Pasu.
   - **🤖 AI Insights:** Generate professional report cards, draft official advisory letters to restaurant owners, or chat with the AI Data Advisor (Powered by Google Gemini).

---

## csv Dataset Requirements

The dashboard expects a CSV file containing food reviews and sentiment scores. For the app to process the data successfully, your CSV file **must** include the following columns:

| Column Name | Description | Example Value |
| :--- | :--- | :--- |
| **`text`** | The raw text of the customer review | *"Sangat sedap dan berbaloi makan di sini!"* |
| **`sentiment`** | Classified sentiment (`positive`, `negative`, or `neutral`) | `positive` |
| **`sentiment score`** | Numerical sentiment score (typically 0.0 to 1.0 or -1.0 to 1.0) | `0.95` |
| **`place`** | The name of the food destination or restaurant | `Nasi Kandar Yasmeen` |
| **`bigrams`** | Comma-separated top keyword bigrams parsed from the review | `nasi kandar, ayam goreng` |
| **`date`** *(optional)* | The date of the review (for Time Series analytics) | `2026-06-25` |

> 💡 **Tip:** A sample dataset `Sentiment_Food_Data.csv` is provided in this repository to test the dashboard.

---

## 🛠️ Local Setup & Installation

If you wish to run this dashboard locally on your machine:

### Prerequisite
Ensure you have Python 3.11 or 3.12 installed.

### 1. Clone the Repository
```bash
git clone https://github.com/faizlyanaPunya/FYP-TastePulse-faiz.git
cd FYP-TastePulse-faiz
```

### 2. Install Dependencies
```bash
pip install -r requirements.txt
```

### 3. Set Up API Keys (Optional)
If you want to use the AI Insights tab locally:
1. Create a folder named `.streamlit` in the root directory.
2. Create a file inside it named `secrets.toml`.
3. Add your Gemini API key (get one for free from [Google AI Studio](https://aistudio.google.com)):
   ```toml
   GEMINI_API_KEY = "YOUR_GEMINI_API_KEY"
   ```

### 4. Run the App
```bash
python -m streamlit run dashboard.py
```
Your browser will open automatically at `http://localhost:8501`.
