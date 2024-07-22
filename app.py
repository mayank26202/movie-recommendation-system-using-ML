# 

import pickle
import streamlit as st
import requests

# Function to fetch movie poster path
def fetch_poster(movie_id):
    url = f"https://api.themoviedb.org/3/movie/{movie_id}?api_key=7802d460e9e7a3c69525f0d256e19e8a"
    try:
        response = requests.get(url)
        response.raise_for_status()  # Check if the request was successful
        data = response.json()
        
        poster_path = data.get('poster_path')
        if poster_path:
            full_path = "https://image.tmdb.org/t/p/w500/" + poster_path
        else:
            full_path = "URL to a default image or placeholder"  # Handle missing poster path
            st.warning(f"Poster path not found for movie ID {movie_id}.")
        
        return full_path
    
    except requests.exceptions.RequestException as e:
        st.error(f"HTTP request failed: {e}")
        return "URL to a default image or placeholder"  # Handle request failure

# Function to recommend movies
def recommend(movie):
    index = movies[movies['title'] == movie].index[0]
    distances = sorted(list(enumerate(similarity[index])), reverse=True, key=lambda x: x[1])
    recommended_movies_name = []
    recommended_movies_poster = []
    
    for i in distances[1:6]:
        movie_id = movies.iloc[i[0]].movie_id
        recommended_movies_name.append(movies.iloc[i[0]].title)
        recommended_movies_poster.append(fetch_poster(movie_id))
    
    return recommended_movies_name, recommended_movies_poster

# Streamlit header
st.header("Movie Recommendation System Using Machine Learning")

# Load the pickled data
movies = pickle.load(open('artificats/movie_list.pkl', 'rb'))
similarity = pickle.load(open('artificats/similarity.pkl', 'rb'))

# Movie selection box
movie_list = movies['title'].values
selected_movie = st.selectbox(
    'Type or select a movie to get recommendation',
    movie_list
)

# Show recommendations on button click
if st.button('Show recommendation'):
    recommended_movies_name, recommended_movies_poster = recommend(selected_movie)
    
    col1, col2, col3, col4, col5 = st.columns(5)
    
    with col1:
        st.text(recommended_movies_name[0])
        st.image(recommended_movies_poster[0])
    
    with col2:
        st.text(recommended_movies_name[1])
        st.image(recommended_movies_poster[1])
    
    with col3:
        st.text(recommended_movies_name[2])
        st.image(recommended_movies_poster[2])
    
    with col4:
        st.text(recommended_movies_name[3])
        st.image(recommended_movies_poster[3])
    
    with col5:
        st.text(recommended_movies_name[4])
        st.image(recommended_movies_poster[4])
