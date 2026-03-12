import streamlit as st
import pandas as pd
from controllers.history_controller import get_prediction_history, get_prediction_statistics

def show_history_page():
    """Display prediction history and analytics"""
    
    st.title(" Prediction History & Analytics")
    st.write("View all customer predictions and analytics.")
    
    # Get prediction data
    df = get_prediction_history()
    stats = get_prediction_statistics()
    
    # Display statistics
    st.subheader(" Summary Statistics")
    
    stat_col1, stat_col2, stat_col3, stat_col4 = st.columns(4)
    
    with stat_col1:
        st.metric("Total Predictions", int(stats['total_predictions']))
    
    with stat_col2:
        st.metric("Churn Count", int(stats['churn_count']))
    
    with stat_col3:
        st.metric("Stay Count", int(stats['stay_count']))
    
    with stat_col4:
        st.metric("Churn Rate", f"{stats['churn_rate']}%")
    
    st.markdown("---")
    
    # Display prediction history table
    if not df.empty:
        st.subheader("Detailed Prediction Records")
        
        # Format dataframe for display
        df_display = df.copy()
        
        # Reorder columns for better readability
        column_order = [
            'id', 'prediction_date', 'credit_score', 'age', 'tenure', 
            'balance', 'num_products', 'has_card', 'active_member', 
            'salary', 'geography_germany', 'geography_spain', 'gender_male', 'prediction'
        ]
        
        # Select only existing columns
        existing_columns = [col for col in column_order if col in df_display.columns]
        df_display = df_display[existing_columns]
        
        # Rename columns for better readability
        df_display.columns = [
            'ID', 'Date', 'Credit Score', 'Age', 'Tenure (yrs)', 
            'Balance ($)', 'Products', 'Has Card', 'Active Member',
            'Salary ($)', 'Germany', 'Spain', 'Male', 'Prediction'
        ]
        
        # Display the dataframe
        st.dataframe(df_display, width='stretch', hide_index=True)
        
        # Export functionality
        st.subheader("")
        csv = df_display.to_csv(index=False)
        st.download_button(
            label=" Download CSV",
            data=csv,
            file_name="prediction_history.csv",
            mime="text/csv"
        )
        
    
        st.subheader(" Filter Records")
        filter_option = st.selectbox(
            "Filter by Prediction",
            options=["All", "CHURN", "STAY"],
            key="filter_prediction"
        )
        
        if filter_option != "All":
            filtered_df = df_display[df_display['Prediction'] == filter_option]
            st.write(f"**Showing {len(filtered_df)} records**")
            st.dataframe(filtered_df, width='stretch', hide_index=True)
    else:
        st.info(" No prediction history available yet. Make a prediction on the Prediction page to get started!")