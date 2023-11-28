import os
import requests
from collections import defaultdict
from flask import Flask, request, redirect, session, url_for, render_template
from helpers import *  # Import helper functions

app = Flask(__name__)
app.secret_key = os.urandom(24)  # Set a secret key for session management



@app.route("/")
def index():
    return render_template("index.html")  # Render the "index.html" template

@app.route("/login")
def login():
    # Build the Spotify authorization URL with appropriate parameters
    params = {
        "client_id": CLIENT_ID,
        "response_type": "code",
        "redirect_uri": REDIRECT_URI,
        "scope": SCOPES,
        "code_challenge_method": "S256",
        "code_challenge": code_challenge
    }
    url = f"https://accounts.spotify.com/authorize?{requests.compat.urlencode(params)}"

    return redirect(url)  # Redirect the user to the Spotify login page

@app.route("/callback")
def callback():
    code = request.args.get("code")
    error = request.args.get("error")

    if error:
        return f"Error received from Spotify: {error}"
    if code:
        # Exchange the authorization code for an access token
        session["access_token"] = exchange_code_for_token(code)
        return redirect(url_for(session["lookup"]))  # Redirect to the original lookup route

    return "No code provided by Spotify"

@app.route("/top_tracks", methods=["GET", "POST"])
def top_tracks():
    if "access_token" not in session:
        session["lookup"] = "top_tracks"
        return redirect(url_for("login"))

    try:
        access_token = session["access_token"]

        # Default time range for GET requests or if no time range is provided via POST
        time_range = "medium_term"

        if request.method == "POST":
            # Update time range based on POST request
            time_range = request.form.get("time_range", "medium_term")

        # Call function to get top tracks from Spotify API
        api_results = get_top_tracks(access_token, 10, time_range)
        top_tracks = []

        # Parse and structure each track"s data
        for item in api_results["items"]:
            track = {
                "name": shorten(item["name"]),
                "artist": shorten(", ".join([artist["name"] for artist in item["artists"]])),
                "link": item["external_urls"]["spotify"],
                "image": item["album"]["images"][1]["url"],
            }
            top_tracks.append(track)

        # Render the top tracks page with the tracks data
        return render_template("top_tracks.html", top_tracks=top_tracks)

    except requests.exceptions.RequestException as e:
    # Check the status code and response text to determine if it"s an expired token
        if e.response and e.response.status_code == 401 and "token expired" in e.response.text:
            # Token has expired, redirect the user to reauthenticate
            session["lookup"] = "top_tracks"
            return redirect(url_for("login"))
        else:
            # Other error, display error page
            return render_template("error.html", error=str(e))


@app.route("/top_artists", methods=["GET", "POST"])
def top_artists():
    if "access_token" not in session:
        session["lookup"] = "top_artists"
        return redirect(url_for("login"))

    try:
        access_token = session["access_token"]

        # Default time range for GET requests or if no time range is provided via POST
        time_range = "medium_term"

        if request.method == "POST":
            # Update time range based on POST request
            time_range = request.form.get("time_range", "medium_term")

        # Call function to get top tracks from Spotify API
            api_results = get_top_artists(access_token, 10, time_range)
            artists_list = api_results["items"]
            artist_info_list = []

            for artist in artists_list:
                artist_dict = {
                    "name": shorten(artist["name"]),
                    "genres": shorten(", ".join(artist["genres"])),
                    "link": artist["external_urls"]["spotify"],
                    "image": artist["images"][1]["url"],
                }
                artist_info_list.append(artist_dict)

            return render_template("top_artists.html", top_artists=artist_info_list)

    except requests.exceptions.RequestException as e:
    # Check the status code and response text to determine if it"s an expired token
        if e.response and e.response.status_code == 401 and "token expired" in e.response.text:
            # Token has expired, redirect the user to reauthenticate
            session["lookup"] = "top_artists"
            return redirect(url_for("login"))
        else:
            # Other error, display error page
            return render_template("error.html", error=str(e))


@app.route("/top_genres", methods=["GET", "POST"])
def top_genres():
    if request.method == "GET":
        try:
            access_token = session["access_token"]

            # Retrieve the user"s top artists from Spotify
            top_artists = get_top_artists(access_token, 50, "medium_term")
            artists_list = top_artists["items"]

            # A dictionary to count the occurrences of each genre
            genre_count = {}
            # Iterate through the artists and count their genres
            for artist in artists_list:
                for genre in artist["genres"]:
                    if genre in genre_count:
                        genre_count[genre] += 1
                    else:
                        genre_count[genre] = 1

            # Convert the dictionary to a list of (genre, count) tuples and sort it
            sorted_genres = sorted(genre_count.items(), key=lambda x: x[1], reverse=True)[:10]
            return render_template("top_genres.html", top_genres=sorted_genres)
        except Exception as e:
            return render_template("error.html", error=e)
    else:
        session["lookup"] = "top_genres"
        return redirect(url_for("login"))

@app.route("/search_genre", methods=["POST"])
def search_genre():
    try:
        access_token = session["access_token"]
        selected_genre = request.form.get("search_genre")

        # Perform a Spotify search for playlists in the selected genre
        search_response = search(access_token, selected_genre)

        # Check if "playlists" key exists and if there are items
        if "playlists" in search_response and "items" in search_response["playlists"]:
            playlists = search_response["playlists"]["items"]

            # Check if there are any playlists in the search results
            if playlists:
                # Get the external URL of the first matching playlist
                playlist_url = playlists[0]["external_urls"]["spotify"]

                # Open the playlist in a new window
                return redirect(playlist_url)

    except Exception as e:
        return render_template("error.html", error=e)


@app.route('/contact', methods=['GET', 'POST'])
def contact():
    if request.method == 'POST':
        name = request.form.get('name')
        email = request.form.get('email')
        message = request.form.get('message')

        #process mail
        return render_template('index.html', success=True)
    return render_template('index.html', success=False)


