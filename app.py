import base64
import json
from flask import Flask, render_template, request, redirect, url_for, session
import boto3
import os
from dotenv import load_dotenv
from datetime import datetime
from flask_bootstrap import Bootstrap5
import requests
from functools import wraps
from jose import jwt



# Load secrets
load_dotenv()
app = Flask(__name__)
app.secret_key = 'secret-key'
bootstrap = Bootstrap5(app)


#Cognito Configurations
COGNITO_DOMAIN = os.getenv('COGNITO_DOMAIN')
CLIENT_ID = os.getenv('CLIENT_ID')
REDIRECT_URI = 'http://localhost:5000/callback'
TOKEN_URL = f'https://{COGNITO_DOMAIN}/oauth2/token'
LOGOUT_URL = f'https://{COGNITO_DOMAIN}/logout?client_id={CLIENT_ID}&logout_uri=http://localhost:5000/'
COGNITO_USERPOOL_ID = os.getenv('COGNITO_USERPOOL_ID')
COGNITO_REGION = os.getenv('COGNITO_REGION')


def login_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if 'id_token' not in session:
            return redirect(url_for('login'))
        return f(*args, **kwargs)
    return decorated_function


#For testing use only
def generate_fake_jwt():
    header = {
        "alg": "none",
        "typ": "JWT"
    }

    payload = {
        "email": "test@example.com",
        "name": "Test User"
    }

    header_b64 = base64.urlsafe_b64encode(json.dumps(header).encode()).rstrip(b'=')
    payload_b64 = base64.urlsafe_b64encode(json.dumps(payload).encode()).rstrip(b'=')

    fake_token = header_b64 + b'.' + payload_b64 + b'.'
    return fake_token.decode()


@app.route("/", methods=["GET", "POST"])
def index():
    return render_template("home.html")


@app.route("/login")
def login():
    hosted_ui_url = (
        f'https://{COGNITO_DOMAIN}/login?client_id={CLIENT_ID}'
        f'&response_type=code&scope=email+openid+phone+profile'
        f'&redirect_uri={REDIRECT_URI}'
    )
    return redirect(hosted_ui_url)


@app.route('/signup')
def signup():
    hosted_ui_url = (
        f'https://{COGNITO_DOMAIN}/signup?client_id={CLIENT_ID}'
        f'&response_type=code&scope=email+openid+phone+profile'
        f'&redirect_uri={REDIRECT_URI}'
    )
    return redirect(hosted_ui_url)


@app.route("/callback", methods=["GET", "POST"]) #Using for Cognito Hosted UI
def callback():
    code = request.args.get('code') #Grabs code from header
    if not code:
        return 'Missing code', 400

    #Prepares the data for the OAuth2 token exchange.
    #Standard OAuth2 Authorization Code Grant request
    data = {
        'grant_type': 'authorization_code',
        'client_id': CLIENT_ID,
        'code': code,
        'redirect_uri': REDIRECT_URI
    }

    headers = {'Content-Type': 'application/x-www-form-urlencoded'} #OAuth2 expects application/x-www-form-urlencoded data.

    #Sends code and client info to exchange it for tokens
    response = requests.post(TOKEN_URL, data=data, headers=headers) #POST request to Cognito's token endpoint.
    if response.status_code != 200:
        return f'Error exchanging code: {response.text}', 400

    tokens = response.json() #Parses the JSON response containing tokens.

    #Saves the ID token and Access token into the Flask session
    session['id_token'] = tokens['id_token']
    session['access_token'] = tokens['access_token']

    return redirect('/dashboard')


# @login_required
@app.route("/dashboard", methods=["GET", "POST"])
def dashboard():
    #For testing
    if 'id_token' not in session:
        session['id_token'] = generate_fake_jwt()

    id_token = session.get('id_token')
    
    # Decode the ID token
    decoded_token = jwt.get_unverified_claims(id_token)

    user_email = decoded_token.get('email', 'Unknown')
    user_name = decoded_token.get('name', 'User')

    return render_template("dashboard.html", user_email=user_email, user_name=user_name)


@app.route('/logout')
def logout():
    session.clear()
    return redirect(LOGOUT_URL)


if __name__ == "__main__":
    app.run(debug=True)
