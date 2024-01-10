from flask import Flask, render_template, request, session, redirect
import requests
import random
import spacy

app = Flask(__name__)

# Key za Last.fm API
LASTFM_API_KEY = "1f409887755c3e139b87863f4adb90f3"
# Key za flask session
app.secret_key = '1E49D7841D26ED759CB1FF65DCFC8'
# Učitavanje engleskog modela spaCy
nlp = spacy.load("en_core_web_sm")

user_history = {}

def record_user_preference(user, genre):
    if user in user_history:
        user_history[user].append(genre)
    else:
        user_history[user] = [genre]

def recommend_music(user, genre):
    record_user_preference(user, genre)  # Pamti preferenciju korisnika

    # Procesuiraj tekst spaCy modelom
    doc = nlp(genre)

    # Dobivanje ključnih riječi (žanra) iz teksta
    genre_keywords = [token.text.lower() for token in doc if token.is_alpha]

    # API request za top pjesme iz zadanog zanra
    api_url = f"http://ws.audioscrobbler.com/2.0/?method=tag.gettoptracks&tag={'%20'.join(genre_keywords)}&api_key={LASTFM_API_KEY}&format=json"
    response = requests.get(api_url)

    if response.status_code == 200:
        tracks = response.json().get('tracks', {}).get('track', [])

        # Broj pjesama za generisanje
        num_songs_to_recommend = min(len(tracks), 10)
        
        random_songs = random.sample(tracks, num_songs_to_recommend)

        recommended_songs = []

        for track in random_songs:
            title = track.get('name', '')
            artist_info = track.get('artist', {})
            artist = artist_info.get('name', '') if artist_info else ''

            # Provjeri da li nedostaje ili je prazna informacija o izvođaču
            if title and artist:
                recommended_songs.append({"title": title, "artist": artist})

        return recommended_songs

    return []

@app.route('/', methods=['GET', 'POST'])
def index():
    chat_history = session.get('chat_history', [])

    if request.method == 'POST':
        user_genre = request.form['genre']

        if not user_genre.strip():
            return render_template('index.html',chat_history=chat_history)

        # Preporuka na osnovu Last.fm API
        recommended_music = recommend_music("user", user_genre.lower())
        chat_history.append({"user": True, "text": user_genre})

        if not recommended_music:
            chat_history.append({"user": False, "no_songs_found": True})
        else:
            chat_history.append({"user": False, "no_songs_found": False,  "songs": recommended_music})
        session['chat_history'] = chat_history
        return redirect("/")

    return render_template('index.html', chat_history=chat_history)


    
@app.route('/clear_session', methods=['POST'])
def clear_session():
    session.clear()
    return redirect("/")

if __name__ == "__main__":
    app.run(debug=True)

    
