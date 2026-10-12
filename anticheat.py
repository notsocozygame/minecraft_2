import json
import os
import auth

def reset_diamonds_on_creative(username):
    accounts = auth.load_accounts()
    if username in accounts:
        accounts[username]["diamonds"] = 0
        auth.save_accounts(accounts)
        print(f"[WARNING] Creative mode used! {username}'s survival diamonds reset to 0!")

def trigger_strike(username):
    accounts = auth.load_accounts()
    if username not in accounts:
        return

    user = accounts[username]
    current_bans = user.get("ban_count", 0) + 1
    user["ban_count"] = current_bans

    # Check if they were previously temp-banned and came back to hack again
    if user.get("ban_status") == "temp_banned" and current_bans > 1:
        # Instant Permanent Ban via Red-Eyed Nuke for repeat offense after 1-month ban
        user["ban_status"] = "perm_banned"
        auth.save_accounts(accounts)
        print("\n" + "="*50)
        print("🔴 REPEAT OFFENDER DETECTED AFTER 1-MONTH BAN! 🔴")
        print("You ran a script again! The anime warrior's EYES TURN GLOWING RED!")
        print("They pull out a massive NUKE, light the fuse, and throw it at your character!")
        print("BOOOOOOM!!! 💣💥")
        print(">>> ANTI-CHEAT CAUGHT YOU RUNNING A SCRIPT AGAIN! PERMANENT BAN! <<<")
        print("="*50 + "\n")
        return

    if current_bans == 1:
        # Strike 1: Fire Hammer Slam -> 1 Month Ban
        user["ban_status"] = "temp_banned"
        auth.save_accounts(accounts)
        print("\n" + "="*50)
        print("💥 ANIME ANTI-CHEAT ACTIVATED! 💥")
        print("An anime warrior appears with a massive FIRE HAMMER!")
        print("SLAM! You have been hit with the Fire Hammer!")
        print(">>> ANTI-CHEAT CAUGHT YOU! YOU ARE BANNED FOR 1 MONTH. <<<")
        print("="*50 + "\n")

    else:
        # Strike 2+: Permanent Ban
        user["ban_status"] = "perm_banned"
        auth.save_accounts(accounts)
        print("\n" + "="*50)
        print("🔴 ANIME ANTI-CHEAT RE-ACTIVATED! 🔴")
        print("The anime warrior returns with GLOWING RED EYES!")
        print("They pull out a NUKE, light the fuse, and throw it at your character!")
        print("BOOOOOOM!!! 💣💥")
        print(">>> ANTI-CHEAT CAUGHT YOU AGAIN! PERMANENT BAN ISSUED. <<<")
        print("="*50 + "\n")
