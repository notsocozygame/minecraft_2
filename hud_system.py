from ursina import *
import voxels

class GameHUD:
    def __init__(self, player, is_watch_or_small_screen=True):
        self.player = player
        self.selected_slot = 0
        self.camera_mode = 0
        self.small_screen_mode = is_watch_or_small_screen
        self.virtual_mouse_enabled = False

        # --- TOP HEADER ACTION BUTTONS ---
        self.btn_chat_touch = Button(text='Chat', position=(-0.4, 0.44), scale=(0.09, 0.05), color=color.rgb(40, 40, 40, 200), parent=camera.ui, on_click=self.toggle_chat)
        self.btn_emote_touch = Button(text='Emote', position=(-0.28, 0.44), scale=(0.09, 0.05), color=color.rgb(40, 40, 40, 200), parent=camera.ui, on_click=self.toggle_emotes)
        self.btn_cam_touch = Button(text='Cam', position=(0.28, 0.44), scale=(0.09, 0.05), color=color.rgb(40, 40, 40, 200), parent=camera.ui, on_click=self.cycle_camera)
        
        # Virtual Mouse Toggle Button (Top-Right)
        self.btn_mouse_toggle = Button(text='Mouse: OFF', position=(0.4, 0.44), scale=(0.11, 0.05), color=color.rgb(60, 60, 60, 200), parent=camera.ui, on_click=self.toggle_virtual_mouse)

        # Virtual Mouse Pointer Entity
        self.mouse_cursor = Entity(model='quad', color=color.white, scale=(0.02, 0.03), z=-5, enabled=False, parent=camera.ui)

        # --- HOTBAR ---
        slot_count = 3 if self.small_screen_mode else 9
        self.hotbar_slots = []
        for i in range(slot_count):
            x_pos = -0.12 + (i * 0.12) if self.small_screen_mode else -0.32 + (i * 0.08)
            slot = Button(text=str(i+1), position=(x_pos, -0.42), scale=(0.08, 0.08), color=color.rgb(60, 60, 60, 200), parent=camera.ui, on_click=Func(self.select_slot, i))
            if i == 0:
                slot.color = color.white
            self.hotbar_slots.append(slot)

        # --- HEALTH & HUNGER TEXT READOUTS ---
        self.health_text = Text(text='HP: 20/20', position=(-0.4, -0.34), scale=0.7, color=color.red, parent=camera.ui)
        self.hunger_text = Text(text='Food: 20/20', position=(0.25, -0.34), scale=0.7, color=color.orange, parent=camera.ui)

        # --- TOUCH CONTROLS & MINE / PLACE BUTTONS ---
        self.btn_fwd = Button(text='W', position=(-0.4, -0.2), scale=(0.06, 0.06), color=color.rgb(30, 30, 30, 180), parent=camera.ui)
        self.btn_back = Button(text='S', position=(-0.4, -0.32), scale=(0.06, 0.06), color=color.rgb(30, 30, 30, 180), parent=camera.ui)
        self.btn_left = Button(text='A', position=(-0.46, -0.26), scale=(0.06, 0.06), color=color.rgb(30, 30, 30, 180), parent=camera.ui)
        self.btn_right = Button(text='D', position=(-0.34, -0.26), scale=(0.06, 0.06), color=color.rgb(30, 30, 30, 180), parent=camera.ui)
        self.btn_jump = Button(text='JUMP', position=(0.4, -0.32), scale=(0.09, 0.07), color=color.rgb(50, 120, 200, 200), parent=camera.ui)

        self.btn_mine = Button(text='MINE', position=(0.28, -0.2), scale=(0.1, 0.07), color=color.rgb(180, 50, 50, 220), parent=camera.ui, on_click=voxels.mine_block)
        self.btn_place = Button(text='PLACE', position=(0.4, -0.2), scale=(0.1, 0.07), color=color.rgb(50, 150, 50, 220), parent=camera.ui, on_click=lambda: voxels.place_block(self.selected_slot + 1))

        # --- CHAT SYSTEM ---
        self.chat_input = InputField(default_value='Chat...', y=-0.1, x=0, scale=(0.4, 0.06), enabled=False, parent=camera.ui)
        self.chat_send_btn = Button(text='Send', position=(0.25, -0.1), scale=(0.08, 0.06), color=color.green, enabled=False, parent=camera.ui, on_click=self.send_chat)
        self.chat_log = Text(text='[SERVER] Engine Ready! Bluetooth Keyboard & Mouse Supported', position=(-0.45, 0.28), scale=0.7, parent=camera.ui)

        # --- EMOTE MENU ---
        self.emote_menu = Entity(model='quad', color=color.rgb(20, 20, 20), scale=(0.4, 0.4), z=-2, enabled=False, parent=camera.ui)
        self.emote_title = Text(text='EMOTES', origin=(0, 0), y=0.15, scale=0.8, parent=self.emote_menu)
        self.emote_wave = Button(text='Wave', y=0.05, scale=(0.7, 0.12), parent=self.emote_menu, on_click=lambda: self.play_emote("Waving"))
        self.emote_dance = Button(text='Dance', y=-0.08, scale=(0.7, 0.12), parent=self.emote_menu, on_click=lambda: self.play_emote("Dancing"))

    def toggle_virtual_mouse(self):
        self.virtual_mouse_enabled = not self.virtual_mouse_enabled
        self.mouse_cursor.enabled = self.virtual_mouse_enabled
        mouse.visible = self.virtual_mouse_enabled
        self.btn_mouse_toggle.text = "Mouse: ON" if self.virtual_mouse_enabled else "Mouse: OFF"
        self.btn_mouse_toggle.color = color.green if self.virtual_mouse_enabled else color.rgb(60, 60, 60, 200)

    def select_slot(self, slot_index):
        self.selected_slot = slot_index
        for i, slot in enumerate(self.hotbar_slots):
            slot.color = color.white if i == slot_index else color.rgb(60, 60, 60, 200)

    def cycle_camera(self):
        self.camera_mode = (self.camera_mode + 1) % 3
        if self.camera_mode == 0:
            camera.position = (0, 0, 0)
            camera.rotation = (0, 0, 0)
        elif self.camera_mode == 1:
            camera.position = (0, 2, -5)
            camera.rotation = (10, 0, 0)
        elif self.camera_mode == 2:
            camera.position = (0, 2, 5)
            camera.rotation = (10, 180, 0)

    def toggle_chat(self):
        self.chat_input.enabled = not self.chat_input.enabled
        self.chat_send_btn.enabled = self.chat_input.enabled

    def send_chat(self):
        if self.chat_input.text:
            self.chat_log.text += f"\n[notsocozygames]: {self.chat_input.text}"
            self.chat_input.text = ""
            self.chat_input.enabled = False
            self.chat_send_btn.enabled = False

    def toggle_emotes(self):
        self.emote_menu.enabled = not self.emote_menu.enabled

    def play_emote(self, emote_name):
        self.chat_log.text += f"\n* notsocozygames is {emote_name}"
        self.emote_menu.enabled = False

    def update_controls(self):
        # Update virtual mouse cursor position if active
        if self.virtual_mouse_enabled:
            self.mouse_cursor.position = (mouse.x, mouse.y)

        # Bluetooth / Hardware Keyboard Shortcuts
        if held_keys['f5']:
            self.cycle_camera()
        if held_keys['t'] and not self.chat_input.enabled:
            self.toggle_chat()
        if held_keys['b']:
            self.toggle_emotes()
        
        # Hardware Mouse Clicks (Bluetooth / USB Mouse)
        if held_keys['left mouse']:
            voxels.mine_block()
        if held_keys['right mouse']:
            voxels.place_block(self.selected_slot + 1)

        # Movement (Supports both Bluetooth Keyboard WASD & Touch Buttons)
        speed = 5 * time.dt
        if self.btn_fwd.hovered or held_keys['w']:
            self.player.position += self.player.forward * speed
        if self.btn_back.hovered or held_keys['s']:
            self.player.position += self.player.back * speed
        if self.btn_left.hovered or held_keys['a']:
            self.player.position += self.player.left * speed
        if self.btn_right.hovered or held_keys['d']:
            self.player.position += self.player.right * speed
        if self.btn_jump.hovered or held_keys['space']:
            self.player.y += speed
