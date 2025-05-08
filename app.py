from flask import Flask, render_template, request, redirect
import boto3
import os
from dotenv import load_dotenv
from datetime import datetime
from flask_bootstrap import Bootstrap5


# Load secrets
load_dotenv()
app = Flask(__name__)
bootstrap = Bootstrap5(app)


@app.route("/", methods=["GET", "POST"])
def index():
    return render_template("home.html")


if __name__ == "__main__":
    app.run(debug=True)
