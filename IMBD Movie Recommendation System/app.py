import streamlit as st
import pandas as pd
import requests

def recommend(movie):
    movie_index = list(movies_list).index(movie)
    distances = similarity[movie_index]
    similar_movie_list = sorted(list(enumerate(distances)), reverse=True, key=lambda x:x[1])[1:6]

    movies_name = []
    movies_poster = []
    for x in similar_movie_list:
        movie_title=movies_list[x[0]]
        movies_name.append(movie_title)
        movies_poster.append(movies_df[movies_df['Series_Title'] == movie_title]['Poster_Link'].values[0])

    return movies_name, movies_poster

# Load the data
movies_df = pd.read_pickle('movies.pkl')
movies_list = movies_df['Series_Title'].values
similarity = pd.read_pickle('similarity_matrix.pkl')

# Streamlit UI starts here
st.set_page_config(page_title='Movie Recommender', page_icon=':clapper:', layout='wide')

# Custom CSS to set background, text color, and selectbox styles
st.markdown("""
    <style>
        .main {
            background-color: black;
            color: white;
        }
        .stButton button {
            border-radius: 8px;
            font-weight: bold;
            background-color: #4CAF50;
            color: white;
        }
        .stSelectbox div[data-baseweb="select"] > div {
            background-color: #333333;
            color: white;
            border-radius: 8px;
        }
        .stSelectbox div[data-baseweb="select"] > div > div {
            color: white;
        }
        h1, h2, h3, h4, h5, h6, p, div {
            color: white;
        }
    </style>
    """, unsafe_allow_html=True)

# Header Section
st.title('🍿 Movie Recommender System')
st.write("## Select a movie and get recommendations tailored just for you!")

# Layout for movie selection
with st.container():
    st.write("### 🎬 Choose a Movie")
    Selected_movie = st.selectbox('', movies_list)

# Button to trigger recommendations
if st.button('Recommend', help='Click to get movie recommendations based on your choice'):
    with st.spinner('Finding recommendations...'):
        recommended_movies, recommended_posters = recommend(Selected_movie)
    
    # Display recommendations in a well-formatted way
    st.write("### 🎥 Movies you might like:")
    num_cols = min(5, len(recommended_movies))  # Adjust 5 if you have a different number of movies
    cols = st.columns(num_cols)  # Create columns dynamically
    
    for i, (movie, poster) in enumerate(zip(recommended_movies, recommended_posters)):
        if i < num_cols:  # Ensure we do not exceed the number of available columns
            with cols[i]:
                st.image(poster, use_column_width=True)
                st.write(f"**{movie}**")
        else:
            break  # Break the loop if there are more movies than columns
    
    # Provide an option to explore another movie
    st.markdown("---")
    st.write("Want to explore another movie? Just select one from the dropdown above!")

