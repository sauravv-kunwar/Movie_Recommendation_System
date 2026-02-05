Movie Recommendation System
A smart movie recommendation system built with Streamlit that suggests similar movies based on user preferences.

🎯 Features
AI-Powered Recommendations: Uses cosine similarity to find movies similar to your selection

Beautiful UI: Dark aesthetic theme with gradient accents

Movie Posters: Fetches high-quality posters from TMDB API

Real-time Suggestions: Get instant recommendations with one click

Movie Details: View ratings, release years, and descriptions

🛠️ Technologies Used
Python 3.9+

Streamlit - Web application framework

Scikit-learn - Cosine similarity for recommendations

Pandas - Data manipulation

Requests - API calls to TMDB

Pickle - Model serialization

movie-recommender/
├── app.py                    # Main Streamlit application
├── model/
│   ├── movie_list.pkl       # Movie dataset
│   └── similarity.pkl       # Precomputed similarity matrix
├── requirements.txt         # Python dependencies
└── README.md               # This file
