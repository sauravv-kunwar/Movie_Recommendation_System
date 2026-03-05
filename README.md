# 🎬 Movie Recommender System

A content-based Movie Recommendation System built using **Machine Learning** and deployed with **Streamlit**.

🔗 **Live Website:**
👉 https://movie-recommender-system-2-k03x.onrender.com/

---

## 🚀 Features

* 🔎 Search for any movie
* 🎥 Get top 5 similar movie recommendations
* 🖼️ Movie posters displayed using TMDB API
* ⚡ Fast and interactive UI built with Streamlit
* 🌐 Deployed on Render

---

## 🧠 How It Works

This project uses **content-based filtering**:

1. Movie metadata (genres, keywords, cast, crew) is combined.
2. Text vectorization is applied.
3. Cosine similarity is calculated between movies.
4. Top similar movies are recommended.

---

## 🛠️ Tech Stack

* **Python**
* **Pandas**
* **NumPy**
* **Scikit-learn**
* **Streamlit**
* **TMDB API**
* **Render (Deployment)**

---

## 📂 Project Structure

```
├── app.py
├── movies.pkl
├── similarity.pkl
├── requirements.txt
├── runtime.txt
└── README.md
```

---

## ⚙️ Installation (Run Locally)

1. Clone the repository:

```bash
git clone https://github.com/your-username/your-repo-name.git
cd your-repo-name
```

2. Install dependencies:

```bash
pip install -r requirements.txt
```

3. Run the app:

```bash
streamlit run app.py
```

---

## 🌍 Deployment

This app is deployed using **Render**.

Start command used:

```bash
streamlit run app.py --server.port $PORT --server.address 0.0.0.0
```

---



## 👨‍💻 Author

**Saurav Kunwar**

## Computer Engineering Student
## Passionate about Machine Learning & AI 🚀

---

⭐ If you like this project, give it a star on GitHub!
