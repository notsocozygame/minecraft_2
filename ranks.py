import json
import os

RANKS_FILE = 'ranks.json'

DEFAULT_RANKS = {
    "notsocozygames": {"rank": "Owner", "badge": "[🔲]", "can_use_commands": True, "gamemode_override": "owner"}
}

def load_ranks():
    if os.path.exists(RANKS_FILE):
        with open(RANKS_FILE, 'r') as f:
            return json.load(f)
    return DEFAULT_RANKS

def save_ranks(ranks_data):
    with open(RANKS_FILE, 'w') as f:
        json.dump(ranks_data, f, indent=4)

def set_player_rank(username, rank_name):
    ranks = load_ranks()
    valid_ranks = {
        "Owner": {"badge": "[🔲]", "can_use_commands": True},
        "Admin": {"badge": "[🛡️]", "can_use_commands": True},
        "Mod": {"badge": "[⚔️]", "can_use_commands": True},
        "VIP": {"badge": "[⭐]", "can_use_commands": False},
        "Player": {"badge": "", "can_use_commands": False}
    }
    
    if rank_name in valid_ranks:
        ranks[username] = {
            "rank": rank_name,
            "badge": valid_ranks[rank_name]["badge"],
            "can_use_commands": valid_ranks[rank_name]["can_use_commands"]
        }
        save_ranks(ranks)
        return True, f"Successfully set {username}'s rank to {rank_name}!"
    return False, "Invalid rank specified."

def get_player_rank(username):
    ranks = load_ranks()
    return ranks.get(username, {"rank": "Player", "badge": "", "can_use_commands": False})
