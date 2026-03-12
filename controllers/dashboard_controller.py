import pandas as pd
from models.db import DatabaseConnection
from models.prediction_model import PredictionModel
import streamlit as st

def get_kpi_metrics():
    """
    Retrieve KPI metrics from the database
    
    Returns:
        Dictionary with KPI data
    """
    try:
        db = DatabaseConnection()
        predictions = db.get_prediction_history()
        
        if not predictions:
            return {
                "total_predictions": 0,
                "churn_count": 0,
                "stay_count": 0,
                "churn_rate": 0.0
            }
        
        df = pd.DataFrame(predictions)
        total = len(df)
        churn = len(df[df['prediction'] == 'CHURN'])
        stay = len(df[df['prediction'] == 'STAY'])
        churn_rate = (churn / total * 100) if total > 0 else 0
        
        return {
            "total_predictions": total,
            "churn_count": churn,
            "stay_count": stay,
            "churn_rate": round(churn_rate, 2)
        }
    except Exception as e:
        st.error(f"Error retrieving KPI metrics: {e}")
        return {
            "total_predictions": 0,
            "churn_count": 0,
            "stay_count": 0,
            "churn_rate": 0.0
        }


def get_churn_distribution():
    """
    Get churn vs stay distribution
    
    Returns:
        DataFrame with prediction counts
    """
    try:
        db = DatabaseConnection()
        predictions = db.get_prediction_history()
        
        if not predictions:
            return pd.DataFrame()
        
        df = pd.DataFrame(predictions)
        distribution = df['prediction'].value_counts().reset_index()
        distribution.columns = ['Prediction', 'Count']
        return distribution
    except Exception as e:
        st.error(f"Error retrieving churn distribution: {e}")
        return pd.DataFrame()


def get_age_distribution():
    """
    Get age distribution of customers
    
    Returns:
        DataFrame with age data
    """
    try:
        db = DatabaseConnection()
        predictions = db.get_prediction_history()
        
        if not predictions:
            return pd.DataFrame()
        
        df = pd.DataFrame(predictions)
        return df[['age']].dropna()
    except Exception as e:
        st.error(f"Error retrieving age distribution: {e}")
        return pd.DataFrame()


def get_high_risk_customers():
    """
    Get customers predicted as CHURN (high risk)
    
    Returns:
        DataFrame with high-risk customers
    """
    try:
        db = DatabaseConnection()
        predictions = db.get_prediction_history()
        
        if not predictions:
            return pd.DataFrame()
        
        df = pd.DataFrame(predictions)
        
        # Filter for CHURN predictions
        churn_df = df[df['prediction'] == 'CHURN'].copy()
        
        # Select relevant columns
        columns_to_display = [
            'id', 'age', 'balance', 'num_products', 'salary', 
            'credit_score', 'tenure', 'prediction', 'prediction_date'
        ]
        
        # Select only existing columns
        existing_cols = [col for col in columns_to_display if col in churn_df.columns]
        churn_df = churn_df[existing_cols]
        
        # Sort by prediction date (most recent first)
        if 'prediction_date' in churn_df.columns:
            churn_df = churn_df.sort_values('prediction_date', ascending=False)
        
        return churn_df
    except Exception as e:
        st.error(f"Error retrieving high-risk customers: {e}")
        return pd.DataFrame()


def get_feature_importance():
    """
    Extract feature importance from the trained model
    
    Returns:
        DataFrame with feature names and importance scores
    """
    try:
        predictor = PredictionModel()
        
        if predictor.model is None:
            return pd.DataFrame()
        
        # Extract coefficients from Logistic Regression
        feature_names = [
            'Credit Score',
            'Age',
            'Tenure',
            'Balance',
            'Num of Products',
            'Has Credit Card',
            'Is Active Member',
            'Estimated Salary',
            'Geography: Germany',
            'Geography: Spain',
            'Gender: Male'
        ]
        
        # Get coefficients (absolute values for importance)
        coefficients = predictor.model.coef_[0]
        importance_scores = abs(coefficients)
        
        # Create DataFrame
        importance_df = pd.DataFrame({
            'Feature': feature_names,
            'Importance': importance_scores
        })
        
        # Sort by importance
        importance_df = importance_df.sort_values('Importance', ascending=True)
        
        return importance_df
    except Exception as e:
        st.error(f"Error retrieving feature importance: {e}")
        return pd.DataFrame()


def classify_risk_level(probability):
    """
    Classify customer risk level based on churn probability
    
    Args:
        probability: Churn probability (0-1)
    
    Returns:
        Tuple of (risk_level, color)
    """
    if probability < 0.30:
        return "LOW RISK", "🟢"
    elif probability < 0.60:
        return "MEDIUM RISK", "🟡"
    else:
        return "HIGH RISK", "🔴"


def get_risk_level_summary():
    """
    Get count of customers by risk level
    
    Returns:
        Dictionary with risk level counts
    """
    try:
        predictor = PredictionModel()
        db = DatabaseConnection()
        predictions = db.get_prediction_history()
        
        if not predictions or predictor.model is None:
            return {
                "low_risk": 0,
                "medium_risk": 0,
                "high_risk": 0
            }
        
        df = pd.DataFrame(predictions)
        
        # Calculate probability for each prediction
        low_count = 0
        medium_count = 0
        high_count = 0
        
        for _, row in df.iterrows():
            # Reconstruct feature vector
            features = {
                'CreditScore': row.get('credit_score', 0),
                'Age': row.get('age', 0),
                'Tenure': row.get('tenure', 0),
                'Balance': row.get('balance', 0),
                'NumOfProducts': row.get('num_products', 0),
                'HasCrCard': row.get('has_card', 0),
                'IsActiveMember': row.get('active_member', 0),
                'EstimatedSalary': row.get('salary', 0),
                'Geography_Germany': row.get('geography_germany', 0),
                'Geography_Spain': row.get('geography_spain', 0),
                'Gender_Male': row.get('gender_male', 0)
            }
            
            prediction, prob, _ = predictor.predict(features)
            
            if prob is not None:
                # Calculate actual churn probability (0-1)
                # If prediction == 0 (STAY), prob is P(STAY), so churn_prob = 1 - prob
                # If prediction == 1 (CHURN), prob is P(CHURN), so churn_prob = prob
                if prediction == 0:
                    churn_prob = 1 - prob
                else:
                    churn_prob = prob
                
                # Classify risk level based on churn probability
                if churn_prob < 0.30:
                    low_count += 1
                elif churn_prob < 0.60:
                    medium_count += 1
                else:
                    high_count += 1
        
        return {
            "low_risk": low_count,
            "medium_risk": medium_count,
            "high_risk": high_count
        }
    except Exception as e:
        st.error(f"Error calculating risk levels: {e}")
        return {
            "low_risk": 0,
            "medium_risk": 0,
            "high_risk": 0
        }
