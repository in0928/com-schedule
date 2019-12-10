from pymongo import MongoClient


class MongoFetcher:

    def __init__(self):
        # real DB
        self.client = MongoClient("mongodb+srv://in0928:trybest920928LAISAI@cluster0-nfgyd.gcp.mongodb.net/test?retryWrites=true&w=majority")  # host uri
        self.db = self.client.NSDB  # Select the database
        self.schedule_this_month = self.db.scheduleThisMonth
        self.schedule_next_month = self.db.scheduleNextMonth
        self.unions = self.db.unions  # 2 this is used with schedule
