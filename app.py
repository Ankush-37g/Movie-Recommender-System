import streamlit as st
import pandas as pd
import os
from recommendation_engine import MovieRecommender

# Set page configuration
st.set_page_config(
    page_title="🎬 Movie Recommender System",
    page_icon="🎬",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom styling with poster cards
st.markdown("""
    <style>
        .main {
            padding: 2rem;
        }
        .title-text {
            font-size: 3rem;
            font-weight: bold;
            color: #FF6B6B;
            text-align: center;
            margin-bottom: 1rem;
        }
        .subtitle-text {
            font-size: 1.2rem;
            text-align: center;
            color: #666;
            margin-bottom: 2rem;
        }
        .movie-card {
            padding: 1rem;
            border-radius: 0.5rem;
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            margin: 0.5rem 0;
            border-left: 5px solid #FF6B6B;
            color: white;
            font-weight: bold;
            font-size: 1.05rem;
            box-shadow: 0 4px 6px rgba(0, 0, 0, 0.2);
            transition: transform 0.2s, box-shadow 0.2s;
        }
        .movie-card:hover {
            transform: translateX(5px);
            box-shadow: 0 6px 12px rgba(0, 0, 0, 0.3);
        }
    </style>
""", unsafe_allow_html=True)

# Initialize session state for the recommender
@st.cache_resource
def load_recommender():
    """Load and train the recommender model"""
    current_dir = os.path.dirname(os.path.abspath(__file__))
    movies_csv = os.path.join(current_dir, 'tmdb_5000_movies.csv')
    credits_csv = os.path.join(current_dir, 'tmdb_5000_credits.csv')
    
    if not os.path.exists(movies_csv) or not os.path.exists(credits_csv):
        st.error("❌ CSV files not found. Please ensure tmdb_5000_movies.csv and tmdb_5000_credits.csv are in the same directory.")
        return None
    
    with st.spinner("🔄 Loading and training the recommendation engine..."):
        recommender = MovieRecommender(movies_csv, credits_csv)
        recommender.train()
    
    return recommender

# Load the recommender
recommender = load_recommender()

if recommender is None:
    st.stop()

# Title and description
st.markdown('<div class="title-text">🎬 Movie Recommender System</div>', unsafe_allow_html=True)
st.markdown('<div class="subtitle-text">Discover movies you\'ll love based on your favorites</div>', unsafe_allow_html=True)

# Sidebar
with st.sidebar:
    st.header("⚙️ Settings")
    num_recommendations = st.slider("Number of recommendations", 1, 10, 5, help="How many movies to recommend")
    st.markdown("---")
    st.info("💡 This system recommends movies based on genres, cast, crew, keywords, and plot descriptions.")

# Main content
tab1, tab2 = st.tabs(["🔍 Get Recommendations", "📊 Browse Movies"])

with tab1:
    col1, col2 = st.columns([2, 1])
    
    with col1:
        st.subheader("Select a Movie")
        all_movies = recommender.get_all_movies()
        selected_movie = st.selectbox(
            "Choose a movie you like:",
            all_movies,
            help="Select a movie and get similar recommendations"
        )
    
    with col2:
        st.subheader("&nbsp;")
        if st.button("🚀 Get Recommendations", use_container_width=True):
            st.session_state.show_recommendations = True
    
    # Display selected movie
    if selected_movie:
        st.markdown("---")
        st.subheader(f"🎬 {selected_movie}")
        st.write("*Click the button above to see similar movies*")
    
    if st.session_state.get('show_recommendations', False):
        st.markdown("---")
        st.subheader(f"📽️ Movies similar to **{selected_movie}**")
        
        recommendations = recommender.recommend(selected_movie, num_recommendations)
        
        if recommendations:
            st.success(f"✅ Found {len(recommendations)} recommendations!")
            for idx, movie in enumerate(recommendations, 1):
                st.markdown(f'<div class="movie-card">🎬 <strong>{idx}. {movie}</strong></div>', unsafe_allow_html=True)
        else:
            st.warning(f"⚠️ No recommendations found for '{selected_movie}'")

with tab2:
    st.subheader("📊 Movie Database")
    
    col1, col2 = st.columns([3, 1])
    
    with col1:
        search_query = st.text_input("🔎 Search movies", placeholder="Type a movie name...")
    
    with col2:
        st.markdown("&nbsp;")
        show_all = st.checkbox("Show all movies")
    
    # Create dataframe for display
    display_df = recommender.new_df[['title']].copy()
    display_df.columns = ['Movie Title']
    display_df.index = display_df.index + 1
    
    # Filter based on search
    if search_query:
        filtered_df = display_df[display_df['Movie Title'].str.contains(search_query, case=False, na=False)]
        st.write(f"Found {len(filtered_df)} movie(s)")
        st.dataframe(filtered_df, use_container_width=True)
    elif show_all:
        st.write(f"Total movies: {len(display_df)}")
        st.dataframe(display_df, use_container_width=True)
    else:
        st.info("💡 Search for a movie or check 'Show all movies' to browse the database")

# Footer
st.markdown("---")
st.markdown(
    """
    <div style="text-align: center; color: #666; font-size: 0.9rem;">
        Built with Streamlit | Movie data from TMDB | Content-based recommendation using cosine similarity
    </div>
    """,
    unsafe_allow_html=True
)
