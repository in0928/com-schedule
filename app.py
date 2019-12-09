import json
from datetime import datetime
from flask import Flask, render_template, request, redirect, url_for  # For flask implementation
from bson import ObjectId  # For ObjectId to work
from pymongo import MongoClient

app = Flask(__name__)

# schedule_this_month_data =
# schedule_next_month_data =


@app.route("/")
def home():
    t = "COM Schedule"
    return render_template("schedule.html", title=t)

if __name__ == "__main__":
    app.run(debug=True)