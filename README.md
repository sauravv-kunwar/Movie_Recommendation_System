# Movie Recommendation System 🎬
A smart movie recommendation system built with Streamlit that suggests similar movies based on user preferences.

# ✨ Features
AI-Powered Recommendations: Uses cosine similarity to find movies similar to your selection

Beautiful UI: Dark aesthetic theme with gradient accents

Movie Posters: Fetches high-quality posters from TMDB API

Real-time Suggestions: Get instant recommendations with one click

Movie Details: View ratings, release years, and descriptions

# 🛠️ Technologies Used
Python 3.9+

Streamlit - Web application framework

Scikit-learn - Cosine similarity for recommendations

Pandas - Data manipulation

Requests - API calls to TMDB

Pickle - Model serialization

# 📁 Project Structure
text
movie-recommender/
├── app.py                    # Main Streamlit application
├── model/
│   ├── movie_list.pkl       # Movie dataset
│   └── similarity.pkl       # Precomputed similarity matrix
├── requirements.txt         # Python dependencies
└── README.md               # This file


# 🚀 Quick Start
Installation
Clone the repository

# bash
git clone https://github.com/yourusername/movie-recommender.git
cd movie-recommender
Create virtual environment

# bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
Install dependencies

# bash
pip install -r requirements.txt
Run the application

# bash
streamlit run app.py
Open your browser at http://localhost:8501

# 📦 Requirements
Create requirements.txt:

txt
streamlit==1.28.0
requests==2.31.0
pandas==1.5.3
scikit-learn==1.3.0


# 🔧 How It Works
Data Processing: The system uses a dataset of movies with features like genres, keywords, cast, and crew

Similarity Calculation: Cosine similarity is computed between movie vectors

Recommendation: When you select a movie, it finds the 5 most similar movies

Presentation: Displays recommendations with posters and details fetched from TMDB API

# 📊 Dataset
The system uses a movie dataset containing:

Movie titles and IDs

Genres and keywords

Cast and crew information

User ratings and popularity scores

# 🌐 API Integration
The application integrates with The Movie Database (TMDB) API to:

Fetch movie posters

Get updated movie details

Retrieve ratings and release information



