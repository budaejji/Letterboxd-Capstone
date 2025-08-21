import pandas as pd
import streamlit as st
import altair as alt

movies = pd.read_csv("../data/processed/merged_enriched_movies.csv")

# Find movies with biggest differential in rating vs power_users_rating
movies["rating_diff"] = movies["rating"] - movies["power_users_rating"]
higher_rated_by_avg_users = movies.loc[movies["rating_diff"].nlargest(10).index]

higher_rated_by_avg_users_long_data = higher_rated_by_avg_users.melt(
    id_vars="movie_title",
    value_vars=["rating", "power_users_rating"],
    var_name="rating_type",
    value_name="avg_rating"
)

# Display these side by side in a bar chart
higher_rated_by_avg_users_chart = alt.Chart(
    higher_rated_by_avg_users_long_data
).mark_bar().encode(
    x=alt.X(
        "movie_title",
        sort=alt.EncodingSortField(
            field="rating_diff",
            order="descending"
        ),
        title="Movie Title"),
    y=alt.Y(
        "avg_rating",
        title="Average Rating"
    ),
    color=alt.Color(
        "rating_type",
        scale=alt.Scale(
            domain=['rating', 'power_users_rating'],
            range=['#40bcf4', '#F27405']
        )
    ),
    xOffset="rating_type:N"
).properties(
    title="Movies Rated Higher by Average User",
    height=600
)

st.altair_chart(higher_rated_by_avg_users_chart, use_container_width=True)

# Find movies with biggest differential in power users rating vs rating
movies["rating_diff"] = movies["power_users_rating"] - movies["rating"]
higher_rated_by_power_users = movies.loc[movies["rating_diff"].nlargest(10).index]

higher_rated_by_power_users_long_data = higher_rated_by_power_users.melt(
    id_vars="movie_title",
    value_vars=["rating", "power_users_rating"],
    var_name="rating_type",
    value_name="avg_rating"
)

# Display these side by side in a bar chart
higher_rated_by_power_users_chart = alt.Chart(
    higher_rated_by_power_users_long_data
).mark_bar().encode(
    x=alt.X(
        "movie_title",
        sort=alt.EncodingSortField(
            field="rating_diff",
            order="descending"
        ),
        title="Movie Title"),
    y=alt.Y(
        "avg_rating",
        title="Average Rating",
        scale=alt.Scale(domain=[0, 9])
    ),
    color=alt.Color(
        "rating_type",
        scale=alt.Scale(
            domain=['rating', 'power_users_rating'],
            range=['#40bcf4', '#F27405']
        )
    ),
    xOffset="rating_type:N"
).properties(
    title="Movies Rated Higher by Power Users",
    height=600
)

st.altair_chart(higher_rated_by_power_users_chart, use_container_width=True)
