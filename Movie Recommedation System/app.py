import streamlit as st
import pandas as pd

def recommend(movie):
    movie_index = list(movies_list).index(movie)
    distances = similarity[movie_index]
    similar_movie_list = sorted(list(enumerate(distances)), reverse=True, key=lambda x:x[1])[1:6]

    movies_name = []
    for x in similar_movie_list:
        movies_name.append(movies_list[x[0]])

    return movies_name

# Load the data
movies_df = pd.read_pickle('movies.pkl')
movies_list = movies_df['title'].values
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
        recommendations = recommend(Selected_movie)
    
    # Display recommendations in a well-formatted way
    st.write("### 🎥 Movies you might like:")
    for i, movie in enumerate(recommendations, 1):
        st.write(f"**{i}.** {movie}")
    
    # Provide an option to explore another movie
    st.markdown("---")
    st.write("Want to explore another movie? Just select one from the dropdown above!")

