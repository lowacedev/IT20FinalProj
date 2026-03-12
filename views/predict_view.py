import streamlit as st
from controllers.prediction_controller import make_prediction, save_prediction

def show_predict_page():
    """Display prediction interface and handle prediction logic"""
    
    st.title(" Customer Churn Prediction")
    st.write("Enter customer information below to predict whether they are likely to churn.")
    
    # Create columns for better layout
    col1, col2 = st.columns(2)
    
    with col1:
        st.subheader("Financial Information")
        credit_score = st.number_input("Credit Score", min_value=300, max_value=900, value=650)
        balance = st.number_input("Account Balance ($)", min_value=0.0, value=50000.0)
        salary = st.number_input("Estimated Salary ($)", min_value=0.0, value=80000.0)
        num_products = st.slider("Number of Products", min_value=1, max_value=4, value=2)
    
    with col2:
        st.subheader("Customer Information")
        age = st.number_input("Age", min_value=18, max_value=100, value=40)
        tenure = st.slider("Years as Customer", min_value=0, max_value=10, value=5)
        has_credit_card = st.selectbox("Has Credit Card?", options=[("Yes", 1), ("No", 0)], format_func=lambda x: x[0])
        is_active_member = st.selectbox("Is Active Member?", options=[("Yes", 1), ("No", 0)], format_func=lambda x: x[0])
    
    col3, col4 = st.columns(2)
    
    with col3:
        st.subheader("Demographics")
        geography = st.selectbox("Country", options=["France", "Germany", "Spain"])
        gender = st.selectbox("Gender", options=["Male", "Female"])
    

    geography_germany = 1 if geography == "Germany" else 0
    geography_spain = 1 if geography == "Spain" else 0
    gender_male = 1 if gender == "Male" else 0
    

    customer_data = {
        "CreditScore": credit_score,
        "Age": age,
        "Tenure": tenure,
        "Balance": balance,
        "NumOfProducts": num_products,
        "HasCrCard": has_credit_card[1],
        "IsActiveMember": is_active_member[1],
        "EstimatedSalary": salary,
        "Geography_Germany": geography_germany,
        "Geography_Spain": geography_spain,
        "Gender_Male": gender_male
    }
    

    st.markdown("---")
    
    col_predict = st.columns([1, 1, 1])
    with col_predict[1]:
        predict_button = st.button(" Generate Prediction", use_container_width=True)
    
    if predict_button:

        prediction, probability, status_text = make_prediction(customer_data)
        
        if prediction is not None:
       
            save_prediction(customer_data, prediction, status_text)
        
            st.markdown("---")
            st.subheader(" Prediction Result")
            
            if prediction == 1:
                st.error(f" {status_text}")
                col_metric1, col_metric2 = st.columns(2)
                with col_metric1:
                    st.metric("Churn Risk", f"{probability*100:.1f}%")
                with col_metric2:
                    st.metric("Risk Level", "High")
            else:
                st.success(f" {status_text}")
                col_metric1, col_metric2 = st.columns(2)
                with col_metric1:
                    st.metric("Retention Probability", f"{probability*100:.1f}%")
                with col_metric2:
                    st.metric("Risk Level", "Low")
            
          
            with st.expander(" Customer Profile Summary"):
                profile_col1, profile_col2 = st.columns(2)
                with profile_col1:
                    st.write(f"**Age:** {age} years")
                    st.write(f"**Tenure:** {tenure} years")
                    st.write(f"**Credit Score:** {credit_score}")
                    st.write(f"**Products:** {num_products}")
                with profile_col2:
                    st.write(f"**Salary:** ${salary:,.2f}")
                    st.write(f"**Balance:** ${balance:,.2f}")
                    st.write(f"**Country:** {geography}")
                    st.write(f"**Gender:** {gender}")