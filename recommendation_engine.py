import pandas as pd
import numpy as np
import ast
from nltk.stem.porter import PorterStemmer
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.metrics.pairwise import cosine_similarity
import pickle
import os

class MovieRecommender:
    def __init__(self, movies_csv, credits_csv):
        """Initialize the recommendation engine with movie and credit data"""
        self.movies = pd.read_csv(movies_csv)
        self.credits = pd.read_csv(credits_csv)
        self.new_df = None
        self.similarity = None
        self.cv = None
        self.ps = PorterStemmer()
        
    def convert_genres_keywords(self, obj):
        """Convert JSON string to list of names"""
        L = []
        try:
            for i in ast.literal_eval(obj):
                L.append(i['name'])
        except:
            pass
        return L
    
    def convert_cast(self, obj):
        """Convert JSON string to list of top 3 cast members"""
        L = []
        counter = 0
        try:
            for i in ast.literal_eval(obj):
                if counter != 3:
                    L.append(i['name'])
                    counter += 1
                else:
                    break
        except:
            pass
        return L
    
    def fetch_director(self, obj):
        """Extract director from crew JSON"""
        L = []
        try:
            for i in ast.literal_eval(obj):
                if i['job'] == 'Director':
                    L.append(i['name'])
        except:
            pass
        return L
    
    def stem_text(self, text):
        """Apply Porter stemming to text"""
        y = []
        for i in text.split():
            y.append(self.ps.stem(i))
        return " ".join(y)
    
    def preprocess_data(self):
        """Preprocess movies and credits data"""
        # Merge datasets
        self.movies = self.movies.merge(self.credits, on='title')
        
        # Select relevant columns
        self.movies = self.movies[['movie_id', 'title', 'genres', 'keywords', 'overview', 'cast', 'crew']]
        
        # Remove nulls
        self.movies.dropna(inplace=True)
        
        # Convert JSON strings to lists
        self.movies['genres'] = self.movies['genres'].apply(self.convert_genres_keywords)
        self.movies['keywords'] = self.movies['keywords'].apply(self.convert_genres_keywords)
        self.movies['cast'] = self.movies['cast'].apply(self.convert_cast)
        self.movies['crew'] = self.movies['crew'].apply(self.fetch_director)
        
        # Remove spaces from names
        self.movies['genres'] = self.movies['genres'].apply(lambda x: [i.replace(" ", "") for i in x])
        self.movies['keywords'] = self.movies['keywords'].apply(lambda x: [i.replace(" ", "") for i in x])
        self.movies['cast'] = self.movies['cast'].apply(lambda x: [i.replace(" ", "") for i in x])
        self.movies['crew'] = self.movies['crew'].apply(lambda x: [i.replace(" ", "") for i in x])
        
        # Split overview into words
        self.movies['overview'] = self.movies['overview'].apply(lambda x: x.split())
        
        # Combine all tags
        self.movies['tags'] = (self.movies['genres'] + self.movies['keywords'] + 
                               self.movies['cast'] + self.movies['crew'] + self.movies['overview'])
        
        # Create new dataframe with relevant columns
        self.new_df = self.movies[['movie_id', 'title', 'tags']].copy()
        self.new_df['tags'] = self.new_df['tags'].apply(lambda x: " ".join(x))
        self.new_df['tags'] = self.new_df['tags'].apply(lambda x: x.lower())
        self.new_df['tags'] = self.new_df['tags'].apply(self.stem_text)
    
    def build_similarity_matrix(self):
        """Build cosine similarity matrix"""
        self.cv = CountVectorizer(max_features=5000, stop_words='english')
        vectors = self.cv.fit_transform(self.new_df['tags']).toarray()
        self.similarity = cosine_similarity(vectors)
    
    def recommend(self, movie_title, num_recommendations=5):
        """Get recommendations for a movie"""
        try:
            movie_index = self.new_df[self.new_df['title'] == movie_title].index[0]
        except IndexError:
            return []
        
        distances = self.similarity[movie_index]
        movies_list = sorted(list(enumerate(distances)), reverse=True, key=lambda x: x[1])[1:num_recommendations+1]
        
        recommendations = []
        for i in movies_list:
            recommendations.append(self.new_df.iloc[i[0]]['title'])
        
        return recommendations
    
    def get_all_movies(self):
        """Get all movie titles"""
        return sorted(self.new_df['title'].tolist())
    
    def train(self):
        """Train the recommendation engine"""
        self.preprocess_data()
        self.build_similarity_matrix()
    
    def save_model(self, filepath):
        """Save the trained model"""
        with open(filepath, 'wb') as f:
            pickle.dump({
                'new_df': self.new_df,
                'similarity': self.similarity,
                'cv': self.cv,
                'ps': self.ps
            }, f)
    
    def load_model(self, filepath):
        """Load a trained model"""
        with open(filepath, 'rb') as f:
            data = pickle.load(f)
            self.new_df = data['new_df']
            self.similarity = data['similarity']
            self.cv = data['cv']
            self.ps = data['ps']
