import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import os
import spacy
import subprocess  # To handle model download

# Automatically download spaCy model if missing
try:
    nlp = spacy.load("en_core_web_sm")
except:
    subprocess.run(["python", "-m", "spacy", "download", "en_core_web_sm"])
    nlp = spacy.load("en_core_web_sm")

# Streamlit page config
st.set_page_config(page_title="Chennai Risk Chatbot AI", page_icon="🧠")
st.markdown("""
    <style>
        .big-font {
            font-size:24px !important;
        }
        .highlight {
            color: #FF4B4B;
            font-weight: bold;
        }
    </style>
""", unsafe_allow_html=True)

st.title("🤖 Chennai AI Risk Chatbot")
st.markdown("<p class='big-font'>Ask about <span class='highlight'>accidents, pollution, crime, heat, flood, population, or risk factors</span>.</p>", unsafe_allow_html=True)

# Load Excel files
accident_df = pd.read_excel("accident1.xlsx")
air_df = pd.read_excel("air pollution.xlsx")
crime_df = pd.read_excel("crime details 1.xlsx")
heat_df = pd.read_excel("heat.xlsx")
flood_df = pd.read_excel("flood.xlsx")
population_df = pd.read_excel("population.xlsx")
Riskfactor_df = pd.read_excel("riskanalysis.xlsx")

# Combine all zone names
all_zones = set(accident_df["Zone / Area"].dropna().unique()) | \
            set(air_df["Zone / Area"].dropna().unique()) | \
            set(crime_df["Zone Name"].dropna().unique()) | \
            set(heat_df["Area"].dropna().unique()) | \
            set(flood_df["Area"].dropna().unique()) | \
            set(population_df["Zone Name"].dropna().unique()) | \
            set(Riskfactor_df["Area"].dropna().unique())

# Input field
user_input = st.chat_input("Type your questions here...")

# Detect zone
def detect_zone(user_input, zones):
    doc = nlp(user_input.lower())
    for ent in doc.ents:
        if ent.text in zones:
            return ent.text
    for z in zones:
        if z.lower() in user_input.lower():
            return z
    return None

# Bar chart display
def bar_chart(df, x_col, y_col, title, color):
    df.columns = df.columns.str.strip()
    df[y_col] = pd.to_numeric(df[y_col], errors="coerce")
    df = df.dropna(subset=[x_col, y_col])
    chart_data = df[[x_col, y_col]].copy()
    chart_data = chart_data.groupby(x_col).sum().sort_values(y_col, ascending=False)
    fig, ax = plt.subplots(figsize=(12, 6))
    bars = ax.bar(chart_data.index, chart_data[y_col], color=color)
    ax.set_ylabel(y_col)
    ax.set_title(title)
    plt.xticks(rotation=45, ha='right')
    for bar in bars:
        height = bar.get_height()
        ax.annotate(f'{int(height)}', xy=(bar.get_x() + bar.get_width() / 2, height), xytext=(0, 3),
                    textcoords="offset points", ha='center', va='bottom')
    st.pyplot(fig)

# Show data by zone
def zone_data(df, zone_col, title, detected_zone=None):
    zones = df[zone_col].dropna().unique()
    if detected_zone and detected_zone in zones:
        selected_zone = detected_zone
    else:
        selected_zone = st.selectbox(f"📍 Select Zone ({title}):", sorted(zones))
    filtered_data = df[df[zone_col] == selected_zone]
    st.success(f"Showing {title.lower()} data for *{selected_zone}*")
    st.dataframe(filtered_data)

# Response to user query
if user_input:
    query = user_input.lower()
    detected_zone = detect_zone(user_input, all_zones)

    if detected_zone:
        st.success(f"✅ Detected Zone: {detected_zone}")

    if "accident" in query or "hospital" in query:
        st.subheader("🚧 Accident Insights")
        zone_data(accident_df, "Zone / Area", "Accidents", detected_zone)
        bar_chart(accident_df, "Zone / Area", "No. of Cases", "Zone-wise Accident Cases", 'crimson')

    elif "pollution" in query or "air" in query:
        st.subheader("🌫 Air Pollution Overview")
        zone_data(air_df, "Zone / Area", "Air Pollution", detected_zone)
        bar_chart(air_df, "Zone / Area", "Avg. Value (µg/m³) or AQI", "Zone-wise Air Pollution Levels", 'grey')

    elif "crime" in query:
        st.subheader("🚔 Crime Statistics")
        zone_data(crime_df, "Zone Name", "Crime", detected_zone)
        bar_chart(crime_df, "Zone Name", "Total Crimes", "Zone-wise Crime Rates", 'blue')

    elif "heat" in query:
        st.subheader("🥵 Heat-related Issues")
        zone_data(heat_df, "Area", "Heat", detected_zone)
        bar_chart(heat_df, "Area", "Heatstroke Cases", "Zone-wise Heatstroke Cases", 'orange')

    elif "flood" in query:
        st.subheader("🌊 Flood Reports")
        zone_data(flood_df, "Area", "Flood", detected_zone)
        bar_chart(flood_df, "Area", "People Affected", "Zone-wise Flood Impact", 'black')

    elif "population" in query:
        st.subheader("👨‍👩‍👧‍👦 Population Density")
        zone_data(population_df, "Zone Name", "Population", detected_zone)
        bar_chart(population_df, "Zone Name", "Population", "Zone-wise Population Distribution", 'purple')

    elif "riskfactor" in query or "risk factor" in query:
        st.subheader("🚨 Comprehensive Risk Factors")
        zone_data(Riskfactor_df, "Area", "Risk Factors", detected_zone)

        melted_df = Riskfactor_df.melt(
            id_vars=["Area"],
            value_vars=["Accident", "Air Pollution", "Flood", "Heat", "Crime", "Population"],
            var_name="Risk Type",
            value_name="Level"
        )

        fig, ax = plt.subplots(figsize=(14, 6))
        pivot_df = melted_df.pivot(index="Area", columns="Risk Type", values="Level")
        pivot_df.plot(kind="bar", ax=ax, colormap="coolwarm", edgecolor='black')

        plt.title("Risk Factor Levels by Zone")
        plt.xlabel("Zone")
        plt.ylabel("Risk Level (1=Low, 2=Medium, 3=High)")
        plt.xticks(rotation=45, ha='right')
        plt.legend(title="Risk Type", bbox_to_anchor=(1.05, 1), loc='upper left')
        plt.tight_layout()
        st.pyplot(plt)

    else:
        st.info("❓ Try asking about accidents, crime, air pollution, heat, flood, population, or risk levels.")
