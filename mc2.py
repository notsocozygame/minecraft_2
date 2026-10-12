from ursina import *
from ursina.prefabs.first_person_controller import FirstPersonController
import auth
import world_creator
import multiplayer
import hud_system
import inventory_system
import voxels
import ranks
import math

app = Ursina()

# --- INTRO LOGO & ANIMATION ---
command_block = Entity(model='cube', position=(0, 0, 0), scale=(0, 0, 0), color=color.rgb(180, 100, 50))
logo_text = Text(text='MINECRAFT 2', origin=(0, 0), scale=0, color=color.gold, y=0.32)
edition_subtext = Text(text='JAVA EDITION v0.1', origin=(0, 0), scale=1, color=color.yellow, y=0.24)

loading_bg = Entity(model='quad', color=color.white, scale=(20, 20, 1), z=-1, y=10)
welcome_text = Text(text='Welcome OG Player', origin=(0, 0), scale=2, color=color.black, z=-2, y=10)

# --- LOGIN MENU UI ---
username_input = InputField(default_value='notsocozygames', y=0.1, scale=(0.4, 0.05), z=-4, enabled=False)
password_input = InputField(default_value='cozygame123', hide_content=True, y=0.03, scale=(0.4, 0.05), z=-4, enabled=False)
login_status = Text(text='', origin=(0, 0), y=-0.04, color=color.orange, z=-4, enabled=False)

current_user_data = None

# --- HOME MENU BUTTONS ---
btn_sp = Button(text='Singleplayer', color=color.rgb(100, 100, 100), highlight_color=color.rgb(140, 140, 220), scale=(0.4, 0.06), y=-0.1, z=-4, enabled=False)
btn_mp = Button(text='Multiplayer', color=color.rgb(100, 100, 100), highlight_color=color.rgb(140, 140, 220), scale=(0.4, 0.06), y=-0.18, z=-4, enabled=False)
owner_btn = Button(text='Owner Bypass [CB]', color=color.rgb(120, 70, 30), highlight_color=color.rgb(180, 100, 50), scale=(0.4, 0.06), y=-0.26, z=-4, enabled=False)

# --- IN-GAME LOADING SCREEN UI ---
load_bg = Entity(model='quad', color=color.rgb(40, 30, 20), scale=(12, 9, 1), z=-3, enabled=False)
load_logo = Text(text='MINECRAFT 2', origin=(0, 0), y=0.3, scale=2, color=color.gold, z=-4, enabled=False)
load_ver = Text(text='JAVA EDITION v0.1', origin=(0, 0), y=0.22, scale=1.1, color=color.yellow, z=-4, enabled=False)
load_status = Text(text='Loading world / Joining server...', origin=(0, 0), y=-0.15, scale=1, color=color.white, z=-4, enabled=False)
progress_bar_bg = Entity(model='quad', color=color.rgb(10, 10, 10), scale=(6, 0.3, 1), y=-0.25, z=-3.5, enabled=False)
progress_bar_fill = Entity(model='quad', color=color.rgb(60, 180, 60), scale=(0.1, 0.25, 1), position=(-2.95, -0.25, -3.9), origin=(-0.5, 0), enabled=False)

game_hud = None
game_inv = None
active_player = None

def start_world_loading(destination_name):
    hide_home_menu()
    world_menu.hide()
    multiplayer_menu.hide()
    
    for e in [load_bg, load_logo, load_ver, load_status, progress_bar_bg, progress_bar_fill]:
        e.enabled = True
        
    load_status.text = f"Joining {destination_name}...\nLoading Items & Terrain..."
    animate_loading(0)

def animate_loading(step):
    if step <= 100:
        progress_bar_fill.scale_x = (step / 100.0) * 5.9
        invoke(animate_loading, step + 10, delay=0.1)
    else:
        for e in [load_bg, load_logo, load_ver, load_status, progress_bar_bg, progress_bar_fill]:
            e.enabled = False
        
        voxels.generate_world(size=10)
        spawn_player()

def spawn_player():
    global game_hud, game_inv, active_player, hud_display
    active_player = FirstPersonController()
    active_player.y = 5
    
    game_hud = hud_system.GameHUD(active_player, is_watch_or_small_screen=True)
    game_inv = inventory_system.InventoryMenu(mode="creative")
    
    if current_user_data and current_user_data.get("display_name_style") == "blue_purple_glitch":
        badge_text = "[CB]" if current_user_data.get("badge") == "command_block" else ""
        hud_display = Text(text=f"{badge_text} notsocozygames [OG]", position=(-0.85, 0.45), scale=1.2)

world_menu = world_creator.WorldCreateMenu(on_world_created_callback=lambda w, gm: start_world_loading(f"World '{w}' ({gm.upper()})"))
multiplayer_menu = multiplayer.MultiplayerMenu(on_join_server_callback=lambda ip: start_world_loading(f"Server {ip}"))

def open_sp_menu():
    hide_login_inputs()
    world_menu.show()

def open_mp_menu():
    hide_login_inputs()
    multiplayer_menu.show()

def on_login():
    global current_user_data
    success, msg, user_data = auth.authenticate_user(username_input.text, password_input.text)
    login_status.text = msg
    if success:
        current_user_data = user_data
        show_home_buttons()

def on_owner_bypass():
    global current_user_data
    accounts = auth.load_accounts()
    if username_input.text in accounts and accounts[username_input.text]["password"] == password_input.text:
        current_user_data = accounts[username_input.text]
        login_status.text = "OWNER BYPASS GRANTED!"
        show_home_buttons()
    else:
        login_status.text = "Invalid Owner Credentials!"

btn_sp.on_click = open_sp_menu
btn_mp.on_click = open_mp_menu
owner_btn.on_click = on_owner_bypass

def show_login_inputs():
    for e in [username_input, password_input, login_status, btn_sp, btn_mp, owner_btn]:
        e.enabled = True

def hide_login_inputs():
    for e in [username_input, password_input, login_status, btn_sp, btn_mp, owner_btn]:
        e.enabled = False

def show_home_buttons():
    username_input.enabled = False
    password_input.enabled = False
    login_status.text = "Logged in as OG Owner!"

def hide_home_menu():
    hide_login_inputs()

def input(key):
    global game_inv, game_hud
    if key == 'e' and game_inv:
        game_inv.toggle(current_gamemode="creative")
        if game_hud:
            # Sync inventory selected item to hotbar
            game_hud.selected_slot = game_inv.selected_item_id - 1

hud_display = None
intro_timer = 0
menu_active = False

def update():
    global intro_timer, menu_active, hud_display, game_hud
    
    if game_hud:
        game_hud.update_controls()

    if hud_display:
        t = time.time() * 5
        r = int(100 + 50 * math.sin(t))
        g = int(50 + 20 * math.cos(t * 0.5))
        b = int(225 + 30 * math.sin(t * 1.5))
        hud_display.color = color.rgb(r, g, b)

    if not menu_active:
        intro_timer += time.dt
        if intro_timer < 2:
            command_block.scale = lerp(command_block.scale, (2, 2, 2), time.dt * 4)
            command_block.y = lerp(command_block.y, 1, time.dt * 4)
            logo_text.scale = lerp(logo_text.scale, 2, time.dt * 4)
        elif intro_timer < 4:
            loading_bg.y = lerp(loading_bg.y, 0, time.dt * 6)
            welcome_text.y = lerp(welcome_text.y, 0, time.dt * 6)
        else:
            destroy(loading_bg)
            destroy(welcome_text)
            destroy(command_block)
            destroy(logo_text)
            show_login_inputs()
            menu_active = True

app.run()
