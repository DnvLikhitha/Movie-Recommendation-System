import streamlit as st
import pickle
import pandas as pd
import requests

def fetch_poster(movie_id):
    url = f"https://api.themoviedb.org/3/movie/{movie_id}?api_key=876c08e96099aa7bbbb677424d11c143"
    try:
        response = requests.get(url, timeout=10)
        response.raise_for_status()
        data = response.json()
        poster_path = data.get('poster_path')
        if poster_path:
            full_path = "https://image.tmdb.org/t/p/w500" + poster_path
            return full_path
        else:
            return "https://via.placeholder.com/500x750?text=No+Image+Available"
    except (requests.ConnectionError, requests.Timeout) as e:
        st.error(f"Connection error: {e}")
        return "https://via.placeholder.com/500x750?text=No+Image+Available"
    except Exception as e:
        st.error(f"An error occurred: {e}")
        return "https://via.placeholder.com/500x750?text=No+Image+Available"

movies_dict = pickle.load(open('movie_dict.pkl', 'rb'))
movies = pd.DataFrame(movies_dict)
similarity = pickle.load(open('similarity.pkl', 'rb'))

def recommend(movie):
    index = movies[movies['title'] == movie].index[0]
    distances = sorted(list(enumerate(similarity[index])), reverse=True, key=lambda x: x[1])
    recommended_movie_names = []
    recommended_movie_posters = []
    for i in distances[1:6]:
        movie_id = movies.iloc[i[0]].id
        recommended_movie_names.append(movies.iloc[i[0]].title)
        recommended_movie_posters.append(fetch_poster(movie_id))
    return recommended_movie_names, recommended_movie_posters

st.title("Movie Recommendation System")
selected_movie_name = st.selectbox('Select a Movie:', movies['title'].values)

if st.button('Recommend'):
    recommended_movie_names, recommended_movie_posters = recommend(selected_movie_name)
    col1, col2, col3, col4, col5 = st.columns(5)
    for i, col in enumerate([col1, col2, col3, col4, col5]):
        with col:
            st.text(recommended_movie_names[i])
            st.image(recommended_movie_posters[i])
