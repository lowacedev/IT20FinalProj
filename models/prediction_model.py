import joblib
import pandas as pd
import streamlit as st
import os

class PredictionModel:
    def __init__(self, model_path="trained_model/refined_logistic_model.pkl", scaler_path="trained_model/scaler.pkl"):
        self.model_path = model_path
        self.scaler_path = scaler_path
        self.model = None
        self.scaler = None
        self.load_model()

    def load_model(self):
        """Load trained model and scaler"""
        try:
            if os.path.exists(self.model_path) and os.path.exists(self.scaler_path):
                self.model = joblib.load(self.model_path)
                self.scaler = joblib.load(self.scaler_path)
            else:
                st.error(f"Model files not found. Please ensure '{self.model_path}' and '{self.scaler_path}' exist.")
        except Exception as e:
            st.error(f"Error loading model: {e}")

    def predict(self, features_dict):
        """
        Make prediction using the trained model
        
        Args:
            features_dict: Dictionary with all 11 features
        
        Returns:
            Tuple of (prediction, probability, status_text)
        """
        if self.model is None or self.scaler is None:
            return None, None, "Model not loaded"
        
        try:
            # Create DataFrame from features
            df = pd.DataFrame([features_dict])
            
            # Scale features
            df_scaled = self.scaler.transform(df)
            
            # Get prediction
            prediction = self.model.predict(df_scaled)[0]
            
            # Get prediction probability
            probability = self.model.predict_proba(df_scaled)[0]
            
            # Determine status text
            if prediction == 1:
                status_text = "Customer will CHURN"
                churn_prob = probability[1]
            else:
                status_text = "Customer will STAY"
                churn_prob = probability[0]
            
            return prediction, churn_prob, status_text
        except Exception as e:
            st.error(f"Error making prediction: {e}")
            return None, None, f"Error: {str(e)}"