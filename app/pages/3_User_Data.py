import pandas as pd
import streamlit as st 
import altair as alt

movies = pd.read_csv("../data/processed/merged_enriched_movies.csv")
user_ratings = pd.read_csv("../data/processed/cleaned_user_ratings.csv")
aggregated_user_ratings = pd.read_csv("../data/processed/aggregated_user_ratings.csv")

with st.expander("Aggregated User Ratings Data"):
    st.write(aggregated_user_ratings)

users_average = round(aggregated_user_ratings["user_average_rating"].mean(), 2)
average_rating_count = round(aggregated_user_ratings["rating_count"].mean())

# Filter out users with less than 50 rating count
filtered_user_ratings = aggregated_user_ratings[aggregated_user_ratings["rating_count"] >= 50]

# Find correlation coefficient for runtime vs average rating
corr = filtered_user_ratings["rating_count"].corr(filtered_user_ratings["user_average_rating"])

col1, col2, col3, col4, col5 = st.columns([0.3, 1, 1, 1, 0.3])
with col2:
    st.metric(label="Power users average rating", value=users_average)
with col3:
    st.metric(label="Average number of ratings per user", value=average_rating_count)
with col4:
    st.metric(label="Correlation coefficient", value=f"{corr:.2f}")


rating_avg_vs_rating_count_scatter = (
    alt.Chart(filtered_user_ratings)
    .mark_circle(size=10)
    .encode(
        x="rating_count",
        y="user_average_rating",
        tooltip=["user_id", "rating_count", "user_average_rating"],
        color=alt.value("#40bcf4")
    )
    .properties(
        title="User Ratings: Average vs Count",
        width=700,
        height=600
    )
    .interactive()
)

regression = rating_avg_vs_rating_count_scatter.transform_regression(
    "rating_count", "user_average_rating"
).mark_line().encode(color=alt.value("#F27405"))

st.altair_chart(rating_avg_vs_rating_count_scatter + regression, use_container_width=True)

# Find harsh critics
harsh_critics = filtered_user_ratings[
    (
        filtered_user_ratings["user_average_rating"] < users_average - 2
    ) & (
        filtered_user_ratings["rating_count"] > 350
    )
].reset_index(drop=True)

st.markdown(
    """
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Abril+Fatface&display=swap');

    .homepage-header {
        font-family: 'Abril Fatface', serif !important;
        font-weight: 400;
        font-style: normal;
        font-size: 30px !important;
        color: #FFFFFF !important;
        text-align: center;
    }
    </style>
    <h1 class="homepage-header">Harsh Critics</h1>
    """,
    unsafe_allow_html=True
)

st.markdown(
    """
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Homenaje&display=swap');

    .homepage-text {
        font-family: 'Homenaje', sans-serif !important;
        font-weight: 400;
        font-style: normal;
        font-size: 20px !important;
        color: #FFFFFF !important;
        text-align: left;
    }

    </style>
    <br></br>
    <h6 class="homepage-text">
    Harsh critics are defined as users whose average rating is
    2 or more points below the overall user average. We've identified
    these users to see which films are still rated highly among them.
    </h6>
    <br></br>
    """,
    unsafe_allow_html=True
)

st.write(harsh_critics)

# List of user_ids who are harsh critics
harsh_critics_options = harsh_critics["user_id"]

# User ratings table filtered for only harsh critics
user_ratings_filtered = user_ratings[user_ratings["user_id"].isin(harsh_critics_options)]
# Find the top 20 films as rated by harsh critics
user_ratings_filtered = user_ratings_filtered.groupby("movie_id").agg(
    {"rating_val": ["mean", "count"]}
).reset_index()
user_ratings_filtered.columns = ["movie_id", "average_rating", "rating_count"]
user_ratings_filtered["average_rating"] = user_ratings_filtered["average_rating"].round(2)
user_ratings_filtered = user_ratings_filtered.sort_values(by="average_rating", ascending=False).head(20)
user_ratings_filtered.reset_index(drop=True, inplace=True)
# Display top 20 films as rated by harsh critics

st.markdown(
    """
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Homenaje&display=swap');

    .homepage-text {
        font-family: 'Homenaje', sans-serif !important;
        font-weight: 400;
        font-style: normal;
        font-size: 20px !important;
        color: #FFFFFF !important;
        text-align: left;
    }

    </style>
    <br></br>
    <h6 class="homepage-text">
    Top 20 films as rated by harsh critics:
    </h6>
    <br></br>
    """,
    unsafe_allow_html=True
)
st.write(user_ratings_filtered)

# Select a harsh critic
harsh_critic_chosen = st.selectbox("Select a harsh critic", harsh_critics_options)

# Show user_ratings table where user_id is the selected harsh critic
harsh_critic_ratings = user_ratings[user_ratings["user_id"] == harsh_critic_chosen]
harsh_critic_ratings.sort_values(by="rating_val", ascending=False, inplace=True)
st.write(harsh_critic_ratings)