# 🎬 Movie Recommender System - Streamlit Web App

[![Streamlit App](https://static.streamlit.io/badges/streamlit_badge_black_white.svg)](https://streamlit.io)
[![Python 3.8+](https://img.shields.io/badge/python-3.8+-blue.svg)](https://www.python.org/downloads/)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)

A **content-based movie recommendation system** built with Streamlit. Get personalized movie recommendations based on genres, cast, crew, keywords, and plot descriptions using **cosine similarity**.

**🌐 [Try the Live Demo](https://your-username-movie-recommender.streamlit.app)** (Deploy your own!)

## 📋 Features

- ✅ **Search & Recommend**: Find any movie and get 5-10 similar recommendations instantly
- ✅ **Browse Catalog**: Explore all 5,000 TMDB movies with search functionality
- ✅ **Content-Based Filtering**: Advanced cosine similarity algorithm
- ✅ **Beautiful UI**: Dark-themed interface with gradient styling
- ✅ **Fast & Responsive**: Cached model for instant recommendations
- ✅ **No Login Required**: Open to everyone!

## 🚀 Quick Start (Local)

### Prerequisites
- Python 3.8 or higher
- Git

### Installation

1. **Clone the repository**
```bash
git clone https://github.com/YOUR_USERNAME/movie-recommender.git
cd movie-recommender
```

2. **Install dependencies**
```bash
pip install -r requirements.txt
```

3. **Download NLTK data** (first time only)
```bash
python -c "import nltk; nltk.download('punkt')"
```

4. **Run the app**
```bash
streamlit run app.py
```

The app will open at `http://localhost:8501` 🎬

## 📁 Project Structure

```
movie-recommender/
├── app.py                      # Main Streamlit application
├── recommendation_engine.py    # Core recommendation logic
├── requirements.txt            # Python dependencies
├── Procfile                    # Heroku deployment config
├── .streamlit/
│   └── config.toml             # Streamlit configuration
├── .gitignore                  # Git ignore rules
└── README.md                   # This file
```

### Data Files
- `tmdb_5000_movies.csv` - Movie metadata (title, genres, overview, etc.)
- `tmdb_5000_credits.csv` - Cast and crew information
- `movie-recommender.ipynb` - Original Jupyter notebook

## 🔧 How It Works

The recommendation engine uses a **content-based filtering** approach:

1. **Data Collection**: Combines genres, keywords, cast, director, and plot overview
2. **Text Processing**: 
   - Removes special characters and spaces
   - Applies Porter Stemming for word normalization
   - Handles stop words
3. **Vectorization**: Converts text to numerical vectors using CountVectorizer (5,000 features)
4. **Similarity Calculation**: Computes cosine similarity between all movie pairs
5. **Ranking & Recommendation**: Returns top N movies with highest similarity scores

### Example
Search for "Avatar" → Gets recommendations like "Inception", "Avatar 2", "Avatar: The Way of Water", etc.

## 💻 How to Use

### 🎬 Get Recommendations Tab
1. **Select a movie** from the dropdown menu
2. **Adjust slider** for number of recommendations (1-10)
3. **Click** "Get Recommendations" button
4. **View** similar movies instantly!

### 📊 Browse Movies Tab
- **Search** for any movie by title
- **Show all** to see the complete database

## 🌐 Deployment

### Option 1: Streamlit Cloud (Recommended ⭐)

**Best for**: Quick & free hosting with automatic updates

1. **Push to GitHub**
```bash
git add .
git commit -m "Initial commit: Movie Recommender"
git push -u origin main
```

2. **Deploy on Streamlit Cloud**
   - Go to https://streamlit.io/cloud
   - Click "New app"
   - Select repository, branch (`main`), and file (`app.py`)
   - Click "Deploy"

3. **Share your link!**
   - Your app is now live: `https://your-username-movie-recommender.streamlit.app`

### Option 2: Heroku

**Best for**: More control & custom domain

```bash
# Create Heroku app
heroku create your-app-name

# Deploy
git push heroku main

# View logs
heroku logs --tail
```

Your app will be at: `https://your-app-name.herokuapp.com`

### Option 3: Railway / Render

Similar process - connect GitHub repo and auto-deploy!

## 📊 Model Details

| Component | Details |
|-----------|---------|
| **Algorithm** | Cosine Similarity (Content-Based) |
| **Features** | Genres, Keywords, Cast (top 3), Director, Overview |
| **Vectorizer** | CountVectorizer with 5,000 features |
| **Text Preprocessing** | Porter Stemmer + Stop word removal |
| **Dataset Size** | 5,000 movies |
| **Training Time** | ~30 seconds on first load |

## 🎯 Future Enhancements

- [ ] Add real movie posters from TMDB API
- [ ] Implement collaborative filtering
- [ ] User ratings and reviews system
- [ ] Multiple recommendation algorithms (Hybrid approach)
- [ ] Movie trailers integration
- [ ] Genre-based filtering
- [ ] User authentication & personalization

## 📝 Tech Stack

- **Frontend**: Streamlit
- **Backend**: Python 3.8+
- **ML**: scikit-learn, pandas, numpy
- **NLP**: NLTK
- **Data**: TMDB 5000 Movies dataset

## 🐛 Troubleshooting

| Issue | Solution |
|-------|----------|
| App takes long to load | Normal on first run. Model trains in ~30s. Subsequent loads are instant. |
| "NLTK data missing" error | Run: `python -c "import nltk; nltk.download('punkt')"` |
| "CSV files not found" | Ensure `tmdb_5000_*.csv` files are in same directory as `app.py` |
| Port 8501 already in use | Run: `streamlit run app.py --server.port 8502` |

## 📞 Support

- Found a bug? Open an issue on GitHub
- Have suggestions? Create a discussion
- Want to contribute? Submit a pull request!

## ⚖️ License

MIT License - Feel free to use this project however you like!

## 📚 Data Source

Dataset from [TMDB 5000 Movies](https://www.kaggle.com/tmdb/tmdb-movie-metadata) on Kaggle

## 🙏 Acknowledgments

- Streamlit for the amazing framework
- TMDB for the movie dataset
- scikit-learn for ML tools

---

**Made with ❤️ by a Movie Enthusiast**

⭐ If you like this project, please star it on GitHub!

🚀 **[Deploy your own now!](https://streamlit.io/cloud)**
