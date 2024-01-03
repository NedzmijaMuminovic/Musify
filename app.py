from flask import Flask, render_template, request
import spacy

# Učitavanje engleskog modela
nlp = spacy.load("en_core_web_sm")

app = Flask(__name__)

# Simulacija baze podataka
music_database = {
    "rock": [
        {"title": "Stairway to Heaven", "artist": "Led Zeppelin", "year": 1971},
        {"title": "Bohemian Rhapsody", "artist": "Queen", "year": 1975},
        {"title": "Hotel California", "artist": "Eagles", "year": 1977}
    ],
    "pop": [
        {"title": "Shape of You", "artist": "Ed Sheeran", "year": 2017},
        {"title": "Uptown Funk", "artist": "Mark Ronson ft. Bruno Mars", "year": 2014},
        {"title": "Happy", "artist": "Pharrell Williams", "year": 2013}
    ],
    "hip hop": [
        {"title": "Sicko Mode", "artist": "Travis Scott", "year": 2018},
        {"title": "Old Town Road", "artist": "Lil Nas X ft. Billy Ray Cyrus", "year": 2019},
        {"title": "God's Plan", "artist": "Drake", "year": 2018}
    ],
    "jazz": [
        {"title": "Take Five", "artist": "Dave Brubeck Quartet", "year": 1959},
        {"title": "So What", "artist": "Miles Davis", "year": 1959},
        {"title": "My Favorite Things", "artist": "John Coltrane", "year": 1961}
    ],
    "electronic": [
        {"title": "Strobe", "artist": "Deadmau5", "year": 2009},
        {"title": "Summertime Sadness", "artist": "Lana Del Rey vs. Cedric Gervais", "year": 2013},
        {"title": "Clarity", "artist": "Zedd ft. Foxes", "year": 2012}
    ],
    # Dodaj više žanrova i pjesama prema potrebi
}

user_history = {}

def record_user_preference(user, genre):
    if user in user_history:
        user_history[user].append(genre)
    else:
        user_history[user] = [genre]

def recommend_music(user, genre):
    record_user_preference(user, genre)  # Pamti preferenciju korisnika

    # Povratak preporučenih pjesama
    recommended_songs = music_database.get(genre.lower(), [])

    return recommended_songs

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/recommend', methods=['POST'])
def recommend():
    user_genre = request.form['genre']

    # Procesuiraj tekst spaCy modelom
    doc = nlp(user_genre)

    # Dobivanje ključnih riječi (žanra) iz teksta
    genre_keywords = [token.text.lower() for token in doc if token.is_alpha]

    # Pretvori ključne riječi u string
    genre_string = " ".join(genre_keywords)

    # Preporuka glazbe na temelju žanra
    recommended_music = recommend_music("user", genre_string)  # Zamijeni "user" s pravim imenom

    # Ispravljeni dio za ispis preporučenih pjesama
    if not recommended_music:
        return render_template('index.html', genre_not_found=True, user_genre=user_genre)

    return render_template('index.html', recommended_music=recommended_music)

if __name__ == "__main__":
    app.run(debug=True)