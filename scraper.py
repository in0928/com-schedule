from bs4 import BeautifulSoup as bs
from requests import Session
from html.parser import HTMLParser
from pymongo import MongoClient
from datetime import datetime
from dateutil.relativedelta import relativedelta

client = MongoClient("mongodb+srv://in0928:trybest920928LAISAI@cluster0-nfgyd.gcp.mongodb.net/test?retryWrites=true&w=majority")  # host uri
db = client.NSDB  # Select the database
schedule_this_month = db.scheduleThisMonth
schedule_next_month = db.scheduleNextMonth


def login():
    with Session() as s:
        login_url = "https://www.improveonline.jp/"
        login_data = {"loginid": "in0928", "password": "54hanghang"}
        s.post(login_url, login_data)
    return s


def get_table_data(SessionObj, url):
    """Given any union url, returns the html with all tr tags"""
    schedule = SessionObj.get(url)
    schedule_content = bs(schedule.content, "html.parser")
    schedule_table = schedule_content.find_all("tr")  # get the full table in list
    return schedule_table


def insert_row_data(table, union_name, cursor):
    for row in table:
        row_date = row.find("th").text
        row_data = row.find_all("td")
        row_dic_keys = ["date", "union_name", "content", "time", "SP", "MC_AC", "venue"]
        row_list = [row_date, union_name]
        row_data_dic = {}
        # iterate through every cell
        for item in row_data:
            val = item.text
            row_list.append(val) # a list with 5 values from 5 cells in the same row

        # Create a dic to send to MongoDB
        for i in range(len(row_dic_keys)):
            row_data_dic[row_dic_keys[i]] = row_list[i]
        cursor.insert_one(row_data_dic)


def create_urls(group_id, year_month):
    base = "https://www.improveonline.jp/mypage/union/schedule_detail.php?"
    date = "date=" + year_month + "&"  # notice & is attached
    suffix = "&mc=8"  # notice & is at the beginning
    return base + date + group_id + suffix


# call this upon clicking refresh
def fetch_schedule():
    tokyo_union_ids = {"AiM": "group=91",
                       "AXIS": "group=12",
                       "BLAST": "group=20",
                       "DUCERE": "group=25",
                       "FEST": "group=42",
                       "GATE": "group=11",
                       "IDEA": "group=46",
                       "INNOVATION": "group=65",
                       "LIBERTAS": "group=79",
                       "ONE": "group=13",
                       "PRESTO": "group=4",
                       "RIZING TOKYO": "group=86",
                       "SPIRITS": "group=19",
                       "零（Rei）": "group=24"}

    this_year_month = datetime.now().strftime("%Y-%m")
    next_year_month = (datetime.now() + relativedelta(months=1)).strftime("%Y-%m")
    session = login()
    schedule_this_month.insert_one({"timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S")})
    schedule_next_month.insert_one({"timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S")})

    for union, id in tokyo_union_ids.items():
        print(f"START fetching for {union}")
        this_url = create_urls(id, this_year_month)
        this_table = get_table_data(session, this_url)
        insert_row_data(this_table, union, schedule_this_month)

        next_url = create_urls(id, next_year_month)
        next_table = get_table_data(session, next_url)
        insert_row_data(next_table, union, schedule_next_month)
        print(f"DONE fetching for {union}")
        print("------")

if __name__ == "__main__":
    schedule_this_month.delete_many({})
    schedule_next_month.delete_many({})
    fetch_schedule()
