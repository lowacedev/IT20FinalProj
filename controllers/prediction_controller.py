from models.prediction_model import PredictionModel
from models.db import DatabaseConnection
import streamlit as st

def make_prediction(customer_data):
    """
    Process customer data and make churn prediction
    
    Args:
        customer_data: Dictionary with all customer features
    
    Returns:
        Tuple of (prediction, probability, status_text)
    """
    # Initialize prediction model
    predictor = PredictionModel()
    
    # Get prediction from model
    prediction, probability, status_text = predictor.predict(customer_data)
    
    if prediction is None:
        return None, None, status_text
    
    return prediction, probability, status_text


def save_prediction(customer_data, prediction, status_text):
    """
    Save prediction to database
    
    Args:
        customer_data: Dictionary with customer features
        prediction: Binary prediction (0 or 1)
        status_text: Human-readable prediction text
    
    Returns:
        Boolean indicating success
    """
    try:
        # Prepare data for database insertion
        insert_data = (
            customer_data.get("CreditScore"),
            customer_data.get("Age"),
            customer_data.get("Tenure"),
            customer_data.get("Balance"),
            customer_data.get("NumOfProducts"),
            customer_data.get("HasCrCard"),
            customer_data.get("IsActiveMember"),
            customer_data.get("EstimatedSalary"),
            customer_data.get("Geography_Germany", 0),
            customer_data.get("Geography_Spain", 0),
            customer_data.get("Gender_Male", 0),
            "CHURN" if prediction == 1 else "STAY"
        )
        
        # Connect and insert to database
        db = DatabaseConnection()
        db.create_database()
        db.create_table()
        success = db.insert_prediction(insert_data)
        
        return success
    except Exception as e:
        st.error(f"Error saving prediction: {e}")
        return False

    return result