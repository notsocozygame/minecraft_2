import json
import os

ACCOUNTS_FILE = 'accounts.json'

def load_accounts():
    if os.path.exists(ACCOUNTS_FILE):
        with open(ACCOUNTS_FILE, 'r') as f:
            return json.load(f)
    return {}

def save_accounts(data):
    with open(ACCOUNTS_FILE, 'w' ) as f:
        json.dump(data, f, indent=4)

def register_user(username, password, is_og_phase=True):
    accounts = load_accounts()
    if username in accounts:
        return False, "Username already exists!", None
    
    user_data = {
        "password": password,
        "is_og": is_og_phase,
        "diamonds": 0,
        "ban_status": "none",
        "ban_count": 0,
        "display_name_style": "standard",
        "badge": "none"
    }
    accounts[username] = user_data
    save_accounts(accounts)
    return True, "Account created successfully!", user_data

def authenticate_user(username, password):
    accounts = load_accounts()
    if username not in accounts:
        return False, "User not found!", None
    
    user = accounts[username]
    
    if user.get("ban_status") == "perm_banned":
        return False, "ANTI-CHEAT: RED EYES ANIME NUKE PERM BAN ACTIVE!", None
    elif user.get("ban_status") == "temp_banned":
        return False, "ANTI-CHEAT: FIRE HAMMER 1-MONTH BAN ACTIVE!", None
        
    if user["password"] == password:
        return True, f"Welcome back, {username}!", user
    return False, "Incorrect password!", None
