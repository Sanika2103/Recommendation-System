
#importing required libraries

import streamlit as st
import pickle
import pandas as pd
import requests

#Open files
movies_dict = pickle.load(open('movie_dict.pkl','rb'))
movies = pd.DataFrame(movies_dict)
genres_db = pickle.load(open('genres.pkl','rb'))
genre = pd.DataFrame(genres_db)

#function to display poster for a movie

def fetch_poster(movie_id):
     response = requests.get('https://api.themoviedb.org/3/movie/{}?api_key=2f618bd4e6cb76cc612b9be6fee82cb0&language=en-US'.format(movie_id))
     data = response.json()
     return "https://image.tmdb.org/t/p/w500/" + data['poster_path']

#function to recommend movie

def recommend(movie):
     index = movies[movies['title'] == movie].index[0]
     distances = sorted(list(enumerate(similarity[index])), reverse=True, key=lambda x: x[1])
     recommended_movies = []
     recommended_movies_posters = []
     for i in distances[1:6]:
          movie_id = movies.iloc[i[0]].movie_id
          recommended_movies.append(movies.iloc[i[0]].title)
          recommended_movies_posters.append(fetch_poster(movie_id))
     return recommended_movies,recommended_movies_posters

#function to recommend movie based on genre

def recommend_genre(gen):
    genre_dict = {}
    N = 5
    recommended_genre = []
    recommended_genre_posters = []

    for i in range(genre['genres'].count()):
        if i in genre.index :
            if gen in genre['genres'][i]:
                genre_dict[i] = genre['votes'][i]
    topN = sorted(genre_dict.items(), key = lambda x: x[1], reverse=True)
    for i in range(N):
        if i < len(topN):
            genre_id = genre.iloc[topN[i][0]].movie_id
            recommended_genre.append(genre['name'][topN[i][0]])
            recommended_genre_posters.append(fetch_poster(genre_id))
        else:
            break
    return recommended_genre,recommended_genre_posters


# Top rated movies based on votes

def recommend_top():
    N = 5
    recommended_top = []
    recommended_top_posters = []
    gen_db = genre.sort_values(by="votes", ascending=False, kind="mergesort").head(N)
    for index,row in gen_db.iterrows():
        gen_id = gen_db['movie_id'][index]
        recommended_top.append(gen_db['name'][index])
        recommended_top_posters.append(fetch_poster(gen_id))
    return recommended_top, recommended_top_posters

# Open similarity file

similarity = pickle.load(open('similarity.pkl','rb'))
st.title('Movie Recommender System')
selected_movie_name = st.selectbox(
     'Search for a movie',
     movies['title'].values)
if st.button('Recommend'):
     names,posters = recommend(selected_movie_name)

     col1, col2, col3, col4, col5 = st.columns(5)
     with col1:
          st.text(names[0])
          st.image(posters[0])
     with col2:
          st.text(names[1])
          st.image(posters[1])

     with col3:
          st.text(names[2])
          st.image(posters[2])
     with col4:
          st.text(names[3])
          st.image(posters[3])
     with col5:
          st.text(names[4])
          st.image(posters[4])

# basesd on rating

st.subheader('Search for your favourite genre')
selected_genre_name = st.selectbox(
     'Select a genre',
     ('Action', 'Adventure','Animation', 'Crime', 'Comedy', 'Drama', 'Family', 'Fantasy','Horror',
      'History','Music','Mystery', 'Thriller', 'Romance',
      'ScienceFiction','War','Western'))
if st.button('Recommend '):
     title,poster = recommend_genre(selected_genre_name)
     col1, col2, col3, col4, col5 = st.columns(5)
     with col1:
         st.text(title[0])
         st.image(poster[0])
     with col2:
         st.text(title[1])
         st.image(poster[1])

     with col3:
         st.text(title[2])
         st.image(poster[2])
     with col4:
         st.text(title[3])
         st.image(poster[3])
     with col5:
         st.text(title[4])
         st.image(poster[4])

# top rated

st.subheader('Top Rated')

if st.button('Show top rated'):
     title,poster = recommend_top()
     col1, col2, col3, col4, col5 = st.columns(5)

     with col1:
         st.text(title[0])
         st.image(poster[0])
     with col2:
         st.text(title[1])
         st.image(poster[1])

     with col3:
         st.text(title[2])
         st.image(poster[2])
     with col4:
         st.text(title[3])
         st.image(poster[3])
     with col5:
         st.text(title[4])
         st.image(poster[4])

