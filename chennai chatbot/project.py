import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt

st.set_page_config(page_title="Chennai Risk Chatbot", page_icon="🧠")
st.title("🧠 Chennai Risk Chatbot")
st.write("Ask me about *accident, **air pollution, **crime, **heat, **flood,**population, **riskfactor data!")

st.write("📂 Current working directory:", os.getcwd())
st.write("📄 Files in this directory:", os.listdir())

# Load Excel files
accident_df = pd.read_excel("accident1.xlsx")
air_df = pd.read_excel("air pollution.xlsx")
crime_df = pd.read_excel("crime details 1.xlsx")
heat_df=pd.read_excel("heat.xlsx")
flood_df=pd.read_excel("flood.xlsx")
population_df=pd.read_excel("population.xlsx")
Riskfactor_df=pd.read_excel("riskanalysis.xlsx")

user_input = st.text_input("💬 Your question:")

if user_input:
    query = user_input.lower()

    # ---------------- Accident Data ----------------
    if "accident" in query or "hospital" in query:
        st.subheader("🚧 Accident Data")

        zones = accident_df["Zone / Area"].unique()
        selected_zone = st.selectbox("📍 Select Zone (Accident):", sorted(zones))
        filtered_data = accident_df[accident_df["Zone / Area"] == selected_zone]
        st.write(f"Showing accident data for *{selected_zone}*")
        st.dataframe(filtered_data)

        accident_df.columns = accident_df.columns.str.strip()
        accident_df["No. of Cases"] = pd.to_numeric(accident_df["No. of Cases"], errors="coerce")
        accident_df = accident_df.dropna(subset=["Zone / Area", "No. of Cases"])
        st.write("### 🔎 Zone-wise Accident Overview")

        chart_data = accident_df[["Zone / Area", "No. of Cases"]].copy()
        chart_data = chart_data.groupby("Zone / Area").sum().sort_values("No. of Cases", ascending=False)

        fig, ax = plt.subplots(figsize=(12, 6))
        bars = ax.bar(chart_data.index, chart_data["No. of Cases"], color='crimson')
        ax.set_ylabel("No. of Cases")
        ax.set_title("Zone-wise Accident Cases")
        plt.xticks(rotation=45, ha='right')

        for bar in bars:
            height = bar.get_height()
            ax.annotate(f'{int(height)}',
                        xy=(bar.get_x() + bar.get_width() / 2, height),
                        xytext=(0, 3),
                        textcoords="offset points",
                        ha='center', va='bottom')

        st.pyplot(fig)

    # ---------------- Air Pollution Data ----------------
    elif "pollution" in query or "air" in query:
        st.subheader("🌫 Air Pollution Data")

        zones = air_df["Zone / Area"].dropna().unique()
        selected_zone = st.selectbox("📍 Select Zone / Area (Air Pollution):", sorted(zones))

        filtered_data = air_df[air_df["Zone / Area"] == selected_zone]
        st.write(f"Showing air quality data for *{selected_zone}*")
        st.dataframe(filtered_data)  

        air_df.columns = air_df .columns.str.strip()
        air_df ["Avg. Value (µg/m³) or AQI"] = pd.to_numeric(air_df ["Avg. Value (µg/m³) or AQI"], errors="coerce")
        air_df  = air_df .dropna(subset=["Zone / Area", "Avg. Value (µg/m³) or AQI"])

        st.write("### 🔎 Zone-wise Airpollution Overview")

        chart_data = air_df [["Zone / Area", "Avg. Value (µg/m³) or AQI"]].copy()
        chart_data = chart_data.groupby("Zone / Area").sum().sort_values("Avg. Value (µg/m³) or AQI", ascending=False)

        fig, ax = plt.subplots(figsize=(12, 6))
        bars = ax.bar(chart_data.index, chart_data["Avg. Value (µg/m³) or AQI"], color='grey')
        ax.set_ylabel("Avg. Value (µg/m³) or AQI")
        ax.set_title("Zone-wise air pollution Cases")
        plt.xticks(rotation=45, ha='right')

        for bar in bars:
            height = bar.get_height()
            ax.annotate(f'{int(height)}',
                        xy=(bar.get_x() + bar.get_width() / 2, height),
                        xytext=(0, 3),
                        textcoords="offset points",
                        ha='center', va='bottom')

        st.pyplot(fig)

    # ---------------- Crime Data ----------------
    elif "crime" in query or "theft" in query or "assault" in query or "cyber" in query or "women" in query:
        st.subheader("🚔 Crime Data")

        zones = crime_df["Zone Name"].dropna().unique()
        selected_zone = st.selectbox("📍 Select Zone (Crime):", sorted(zones))

        filtered_data = crime_df[crime_df["Zone Name"] == selected_zone]
        st.write(f"Showing crime data for *{selected_zone}*")
        st.dataframe(filtered_data)

        crime_df.columns = crime_df .columns.str.strip()
        crime_df ["Total Crimes"] = pd.to_numeric(crime_df["Total Crimes"], errors="coerce")
        crime_df  = crime_df .dropna(subset=["Zone Name", "Total Crimes"])

        st.write("### 🔎 Zone-wise Crime Overview")

        chart_data = crime_df [["Zone Name", "Total Crimes"]].copy()
        chart_data = chart_data.groupby("Zone Name").sum().sort_values("Total Crimes", ascending=False)
    
        fig, ax = plt.subplots(figsize=(12, 6))
        bars = ax.bar(chart_data.index, chart_data["Total Crimes"], color='Blue')
        ax.set_ylabel("Total Crimes")
        ax.set_title("Zone-wise Crime Cases")
        plt.xticks(rotation=45, ha='right')

        for bar in bars:
            height = bar.get_height()
            ax.annotate(f'{int(height)}',
                        xy=(bar.get_x() + bar.get_width() / 2, height),
                        xytext=(0, 3),
                        textcoords="offset points",
                        ha='center', va='bottom')

        st.pyplot(fig)


    elif "heat" in query or "year" in query or "Heatstroke Cases" in query or "Dehydration Cases" in query or "Hospitalizations" in query:
        st.subheader("🥵 Heat Data")

        zones = heat_df["Area"].dropna().unique()
        selected_zone = st.selectbox("📍 Select Zone (heat):", sorted(zones))

        filtered_data = heat_df[heat_df["Area"] == selected_zone]
        st.write(f"Showing crime data for *{selected_zone}*")
        st.dataframe(filtered_data)

        heat_df.columns = heat_df .columns.str.strip()
        heat_df ["Heatstroke Cases"] = pd.to_numeric(heat_df["Heatstroke Cases"], errors="coerce")
        heat_df  = heat_df.dropna(subset=["Area", "Heatstroke Cases"])
        st.write("### 🔎 Zone-wise Crime Overview")

        chart_data = heat_df[["Area", "Heatstroke Cases"]].copy()
        chart_data = chart_data.groupby("Area").sum().sort_values("Heatstroke Cases", ascending=False)

        fig, ax = plt.subplots(figsize=(12, 6))
        bars = ax.bar(chart_data.index, chart_data["Heatstroke Cases"], color='orange')
        ax.set_ylabel("Heatstroke Cases")
        ax.set_title("Zone-wise Heat Cases")
        plt.xticks(rotation=45, ha='right')

        for bar in bars:
            height = bar.get_height()
            ax.annotate(f'{int(height)}',
                        xy=(bar.get_x() + bar.get_width() / 2, height),
                        xytext=(0, 3),
                        textcoords="offset points",
                        ha='center', va='bottom')

        st.pyplot(fig)
    
    elif "flood" in query or "rainfall" in query:
        st.subheader("🌊Flood Data")

        zones = flood_df["Area"].dropna().unique()
        selected_zone = st.selectbox("📍 Select Zone (flood):", sorted(zones))

        filtered_data = flood_df[flood_df["Area"] == selected_zone]
        st.write(f"Showing crime data for *{selected_zone}*")
        st.dataframe(filtered_data)

        flood_df.columns =flood_df .columns.str.strip()
        flood_df ["People Affected"] = pd.to_numeric(flood_df["People Affected"], errors="coerce")
        flood_df = flood_df .dropna(subset=["Area", "People Affected"])

        st.write("### 🔎 Zone-wise flood Overview")
        chart_data = flood_df [["Area", "People Affected"]].copy()
        chart_data = chart_data.groupby("Area").sum().sort_values("People Affected", ascending=False)

        fig, ax = plt.subplots(figsize=(12, 6))
        bars = ax.bar(chart_data.index, chart_data["People Affected"], color='black')
        ax.set_ylabel("People Affected")
        ax.set_title("Zone-wise flood Cases")
        plt.xticks(rotation=45, ha='right')

        for bar in bars:
            height = bar.get_height()
            ax.annotate(f'{int(height)}',
                        xy=(bar.get_x() + bar.get_width() / 2, height),
                        xytext=(0, 3),
                        textcoords="offset points",
                        ha='center', va='bottom')

        st.pyplot(fig)

    elif "population" in query or "citizens" in query:
        st.subheader("👩‍👩‍👧‍👦 Population Data")

        zones = population_df["Zone Name"].dropna().unique()
        selected_zone = st.selectbox("📍 Select Zone (Population):", sorted(zones))

        filtered_data = population_df[population_df["Zone Name"] == selected_zone]
        st.write(f"Showing crime data for *{selected_zone}*")
        st.dataframe(filtered_data) 

        population_df.columns = population_df.columns.str.strip()
        population_df["Population"] = pd.to_numeric(population_df["Population"], errors="coerce")
        population_df = population_df.dropna(subset=["Zone Name", "Population"])

        st.write("### 🔎 Zone-wise Population Overview")

        chart_data = population_df[["Zone Name", "Population"]].copy()
        chart_data = chart_data.groupby("Zone Name").sum().sort_values("Population", ascending=False)

        fig, ax = plt.subplots(figsize=(12, 6))
        bars = ax.bar(chart_data.index, chart_data["Population"], color='purple')
        ax.set_ylabel("Population")
        ax.set_title("Zone-wise Population Cases")
        plt.xticks(rotation=45, ha='right')

        for bar in bars:
            height = bar.get_height()
            ax.annotate(f'{int(height)}',
                        xy=(bar.get_x() + bar.get_width() / 2, height),
                        xytext=(0, 3),
                        textcoords="offset points",
                        ha='center', va='bottom')

        st.pyplot(fig)   

    elif "riskfactor" in query or "percentage" in query:
        st.subheader("🚨 Risk factor Data")

        zones = Riskfactor_df["Area"].dropna().unique()
        selected_zone = st.selectbox("📍 Select Zone (Riskfactor):", sorted(zones))

        filtered_data = Riskfactor_df[Riskfactor_df["Area"] == selected_zone]
        st.write(f"Showing crime data for *{selected_zone}*")
        st.dataframe(filtered_data) 

        st.write("📊 Risk Levels for Each Zone")
        melted_df = Riskfactor_df.melt(
            id_vars=["Area"],
            value_vars=["Accident", "Air Pollution", "Flood", "Heat", "Crime", "Population"],
            var_name="Risk Type",
            value_name="Level"
        )

        plt.figure(figsize=(14, 6))
        ax = plt.subplot()

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
        st.warning("❓ Sorry, I didn't understand. Try asking about *accident, **air pollution, **crime, **heat, **flood, **population*, **riskfactor*.")
