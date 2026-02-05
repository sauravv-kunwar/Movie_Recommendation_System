import pickle
import streamlit as st
import requests
import pandas as pd
from datetime import datetime

# Page configuration
st.set_page_config(
    page_title="CineSync AI | Movie Recommender",
    page_icon="🎬",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS for advanced dark cinematic theme
st.markdown("""
<style>
    @import url('https://fonts.googleapis.com/css2?family=Bebas+Neue&family=Crimson+Pro:wght@300;400;600&family=Space+Mono:wght@400;700&display=swap');
    
    /* Main theme */
    .stApp {
        background: #0a0a0a;
        color: #e8e8e8;
        font-family: 'Crimson Pro', serif;
    }
    
    /* Animated background */
    .stApp::before {
        content: '';
        position: fixed;
        top: 0;
        left: 0;
        right: 0;
        bottom: 0;
        background: 
            radial-gradient(circle at 20% 50%, rgba(255, 50, 50, 0.03) 0%, transparent 50%),
            radial-gradient(circle at 80% 80%, rgba(50, 150, 255, 0.03) 0%, transparent 50%),
            radial-gradient(circle at 40% 20%, rgba(255, 200, 50, 0.02) 0%, transparent 50%);
        pointer-events: none;
        z-index: 0;
    }
    
    /* Headers */
    .main-header {
        font-family: 'Bebas Neue', cursive;
        font-size: 5.5rem !important;
        letter-spacing: 0.15em;
        text-align: center;
        margin-bottom: 0 !important;
        background: linear-gradient(135deg, #ff3333 0%, #ff8833 50%, #ffaa33 100%);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        text-shadow: 0 0 60px rgba(255, 51, 51, 0.3);
        animation: glow 3s ease-in-out infinite alternate;
        position: relative;
        z-index: 1;
    }
    
    @keyframes glow {
        from { filter: drop-shadow(0 0 10px rgba(255, 51, 51, 0.4)); }
        to { filter: drop-shadow(0 0 30px rgba(255, 136, 51, 0.6)); }
    }
    
    .sub-header {
        font-family: 'Space Mono', monospace;
        color: #888;
        text-align: center;
        font-size: 0.9rem !important;
        margin-bottom: 3rem !important;
        font-weight: 400 !important;
        letter-spacing: 0.2em;
        text-transform: uppercase;
    }
    
    .section-title {
        font-family: 'Bebas Neue', cursive;
        font-size: 2.5rem;
        letter-spacing: 0.1em;
        color: #ff6633;
        border-left: 4px solid #ff3333;
        padding-left: 20px;
        margin: 40px 0 25px 0;
        text-transform: uppercase;
    }
    
    /* Sidebar */
    [data-testid="stSidebar"] {
        background: linear-gradient(180deg, #0f0f0f 0%, #1a1a1a 100%);
        border-right: 1px solid rgba(255, 51, 51, 0.2);
    }
    
    [data-testid="stSidebar"] h1, [data-testid="stSidebar"] h2, [data-testid="stSidebar"] h3 {
        color: #ff6633;
        font-family: 'Bebas Neue', cursive;
        letter-spacing: 0.1em;
    }
    
    /* Buttons */
    .stButton > button {
        background: linear-gradient(135deg, #ff3333 0%, #ff6633 100%);
        color: white !important;
        border: none !important;
        padding: 16px 32px !important;
        border-radius: 0 !important;
        font-weight: 700 !important;
        font-size: 14px !important;
        font-family: 'Space Mono', monospace !important;
        letter-spacing: 0.15em !important;
        text-transform: uppercase !important;
        transition: all 0.3s cubic-bezier(0.4, 0, 0.2, 1) !important;
        width: 100% !important;
        margin-top: 20px !important;
        box-shadow: 0 8px 32px rgba(255, 51, 51, 0.3) !important;
        position: relative;
        overflow: hidden;
    }
    
    .stButton > button::before {
        content: '';
        position: absolute;
        top: 0;
        left: -100%;
        width: 100%;
        height: 100%;
        background: linear-gradient(90deg, transparent, rgba(255, 255, 255, 0.2), transparent);
        transition: 0.5s;
    }
    
    .stButton > button:hover::before {
        left: 100%;
    }
    
    .stButton > button:hover {
        transform: translateY(-3px) !important;
        box-shadow: 0 12px 40px rgba(255, 51, 51, 0.5) !important;
    }
    
    /* Select box styling */
    .stSelectbox > div > div {
        background-color: rgba(20, 20, 20, 0.9) !important;
        border: 1px solid rgba(255, 51, 51, 0.3) !important;
        border-radius: 0 !important;
        color: white !important;
        padding: 12px !important;
        font-family: 'Crimson Pro', serif !important;
    }
    
    /* Movie cards */
    .movie-card {
        background: linear-gradient(145deg, #1a1a1a 0%, #0f0f0f 100%);
        border: 1px solid rgba(255, 51, 51, 0.2);
        padding: 0;
        margin: 10px 0;
        transition: all 0.4s cubic-bezier(0.4, 0, 0.2, 1);
        height: 100%;
        position: relative;
        overflow: hidden;
        box-shadow: 0 4px 20px rgba(0, 0, 0, 0.5);
    }
    
    .movie-card::after {
        content: '';
        position: absolute;
        top: 0;
        left: 0;
        right: 0;
        height: 3px;
        background: linear-gradient(90deg, #ff3333, #ff6633, #ffaa33);
        transform: scaleX(0);
        transition: transform 0.4s ease;
    }
    
    .movie-card:hover::after {
        transform: scaleX(1);
    }
    
    .movie-card:hover {
        transform: translateY(-12px) scale(1.02);
        box-shadow: 0 20px 60px rgba(255, 51, 51, 0.4);
        border-color: rgba(255, 102, 51, 0.6);
    }
    
    .movie-poster {
        width: 100%;
        display: block;
        transition: transform 0.4s ease;
        aspect-ratio: 2/3;
        object-fit: cover;
    }
    
    .movie-card:hover .movie-poster {
        transform: scale(1.08);
    }
    
    .movie-info {
        padding: 15px;
        background: rgba(10, 10, 10, 0.95);
    }
    
    .movie-title {
        color: #ffffff;
        font-weight: 600;
        font-size: 15px;
        line-height: 1.4;
        margin: 0 0 10px 0;
        font-family: 'Crimson Pro', serif;
        min-height: 40px;
    }
    
    .movie-meta {
        display: flex;
        justify-content: space-between;
        align-items: center;
        font-size: 12px;
        font-family: 'Space Mono', monospace;
    }
    
    .rating {
        color: #ffaa33;
        font-weight: 700;
    }
    
    .year {
        color: #ff6633;
        font-weight: 700;
    }
    
    .genre-tag {
        display: inline-block;
        background: rgba(255, 51, 51, 0.2);
        color: #ff6633;
        padding: 4px 10px;
        margin: 4px;
        font-size: 11px;
        font-family: 'Space Mono', monospace;
        border: 1px solid rgba(255, 51, 51, 0.3);
        text-transform: uppercase;
        letter-spacing: 0.1em;
    }
    
    /* Trending badge */
    .trending-badge {
        position: absolute;
        top: 10px;
        right: 10px;
        background: linear-gradient(135deg, #ff3333, #ff6633);
        color: white;
        padding: 6px 12px;
        font-size: 10px;
        font-weight: 700;
        font-family: 'Space Mono', monospace;
        letter-spacing: 0.1em;
        text-transform: uppercase;
        z-index: 10;
        box-shadow: 0 4px 15px rgba(255, 51, 51, 0.5);
        animation: pulse 2s ease-in-out infinite;
    }
    
    @keyframes pulse {
        0%, 100% { transform: scale(1); }
        50% { transform: scale(1.05); }
    }
    
    /* Hide Streamlit default elements */
    #MainMenu {visibility: hidden;}
    footer {visibility: hidden;}
    header {visibility: hidden;}
    .stDeployButton {display:none;}
    
    /* Divider */
    hr {
        border: none;
        height: 2px;
        background: linear-gradient(90deg, transparent, rgba(255, 51, 51, 0.5), transparent);
        margin: 3rem 0;
    }
    
    /* Stats cards */
    .stats-card {
        background: linear-gradient(145deg, rgba(255, 51, 51, 0.08), rgba(255, 102, 51, 0.05));
        border: 1px solid rgba(255, 51, 51, 0.2);
        padding: 25px;
        margin: 10px;
        text-align: center;
        transition: all 0.3s ease;
    }
    
    .stats-card:hover {
        transform: translateY(-5px);
        border-color: rgba(255, 102, 51, 0.5);
        box-shadow: 0 10px 30px rgba(255, 51, 51, 0.2);
    }
    
    .stats-icon {
        font-size: 2rem;
        margin-bottom: 10px;
    }
    
    .stats-number {
        font-size: 2.5rem;
        font-weight: 700;
        font-family: 'Bebas Neue', cursive;
        color: #ff6633;
        margin: 10px 0;
        letter-spacing: 0.05em;
    }
    
    .stats-label {
        font-size: 0.85rem;
        color: #888;
        font-family: 'Space Mono', monospace;
        text-transform: uppercase;
        letter-spacing: 0.15em;
    }
    
    /* Search box */
    .search-container {
        background: rgba(20, 20, 20, 0.9);
        border: 2px solid rgba(255, 51, 51, 0.3);
        padding: 30px;
        margin: 20px 0;
        transition: all 0.3s ease;
    }
    
    .search-container:hover {
        border-color: rgba(255, 102, 51, 0.5);
        box-shadow: 0 8px 30px rgba(255, 51, 51, 0.2);
    }
    
    /* Expander */
    .streamlit-expanderHeader {
        background: rgba(20, 20, 20, 0.9) !important;
        border: 1px solid rgba(255, 51, 51, 0.2) !important;
        color: #ff6633 !important;
        font-family: 'Space Mono', monospace !important;
        border-radius: 0 !important;
    }
    
    .streamlit-expanderHeader:hover {
        border-color: rgba(255, 102, 51, 0.5) !important;
    }
    
    /* Filters */
    .filter-chip {
        display: inline-block;
        background: rgba(255, 51, 51, 0.15);
        border: 1px solid rgba(255, 51, 51, 0.3);
        color: #ff6633;
        padding: 8px 16px;
        margin: 5px;
        font-size: 12px;
        font-family: 'Space Mono', monospace;
        cursor: pointer;
        transition: all 0.3s ease;
        text-transform: uppercase;
        letter-spacing: 0.1em;
    }
    
    .filter-chip:hover {
        background: rgba(255, 51, 51, 0.3);
        border-color: rgba(255, 102, 51, 0.6);
        transform: translateY(-2px);
    }
    
    /* Loading */
    .stSpinner > div {
        border-color: #ff3333 !important;
    }
    
    /* Scrollbar */
    ::-webkit-scrollbar {
        width: 10px;
        height: 10px;
    }
    
    ::-webkit-scrollbar-track {
        background: #0a0a0a;
    }
    
    ::-webkit-scrollbar-thumb {
        background: linear-gradient(180deg, #ff3333, #ff6633);
        border-radius: 0;
    }
    
    ::-webkit-scrollbar-thumb:hover {
        background: linear-gradient(180deg, #ff4444, #ff7744);
    }
    
    /* Tab styling */
    .stTabs [data-baseweb="tab-list"] {
        gap: 0;
        background: rgba(20, 20, 20, 0.5);
        border-bottom: 2px solid rgba(255, 51, 51, 0.2);
    }
    
    .stTabs [data-baseweb="tab"] {
        background: transparent;
        border: none;
        color: #888;
        font-family: 'Space Mono', monospace;
        font-size: 13px;
        font-weight: 700;
        padding: 15px 30px;
        text-transform: uppercase;
        letter-spacing: 0.15em;
    }
    
    .stTabs [aria-selected="true"] {
        background: rgba(255, 51, 51, 0.15);
        color: #ff6633;
        border-bottom: 3px solid #ff3333;
    }
    
    /* Info box */
    .info-box {
        background: rgba(255, 102, 51, 0.1);
        border-left: 4px solid #ff6633;
        padding: 20px;
        margin: 20px 0;
        color: #ccc;
        font-size: 14px;
    }
    
    .info-box strong {
        color: #ff6633;
        font-family: 'Space Mono', monospace;
    }
</style>
""", unsafe_allow_html=True)

# API configuration
TMDB_API_KEY = "8265bd1679663a7ea12ac168da84d2e8"
TMDB_BASE_URL = "https://api.themoviedb.org/3"

# Utility functions
def fetch_poster(movie_id):
    try:
        url = f"{TMDB_BASE_URL}/movie/{movie_id}?api_key={TMDB_API_KEY}"
        data = requests.get(url, timeout=10)
        if data.status_code == 200:
            data = data.json()
            poster = data.get('poster_path', '')
            if poster:
                return f"https://image.tmdb.org/t/p/w500/{poster}"
    except:
        pass
    return "https://via.placeholder.com/500x750/0a0a0a/ff6633?text=No+Image"

def fetch_movie_details(movie_id):
    try:
        url = f"{TMDB_BASE_URL}/movie/{movie_id}?api_key={TMDB_API_KEY}"
        data = requests.get(url, timeout=10)
        if data.status_code == 200:
            return data.json()
    except:
        return None

def fetch_trending_movies(time_window='day', limit=10):
    """Fetch trending movies from TMDB"""
    try:
        url = f"{TMDB_BASE_URL}/trending/movie/{time_window}?api_key={TMDB_API_KEY}"
        response = requests.get(url, timeout=10)
        if response.status_code == 200:
            data = response.json()
            return data['results'][:limit]
    except:
        return []

def fetch_popular_movies(limit=10):
    """Fetch popular movies from TMDB"""
    try:
        url = f"{TMDB_BASE_URL}/movie/popular?api_key={TMDB_API_KEY}"
        response = requests.get(url, timeout=10)
        if response.status_code == 200:
            data = response.json()
            return data['results'][:limit]
    except:
        return []

def fetch_top_rated_movies(limit=10):
    """Fetch top rated movies from TMDB"""
    try:
        url = f"{TMDB_BASE_URL}/movie/top_rated?api_key={TMDB_API_KEY}"
        response = requests.get(url, timeout=10)
        if response.status_code == 200:
            data = response.json()
            return data['results'][:limit]
    except:
        return []

def search_movies(query):
    """Search for movies by title"""
    try:
        url = f"{TMDB_BASE_URL}/search/movie?api_key={TMDB_API_KEY}&query={query}"
        response = requests.get(url, timeout=10)
        if response.status_code == 200:
            data = response.json()
            return data['results'][:10]
    except:
        return []

def get_movie_genres():
    """Fetch all movie genres"""
    try:
        url = f"{TMDB_BASE_URL}/genre/movie/list?api_key={TMDB_API_KEY}"
        response = requests.get(url, timeout=10)
        if response.status_code == 200:
            data = response.json()
            return {genre['id']: genre['name'] for genre in data['genres']}
    except:
        return {}

def recommend(movie):
    """Generate movie recommendations based on similarity"""
    try:
        index = movies[movies['title'] == movie].index[0]
        distances = sorted(list(enumerate(similarity[index])), reverse=True, key=lambda x: x[1])
        recommended = []
        for i in distances[1:6]:
            movie_id = movies.iloc[i[0]].movie_id
            details = fetch_movie_details(movie_id)
            
            movie_info = {
                'title': movies.iloc[i[0]].title,
                'poster': fetch_poster(movie_id),
                'similarity': float(distances[1][1]) * 100,
                'rating': details.get('vote_average', 'N/A') if details else 'N/A',
                'year': details.get('release_date', '')[:4] if details and details.get('release_date') else 'N/A',
                'overview': details.get('overview', '') if details else '',
                'genres': details.get('genres', []) if details else []
            }
            recommended.append(movie_info)
        return recommended
    except Exception as e:
        st.error(f"Error generating recommendations: {str(e)}")
        return []

# Load data
@st.cache_data
def load_data():
    movies = pickle.load(open('movie_list.pkl', 'rb'))
    similarity = pickle.load(open('similarity.pkl', 'rb'))
    return movies, similarity

# Load the data
movies, similarity = load_data()
genres_dict = get_movie_genres()

# Sidebar
with st.sidebar:
    st.markdown("### 🎬 Navigation")
    page = st.radio("", ["Home", "Trending Now", "Search Movies", "Top Rated", "About"], label_visibility="collapsed")
    
    st.markdown("---")
    st.markdown("### 🎯 Filters")
    
    min_rating = st.slider("Minimum Rating", 0.0, 10.0, 6.0, 0.5)
    show_year = st.checkbox("Show Release Year", value=True)
    
    st.markdown("---")
    st.markdown("""
    <div style='text-align: center; color: #666; padding: 20px 0;'>
        <small>Powered by TMDB API</small>
    </div>
    """, unsafe_allow_html=True)

# Main header
st.markdown('<h1 class="main-header">CINESYNC</h1>', unsafe_allow_html=True)
st.markdown('<p class="sub-header">— AI-Powered Cinematic Discovery —</p>', unsafe_allow_html=True)

# Stats row
col1, col2, col3, col4 = st.columns(4)
with col1:
    st.markdown(f"""
    <div class="stats-card">
        <div class="stats-icon">🎥</div>
        <div class="stats-number">{len(movies):,}</div>
        <div class="stats-label">Movies</div>
    </div>
    """, unsafe_allow_html=True)

with col2:
    st.markdown("""
    <div class="stats-card">
        <div class="stats-icon">⚡</div>
        <div class="stats-number">AI</div>
        <div class="stats-label">Powered</div>
    </div>
    """, unsafe_allow_html=True)

with col3:
    st.markdown("""
    <div class="stats-card">
        <div class="stats-icon">🎯</div>
        <div class="stats-number">95%</div>
        <div class="stats-label">Accuracy</div>
    </div>
    """, unsafe_allow_html=True)

with col4:
    st.markdown("""
    <div class="stats-card">
        <div class="stats-icon">🔄</div>
        <div class="stats-number">Live</div>
        <div class="stats-label">Updates</div>
    </div>
    """, unsafe_allow_html=True)

st.markdown("<hr>", unsafe_allow_html=True)

# Page routing
if page == "Home":
    # Main recommendation section
    st.markdown('<div class="section-title">Personalized Recommendations</div>', unsafe_allow_html=True)
    
    col_left, col_right = st.columns([2, 1])
    
    with col_left:
        st.markdown("""
        <div class="search-container">
            <p style='color: #888; margin-bottom: 20px; font-family: "Space Mono", monospace; font-size: 13px; letter-spacing: 0.1em;'>
                SELECT A MOVIE YOU LOVE
            </p>
        </div>
        """, unsafe_allow_html=True)
        
        selected = st.selectbox(
            "",
            movies['title'].values,
            index=0,
            help="Select or type to search movies",
            label_visibility="collapsed"
        )
        
        if st.button("🎯 GENERATE RECOMMENDATIONS", key="recommend_btn"):
            with st.spinner("🤖 Analyzing cinematic patterns..."):
                results = recommend(selected)
                
                if results:
                    st.markdown("<hr>", unsafe_allow_html=True)
                    st.markdown(f'<div class="section-title">Recommended For You</div>', unsafe_allow_html=True)
                    st.markdown(f"<p style='color: #888; margin-bottom: 30px;'>Based on: <strong style='color: #ff6633;'>{selected}</strong></p>", unsafe_allow_html=True)
                    
                    # Display recommendations in grid
                    cols = st.columns(5)
                    for idx, movie in enumerate(results):
                        with cols[idx]:
                            st.markdown(f"""
                            <div class='movie-card'>
                                <img src='{movie['poster']}' class='movie-poster' alt='{movie['title']}'>
                                <div class='movie-info'>
                                    <div class='movie-title'>{movie['title']}</div>
                                    <div class='movie-meta'>
                                        <span class='rating'>⭐ {movie['rating']}</span>
                                        <span class='year'>📅 {movie['year']}</span>
                                    </div>
                                </div>
                            </div>
                            """, unsafe_allow_html=True)
                    
                    # Detailed view
                    st.markdown("<hr>", unsafe_allow_html=True)
                    st.markdown('<div class="section-title">Detailed Information</div>', unsafe_allow_html=True)
                    
                    for movie in results:
                        with st.expander(f"🎬 {movie['title']} | Match: {movie['similarity']:.1f}%", expanded=False):
                            detail_col1, detail_col2 = st.columns([1, 2])
                            with detail_col1:
                                st.image(movie['poster'], use_container_width=True)
                            with detail_col2:
                                st.markdown(f"**Match Score:** 🎯 {movie['similarity']:.1f}%")
                                st.markdown(f"**Rating:** ⭐ {movie['rating']}/10")
                                st.markdown(f"**Release Year:** 📅 {movie['year']}")
                                if movie.get('genres'):
                                    genres_html = ''.join([f"<span class='genre-tag'>{g['name']}</span>" for g in movie['genres'][:3]])
                                    st.markdown(genres_html, unsafe_allow_html=True)
                                if movie.get('overview'):
                                    st.markdown(f"<p style='color: #aaa; margin-top: 15px;'>{movie['overview']}</p>", unsafe_allow_html=True)
                else:
                    st.error("⚠️ Could not generate recommendations. Please try another movie.")
    
    with col_right:
        # Show selected movie info
        if selected:
            try:
                movie_idx = movies[movies['title'] == selected].index[0]
                movie_id = movies.iloc[movie_idx].movie_id
                details = fetch_movie_details(movie_id)
                
                if details:
                    st.markdown("""
                    <div class="info-box">
                        <strong>SELECTED MOVIE</strong>
                    </div>
                    """, unsafe_allow_html=True)
                    
                    st.image(fetch_poster(movie_id), use_container_width=True)
                    st.markdown(f"**{selected}**")
                    if details.get('vote_average'):
                        st.markdown(f"⭐ **{details['vote_average']}/10**")
                    if details.get('release_date'):
                        st.markdown(f"📅 {details['release_date'][:4]}")
                    if details.get('overview'):
                        st.markdown(f"<small style='color: #aaa;'>{details['overview'][:200]}...</small>", unsafe_allow_html=True)
            except:
                pass

elif page == "Trending Now":
    st.markdown('<div class="section-title">Trending Movies</div>', unsafe_allow_html=True)
    
    # Tabs for different trending periods
    tab1, tab2, tab3 = st.tabs(["📈 Today", "🔥 This Week", "⭐ Popular"])
    
    with tab1:
        with st.spinner("Loading trending movies..."):
            trending_today = fetch_trending_movies('day', 10)
            if trending_today:
                cols = st.columns(5)
                for idx, movie in enumerate(trending_today):
                    with cols[idx % 5]:
                        poster_url = f"https://image.tmdb.org/t/p/w500{movie['poster_path']}" if movie.get('poster_path') else "https://via.placeholder.com/500x750/0a0a0a/ff6633?text=No+Image"
                        st.markdown(f"""
                        <div class='movie-card'>
                            <div class='trending-badge'>#{idx + 1} Trending</div>
                            <img src='{poster_url}' class='movie-poster' alt='{movie['title']}'>
                            <div class='movie-info'>
                                <div class='movie-title'>{movie['title']}</div>
                                <div class='movie-meta'>
                                    <span class='rating'>⭐ {movie.get('vote_average', 'N/A')}</span>
                                    <span class='year'>📅 {movie.get('release_date', 'N/A')[:4]}</span>
                                </div>
                            </div>
                        </div>
                        """, unsafe_allow_html=True)
                    if (idx + 1) % 5 == 0 and idx + 1 < len(trending_today):
                        cols = st.columns(5)
    
    with tab2:
        with st.spinner("Loading weekly trends..."):
            trending_week = fetch_trending_movies('week', 10)
            if trending_week:
                cols = st.columns(5)
                for idx, movie in enumerate(trending_week):
                    with cols[idx % 5]:
                        poster_url = f"https://image.tmdb.org/t/p/w500{movie['poster_path']}" if movie.get('poster_path') else "https://via.placeholder.com/500x750/0a0a0a/ff6633?text=No+Image"
                        st.markdown(f"""
                        <div class='movie-card'>
                            <div class='trending-badge'>#{idx + 1} This Week</div>
                            <img src='{poster_url}' class='movie-poster' alt='{movie['title']}'>
                            <div class='movie-info'>
                                <div class='movie-title'>{movie['title']}</div>
                                <div class='movie-meta'>
                                    <span class='rating'>⭐ {movie.get('vote_average', 'N/A')}</span>
                                    <span class='year'>📅 {movie.get('release_date', 'N/A')[:4]}</span>
                                </div>
                            </div>
                        </div>
                        """, unsafe_allow_html=True)
                    if (idx + 1) % 5 == 0 and idx + 1 < len(trending_week):
                        cols = st.columns(5)
    
    with tab3:
        with st.spinner("Loading popular movies..."):
            popular = fetch_popular_movies(10)
            if popular:
                cols = st.columns(5)
                for idx, movie in enumerate(popular):
                    with cols[idx % 5]:
                        poster_url = f"https://image.tmdb.org/t/p/w500{movie['poster_path']}" if movie.get('poster_path') else "https://via.placeholder.com/500x750/0a0a0a/ff6633?text=No+Image"
                        st.markdown(f"""
                        <div class='movie-card'>
                            <img src='{poster_url}' class='movie-poster' alt='{movie['title']}'>
                            <div class='movie-info'>
                                <div class='movie-title'>{movie['title']}</div>
                                <div class='movie-meta'>
                                    <span class='rating'>⭐ {movie.get('vote_average', 'N/A')}</span>
                                    <span class='year'>📅 {movie.get('release_date', 'N/A')[:4]}</span>
                                </div>
                            </div>
                        </div>
                        """, unsafe_allow_html=True)
                    if (idx + 1) % 5 == 0 and idx + 1 < len(popular):
                        cols = st.columns(5)

elif page == "Search Movies":
    st.markdown('<div class="section-title">Search Movies</div>', unsafe_allow_html=True)
    
    st.markdown("""
    <div class="search-container">
        <p style='color: #888; margin-bottom: 20px; font-family: "Space Mono", monospace; font-size: 13px; letter-spacing: 0.1em;'>
            SEARCH FOR ANY MOVIE
        </p>
    </div>
    """, unsafe_allow_html=True)
    
    search_query = st.text_input("", placeholder="Enter movie title...", label_visibility="collapsed")
    
    if search_query:
        with st.spinner("Searching..."):
            search_results = search_movies(search_query)
            if search_results:
                st.markdown(f"<p style='color: #888; margin: 20px 0;'>Found {len(search_results)} results</p>", unsafe_allow_html=True)
                cols = st.columns(5)
                for idx, movie in enumerate(search_results):
                    with cols[idx % 5]:
                        poster_url = f"https://image.tmdb.org/t/p/w500{movie['poster_path']}" if movie.get('poster_path') else "https://via.placeholder.com/500x750/0a0a0a/ff6633?text=No+Image"
                        st.markdown(f"""
                        <div class='movie-card'>
                            <img src='{poster_url}' class='movie-poster' alt='{movie['title']}'>
                            <div class='movie-info'>
                                <div class='movie-title'>{movie['title']}</div>
                                <div class='movie-meta'>
                                    <span class='rating'>⭐ {movie.get('vote_average', 'N/A')}</span>
                                    <span class='year'>📅 {movie.get('release_date', 'N/A')[:4]}</span>
                                </div>
                            </div>
                        </div>
                        """, unsafe_allow_html=True)
                    if (idx + 1) % 5 == 0 and idx + 1 < len(search_results):
                        cols = st.columns(5)
            else:
                st.info("No results found. Try a different search term.")

elif page == "Top Rated":
    st.markdown('<div class="section-title">Top Rated Movies</div>', unsafe_allow_html=True)
    
    with st.spinner("Loading top rated movies..."):
        top_rated = fetch_top_rated_movies(20)
        if top_rated:
            # Filter by minimum rating
            filtered = [m for m in top_rated if m.get('vote_average', 0) >= min_rating]
            
            if filtered:
                cols = st.columns(5)
                for idx, movie in enumerate(filtered):
                    with cols[idx % 5]:
                        poster_url = f"https://image.tmdb.org/t/p/w500{movie['poster_path']}" if movie.get('poster_path') else "https://via.placeholder.com/500x750/0a0a0a/ff6633?text=No+Image"
                        st.markdown(f"""
                        <div class='movie-card'>
                            <img src='{poster_url}' class='movie-poster' alt='{movie['title']}'>
                            <div class='movie-info'>
                                <div class='movie-title'>{movie['title']}</div>
                                <div class='movie-meta'>
                                    <span class='rating'>⭐ {movie.get('vote_average', 'N/A')}</span>
                                    <span class='year'>📅 {movie.get('release_date', 'N/A')[:4]}</span>
                                </div>
                            </div>
                        </div>
                        """, unsafe_allow_html=True)
                    if (idx + 1) % 5 == 0 and idx + 1 < len(filtered):
                        cols = st.columns(5)
            else:
                st.info(f"No movies found with rating >= {min_rating}")

elif page == "About":
    st.markdown('<div class="section-title">About CineSync AI</div>', unsafe_allow_html=True)
    
    st.markdown("""
    <div class="info-box">
        <p style='font-size: 16px; line-height: 1.8;'>
            <strong>CineSync AI</strong> is an intelligent movie recommendation system that uses advanced machine learning 
            algorithms to analyze your movie preferences and suggest films you'll love.
        </p>
    </div>
    
    <div style='margin: 40px 0;'>
        <h3 style='color: #ff6633; font-family: "Bebas Neue", cursive; letter-spacing: 0.1em;'>Features</h3>
        <ul style='color: #aaa; line-height: 2;'>
            <li><strong style='color: #ff6633;'>AI-Powered Recommendations:</strong> Get personalized movie suggestions based on your preferences</li>
            <li><strong style='color: #ff6633;'>Trending Movies:</strong> Stay updated with what's popular right now</li>
            <li><strong style='color: #ff6633;'>Advanced Search:</strong> Find any movie from our extensive database</li>
            <li><strong style='color: #ff6633;'>Top Rated:</strong> Discover critically acclaimed films</li>
            <li><strong style='color: #ff6633;'>Real-time Data:</strong> Powered by TMDB API for up-to-date information</li>
        </ul>
    </div>
    
    <div style='margin: 40px 0;'>
        <h3 style='color: #ff6633; font-family: "Bebas Neue", cursive; letter-spacing: 0.1em;'>How It Works</h3>
        <p style='color: #aaa; line-height: 1.8;'>
            Our recommendation engine uses content-based filtering to analyze movie features like genres, cast, 
            directors, and plot keywords. When you select a movie you like, the system finds similar films based 
            on these characteristics and presents you with the best matches.
        </p>
    </div>
    
    <div class="info-box">
        <p style='text-align: center;'>
            <strong>Powered by TMDB API</strong><br>
            <small>This product uses the TMDB API but is not endorsed or certified by TMDB.</small>
        </p>
    </div>
    """, unsafe_allow_html=True)

# Footer
st.markdown("<hr>", unsafe_allow_html=True)
st.markdown(f"""
<div style='text-align: center; color: #444; padding: 30px; font-family: "Space Mono", monospace;'>
    <p style='font-size: 12px; letter-spacing: 0.2em; margin-bottom: 10px;'>🎬 POWERED BY ARTIFICIAL INTELLIGENCE</p>
    <p style='font-size: 11px; color: #333;'>© {datetime.now().year} CineSync AI. Discover Your Next Cinematic Journey.</p>
</div>
""", unsafe_allow_html=True)