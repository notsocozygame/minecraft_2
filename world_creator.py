from ursina import *
import json
import os

WORLDS_FILE = 'worlds.json'

def load_worlds():
    if os.path.exists(WORLDS_FILE):
        with open(WORLDS_FILE, 'r') as f:
            return json.load(f)
    return {}

def save_world(world_name, gamemode="survival", difficulty="normal", allow_cheats=False, seed=""):
    worlds = load_worlds()
    worlds[world_name] = {
        "gamemode": gamemode,
        "difficulty": difficulty,
        "allow_cheats": allow_cheats,
        "seed": seed
    }
    with open(WORLDS_FILE, 'w') as f:
        json.dump(worlds, f, indent=4)
    print(f"[WORLD CREATOR] Created world '{world_name}' ({gamemode.upper()} mode)")

class WorldCreateMenu:
    def __init__(self, on_world_created_callback):
        self.on_world_created = on_world_created_callback
        self.gamemodes = ["survival", "creative", "hardcore", "adventure", "spectator", "owner"]
        self.gm_index = 0
        
        self.cheats_enabled = False

        # Menu UI Entities
        self.bg = Entity(model='quad', color=color.rgb(40, 40, 40), scale=(12, 9, 1), z=-3, enabled=False)
        self.title = Text(text='Create New World', origin=(0, 0), y=0.35, scale=1.8, z=-4, enabled=False)

        # World Name Field
        self.name_label = Text(text='World Name', origin=(0, 0), y=0.25, scale=0.9, color=color.gray, z=-4, enabled=False)
        self.name_input = InputField(default_value='New World', y=0.18, scale=(0.4, 0.05), z=-4, enabled=False)

        # Game Mode Switcher Button
        self.gm_btn = Button(text='Game Mode: Survival', color=color.rgb(100, 100, 100), highlight_color=color.rgb(140, 140, 220), scale=(0.4, 0.06), y=0.08, z=-4, enabled=False, on_click=self.toggle_gamemode)

        # Allow Cheats Switcher Button
        self.cheats_btn = Button(text='Allow Cheats: OFF', color=color.rgb(100, 100, 100), highlight_color=color.rgb(140, 140, 220), scale=(0.4, 0.06), y=0.0, z=-4, enabled=False, on_click=self.toggle_cheats)

        # Create & Cancel Buttons
        self.create_btn = Button(text='Create New World', color=color.rgb(60, 140, 60), highlight_color=color.rgb(80, 180, 80), scale=(0.4, 0.06), y=-0.12, z=-4, enabled=False, on_click=self.confirm_creation)

    def show(self):
        for e in [self.bg, self.title, self.name_label, self.name_input, self.gm_btn, self.cheats_btn, self.create_btn]:
            e.enabled = True

    def hide(self):
        for e in [self.bg, self.title, self.name_label, self.name_input, self.gm_btn, self.cheats_btn, self.create_btn]:
            e.enabled = False

    def toggle_gamemode(self):
        self.gm_index = (self.gm_index + 1) % len(self.gamemodes)
        current_gm = self.gamemodes[self.gm_index]
        self.gm_btn.text = f"Game Mode: {current_gm.capitalize()}"

    def toggle_cheats(self):
        self.cheats_enabled = not self.cheats_enabled
        self.cheats_btn.text = f"Allow Cheats: {'ON' if self.cheats_enabled else 'OFF'}"

    def confirm_creation(self):
        world_name = self.name_input.text
        selected_gm = self.gamemodes[self.gm_index]
        save_world(world_name, gamemode=selected_gm, allow_cheats=self.cheats_enabled)
        self.hide()
        self.on_world_created(world_name, selected_gm)
