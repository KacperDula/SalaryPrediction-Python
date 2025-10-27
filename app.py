# Professional Job Salary Predictor - Streamlit Web App
# Save this as: app.py

import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
from sklearn.ensemble import RandomForestRegressor
from sklearn.preprocessing import StandardScaler, OneHotEncoder
from sklearn.compose import ColumnTransformer
from sklearn.pipeline import Pipeline

# Configure Streamlit page
st.set_page_config(
    page_title="Job Salary Predictor",
    page_icon="📊",
    layout="wide",
    initial_sidebar_state="expanded"
)

# ---------------------- Styling ----------------------
st.markdown("""
<style>
/* Header */
.header {
    text-align: center;
    padding: 1.5rem;
    margin-bottom: 2rem;
}
.header h1 {
    font-size: 2.2rem;
    font-weight: 700;
    color: #1e3a8a;
    margin-bottom: 0.3rem;
}
.header p {
    font-size: 1rem;
    color: #555;
}

/* Button */
div.stButton > button:first-child {
    background: linear-gradient(90deg, #2563eb 0%, #1e40af 100%);
    color: white;
    border-radius: 8px;
    height: 3rem;
    font-weight: 600;
}

/* Result Card */
.result-card {
    text-align:center;
    padding:2rem;
    border-radius:12px;
    background:#f8fafc;
    border:1px solid #e2e8f0;
    margin-top:1rem;
}
.result-card h2 {
    color:#1e3a8a;
    margin:0;
    font-size:2rem;
}
.result-card p {
    margin:0.5rem 0 0;
    color:#64748b;
}
.result-card small {
    font-size:0.85rem;
    color:#94a3b8;
}
</style>
""", unsafe_allow_html=True)

# ---------------------- Model Class ----------------------
class SalaryPredictor:
    def __init__(self):
        self.model = None
        self.feature_columns = []
        self.skill_keywords = {
            'python': ['python', 'django', 'flask', 'pandas', 'numpy'],
            'sql': ['sql', 'mysql', 'postgresql', 'sqlite', 'database'],
            'javascript': ['javascript', 'react', 'angular', 'vue', 'node'],
            'cloud': ['aws', 'azure', 'gcp', 'cloud', 'kubernetes', 'docker'],
            'ml': ['machine learning', 'ml', 'ai', 'tensorflow', 'pytorch', 'scikit'],
            'data_viz': ['tableau', 'powerbi', 'matplotlib', 'plotly'],
            'big_data': ['spark', 'hadoop', 'kafka', 'mongodb'],
            'devops': ['devops', 'ci/cd', 'jenkins', 'git', 'linux']
        }
    
    def generate_training_data(self, n_samples=3000):
        np.random.seed(42)
        job_titles = [
            'Junior Data Scientist', 'Data Scientist', 'Senior Data Scientist', 'Lead Data Scientist',
            'Software Engineer', 'Senior Software Engineer', 'Staff Engineer',
            'Data Analyst', 'Senior Data Analyst', 'ML Engineer', 'Senior ML Engineer',
            'Product Manager', 'Senior Product Manager', 'DevOps Engineer', 'Senior DevOps Engineer'
        ]
        companies = [
            'Google', 'Microsoft', 'Amazon', 'Meta', 'Apple', 'Netflix', 'Startup Inc', 'TechCorp'
        ]
        locations = [
            'San Francisco, CA', 'New York, NY', 'Seattle, WA', 'Austin, TX',
            'Boston, MA', 'Chicago, IL', 'Los Angeles, CA', 'Remote'
        ]
        data = []
        for _ in range(n_samples):
            job_title = np.random.choice(job_titles)
            company = np.random.choice(companies)
            location = np.random.choice(locations)
            
            # Base salary
            if 'Junior' in job_title:
                base_salary = np.random.normal(75000, 15000)
            elif 'Senior' in job_title or 'Staff' in job_title:
                base_salary = np.random.normal(140000, 25000)
            elif 'Lead' in job_title:
                base_salary = np.random.normal(180000, 30000)
            else:
                base_salary = np.random.normal(110000, 20000)
            
            # Multipliers
            location_multipliers = {
                'San Francisco, CA': 1.4, 'New York, NY': 1.3, 'Seattle, WA': 1.25,
                'Boston, MA': 1.2, 'Los Angeles, CA': 1.15, 'Austin, TX': 1.1,
                'Remote': 1.0, 'Chicago, IL': 1.05
            }
            big_tech = ['Google', 'Microsoft', 'Amazon', 'Meta', 'Apple', 'Netflix']
            company_multiplier = 1.3 if company in big_tech else 1.0
            
            final_salary = base_salary * location_multipliers.get(location, 1.0) * company_multiplier
            final_salary = max(45000, min(400000, final_salary))
            
            # Skills
            skills = np.random.choice(list(self.skill_keywords.keys()), 
                                   size=np.random.randint(2, 6), replace=False)
            description = f"Required skills: {', '.join(skills)}"
            
            data.append({
                'job_title': job_title,
                'company': company,
                'location': location,
                'job_description': description,
                'employment_type': np.random.choice(['Full-time', 'Contract', 'Part-time'], p=[0.8, 0.15, 0.05]),
                'salary': int(final_salary)
            })
        return pd.DataFrame(data)
    
    def extract_features(self, df):
        df = df.copy()
        def get_seniority(title):
            title_lower = title.lower()
            if 'junior' in title_lower:
                return 'Junior'
            elif 'senior' in title_lower or 'staff' in title_lower or 'lead' in title_lower:
                return 'Senior'
            else:
                return 'Mid'
        df['seniority_level'] = df['job_title'].apply(get_seniority)
        for skill, keywords in self.skill_keywords.items():
            df[f'has_{skill}'] = df['job_description'].apply(
                lambda desc: int(any(keyword in desc.lower() for keyword in keywords))
            )
        df['is_remote'] = (df['location'].str.lower() == 'remote').astype(int)
        big_tech = ['Google', 'Microsoft', 'Amazon', 'Meta', 'Apple', 'Netflix']
        df['is_big_tech'] = df['company'].apply(lambda comp: int(comp in big_tech))
        skill_cols = [f'has_{skill}' for skill in self.skill_keywords.keys()]
        df['total_skills'] = df[skill_cols].sum(axis=1)
        return df
    
    def train_model(self, df):
        df = self.extract_features(df)
        feature_cols = ['seniority_level', 'location', 'employment_type', 'is_remote', 'is_big_tech', 'total_skills']
        skill_cols = [f'has_{skill}' for skill in self.skill_keywords.keys()]
        feature_cols.extend(skill_cols)
        X = df[feature_cols]
        y = df['salary']
        categorical_features = ['seniority_level', 'location', 'employment_type']
        numerical_features = ['is_remote', 'is_big_tech', 'total_skills'] + skill_cols
        preprocessor = ColumnTransformer([
            ('num', StandardScaler(), numerical_features),
            ('cat', OneHotEncoder(drop='first', handle_unknown='ignore'), categorical_features)
        ])
        self.model = Pipeline([
            ('preprocessor', preprocessor),
            ('regressor', RandomForestRegressor(n_estimators=120, random_state=42))
        ])
        self.model.fit(X, y)
        self.feature_columns = feature_cols
        return self.model
    
    def predict(self, job_data):
        df = pd.DataFrame([job_data])
        df = self.extract_features(df)
        X = df[self.feature_columns]
        prediction = self.model.predict(X)[0]
        return prediction

# ---------------------- App Logic ----------------------
if 'predictor' not in st.session_state:
    st.session_state.predictor = SalaryPredictor()
    with st.spinner("Training model..."):
        training_data = st.session_state.predictor.generate_training_data()
        st.session_state.predictor.train_model(training_data)

predictor = st.session_state.predictor

# Header
st.markdown("""
<div class="header">
    <h1>SalaryScope</h1>
    <p>Data-Driven Job Compensation Insights</p>
</div>
""", unsafe_allow_html=True)

# Layout
col1, col2 = st.columns([1, 2])

with col1:
    st.subheader("Job Details")
    job_title = st.selectbox("Job Title", [
        'Junior Data Scientist', 'Data Scientist', 'Senior Data Scientist', 'Lead Data Scientist',
        'Software Engineer', 'Senior Software Engineer', 'Staff Engineer',
        'Data Analyst', 'Senior Data Analyst', 'ML Engineer', 'Senior ML Engineer',
        'Product Manager', 'Senior Product Manager', 'DevOps Engineer', 'Senior DevOps Engineer'
    ])
    company = st.selectbox("Company Type", [
        'Google', 'Microsoft', 'Amazon', 'Meta', 'Apple', 'Netflix',
        'Startup Inc', 'TechCorp', 'Other'
    ])
    location = st.selectbox("Location", [
        'San Francisco, CA', 'New York, NY', 'Seattle, WA', 'Austin, TX',
        'Boston, MA', 'Chicago, IL', 'Los Angeles, CA', 'Remote'
    ])
    employment_type = st.selectbox("Employment Type", ['Full-time', 'Contract', 'Part-time'])
    
    st.subheader("Required Skills")
    skills_display = {
        'python': 'Python',
        'sql': 'SQL & Databases',
        'javascript': 'JavaScript',
        'cloud': 'Cloud Platforms',
        'ml': 'Machine Learning / AI',
        'data_viz': 'Data Visualization',
        'big_data': 'Big Data',
        'devops': 'DevOps'
    }
    selected_skills = {skill: st.checkbox(label) for skill, label in skills_display.items()}

with col2:
    st.subheader("Salary Prediction")
    job_description = "Required skills: " + ", ".join([
        skill for skill, selected in selected_skills.items() if selected
    ])
    if st.button("Predict Salary"):
        job_data = {
            'job_title': job_title,
            'company': company,
            'location': location,
            'employment_type': employment_type,
            'job_description': job_description
        }
        prediction = predictor.predict(job_data)
        st.markdown(f"""
        <div class="result-card">
            <h2>${prediction:,.0f}</h2>
            <p>Predicted Annual Salary</p>
            <small>Range: ${prediction*0.85:,.0f} - ${prediction*1.15:,.0f}</small>
        </div>
        """, unsafe_allow_html=True)
        
        # Benchmark comparison
        st.markdown("#### Salary Benchmark")
        benchmark_data = {
            'Junior Level': 75000,
            'Mid Level': 110000,
            'Senior Level': 150000,
            'Your Prediction': prediction
        }
        fig = px.bar(
            x=list(benchmark_data.keys()),
            y=list(benchmark_data.values()),
            labels={'x': 'Level', 'y': 'Salary (USD)'},
            color=list(benchmark_data.keys()),
            color_discrete_sequence=['#cbd5e1', '#94a3b8', '#64748b', '#1e3a8a']
        )
        fig.update_layout(showlegend=False, height=400)
        st.plotly_chart(fig, use_container_width=True)

# Footer
st.markdown("---")
st.markdown(
    "<div style='text-align:center; color:#666;'>"
    "Built with Streamlit · For demo purposes only"
    "</div>",
    unsafe_allow_html=True
)
