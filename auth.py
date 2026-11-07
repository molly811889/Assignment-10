import hashlib
import hmac
import secrets
from colorama import Fore

class Auth:
    def __init__(self, database):
        self.db = database

    @staticmethod
    def hash_password(password, salt):
        return hashlib.pbkdf2_hmac("sha256", password.encode("utf-8"), salt.encode("utf-8"), 120_000).hex()

    def register(self):
        print(Fore.CYAN + "\n--- Register ---")
        username = input("Create username (3-20 characters): ").strip()
        if not 3 <= len(username) <= 20 or not username.replace("_", "").isalnum():
            print(Fore.RED + "Use 3-20 letters, numbers, or underscores.")
            return
        if self.db.account_exists(username):
            print(Fore.RED + "That username is already registered.")
            return
        password = input("Create password (at least 6 characters): ")
        if len(password) < 6:
            print(Fore.RED + "Password must have at least 6 characters.")
            return
        salt = secrets.token_hex(16)
        self.db.create_account({"username": username, "salt": salt, "password_hash": self.hash_password(password, salt)})
        print(Fore.GREEN + "Account created. You can now log in.")

    def login(self):
        print(Fore.CYAN + "\n--- Log in ---")
        username = input("Username: ").strip()
        password = input("Password: ")
        account = self.db.get_account(username)
        if not account:
            print(Fore.RED + "Account not found.")
            return None
        candidate = self.hash_password(password, account["salt"])
        if not hmac.compare_digest(candidate, account["password_hash"]):
            print(Fore.RED + "Incorrect password.")
            return None
        print(Fore.GREEN + f"Welcome back, {username}!")
        return username
