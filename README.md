# finalproject
Website using Flask and Spotify WebAPI and PKCE workflow

# https://paulwenner.pythonanywhere.com/

# https://youtu.be/sXdGCSMYF4k

# Spotify Stats Viewer
## Project Overview
This project, developed as a final submission for CS50, is a Flask-based web application that allows users to view their Spotify statistics. Similar in functionality to Stats for Spotify, this application provides insights into users' listening habits, top tracks, top artists, and other interesting metrics derived from their Spotify data.

## Features
User Authentication: Secure login through Spotify's OAuth for user-specific data access.
Top Tracks and Artists: Displays user's top tracks and artists over different time periods.
Listening Habits: Analysis of listening habits including genres, playlists, and activity patterns.
Responsive Design: Ensures a seamless experience across various devices and screen sizes.

## Technologies Used
Python & Flask: For server-side scripting and web application framework.
Spotify Web API: To fetch user data and statistics from Spotify.
HTML5, CSS3, and JavaScript: For structuring and styling the frontend.
Bootstrap: For responsive design elements.

## Installation and Usage
Clone the Repository: git clone [repository-link].
Install Dependencies: you need a spotify application, and an .env file with client id and redirect uri
Set Up Spotify API: Register the application in the Spotify Developer Dashboard to obtain the client_id and client_secret. Set these as environment variables.
Initialize the Flask App: Run flask run to start the application.
Access the App: Open a web browser
Contributing
Feedback and contributions are welcome. Please feel free to fork the repository, make changes, and create a pull request.

## Information
"A virtual environment must have been created, and all packages must be installed.

## Files

-app.py: This is the main Python file that runs the Flask server. It handles routing and server-side logic for the web application.

-helpers.py: A Python script containing helper functions used in app.py. These  include data processing and API interaction functions.

-layout.html: The base HTML template that other HTML files extend. It includes the basic structure and elements common to all pages.

-index.html: The homepage of the web application. It provides an overview of the application and links to other sections.

-top_tracks.html: This HTML template displays the top tracks. It's rendered with data provided by the backend.

-top_artists.html: Similar to top_tracks.html, this template shows the top artists.

-top_genres.html: This template displays the top genres in the music database.

-error.html: An error page template displayed when the application encounters an issue.

-script.js: A JavaScript file containing client-side scripts that enhance interactivity and user experience.

-styles.css: The Cascading Style Sheets (CSS) file defining the styling and layout for the web application.



## Design Choices

Framework Selection: Flask was chosen for its simplicity and flexibility in developing small to medium-sized web applications.

Modular HTML Templates: HTML files extend from layout.html to ensure a consistent look and feel while reducing code repetition.

Client-Side Interactivity: JavaScript is used minimally to enhance user experience without overcomplicating the frontend.

Responsive Design: CSS is tailored to ensure the application is usable across various devices and screen sizes.
