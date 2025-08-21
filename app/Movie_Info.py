import pandas as pd
import streamlit as st

movies = pd.read_csv("../data/processed/merged_enriched_movies.csv")
user_ratings = pd.read_csv("../data/processed/cleaned_user_ratings.csv")
aggregated_user_ratings = pd.read_csv("../data/processed/aggregated_user_ratings.csv")

st.set_page_config(
    page_title="Letterboxd Ratings Dashboard",
    page_icon=":movie_camera:",
    layout="wide"
)

st.markdown(
        """
        <style>
        @import url('https://fonts.googleapis.com/css2?family=Abril+Fatface&display=swap');

        .homepage-title {
            font-family: 'Abril Fatface', serif !important;
            font-weight: 400;
            font-style: normal;
            font-size: 48px !important;
            color: #FFFFFF !important;
            text-align: center;
        }
        </style>
        <h1 class="homepage-title">Letterboxd Movie Ratings Analysis</h1>
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
    This app was built with the purpose of analysing Letterboxd
    data to identify rating trends across different attributes.
    </h6>
    <h6 class="homepage-text">
    Data from Letterboxd's users with the most ratings on the site 
    (henceforth known as "Power Users") was compared against the overall user
    base to identify any significant differences in rating behavior between the
    average consumer and a so-called "movie buff".
    </h6>
    <h6 class="homepage-text">
    On this page you can choose a movie to display its various attributes
    and compare its rating on Letterboxd to its average rating by our Power
    Users. Use the sidebar to navigate to different pages that explore rating
    trends and other aspects of the data.
    </h6>
    <br></br>
    """,
    unsafe_allow_html=True
)

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
    <h1 class="homepage-header">Movie Library</h1>
    """,
    unsafe_allow_html=True
)

average_rating = round(movies["rating"].mean(), 2)

movies = movies.sort_values(by="movie_id")
# create dropdown menu of all the movies from movie_id
movie_id = movies["movie_id"].unique().tolist()
options = ["Select a movie"] + movie_id
selected_movie = st.selectbox("Select a movie", options)

if selected_movie != "Select a movie":
    movie_title = movies[movies['movie_id'] == selected_movie]['movie_title'].values[0]
    genres = movies[movies['movie_id'] == selected_movie]['genres'].values[0].strip("[]").replace("'", "")
    original_language = movies[movies['movie_id'] == selected_movie]['original_language'].values[0]
    poster = movies[movies['movie_id'] == selected_movie]['image_url'].values[0]
    runtime = movies[movies['movie_id'] == selected_movie]['runtime'].values[0]
    year_released = movies[movies['movie_id'] == selected_movie]['year_released'].values[0]
    rating = movies[movies['movie_id'] == selected_movie]['rating'].values[0]
    power_users_rating = movies[movies['movie_id'] == selected_movie]['power_users_rating'].values[0]
    ratings_count = movies[movies['movie_id'] == selected_movie]['ratings_count'].values[0]

    st.markdown(
        f"""
        <style>
        @import url('https://fonts.googleapis.com/css2?family=Abril+Fatface&display=swap');

        .custom-title {{
            font-family: 'Abril Fatface', serif !important;
            font-weight: 400;
            font-style: normal;
            font-size: 48px !important;
            color: #00e054 !important;
            text-align: center;
        }}
        </style>
        <h1 class="custom-title">{movie_title}</h1>
        """,
        unsafe_allow_html=True
    )

    st.write("")
    st.write("")

    col1, col2, col3, col4, col5 = st.columns([3, 0.7, 2.8, 1.3, 2])

    with col1:
        st.markdown(
            f"""
            <style>
            @import url('https://fonts.googleapis.com/css2?family=Abril+Fatface&display=swap');
            @import url('https://fonts.googleapis.com/css2?family=Homenaje&display=swap');

            .custom-header {{
                font-family: 'Abril Fatface', serif !important;
                font-weight: 400;
                font-style: normal;
                font-size: 20px !important;
                color: #40bcf4 !important;
                text-align: left;
            }}
            
            .custom-text {{
                font-family: 'Homenaje', sans-serif !important;
                font-weight: 400;
                font-style: normal;
                font-size: 20px !important;
                color: #F27405 !important;
                text-align: left;
            }}
            
            </style>
            <h6 class="custom-header">Genres</h6>
            <h6 class="custom-text">--- {genres}</h6>
            <h6 class="custom-header">Original Language</h6>
            <h6 class="custom-text">--- {original_language}</h6>
            <h6 class="custom-header">Runtime</h6>
            <h6 class="custom-text">--- {runtime} minutes</h6>
            <h6 class="custom-header">Year Released</h6>
            <h6 class="custom-text">--- {year_released}</h6>
            """,
            unsafe_allow_html=True
        )
        
    with col3:
        st.image(
            f"https://a.ltrbxd.com/resized/{poster}.jpg")
    with col5:
        st.metric(label="Rating", value=rating)
        st.metric(label="Power Users' Rating", value=power_users_rating, delta=round(power_users_rating - rating, 2))
        st.metric(label="№ Power Users' Ratings", value=ratings_count)
