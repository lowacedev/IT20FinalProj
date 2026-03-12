import streamlit as st
import pandas as pd
from controllers.dashboard_controller import (
    get_kpi_metrics, 
    get_churn_distribution,
    get_age_distribution,
    get_high_risk_customers,
    get_feature_importance,
    classify_risk_level,
    get_risk_level_summary
)

def show_dashboard_page():
    """Display the comprehensive analytics dashboard"""
    
    st.title(" Churn Analytics Dashboard")
    st.write("Comprehensive analysis of customer churn predictions and model insights.")
    st.markdown("---")
    
    # ===== SECTION 1: KPI METRICS =====
    st.subheader(" Key Performance Indicators")
    
    metrics = get_kpi_metrics()
    
    kpi_col1, kpi_col2, kpi_col3, kpi_col4 = st.columns(4)
    
    with kpi_col1:
        st.metric(
            label="Total Predictions",
            value=int(metrics['total_predictions']),
            delta=None
        )
    
    with kpi_col2:
        st.metric(
            label="Customers Churned",
            value=int(metrics['churn_count']),
            delta="At Risk"
        )
    
    with kpi_col3:
        st.metric(
            label="Customers Retained",
            value=int(metrics['stay_count']),
            delta="Stable"
        )
    
    with kpi_col4:
        st.metric(
            label="Churn Rate",
            value=f"{metrics['churn_rate']}%",
            delta=None
        )
    
    st.markdown("---")
    
    # ===== SECTION 2: RISK LEVEL SUMMARY =====
    st.subheader(" Customer Risk Classification")
    
    risk_summary = get_risk_level_summary()
    
    risk_col1, risk_col2, risk_col3 = st.columns(3)
    
    with risk_col1:
        st.metric(
            label="🟢 Low Risk",
            value=int(risk_summary['low_risk']),
            help="Probability < 30%"
        )
    
    with risk_col2:
        st.metric(
            label="🟡 Medium Risk",
            value=int(risk_summary['medium_risk']),
            help="Probability 30-60%"
        )
    
    with risk_col3:
        st.metric(
            label="🔴 High Risk",
            value=int(risk_summary['high_risk']),
            help="Probability > 60%"
        )
    
    st.markdown("---")
    
    # ===== SECTION 3: CHURN DISTRIBUTION CHART =====
    st.subheader(" Churn Distribution")
    
    churn_dist = get_churn_distribution()
    
    if not churn_dist.empty:
        # Set prediction as index for bar chart
        chart_data = churn_dist.set_index('Prediction')
        st.bar_chart(chart_data)
    else:
        st.info("No prediction data available yet.")
    
    # ===== SECTION 4: AGE DISTRIBUTION =====
    st.subheader(" Customer Age Distribution")
    
    age_data = get_age_distribution()
    
    if not age_data.empty:
        # Create age histogram using numpy
        age_counts, age_bins = pd.cut(age_data['age'], bins=20, retbins=True)
        
        # Count occurrences in each bin
        bin_counts = age_counts.value_counts().sort_index()
        
        # Create DataFrame for display
        age_hist_df = pd.DataFrame({
            'Count': bin_counts.values
        }, index=[f"{int(interval.left)}-{int(interval.right)}" for interval in bin_counts.index])
        
        # Display histogram using bar chart
        st.bar_chart(age_hist_df)
        
        # Show statistics
        stats_col1, stats_col2, stats_col3 = st.columns(3)
        with stats_col1:
            st.metric("Mean Age", f"{age_data['age'].mean():.1f} years")
        with stats_col2:
            st.metric("Median Age", f"{age_data['age'].median():.1f} years")
        with stats_col3:
            st.metric("Age Range", f"{int(age_data['age'].min())}-{int(age_data['age'].max())} years")
    else:
        st.info("No age data available yet.")
    
    st.markdown("---")
    
    # ===== SECTION 5: FEATURE IMPORTANCE =====
    st.subheader("🔍 Feature Importance Analysis")
    
    feature_importance = get_feature_importance()
    
    if not feature_importance.empty:
        # Sort by importance for better visualization
        feature_importance_sorted = feature_importance.sort_values('Importance', ascending=False)
        chart_data = feature_importance_sorted.set_index('Feature')
        st.bar_chart(chart_data)
        
        # Show feature importance details
        with st.expander(" Feature Importance Details"):
            importance_display = feature_importance.copy()
            importance_display['Importance'] = importance_display['Importance'].round(4)
            importance_display = importance_display.sort_values('Importance', ascending=False)
            st.dataframe(importance_display, width='stretch', hide_index=True)
    else:
        st.info("Model features not available yet.")
    
    st.markdown("---")
    
    # ===== SECTION 6: HIGH-RISK CUSTOMERS TABLE =====
    st.subheader(" High-Risk Customers (Predicted Churn)")
    
    high_risk = get_high_risk_customers()
    
    if not high_risk.empty:
        st.write(f"**Total High-Risk Customers: {len(high_risk)}**")
        
        # Format the dataframe for display
        display_df = high_risk.copy()
        
        # Rename columns for readability
        column_mapping = {
            'id': 'ID',
            'age': 'Age',
            'balance': 'Balance ($)',
            'num_products': 'Products',
            'salary': 'Salary ($)',
            'credit_score': 'Credit Score',
            'tenure': 'Tenure (yrs)',
            'prediction': 'Prediction',
            'prediction_date': 'Date'
        }
        
        display_df = display_df.rename(columns=column_mapping)
        
        # Format numeric columns
        if 'Balance ($)' in display_df.columns:
            display_df['Balance ($)'] = display_df['Balance ($)'].apply(lambda x: f"${x:,.2f}" if pd.notna(x) else "N/A")
        if 'Salary ($)' in display_df.columns:
            display_df['Salary ($)'] = display_df['Salary ($)'].apply(lambda x: f"${x:,.2f}" if pd.notna(x) else "N/A")
        
        st.dataframe(display_df, width='stretch', hide_index=True)
        
        # Export option
        csv = display_df.to_csv(index=False)
        st.download_button(
            label="📥 Download High-Risk Customers (CSV)",
            data=csv,
            file_name="high_risk_customers.csv",
            mime="text/csv"
        )
    else:
        st.info(" No customers predicted to churn at this time.")
    
    st.markdown("---")
    
    # ===== SECTION 7: INSIGHTS & RECOMMENDATIONS =====
    st.subheader("💡 Key Insights & Recommendations")
    
    if not metrics['total_predictions'] == 0:
        col_insight1, col_insight2 = st.columns(2)
        
        with col_insight1:
            st.write("**Current Churn Risk Assessment:**")
            if metrics['churn_rate'] < 20:
                st.success(" Churn rate is LOW. Customer retention is strong.")
            elif metrics['churn_rate'] < 40:
                st.warning(" Moderate churn risk detected. Review customer engagement strategies.")
            else:
                st.error(" High churn rate. Immediate retention efforts recommended.")
        
        with col_insight2:
            st.write("**Recommended Actions:**")
            st.info(
                """
                - Focus on high-risk customers (>60% probability)
                - Analyze feature importance to understand key churn drivers
                - Develop targeted retention programs for at-risk segments
                - Monitor age and tenure groups with high churn
                """
            )
    else:
        st.info("Generate predictions to see insights and recommendations.")
