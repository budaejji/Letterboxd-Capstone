import pandas as pd
import streamlit as st
import altair as alt
from src.transform.clean_movies import convert_genres_to_list

movies = pd.read_csv("../data/processed/merged_enriched_movies.csv")

attributes = ['Language', 'Runtime', 'Genre', 'Decade Released']
options = ["Select an attribute"] + attributes

selected_attribute = st.selectbox("Select an attribute to view its rating trends", options)

if selected_attribute != "Select an attribute":
    if selected_attribute == 'Language':
        # Bar chart comparing average ratings by language

        # Aggregate average ratings by language
        average_rating_by_language = movies.groupby("original_language").agg(
            letterboxd_avg=('rating', 'mean'),
            user_avg=('power_users_rating', 'mean')
        ).reset_index()

        # Round averages to 2dp
        average_rating_by_language["letterboxd_avg"] = average_rating_by_language["letterboxd_avg"].round(2)
        average_rating_by_language["user_avg"] = average_rating_by_language["user_avg"].round(2)

        # Sort languages by highest letterboxd average
        sorted_languages = average_rating_by_language.sort_values(
            'letterboxd_avg',
            ascending=False
        )['original_language'].tolist()

        # Convert to long format for Altair
        language_long_data = average_rating_by_language.melt(
            id_vars="original_language",
            value_vars=["letterboxd_avg", "user_avg"],
            var_name="rating_type",
            value_name="avg_rating"
        )

        # Plot grouped bar chart
        rating_vs_language_chart = alt.Chart(language_long_data).mark_bar().encode(
            x=alt.X("original_language", sort=sorted_languages, title="Language"),
            y=alt.Y("avg_rating", title="Average Rating"),
            color=alt.Color(
                "rating_type",
                title="Rating Type",
                scale=alt.Scale(
                    domain=['letterboxd_avg', 'user_avg'],
                    range=['#40bcf4', '#F27405']
                )
            ),
            xOffset="rating_type:N"
        ).properties(
            title="Average Movie Ratings by Language",
            height=600
        )

        st.altair_chart(rating_vs_language_chart, use_container_width=True)
        
        unique_languages = movies["original_language"].unique().tolist()
        
        language_options = ["Select a language"] + unique_languages
        selected_language = st.selectbox("Select a language to view its top rated films", language_options)
        
        if selected_language != "Select a language":
            # Filter movies by selected language
            filtered_movies = movies[movies["original_language"] == selected_language]

            # Get top rated films
            top_rated_films = filtered_movies.nlargest(5, "rating")

            # Display top rated films
            st.write(f"### Top Rated Films - <{selected_language}>")
            for index, row in top_rated_films.iterrows():
                st.write(f"- {row['movie_title']} ({row['year_released']}): {row['rating']}")
    
    elif selected_attribute == 'Runtime':

        # Rating vs runtime

        # Drop movies where runtime is 0
        movies_with_runtime = movies[movies["runtime"] > 0]

        movies_with_runtime = movies_with_runtime.rename(columns={"rating": "letterboxd_avg", "power_users_rating": "user_avg"})

        # Convert to long format for Altair
        runtime_long_data = movies_with_runtime.melt(
            id_vars=['movie_title', 'runtime'],
            value_vars=['letterboxd_avg', 'user_avg'],
            var_name='rating_type',
            value_name='rating_value'
        )

        # Scatterplot of runtime vs rating and power_users_rating
        runtime_vs_rating_plot = alt.Chart(
            runtime_long_data
        ).mark_circle(
            size=15,
            opacity=0.6
        ).encode(
            x=alt.X(
                "runtime",
                title="Runtime (minutes)",
                scale=alt.Scale(domain=[70, 250])
            ),
            y=alt.Y(
                "rating_value",
                title="Rating",
                scale=alt.Scale(domain=[3, 10])
            ),
            color=alt.Color(
                "rating_type",
                title="Rating Type",
                scale=alt.Scale(
                    domain=['letterboxd_avg', 'user_avg'],
                    range=['#40bcf4', '#F27405']
                )
            ),
            tooltip=["movie_title", "runtime", "rating_type", "rating_value"]
        ).properties(
            width=600,
            height=600,
            title="Movie Runtime vs Rating"
        ).interactive()

        # Regression lines to show trends in runtime vs rating
        regression_lines = alt.Chart(runtime_long_data).transform_regression(
            "runtime", "rating_value", groupby=["rating_type"]
        ).mark_line().encode(
            x="runtime:Q",
            y="rating_value:Q",
            color=alt.Color("rating_type:N", scale=alt.Scale(
                domain=['letterboxd_avg', 'user_avg'],
                range=['#40bcf4', '#F27405'])
            )
        )

        # Combine plot with regression lines
        runtime_chart_combined = runtime_vs_rating_plot + regression_lines
        st.altair_chart(runtime_chart_combined, use_container_width=True)

        # Show correlation coefficients
        runtime_vs_rating_corr = movies["runtime"].corr(movies["rating"])
        runtime_vs_users_rating_corr = movies["runtime"].corr(movies["power_users_rating"])

        st.write(
            f"Correlation coefficient for runtime vs Letterboxd rating: "
            f"{runtime_vs_rating_corr:.2f}"
        )
        st.write(
            f"Correlation coefficient for runtime vs users rating: "
            f"{runtime_vs_users_rating_corr:.2f}"
        )

    elif selected_attribute == 'Genre':
        # Rating vs genres

        # When table is saved as a CSV list converts back to string.
        # Want to reconvert it so we can work with it.
        movies = convert_genres_to_list(movies)

        # Split up movies with multiple genres, group by each genre,
        # then find the average rating
        average_rating_by_genre = movies.explode('genres').groupby('genres').agg(
            letterboxd_avg=('rating', 'mean'),
            user_avg=('power_users_rating', 'mean')
        ).reset_index()

        # Round averages to 2dp
        average_rating_by_genre["letterboxd_avg"] = average_rating_by_genre["letterboxd_avg"].round(2)
        average_rating_by_genre["user_avg"] = average_rating_by_genre["user_avg"].round(2)

        # Sort genres by highest letterboxd average
        sorted_genres = average_rating_by_genre.sort_values(
            'letterboxd_avg',
            ascending=False
        )['genres'].tolist()

        # Convert to long format for Altair
        genre_long_data = average_rating_by_genre.melt(
            id_vars="genres",
            value_vars=["letterboxd_avg", "user_avg"],
            var_name="rating_type",
            value_name="avg_rating"
        )

        # Create bar chart and display it
        rating_vs_genre_chart = alt.Chart(genre_long_data).mark_bar().encode(
            x=alt.X("genres", sort=sorted_genres, title="Genre"),
            y=alt.Y(
                "avg_rating",
                title="Average Rating",
                scale=alt.Scale(domain=[0, 9])
                ),
            color=alt.Color(
                "rating_type",
                title="Rating Type",
                scale=alt.Scale(
                    domain=['letterboxd_avg', 'user_avg'],
                    range=['#40bcf4', '#F27405']
                )
            ),
            xOffset="rating_type:N" 
        ).properties(
            title="Average Movie Ratings by Genre",
            height=600
        )

        st.altair_chart(rating_vs_genre_chart, use_container_width=True)
        
    elif selected_attribute == 'Decade Released':
        movies['decade'] = (movies['year_released'] // 10) * 10

        # Group by decade and calculate average ratings
        average_ratings_by_decade = movies.groupby("decade").agg(
            letterboxd_avg=("rating", "mean"),
            user_avg=("power_users_rating", "mean")
        ).reset_index()

        average_ratings_by_decade["letterboxd_avg"] = average_ratings_by_decade["letterboxd_avg"].round(2)
        average_ratings_by_decade["user_avg"] = average_ratings_by_decade["user_avg"].round(2)

        # Melt for Altair
        decade_long = average_ratings_by_decade.melt(
            id_vars="decade",
            value_vars=["letterboxd_avg", "user_avg"],
            var_name="rating_type",
            value_name="avg_rating"
        )

        # Area chart
        decade_chart = alt.Chart(decade_long).mark_line(point=True).encode(
            x=alt.X('decade:O', title='Decade'),
            y=alt.Y(
                'avg_rating:Q',
                title='Average Rating',
                scale=alt.Scale(domain=[6.5, 9])
            ),
            color=alt.Color('rating_type:N', 
                            title='Rating Type', 
                            scale=alt.Scale(
                                domain=['letterboxd_avg', 'user_avg'],
                                range=['#40bcf4', '#F27405']
                            )
                        ),
            tooltip=['decade', 'rating_type', 'avg_rating']
        ).properties(
            title='Average Movie Ratings by Decade',
            width=700,
            height=600
        ).interactive()

        st.altair_chart(decade_chart, use_container_width=True)
