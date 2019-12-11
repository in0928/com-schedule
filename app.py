import json
from datetime import datetime
import calendar
from dateutil.relativedelta import relativedelta
from flask import Flask, render_template, request, redirect, url_for  # For flask implementation
from bson import ObjectId  # For ObjectId to work
from pymongo import MongoClient
from pymongo_fetcher import MongoFetcher
import displaySchedule as ds


app = Flask(__name__)

current_year = datetime.now().year
current_month = datetime.now().month
current_num_days = calendar.monthrange(current_year, current_month)[1]
this_month_date = [str(current_month) + "."+str(i+1) for i in range(current_num_days)]

next_month = (datetime.now() + relativedelta(months=1)).month
next_month_year = current_year if next_month != 1 else current_year + 1
next_num_days = calendar.monthrange(next_month_year, next_month)[1]
next_month_date = [str(next_month) + "."+str(i+1) for i in range(next_num_days)]

mf = MongoFetcher()
schedule_this_month_data = mf.schedule_this_month
schedule_next_month_data = mf.schedule_next_month

# TODO: add an entry for refresh time
def get_schedule(this_month_date_list, next_month_date_list):
    this_month_event = []
    for day in this_month_date_list:
        events = schedule_this_month_data.find({"date": day})
        merged = ds.merge_rows(events)
        for i in merged:
            if i["content"] == "" or i["content"] == "Invisible":  # not show groups with no events
                continue
            else:
                this_month_event.append(i)

    next_month_event = []
    # check if next month table is empty
    if schedule_next_month_data.count() > 0:
        for day in next_month_date_list:
            events = schedule_next_month_data.find({"date": day})
            merged = ds.merge_rows(events)
            for i in merged:
                if i["content"] == "" or i["content"] == "Invisible":  # not show groups with no events
                    continue
                else:
                    next_month_event.append(i)
    return this_month_event, next_month_event


@app.route("/")
def home():
    t = "COM Schedule"
    schedules = get_schedule(this_month_date, next_month_date)
    this_schdl = schedules[0]
    next_schdl = schedules[1]
    return render_template("schedule.html", this_schdl=this_schdl, next_schdl=next_schdl, t=t)


@app.route("/about")
def about():
    t = "About"
    return render_template("about.html", t=t)


if __name__ == "__main__":
    app.run(debug=True)
