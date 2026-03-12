import pandas as pd
from models.db import DatabaseConnection
import streamlit as st

def get_prediction_history():
    """
    Retrieve all prediction history from database
    
    Returns:
        pandas DataFrame with prediction history or empty DataFrame on error
    """
    try:
        db = DatabaseConnection()
        predictions = db.get_prediction_history()
        
        if predictions:
            # Convert list of dictionaries to DataFrame
            df = pd.DataFrame(predictions)
            return df
        else:
            return pd.DataFrame()
    except Exception as e:
        st.error(f"Error retrieving history: {e}")
        return pd.DataFrame()


def get_prediction_statistics():
    """
    Get summary statistics of predictions
    
    Returns:
        Dictionary with statistics
    """
    try:
        db = DatabaseConnection()
        predictions = db.get_prediction_history()
        
        if not predictions:
            return {
                "total_predictions": 0,
                "churn_count": 0,
                "stay_count": 0,
                "churn_rate": 0
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
        st.error(f"Error calculating statistics: {e}")
        return {
            "total_predictions": 0,
            "churn_count": 0,
            "stay_count": 0,
            "churn_rate": 0
        }