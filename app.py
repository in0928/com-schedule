import json
from datetime import datetime
from flask import Flask, render_template, request, redirect, url_for  # For flask implementation
from bson import ObjectId  # For ObjectId to work
from pymongo import MongoClient
from pymongo_fetcher import MongoFetcher
import displaySchedule as ds

app = Flask(__name__)
mf = MongoFetcher()
schedule_this_month_data = mf.schedule_this_month
schedule_next_month_data = mf.schedule_next_month


def get_schedule_for_month(month, num_of_days):
    pass


@app.route("/")
def home():
    t = "COM Schedule"

    month_date = ["10."]*31
    for i in range(31):
        date = str(i+1)
        month_date[i] = month_date[i]+date

    event_list = []
    for day in month_date:
        aug_events = schedule_this_month_data.find({"date": day})
        merged = ds.merge_rows(aug_events)

        for i in merged:
            if i["content"] == "" or i["content"] == "Invisible":  # not show groups with no events
                continue
            else:
                event_list.append(i)
    return render_template("schedule.html", event_list=event_list, t=t)


@app.route("/about")
def about():
    t = "About"
    return render_template("about.html", t=t)

if __name__ == "__main__":
    app.run(debug=True)