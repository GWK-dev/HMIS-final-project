import streamlit as st
import requests
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go

# Page config
st.set_page_config(
    page_title="Kiambu Hospital Management",
    page_icon="🏥",
    layout="wide"
)

# API base URL
API_BASE = "http://localhost:8000"

st.title("🏥 Intelligent Hospital Management System")
st.subheader("Based on Kiambu Level 5 Hospital Research - Addressing Low Clinical Attendance")

# Sidebar
st.sidebar.title("Navigation")
page = st.sidebar.selectbox("Choose a page", ["Dashboard", "Patient Management", "Predictions", "Research Insights"])

if page == "Dashboard":
    st.header("Hospital Analytics Dashboard")
    
    try:
        response = requests.get(f"{API_BASE}/analytics/dashboard")
        if response.status_code == 200:
            data = response.json()
            
            # Key metrics
            col1, col2, col3, col4 = st.columns(4)
            
            with col1:
                st.metric("Total Patients", data.get('total_patients', 0))
            with col2:
                st.metric("High Risk Patients", data.get('high_risk_patients', 0))
            with col3:
                st.metric("High Risk %", f"{data.get('high_risk_percentage', 0):.1f}%")
            with col4:
                avg_sat = data.get('average_satisfaction_scores', {})
                overall_avg = sum(avg_sat.values()) / len(avg_sat) if avg_sat else 0
                st.metric("Avg Satisfaction", f"{overall_avg:.1f}%")
            
            # Satisfaction scores chart
            st.subheader("Patient Satisfaction Scores")
            if data.get('average_satisfaction_scores'):
                sat_data = data['average_satisfaction_scores']
                fig = px.bar(
                    x=list(sat_data.keys()),
                    y=list(sat_data.values()),
                    title="Average Satisfaction Scores by Dimension",
                    labels={'x': 'Satisfaction Dimension', 'y': 'Score (%)'}
                )
                st.plotly_chart(fig)
            
            # Research insights
            st.subheader("Key Research Insights from Kiambu Study")
            insights = data.get('research_based_insights', {})
            for insight, value in insights.items():
                st.info(f"**{insight.replace('_', ' ').title()}**: {value}")
                
        else:
            st.error("Could not fetch dashboard data")
    except:
        st.warning("Backend server not running. Start the backend with: uvicorn backend.app:app --reload")

elif page == "Patient Management":
    st.header("Patient Management")
    
    # Add new patient form
    with st.form("add_patient"):
        st.subheader("Add New Patient")
        
        col1, col2 = st.columns(2)
        
        with col1:
            age_group = st.selectbox("Age Group", ["18-27", "28-37", "38-47", "48+"])
            gender = st.selectbox("Gender", ["Male", "Female"])
            education = st.selectbox("Education Level", ["Primary", "Secondary", "University"])
        
        with col2:
            income_level = st.selectbox("Income Level", ["<11,000", "11,000-20,999", "21,000-30,999", "31,000-40,999", "41,000+"])
            location = st.selectbox("Location", ["Kiambu Town", "Limuru", "Kirigiti", "Thendigua", "Githiga", "Runda", "Other"])
        
        st.subheader("Satisfaction Scores (Based on Research Survey)")
        physical_env = st.slider("Physical Environment Satisfaction", 0, 100, 62)
        technical_quality = st.slider("Technical Quality Satisfaction", 0, 100, 65)
        interpersonal = st.slider("Interpersonal Relations Satisfaction", 0, 100, 82)
        communication = st.slider("Communication Satisfaction", 0, 100, 62)
        accessibility = st.slider("Accessibility Satisfaction", 0, 100, 61)
        
        submitted = st.form_submit_button("Add Patient")
        
        if submitted:
            patient_data = {
                "age_group": age_group,
                "gender": gender,
                "education": education,
                "income_level": income_level,
                "location": location,
                "physical_env_score": physical_env,
                "technical_quality_score": technical_quality,
                "interpersonal_score": interpersonal,
                "communication_score": communication,
                "accessibility_score": accessibility
            }
            
            try:
                response = requests.post(f"{API_BASE}/patients/", json=patient_data)
                if response.status_code == 200:
                    patient = response.json()
                    st.success(f"Patient added successfully! No-Show Probability: {patient['no_show_probability']:.1%}")
                else:
                    st.error("Failed to add patient")
            except:
                st.error("Backend server not running")

elif page == "Predictions":
    st.header("No-Show Prediction System")
    
    st.info("""
    This AI model predicts patient no-show probability based on research findings from Kiambu Level 5 Hospital:
    - **Age 48+**: 48% of respondents (higher risk)
    - **Female**: 73% of survey participants  
    - **Education**: Affects health literacy and attendance
    - **Satisfaction Scores**: Key factors from your research
    """)
    
    # Prediction form
    with st.form("prediction_form"):
        col1, col2 = st.columns(2)
        
        with col1:
            age_group = st.selectbox("Patient Age Group", ["18-27", "28-37", "38-47", "48+"], key="pred_age")
            gender = st.selectbox("Gender", ["Male", "Female"], key="pred_gender")
            education = st.selectbox("Education Level", ["Primary", "Secondary", "University"], key="pred_edu")
        
        with col2:
            physical_env = st.slider("Physical Env. Satisfaction", 0, 100, 62, key="pred_phys")
            technical_quality = st.slider("Technical Quality", 0, 100, 65, key="pred_tech")
            accessibility = st.slider("Accessibility", 0, 100, 61, key="pred_acc")
        
        predict_btn = st.form_submit_button("Predict No-Show Risk")
        
        if predict_btn:
            patient_data = {
                "age_group": age_group,
                "gender": gender, 
                "education": education,
                "income_level": "<11,000",
                "location": "Kiambu Town",
                "physical_env_score": physical_env,
                "technical_quality_score": technical_quality,
                "interpersonal_score": 82,
                "communication_score": 62,
                "accessibility_score": accessibility
            }
            
            try:
                response = requests.post(f"{API_BASE}/predict-no-show/", json={"patient_data": patient_data})
                if response.status_code == 200:
                    prediction = response.json()
                    
                    # Display results
                    st.subheader("Prediction Results")
                    
                    col1, col2 = st.columns(2)
                    
                    with col1:
                        risk_color = "red" if prediction["risk_level"] == "High" else "orange" if prediction["risk_level"] == "Medium" else "green"
                        st.metric("No-Show Probability", f"{prediction['no_show_probability']:.1%}")
                        st.metric("Risk Level", prediction["risk_level"])
                    
                    with col2:
                        st.subheader("Recommended Actions")
                        for action in prediction["recommended_actions"]:
                            st.write(f"• {action}")
                    
                    # Risk gauge chart
                    fig = go.Figure(go.Indicator(
                        mode = "gauge+number+delta",
                        value = prediction['no_show_probability'] * 100,
                        domain = {'x': [0, 1], 'y': [0, 1]},
                        title = {'text': "No-Show Risk Score"},
                        gauge = {
                            'axis': {'range': [None, 100]},
                            'bar': {'color': risk_color},
                            'steps': [
                                {'range': [0, 40], 'color': "lightgreen"},
                                {'range': [40, 70], 'color': "yellow"},
                                {'range': [70, 100], 'color': "red"}
                            ]
                        }
                    ))
                    st.plotly_chart(fig)
                    
                else:
                    st.error("Prediction failed")
            except:
                st.error("Backend server not running")

elif page == "Research Insights":
    st.header("Research Insights from Kiambu Level 5 Hospital Study")
    
    st.subheader("Key Findings from Your Research")
    
    findings = [
        "**Overcrowding**: 89.9% of patients reported clinic overcrowding",
        "**Toilet Cleanliness**: 60.7% dissatisfied with toilet facilities", 
        "**Staff Attitude**: 81.9% satisfied with interpersonal relations",
        "**Communication**: 62.0% satisfied with communication quality",
        "**Accessibility**: 61.4% satisfied with access to care",
        "**Demographics**: 48% of patients aged 48+, 73% female",
        "**Education**: 48% secondary education, 34% primary education"
    ]
    
    for finding in findings:
        st.write(f"• {finding}")
    
    # Satisfaction comparison chart
    st.subheader("Satisfaction Scores Comparison")
    
    research_scores = {
        'Dimension': ['Physical Environment', 'Technical Quality', 'Interpersonal Relations', 'Communication', 'Accessibility'],
        'Research Score': [61.8, 64.8, 81.9, 62.0, 61.4],
        'Industry Benchmark': [75.0, 78.0, 82.0, 75.0, 72.0]
    }
    
    df = pd.DataFrame(research_scores)
    fig = px.bar(df, x='Dimension', y=['Research Score', 'Industry Benchmark'], 
                 title="Patient Satisfaction: Research Findings vs Benchmarks",
                 barmode='group')
    st.plotly_chart(fig)
    
    st.subheader("AI Solution Impact")
    st.success("""
    This system addresses key research findings:
    - **Digital Records**: Solves manual file system issues
    - **Predictive Scheduling**: Reduces 89.9% overcrowding problem  
    - **Smart Reminders**: Improves attendance using patient risk profiles
    - **Resource Optimization**: Better staff and facility utilization
    """)

# Footer
st.markdown("---")
st.markdown("**AI for Software Engineering Final Project** • Based on Kiambu Level 5 Hospital Clinical Attendance Research")