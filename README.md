# Bank Customer Churn Prediction System

A comprehensive machine learning web application that predicts customer churn for banks, helping analysts identify at-risk customers and take proactive retention actions.

## 🎯 Project Overview

This system uses a trained **Logistic Regression model** to predict which customers are likely to leave the bank. It provides:
- **Real-time predictions** with confidence scores
- **Interactive analytics dashboard** with visualizations
- **Prediction history** stored in MySQL
- **Feature importance analysis** for model interpretability
- **Risk classification** (Low/Medium/High) for customers

## 🏗️ Architecture

The project follows **MVC (Model-View-Controller)** architecture:

```
project_root/
├── app.py                          # Main Streamlit application
├── requirements.txt                # Python dependencies
│
├── models/
│   ├── db.py                      # MySQL database connection
│   └── prediction_model.py         # ML model loader and predictor
│
├── controllers/
│   ├── prediction_controller.py    # Prediction logic
│   ├── history_controller.py       # History retrieval
│   └── dashboard_controller.py     # Dashboard analytics
│
├── views/
│   ├── predict_view.py            # Prediction interface
│   ├── history_view.py            # History & analytics page
│   └── dashboard_view.py          # Comprehensive dashboard
│
└── trained_model/
    ├── refined_logistic_model.pkl # Trained ML model
    └── scaler.pkl                 # Feature preprocessor
```

## 📋 Features

### 1. **Prediction Page** 🔮
- Input customer attributes (age, credit score, balance, tenure, etc.)
- Generate churn predictions with probability scores
- Automatic database storage of predictions
- Customer profile summary

### 2. **Prediction History** 📈
- View all stored predictions
- Filter by prediction type (CHURN/STAY)
- Export data to CSV
- Summary statistics

### 3. **Analytics Dashboard** 📊
- **KPI Metrics**: Total predictions, churn count, churn rate
- **Risk Classification**: Low/Medium/High risk breakdown
- **Churn Distribution Chart**: Visual comparison of outcomes
- **Age Distribution**: Histogram of customer ages
- **Feature Importance**: Top factors influencing churn
- **High-Risk Customers Table**: Detailed view of at-risk clients
- **Insights & Recommendations**: Actionable business intelligence

## 🚀 Quick Start

### Prerequisites
- Python 3.13+
- MySQL Server
- Git

### Installation

1. **Clone the repository**
```bash
git clone https://github.com/yourusername/bank-churn-prediction.git
cd bank-churn-prediction
```

2. **Create virtual environment**
```bash
python -m venv venv
venv\Scripts\activate
```

3. **Install dependencies**
```bash
pip install -r requirements.txt
```

4. **Update database credentials** (in `models/db.py`)
```python
database = churn_system
user = root
password = (your_password)
```

5. **Run the application**
```bash
python -m streamlit run app.py
```

The app will launch at `http://localhost:8501`

## 📊 Model Information

- **Algorithm**: Logistic Regression
- **Features Used**: 11 customer attributes
  - Credit Score
  - Age
  - Tenure
  - Balance
  - Number of Products
  - Has Credit Card
  - Is Active Member
  - Estimated Salary
  - Geography (Germany, Spain)
  - Gender (Male)

- **Output**: Binary classification (CHURN / STAY)
- **Probability**: Confidence score for predictions

## 🗄️ Database Schema

**Table: predictions**
```sql
- id (INT, Primary Key, Auto Increment)
- credit_score (INT)
- age (INT)
- tenure (INT)
- balance (FLOAT)
- num_products (INT)
- has_card (INT)
- active_member (INT)
- salary (FLOAT)
- geography_germany (INT)
- geography_spain (INT)
- gender_male (INT)
- prediction (VARCHAR)
- prediction_date (TIMESTAMP)
```

## 🔍 Example Inputs

### Customer Predicted to CHURN (High Risk)
```
Credit Score: 500
Age: 45
Tenure: 2 years
Balance: $5,000
Products: 1
Has Card: No
Active: No
Salary: $120,000
Country: Germany
Gender: Female
```

### Customer Predicted to STAY (Low Risk)
```
Credit Score: 750
Age: 35
Tenure: 8 years
Balance: $150,000
Products: 3
Has Card: Yes
Active: Yes
Salary: $95,000
Country: France
Gender: Male
```

## 📱 Navigation

The application offers easy navigation through:
- **📊 Dashboard** - Comprehensive analytics and insights
- **🔮 Predict Churn** - Make new predictions
- **📈 Prediction History** - View and analyze past predictions

## 🛠️ Tech Stack

- **Frontend**: Streamlit
- **Backend**: Python
- **Database**: MySQL
- **ML Framework**: scikit-learn
- **Data Processing**: pandas, numpy

## 📝 Project Dependencies

See `requirements.txt` for complete list:
- streamlit
- pandas
- scikit-learn
- mysql-connector-python
- joblib
- matplotlib

## 🤝 Contributing

Contributions are welcome! Please feel free to submit pull requests or open issues for bugs and feature requests.

## 📄 License

This project is licensed under the MIT License - see LICENSE file for details.

## 👤 Author

Created for Bank Customer Churn Prediction Project (IT20)

## 📧 Support

For questions or issues, please contact the project maintainer or open an issue on GitHub.

---

**Last Updated**: March 12, 2026
