from ursina import *
import json
import os

SERVERS_FILE = 'servers.json'

def load_servers():
    if os.path.exists(SERVERS_FILE):
        with open(SERVERS_FILE, 'r') as f:
            return json.load(f)
    return {
        "Minecraft 2 Official": {"ip": "127.0.0.1", "port": 25565, "motd": "Official Pre-v1.0 Server"}
    }

class MultiplayerMenu:
    def __init__(self, on_join_server_callback):
        self.on_join_server = on_join_server_callback

        # Menu Background & Title
        self.bg = Entity(model='quad', color=color.rgb(30, 30, 30), scale=(12, 9, 1), z=-3, enabled=False)
        self.title = Text(text='Play Multiplayer', origin=(0, 0), y=0.38, scale=1.8, z=-4, enabled=False)

        # Server List & LAN Friends Display Box
        self.server_box = Entity(model='quad', color=color.rgb(15, 15, 15), scale=(7, 1.8, 1), y=0.15, z=-3.5, enabled=False)
        self.server_info = Text(text='[ONLINE] Minecraft 2 Official\nIP: 127.0.0.1:25565 | Ping: 12ms', origin=(0, 0), y=0.15, scale=0.9, color=color.green, z=-4, enabled=False)

        # LAN Friend's World Scanner Box
        self.lan_box = Entity(model='quad', color=color.rgb(20, 25, 35), scale=(7, 1.8, 1), y=-0.08, z=-3.5, enabled=False)
        self.lan_info = Text(text='📡 Scanning for local games on your network...\n[FRIEND ONLINE] CozyGamer_Friend\'s Survival World\nHost: 192.168.1.15:25565', origin=(0, 0), y=-0.08, scale=0.85, color=color.azure, z=-4, enabled=False)

        # Direct Connection IP Input
        self.ip_label = Text(text='Direct Connect IP:', origin=(0, 0), y=-0.22, scale=0.8, color=color.gray, z=-4, enabled=False)
        self.ip_input = InputField(default_value='192.168.1.15:25565', y=-0.28, scale=(0.4, 0.05), z=-4, enabled=False)

        # Action Buttons
        self.join_btn = Button(text='Join Selected World', color=color.rgb(60, 140, 60), highlight_color=color.rgb(80, 180, 80), scale=(0.35, 0.055), y=-0.36, x=-0.2, z=-4, enabled=False, on_click=self.confirm_join)
        self.cancel_btn = Button(text='Cancel', color=color.rgb(100, 100, 100), highlight_color=color.rgb(140, 140, 140), scale=(0.35, 0.055), y=-0.36, x=0.2, z=-4, enabled=False, on_click=self.hide)

    def show(self):
        for e in [self.bg, self.title, self.server_box, self.server_info, self.lan_box, self.lan_info, self.ip_label, self.ip_input, self.join_btn, self.cancel_btn]:
            e.enabled = True

    def hide(self):
        for e in [self.bg, self.title, self.server_box, self.server_info, self.lan_box, self.lan_info, self.ip_label, self.ip_input, self.join_btn, self.cancel_btn]:
            e.enabled = False

    def confirm_join(self):
        target_ip = self.ip_input.text
        print(f"[MULTIPLAYER] Joining world/server at {target_ip}...")
        self.hide()
        self.on_join_server(target_ip)
