from tinydb import TinyDB, Query
from pathlib import Path

class GameDatabase:
    def __init__(self, path="emberfall_data.json"):
        self.db = TinyDB(Path(__file__).with_name(path))
        self.accounts = self.db.table("accounts")
        self.progress = self.db.table("progress")

    def account_exists(self, username):
        U = Query()
        return self.accounts.contains(U.username == username)

    def get_account(self, username):
        U = Query()
        return self.accounts.get(U.username == username)

    def create_account(self, account):
        self.accounts.insert(account)

    def load_progress(self, username):
        U = Query()
        row = self.progress.get(U.username == username)
        return row.get("data") if row else None

    def save_progress(self, username, data):
        U = Query()
        self.progress.upsert({"username": username, "data": data}, U.username == username)
