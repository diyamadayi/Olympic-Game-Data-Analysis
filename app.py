import streamlit as st
import pandas as pd 
import matplotlib.pyplot as plt
import seaborn as sns
import numpy as np
import plotly.express as px

# ==========================================
# 1. PAGE CONFIGURATION
# ==========================================

st.set_page_config(
    page_title="Olympic Games Analysis",
    page_icon="🏅",
    layout="wide"
)

st.title("🏅 Olympic Games Data Analysis")
st.write("Interactive Exploratory Data Analysis of Olympic Games")

st.markdown("---")


# ==========================================
# 2. LOAD DATASET
# ==========================================

@st.cache_data
def load_data():
    df = pd.read_csv("cleaned_olympic_data.csv")
    return df

df = load_data()


# ==========================================
# 3. SIDEBAR FILTERS
# ==========================================

st.sidebar.title("🔍 Olympic Filters")

years = sorted(df['Year'].unique())

selected_year = st.sidebar.multiselect(
    "Select Year",
    years,
    default=years
)

seasons = sorted(df['Season'].unique())

selected_season = st.sidebar.multiselect(
    "Select Season",
    seasons,
    default=seasons
)

genders = sorted(df['Sex'].dropna().unique())

selected_gender = st.sidebar.multiselect(
    "Select Gender",
    genders,
    default=genders
)

countries = sorted(df['Team'].dropna().unique())

selected_country = st.sidebar.multiselect(
    "Select Country",
    countries
)

sports = sorted(df['Sport'].dropna().unique())

selected_sport = st.sidebar.multiselect(
    "Select Sport",
    sports
)


# ==========================================
# 4. APPLY FILTERS
# ==========================================

filtered_df = df[
    (df['Year'].isin(selected_year)) &
    (df['Season'].isin(selected_season)) &
    (df['Sex'].isin(selected_gender))
]

if selected_country:
    filtered_df = filtered_df[
        filtered_df['Team'].isin(selected_country)
    ]

if selected_sport:
    filtered_df = filtered_df[
        filtered_df['Sport'].isin(selected_sport)
    ]


# ==========================================
# 5. KPI CARDS
# ==========================================

st.subheader("📊 Olympic Overview")

col1, col2, col3, col4 = st.columns(4)

total_athletes = filtered_df['ID'].nunique()

total_countries = filtered_df['NOC'].nunique()

total_sports = filtered_df['Sport'].nunique()

total_medals = filtered_df[
    filtered_df['Medal'] != 'No Medal'
].shape[0]

col1.metric("Total Athletes", f"{total_athletes:,}")

col2.metric("Total Countries", f"{total_countries:,}")

col3.metric("Total Sports", f"{total_sports:,}")

col4.metric("Total Medals", f"{total_medals:,}")


st.markdown("---")


# ==========================================
# 6. GENDER PARTICIPATION
# ==========================================

st.subheader("👨‍👩‍👧 Gender Participation")

gender_data = filtered_df.groupby('Sex')['ID'].nunique().reset_index()

fig1 = px.pie(
    gender_data,
    names='Sex',
    values='ID',
    title="Male vs Female Participation",
    hole=0.4
)

st.plotly_chart(fig1, use_container_width=True)


# ==========================================
# 7. PARTICIPATION OVER YEARS
# ==========================================

st.subheader("📈 Athlete Participation Over Years")

year_data = filtered_df.groupby('Year')['ID'].nunique().reset_index()

fig2 = px.line(
    year_data,
    x='Year',
    y='ID',
    markers=True,
    title="Olympic Participation Over Time"
)

st.plotly_chart(fig2, use_container_width=True)


# ==========================================
# 8. TOP 10 COUNTRIES BY MEDALS
# ==========================================

st.subheader("🌍 Top 10 Countries by Medals")

medal_df = filtered_df[
    filtered_df['Medal'] != 'No Medal'
]

country_medals = (
    medal_df.groupby('Team')['Medal']
    .count()
    .reset_index()
)

country_medals.columns = ['Country', 'Total Medals']

country_medals = country_medals.sort_values(
    by='Total Medals',
    ascending=False
).head(10)

fig3 = px.bar(
    country_medals,
    x='Country',
    y='Total Medals',
    color='Total Medals',
    title="Top 10 Countries by Total Medals"
)

st.plotly_chart(fig3, use_container_width=True)


# ==========================================
# 9. MEDAL DISTRIBUTION
# ==========================================

st.subheader("🥇 Medal Distribution")

medal_distribution = medal_df['Medal'].value_counts().reset_index()

medal_distribution.columns = ['Medal Type', 'Count']

fig4 = px.pie(
    medal_distribution,
    names='Medal Type',
    values='Count',
    title="Gold, Silver and Bronze Distribution",
    hole=0.4
)

st.plotly_chart(fig4, use_container_width=True)


# ==========================================
# 10. TOP 10 SPORTS
# ==========================================

st.subheader("🏃 Top 10 Popular Sports")

sport_data = (
    filtered_df.groupby('Sport')['ID']
    .nunique()
    .reset_index()
)

sport_data.columns = ['Sport', 'Athletes']

sport_data = sport_data.sort_values(
    by='Athletes',
    ascending=False
).head(10)

fig5 = px.bar(
    sport_data,
    x='Athletes',
    y='Sport',
    orientation='h',
    color='Athletes',
    title="Top 10 Sports by Athlete Participation"
)

st.plotly_chart(fig5, use_container_width=True)


# ==========================================
# 11. AGE DISTRIBUTION
# ==========================================

st.subheader("👤 Athlete Age Distribution")

fig6 = px.histogram(
    filtered_df,
    x='Age',
    color='Sex',
    nbins=30,
    title="Age Distribution of Athletes"
)

st.plotly_chart(fig6, use_container_width=True)


# ==========================================
# 12. HEIGHT VS WEIGHT
# ==========================================

st.subheader("📏 Height vs Weight Analysis")

height_weight = filtered_df.dropna(
    subset=['Height', 'Weight']
)

fig7 = px.scatter(
    height_weight,
    x='Height',
    y='Weight',
    color='Sex',
    hover_data=['Name', 'Sport'],
    title="Relationship Between Height and Weight"
)

st.plotly_chart(fig7, use_container_width=True)


# ==========================================
# 13. MEDAL ANALYSIS BY GENDER
# ==========================================

st.subheader("🏅 Medal Analysis by Gender")

gender_medals = medal_df.groupby(
    ['Sex', 'Medal']
).size().reset_index(name='Count')

fig8 = px.bar(
    gender_medals,
    x='Sex',
    y='Count',
    color='Medal',
    barmode='group',
    title="Medal Distribution by Gender"
)

st.plotly_chart(fig8, use_container_width=True)


# ==========================================
# 14. TOP ATHLETES
# ==========================================

st.subheader("🏆 Top 10 Medal Winning Athletes")

athlete_medals = (
    medal_df.groupby('Name')['Medal']
    .count()
    .reset_index()
)

athlete_medals.columns = ['Athlete', 'Total Medals']

athlete_medals = athlete_medals.sort_values(
    by='Total Medals',
    ascending=False
).head(10)

fig9 = px.bar(
    athlete_medals,
    x='Athlete',
    y='Total Medals',
    color='Total Medals',
    title="Top 10 Medal Winning Athletes"
)

st.plotly_chart(fig9, use_container_width=True)


# ==========================================
# 15. DATASET DISPLAY
# ==========================================

st.subheader("📋 Olympic Dataset")

st.write("Filtered Olympic Dataset")

st.dataframe(
    filtered_df,
    use_container_width=True
)


# ==========================================
# 16. DOWNLOAD DATASET
# ==========================================

csv = filtered_df.to_csv(index=False).encode('utf-8')

st.download_button(
    label="📥 Download Filtered Dataset",
    data=csv,
    file_name="olympic_analysis.csv",
    mime="text/csv"
)


# ==========================================
# 17. FOOTER
# ==========================================

st.markdown("---")

st.markdown(
    "<center>🏅 Olympic Games Data Analysis | "
    "Developed using Python, Pandas, Plotly and Streamlit</center>",
    unsafe_allow_html=True
)