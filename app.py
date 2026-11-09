import os
import streamlit as st
import pandas as pd
import numpy as np
import joblib
from datetime import datetime
import plotly.express as px

st.set_page_config(
    page_title="Voyage Analytics",
    page_icon="✈️",
    layout="wide",
    initial_sidebar_state="collapsed",
)

st.markdown(
    """
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700;800&display=swap');
    :root {
        --green: #5D866C;
        --green-hover: #4A6B58;
        --tan: #C2A68C;
        --sand: #E6D8C3;
        --off-white: #F5F5F0;
        --ink: #2F3E34;
    }
    html, body, [class*="css"] {
        font-family: 'Inter', sans-serif;
        color: var(--ink);
    }
    .stApp { background: var(--off-white); }
    [data-testid="stHeader"], [data-testid="stToolbar"], footer,
    #MainMenu, [data-testid="stSidebar"] { visibility: hidden; display: none; }
    .block-container { max-width: 1100px; padding: 1.4rem 1.5rem 2rem; }
    h1, h2, h3 { color: var(--green); letter-spacing: -0.035em; }
    p, li { color: var(--ink); line-height: 1.65; }
    [data-testid="stRadio"] > div { gap: .15rem; }
    [data-testid="stRadio"] label {
        background: transparent; border-radius: 999px; padding: .48rem .7rem;
        color: var(--ink); font-size: .88rem; font-weight: 600;
    }
    [data-testid="stRadio"] label:has(input:checked) {
        background: var(--green); color: white;
    }
    [data-testid="stRadio"] input { display: none; }
    .stButton > button {
        background: var(--green); color: white; border: 1px solid var(--green);
        border-radius: 10px; padding: .58rem 1rem; font-weight: 700;
        transition: background .18s ease, transform .18s ease;
    }
    .stButton > button:hover { background: var(--green-hover); border-color: var(--green-hover); transform: translateY(-1px); color: white; }
    input, textarea, [data-baseweb="select"] > div {
        border-radius: 9px !important; border-color: var(--tan) !important;
    }
    [data-testid="stNumberInput"] input, [data-testid="stDateInput"] input {
        background: var(--off-white);
    }
    [data-testid="stTabs"] button { color: var(--ink); font-weight: 700; }
    [data-testid="stTabs"] button[aria-selected="true"] { color: var(--green); }
    [data-testid="stTabs"] [data-baseweb="tab-highlight"] { background: var(--green); }
    [data-testid="stExpander"] {
        background: var(--off-white); border: 1px solid var(--tan); border-radius: 12px;
    }
    [data-testid="stDataFrame"] { border: 1px solid var(--tan); border-radius: 10px; overflow: hidden; }
    .nav-brand { color: var(--green); font-size: 1.24rem; font-weight: 800; letter-spacing: -.04em; padding-top: .32rem; }
    .hero {
        background: var(--sand); border: 1px solid var(--tan); border-radius: 20px;
        padding: clamp(1.5rem, 5vw, 3.5rem); margin: .25rem 0 1.5rem;
    }
    .hero h1 { font-size: clamp(2.3rem, 6vw, 4.1rem); line-height: 1.03; margin: .35rem 0 .85rem; }
    .eyebrow { color: var(--green); font-size: .76rem; font-weight: 800; letter-spacing: .12em; text-transform: uppercase; }
    .hero-copy { max-width: 690px; font-size: 1.12rem; margin-bottom: 1.3rem; }
    .card {
        height: 100%; background: var(--off-white); border: 1px solid var(--tan);
        border-radius: 14px; padding: 1.15rem; box-shadow: 0 5px 16px rgba(47,62,52,.06);
        transition: transform .18s ease, box-shadow .18s ease;
    }
    .card:hover { transform: translateY(-2px); box-shadow: 0 9px 22px rgba(47,62,52,.11); }
    .card h3 { font-size: 1.04rem; margin: 0 0 .45rem; }
    .card p { font-size: .92rem; margin: 0; }
    .stat-card { background: var(--sand); border-top: 3px solid var(--green); }
    .stat-value { display: block; color: var(--green); font-size: 1.45rem; font-weight: 800; margin-bottom: .28rem; }
    .section-band { background: var(--sand); border-radius: 14px; padding: 1rem 1.2rem; margin: 1.5rem 0 1rem; }
    .section-band h2 { margin: 0; font-size: 1.38rem; }
    .pipeline { display: flex; flex-wrap: wrap; gap: .55rem; margin: .7rem 0 1.3rem; }
    .pipeline span, .chip {
        display: inline-block; background: var(--sand); border: 1px solid var(--tan);
        border-radius: 999px; padding: .42rem .76rem; color: var(--ink); font-weight: 600; font-size: .85rem;
    }
    .flow-card { min-height: 120px; border-left: 4px solid var(--green); }
    .flow-num { color: var(--tan); font-weight: 800; font-size: .76rem; }
    .note { background: var(--sand); border: 1px solid var(--tan); border-left: 4px solid var(--tan); border-radius: 12px; padding: .9rem 1rem; margin: .7rem 0 1rem; }
    .result-box { background: var(--sand); border: 2px solid var(--green); border-radius: 14px; padding: 1rem 1.1rem; margin-top: 1rem; }
    .timeline { border-left: 2px solid var(--tan); padding-left: 1.2rem; margin-left: .55rem; }
    .phase-card { border-left: 4px solid var(--green); margin: 0 0 1rem; }
    .phase-card h3 { margin-bottom: .5rem; }
    .phase-card strong { color: var(--green); }
    .footer {
        margin-top: 3rem; padding: 1.3rem 0 .4rem; border-top: 1px solid var(--tan);
        color: var(--ink); font-size: .82rem;
    }
    .footer strong { color: var(--green); }
    @media (max-width: 700px) {
        .block-container { padding: .7rem .8rem 1.5rem; }
        .nav-brand { font-size: 1rem; }
        [data-testid="stRadio"] label { padding: .35rem .4rem; font-size: .75rem; }
        .hero { border-radius: 15px; }
    }
    </style>
    """,
    unsafe_allow_html=True,
)


def card(title, body, extra_class=""):
    st.markdown(
        f'<div class="card {extra_class}"><h3>{title}</h3><p>{body}</p></div>',
        unsafe_allow_html=True,
    )


def section(title):
    st.markdown(f'<div class="section-band"><h2>{title}</h2></div>', unsafe_allow_html=True)


def footer():
    st.markdown(
        """
        <div class="footer">
            <strong>Voyage Analytics</strong><br>
            Built with Python, scikit-learn, Flask, Docker, Kubernetes, Airflow, MLflow, Streamlit, GitHub Actions
            <br>Educational project
        </div>
        """,
        unsafe_allow_html=True,
    )


# --- Resource caching strategy ---
@st.cache_resource
def load_resources():
    # Resolve relative paths
    flight_pipe = joblib.load('models/best_flight_price_pipeline.joblib')
    gender_pipe = joblib.load('models/gender_pipeline_v1.joblib')
    rec_obj = joblib.load('models/hotel_recommender_v3.joblib')
    return flight_pipe, gender_pipe, rec_obj


try:
    flight_pipeline, gender_pipeline, recommender_data = load_resources()
    all_places = recommender_data['all_places']
    global_pop_places = recommender_data['global_pop_places']
    hotel_catalog = recommender_data['hotel_catalog']
    place_similarity_df = recommender_data['place_similarity_df']
    place_utility_matrix = recommender_data['place_utility_matrix']
    train_df = recommender_data['train_df']
except Exception as e:
    st.error(f"Error loading serialized assets. Please ensure models are compiled. Error: {str(e)}")
    st.stop()


pages = ["Home", "About", "How It Works", "Phases", "Live Demo", "Insights"]
if "page" not in st.session_state:
    st.session_state.page = "Home"
if "nav_radio" not in st.session_state or st.session_state.nav_radio != st.session_state.page:
    st.session_state.nav_radio = st.session_state.page


def update_page_from_navigation():
    st.session_state.page = st.session_state.nav_radio

nav_left, nav_right = st.columns([1.25, 5.75], vertical_alignment="center")
with nav_left:
    st.markdown('<div class="nav-brand">Voyage Analytics</div>', unsafe_allow_html=True)
with nav_right:
    st.radio(
        "Main navigation",
        pages,
        horizontal=True,
        label_visibility="collapsed",
        key="nav_radio",
        on_change=update_page_from_navigation,
    )

page = st.session_state.page

if page == "Home":
    st.markdown(
        """
        <div class="hero">
            <div class="eyebrow">Travel • Data • MLOps</div>
            <h1>Voyage Analytics</h1>
            <p class="hero-copy">Integrating MLOps in Travel: from raw data to a production-ready ML system</p>
        </div>
        """,
        unsafe_allow_html=True,
    )
    hero_demo, hero_how, _ = st.columns([1.35, 1.45, 4.2])
    with hero_demo:
        if st.button("Try the Live Demo", use_container_width=True):
            st.session_state.page = "Live Demo"
            st.rerun()
    with hero_how:
        if st.button("See How It Works", use_container_width=True):
            st.session_state.page = "How It Works"
            st.rerun()

    stats = [
        ("271,888", "flight records"),
        ("1,340", "users"),
        ("9", "destinations / hotels"),
        ("R² 0.91", "price model"),
    ]
    stat_cols = st.columns(4)
    for col, (value, label) in zip(stat_cols, stats):
        with col:
            st.markdown(
                f'<div class="card stat-card"><span class="stat-value">{value}</span><p>{label}</p></div>',
                unsafe_allow_html=True,
            )

    section("What we built")
    features = [
        ("Flight Price Prediction", "A trained pipeline estimates ticket prices from trip and traveler details."),
        ("Flask REST API", "A simple service exposes health and prediction endpoints."),
        ("Docker + Kubernetes", "Containerized deployment with orchestration and self-healing."),
        ("MLflow Tracking", "Experiments and the production model are tracked and versioned."),
        ("Airflow Automation", "A weekly workflow validates data, retrains, and evaluates models."),
        ("CI/CD with GitHub Actions", "Tests run on push before the container image is built and published."),
    ]
    for start in range(0, len(features), 3):
        cols = st.columns(3)
        for col, (title, body) in zip(cols, features[start:start + 3]):
            with col:
                card(title, body)

    section("From raw data to an app")
    st.markdown(
        '<div class="pipeline">' + "".join(
            f"<span>{item}</span>" for item in
            ["Data", "Model", "API", "Container", "Cluster", "Automation", "Tracking", "App"]
        ) + "</div>",
        unsafe_allow_html=True,
    )

elif page == "About":
    st.title("About the project")
    st.write(
        "Voyage Analytics is a student MLOps project that brings travel data, machine-learning "
        "experiments, deployment, and an interactive application into one end-to-end workflow."
    )
    section("The problem")
    st.markdown(
        '<div class="card"><p>A travel company needs useful price predictions and recommendations, '
        'supported by a production-grade machine-learning workflow that can be tested, deployed, '
        'monitored, and retrained.</p></div>',
        unsafe_allow_html=True,
    )
    section("Project objectives")
    objectives = [
        "Train a flight-price regression model", "Expose predictions through a REST API",
        "Package the service with Docker", "Deploy and orchestrate with Kubernetes",
        "Automate retraining with Airflow", "Run CI/CD with GitHub Actions",
        "Track experiments and models with MLflow", "Demonstrate gender classification",
        "Demonstrate hotel / destination recommendation", "Deliver an interactive Streamlit app",
    ]
    for start in range(0, len(objectives), 2):
        cols = st.columns(2)
        for col, item in zip(cols, objectives[start:start + 2]):
            with col:
                card("Objective", item)

    section("The datasets")
    datasets = [
        ("flights.csv", "23.4 MB", "Flight trips with route, type, price, distance, agency, and date."),
        ("users.csv", "51 KB", "User code, company, gender, and age."),
        ("hotels.csv", "2.4 MB", "Bookings with hotel, place, days, price, and total."),
    ]
    cols = st.columns(3)
    for col, (name, size, details) in zip(cols, datasets):
        with col:
            card(f"{name} · {size}", details)

    section("Technology")
    st.markdown(
        '<div class="pipeline">' + "".join(
            f'<span class="chip">{item}</span>' for item in
            ["Python", "scikit-learn", "Flask", "Docker", "Kubernetes", "Airflow", "MLflow", "Streamlit", "GitHub Actions"]
        ) + "</div>",
        unsafe_allow_html=True,
    )
    st.markdown(
        '<div class="note"><strong>Honest note:</strong> Gender and destination models are demonstrations; '
        'the dataset carries little signal for them.</div>',
        unsafe_allow_html=True,
    )

elif page == "How It Works":
    st.title("How it works")
    st.write("The workflow moves travel data through training, serving, deployment, and ongoing automation.")
    flow = [
        ("Raw Data", "Travel records are the source for model development."),
        ("Cleaning & Features", "Data is cleaned and useful route and date features are prepared."),
        ("Model Training", "A regression pipeline learns flight-price patterns."),
        ("MLflow Tracking", "Runs and model versions are recorded for comparison."),
        ("Flask API", "An HTTP service accepts requests and returns predictions."),
        ("Docker Image", "The service and dependencies are packaged together."),
        ("Kubernetes", "The container is deployed with probes and scaling."),
        ("Airflow Retraining", "A scheduled workflow validates, trains, and evaluates."),
        ("CI/CD", "Pushes run tests and build and publish the image."),
        ("Streamlit App", "A website-style interface brings the project to users."),
    ]
    for start in range(0, len(flow), 2):
        cols = st.columns(2)
        for col, (title, body) in zip(cols, flow[start:start + 2]):
            with col:
                idx = flow.index((title, body)) + 1
                st.markdown(
                    f'<div class="card flow-card"><span class="flow-num">STEP {idx:02d}</span>'
                    f'<h3>{title}</h3><p>{body}</p></div>',
                    unsafe_allow_html=True,
                )
    section("A prediction request's journey")
    request_steps = [
        "User enters trip details", "App validates the inputs", "Pipeline encodes and scales",
        "Random Forest predicts", "Price is returned",
    ]
    st.markdown(
        '<div class="pipeline">' + "".join(f"<span>{step}</span>" for step in request_steps) + "</div>",
        unsafe_allow_html=True,
    )
    section("Engineering notes")
    with st.expander("Why use a Pipeline?"):
        st.write("Preprocessing is fitted as part of training and applied consistently at prediction time, helping prevent data leakage.")
    with st.expander("Why version the model in MLflow?"):
        st.write("Tracking runs makes experiments comparable and ties the selected production model to its recorded training results.")
    with st.expander("How does Kubernetes self-heal?"):
        st.write("Health probes let Kubernetes detect unhealthy pods and replace them to maintain the desired deployment.")
    with st.expander("How does scheduled retraining promote models?"):
        st.write("Airflow runs the weekly workflow and promotes a candidate only if its R² is not worse by more than 0.005.")

elif page == "Phases":
    st.title("Project phases")
    st.write("A project timeline from data preparation through deployment and automation.")
    phase_data = [
        ("Phase 1 · Data Prep and EDA",
         "<strong>Goal:</strong> Prepare reliable travel data.<br><strong>What we did:</strong> Cleaned 3 datasets; no missing values or duplicates; all keys matched; kept “none” gender as “Unknown” (~33%); dropped time because it is almost identical to distance (r≈0.99999); built date and route features.<br><strong>Key result:</strong> A consistent dataset with engineered features.<br><strong>Tools:</strong> Python, pandas"),
        ("Phase 2 · Flight Price Model",
         "<strong>Goal:</strong> Predict flight prices.<br><strong>What we did:</strong> 80/20 split with scaling and encoding inside a Pipeline.<br><strong>Key result:</strong><br>Linear Regression — R² 0.772 / RMSE 173.24 / MAE 134.28<br>HistGradientBoosting — 0.904 / 112.30 / 69.80<br>Random Forest (best) — 0.913 / 107.32 / 61.39<br>5-fold CV 0.913 ± 0.002; train-test gap about 0.01. Tuning gave no meaningful gain.<br><strong>Tools:</strong> scikit-learn"),
        ("Phase 3 · Flask REST API",
         "<strong>Goal:</strong> Serve model predictions over HTTP.<br><strong>What we did:</strong> Added POST /predict and GET /health, validated inputs (400 on bad input), and loaded the model once.<br><strong>Key result:</strong> Reusable API endpoints.<br><strong>Tools:</strong> Flask"),
        ("Phase 4 · Docker",
         "<strong>Goal:</strong> Package the prediction service.<br><strong>What we did:</strong> Used python:3.11-slim, gunicorn, a non-root user, and a health check.<br><strong>Key result:</strong> Container returned the same prediction as Colab (1322.34).<br><strong>Tools:</strong> Docker, gunicorn"),
        ("Phase 5 · MLflow",
         "<strong>Goal:</strong> Track experiments and model versions.<br><strong>What we did:</strong> Logged Linear, Random Forest, HistGradientBoosting, and tuned Random Forest runs.<br><strong>Key result:</strong> Best model registered as flight_price_model with the “production” alias.<br><strong>Tools:</strong> MLflow"),
        ("Phase 6 · Gender Classifier",
         "<strong>Goal:</strong> Demonstrate user gender classification.<br><strong>What we did:</strong> Classified male, female, and Unknown. v1 accuracy 0.377 vs 0.336 baseline; v2 with behavioural features CV 0.344, test 0.328.<br><strong>Key result:</strong> Little signal; demonstration only.<br><strong>Tools:</strong> scikit-learn"),
        ("Phase 7 · Hotel / Destination Recommender",
         "<strong>Goal:</strong> Recommend a next destination.<br><strong>What we did:</strong> Each destination has exactly one hotel, so the task became next-destination prediction. Item-based CF HR@3 36.6%, HR@5 60.3% vs random 34.5% / 57.8%.<br><strong>Key result:</strong> Close to random; demonstration only.<br><strong>Tools:</strong> Collaborative filtering"),
        ("Phase 8 · Streamlit App",
         "<strong>Goal:</strong> Make the project approachable and interactive.<br><strong>What we did:</strong> Built this website-style project experience with prediction tools and insights.<br><strong>Key result:</strong> A multi-page interface for the project.<br><strong>Tools:</strong> Streamlit"),
        ("Phase 9 · Kubernetes",
         "<strong>Goal:</strong> Run and scale the containerized API.<br><strong>What we did:</strong> Deployed 2 replicas, health probes, a NodePort service, and HPA (2 to 5 pods). Deleting a pod triggered auto-replacement (self-healing).<br><strong>Key result:</strong> Same prediction returned.<br><strong>Tools:</strong> Kubernetes"),
        ("Phase 10 · Airflow",
         "<strong>Goal:</strong> Automate retraining and evaluation.<br><strong>What we did:</strong> Weekly DAG with validate_data, build_features, train_model, evaluate_and_promote, notify.<br><strong>Key result:</strong> Run reproduced R² 0.9126, RMSE 107.32, MAE 61.39 in about 2 minutes.<br><strong>Tools:</strong> Airflow"),
        ("Phase 11 · CI/CD",
         "<strong>Goal:</strong> Automate test and image delivery.<br><strong>What we did:</strong> GitHub Actions runs 6 pytest tests on every push, then builds and pushes the Docker image to GitHub Container Registry.<br><strong>Key result:</strong> Automated checks and image publishing.<br><strong>Tools:</strong> GitHub Actions, pytest, GHCR"),
    ]
    st.markdown('<div class="timeline">', unsafe_allow_html=True)
    for title, body in phase_data:
        st.markdown(
            f'<div class="card phase-card"><h3>{title}</h3><p>{body}</p></div>',
            unsafe_allow_html=True,
        )
    st.markdown("</div>", unsafe_allow_html=True)

elif page == "Live Demo":
    st.title("Live Demo")
    st.write("Explore the trained models using the same inputs and prediction logic as the original app.")
    tab1, tab2, tab3 = st.tabs(["Flight Price", "Destination Recommender", "Gender Classifier"])

    with tab1:
        st.markdown('<div class="card"><h3>Flight price prediction</h3><p>Estimate a ticket price from trip and traveler details.</p></div>', unsafe_allow_html=True)
        col1, col2, col3 = st.columns(3)
        with col1:
            distance = st.number_input("Distance (dataset units)", min_value=1.0, value=500.0, step=10.0)
            age = st.number_input("User Age", min_value=1, max_value=100, value=30, step=1)
            date_input = st.date_input("Flight Date", min_value=datetime(2010, 1, 1), value=datetime(2026, 6, 15))
        with col2:
            flight_type = st.selectbox("Cabin Class (flightType)", ["economic", "premium", "firstClass"])
            agency = st.selectbox("Booking Agency", ["CloudFy", "FlyingDrops", "Rainbow"])
        with col3:
            gender = st.selectbox("User Gender", ["Unknown", "female", "male"])

        if st.button("Calculate Price Projection", key="price_predict"):
            # Format features to match model pipeline expectations
            flight_month = date_input.month
            flight_dayofweek = date_input.weekday()
            flight_is_weekend = 1 if flight_dayofweek in [5, 6] else 0

            input_payload = pd.DataFrame([{
                'distance': float(distance),
                'age': int(age),
                'flightType': flight_type,
                'agency': agency,
                'gender': gender,
                'flight_month': int(flight_month),
                'flight_dayofweek': int(flight_dayofweek),
                'flight_is_weekend': int(flight_is_weekend)
            }])

            try:
                pred_price = flight_pipeline.predict(input_payload)[0]
                st.markdown(
                    f'<div class="result-box">Predicted Ticket Price: {round(pred_price, 2)} (dataset currency)</div>',
                    unsafe_allow_html=True,
                )
            except Exception as err:
                st.error(f"Calculation error: {err}")

    with tab2:
        st.markdown('<div class="card"><h3>Next destination recommendations</h3><p>Explore suggested destinations based on user history.</p></div>', unsafe_allow_html=True)
        st.markdown('<div class="note">Demonstration only: performance is close to random</div>', unsafe_allow_html=True)
        user_code = st.number_input("User Code Identifier", min_value=-999, value=0, step=1)

        def recommend(user_code, n=3):
            is_known = user_code in train_df['userCode'].unique()
            if not is_known:
                recs_places = global_pop_places[:n]
            else:
                # Item-based collaborative scoring
                if user_code not in place_utility_matrix.index:
                    recs_places = global_pop_places[:n]
                else:
                    user_vector = place_utility_matrix.loc[user_code].to_dict()
                    scores = {}
                    for target_place in all_places:
                        sim_sum = 0.0
                        for place, count in user_vector.items():
                            sim_sum += place_similarity_df.loc[target_place, place] * count
                        scores[target_place] = sim_sum

                    if sum(scores.values()) == 0:
                        recs_places = global_pop_places[:n]
                    else:
                        sorted_recs = sorted(scores.items(), key=lambda x: x[1], reverse=True)
                        recs_places = [place for place, score in sorted_recs[:n]]

            recs_df = pd.DataFrame({'place': recs_places})
            return recs_df.merge(hotel_catalog, on='place', how='left')

        if st.button("Generate Recommendations", key="recommend_places"):
            recs = recommend(int(user_code), n=3)
            st.write(f"Top Recommendations for User {user_code}:")
            st.dataframe(recs, use_container_width=True)

    with tab3:
        st.markdown('<div class="card"><h3>User gender classifier</h3><p>Classify a user profile from age and company.</p></div>', unsafe_allow_html=True)
        st.markdown('<div class="note">Demonstration only: accuracy about the same as guessing</div>', unsafe_allow_html=True)
        col_c1, col_c2 = st.columns(2)
        with col_c1:
            c_age = st.number_input("Age", min_value=1, max_value=100, value=30, step=1, key="gender_age")
        with col_c2:
            c_company = st.selectbox("Corporate Affiliation", ["4You", "Monsters CYA", "Wonka Company", "Acme Factory", "Umbrella LTDA"])

        if st.button("Predict Profile Gender", key="predict_gender"):
            # Compile minimal payload to feed into model preprocessor pipeline
            # Features: ['company', 'age']
            # (Or full set matching users_features if registered v2 expects it; let us match the v2 preprocessor specification: company, age)
            try:
                input_gender_df = pd.DataFrame([{
                    'company': c_company,
                    'age': int(c_age)
                }])
                pred_gender = gender_pipeline.predict(input_gender_df)[0]
                st.markdown(
                    f'<div class="result-box">Predicted User Gender Category: {pred_gender}</div>',
                    unsafe_allow_html=True,
                )
            except Exception as err:
                st.error(f"Predictor encountered an issue: {err}")

elif page == "Insights":
    st.title("Voyage Analytics insights")
    st.write("Explore the distributions and patterns in the cleaned travel datasets.")

    @st.cache_data
    def load_data():
        flights = pd.read_csv('data/flights_clean.csv')
        hotels = pd.read_csv('data/hotels_clean.csv')
        users = pd.read_csv('data/users_clean.csv')
        return flights, hotels, users

    try:
        flights_df, hotels_df, users_df = load_data()

        # Chart 1: Price by flightType
        fig1 = px.box(
            flights_df, x='flightType', y='price', color='flightType',
            title="Ticket Price Distributions by Cabin Class",
            color_discrete_sequence=["#5D866C", "#C2A68C"],
        )
        fig1.update_layout(paper_bgcolor="#F5F5F0", plot_bgcolor="#F5F5F0", font_color="#2F3E34")
        st.markdown('<div class="card"><h3>Ticket prices by cabin class</h3><p>Compare the spread of observed prices across cabin classes.</p></div>', unsafe_allow_html=True)
        st.plotly_chart(fig1, use_container_width=True)

        # Chart 2: Average price by month
        flights_df['date'] = pd.to_datetime(flights_df['date'])
        flights_df['month'] = flights_df['date'].dt.month
        monthly_prices = flights_df.groupby('month')['price'].mean().reset_index()
        fig2 = px.line(
            monthly_prices, x='month', y='price', markers=True,
            title="Average Ticket Price Monthly Fluctuations",
            color_discrete_sequence=["#5D866C"],
        )
        fig2.update_traces(line=dict(width=3), marker=dict(color="#C2A68C"))
        fig2.update_layout(paper_bgcolor="#F5F5F0", plot_bgcolor="#F5F5F0", font_color="#2F3E34")
        st.markdown('<div class="card"><h3>Average price by month</h3><p>Follow how average ticket prices change across calendar months.</p></div>', unsafe_allow_html=True)
        st.plotly_chart(fig2, use_container_width=True)

        # Chart 3: Bookings per place
        place_counts = hotels_df['place'].value_counts().reset_index(name='booking_count')
        place_counts.rename(columns={'index': 'place'}, inplace=True)
        fig3 = px.bar(
            place_counts, x='place', y='booking_count', color='place',
            title="Total Hotel Reservations Mapped by Destination City",
            color_discrete_sequence=["#5D866C", "#C2A68C"],
        )
        fig3.update_layout(paper_bgcolor="#F5F5F0", plot_bgcolor="#F5F5F0", font_color="#2F3E34")
        st.markdown('<div class="card"><h3>Bookings by destination</h3><p>See how hotel bookings are distributed across destinations.</p></div>', unsafe_allow_html=True)
        st.plotly_chart(fig3, use_container_width=True)

        # Chart 4: Users by gender and age
        fig4 = px.box(
            users_df, x='gender', y='age', color='gender',
            title="User Profile Demographics (Age vs Gender)",
            color_discrete_sequence=["#5D866C", "#C2A68C"],
        )
        fig4.update_layout(paper_bgcolor="#F5F5F0", plot_bgcolor="#F5F5F0", font_color="#2F3E34")
        st.markdown('<div class="card"><h3>Age by gender category</h3><p>Review the distribution of user ages across recorded gender categories.</p></div>', unsafe_allow_html=True)
        st.plotly_chart(fig4, use_container_width=True)

    except Exception as err:
        st.error(f"Error processing charts: {err}")

footer()
