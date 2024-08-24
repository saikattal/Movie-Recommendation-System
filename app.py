import pickle
import streamlit as st
import requests
import gdown
import os

@st.cache_resource

def fetch_poster(movie_id):
    url = "https://api.themoviedb.org/3/movie/{}?api_key=8265bd1679663a7ea12ac168da84d2e8&language=en-US".format(movie_id)
    data = requests.get(url)
    data = data.json()
    poster_path = data['poster_path']
    full_path = "https://image.tmdb.org/t/p/w500/" + poster_path
    return full_path

def recommend(movie):
    index = movies[movies['title'] == movie].index[0]
    distances = sorted(list(enumerate(similarity[index])), reverse=True, key=lambda x: x[1])
    recommended_movie_names = []
    recommended_movie_posters = []
    for i in distances[1:6]:
        # fetch the movie poster
        movie_id = movies.iloc[i[0]].movie_id
        recommended_movie_posters.append(fetch_poster(movie_id))
        recommended_movie_names.append(movies.iloc[i[0]].title)

    return recommended_movie_names,recommended_movie_posters

def download_from_gdrive():
    file_id = '1QcFi4Ir1hzspWQVGTSCEP4rA2h2VVseJ'
    url1 = f'https://drive.google.com/uc?id={file_id}'


    output1 = 'artifacts/movie_list.pkl'
    os.makedirs("artifacts/", exist_ok=True)
    if not os.path.exists(output1):

        gdown.download(url1, output1, quiet=False)

    file_id = '1OCM9Ldvd35tOmQ7cj6mc0jtOgoTIK1yS'
    url2 = f'https://drive.google.com/uc?id={file_id}'


    output2 = 'artifacts/similarity.pkl'
    
    if not os.path.exists(output2):
        
        gdown.download(url2, output2, quiet=False)


st.set_page_config(page_title="Movie Recommendation System",page_icon=":movie_camera:")

st.header("Movie Recommendation System using Machine Learning")

with st.spinner("Loading.."):
    download_from_gdrive()
    
output1 = 'artifacts/movie_list.pkl'
output2 = 'artifacts/similarity.pkl'
with open(output1, 'rb') as file:
    movies = pickle.load(file)

with open(output2, 'rb') as file:
    similarity = pickle.load(file)

movie_list = movies['title'].values
selected_movie = st.selectbox(
    "Type or select a movie from the dropdown",
    movie_list
)

if st.button('Show recommendations'):
    recommended_movies, recommended_posters = recommend(selected_movie)
    st.subheader('Recommended Movies based on your selection:')
    col1,col2,col3,col4,col5=st.columns(5)
    cols=[col1,col2,col3,col4,col5]
    for i, movie in enumerate(recommended_movies):
        with cols[i]:
            st.image(recommended_posters[i], caption=movie)
       
    
    