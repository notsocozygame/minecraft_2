from ursina import *
import voxels

class InventoryMenu:
    def __init__(self, mode="creative"):
        self.mode = mode
        self.is_open = False
        self.selected_item_id = 1

        self.bg = Entity(model='quad', color=color.rgb(30, 30, 30, 240), scale=(0.95, 0.85), z=-3, enabled=False, parent=camera.ui)
        self.title = Text(text='Creative Inventory - All Items', position=(-0.42, 0.38), scale=1, parent=self.bg)

        # Category Tab Buttons (No Emojis)
        self.btn_all = Button(text='All', position=(-0.4, 0.3), scale=(0.09, 0.05), color=color.rgb(70, 70, 70), parent=self.bg, on_click=lambda: self.load_category("All"))
        self.btn_building = Button(text='Building', position=(-0.28, 0.3), scale=(0.11, 0.05), color=color.rgb(70, 70, 70), parent=self.bg, on_click=lambda: self.load_category("Building"))
        self.btn_combat = Button(text='Combat', position=(-0.14, 0.3), scale=(0.11, 0.05), color=color.rgb(70, 70, 70), parent=self.bg, on_click=lambda: self.load_category("Combat"))
        self.btn_tools = Button(text='Tools', position=(0.0, 0.3), scale=(0.11, 0.05), color=color.rgb(70, 70, 70), parent=self.bg, on_click=lambda: self.load_category("Tools"))
        self.btn_food = Button(text='Food', position=(0.14, 0.3), scale=(0.11, 0.05), color=color.rgb(70, 70, 70), parent=self.bg, on_click=lambda: self.load_category("Food"))
        self.btn_functional = Button(text='Functional', position=(0.3, 0.3), scale=(0.13, 0.05), color=color.rgb(70, 70, 70), parent=self.bg, on_click=lambda: self.load_category("Functional"))

        self.item_buttons = []
        self.load_category("All")

    def load_category(self, category_name):
        for btn in self.item_buttons:
            destroy(btn)
        self.item_buttons.clear()

        col = 0
        row = 0
        for item_id, data in voxels.BLOCK_TYPES.items():
            if category_name == "All" or data["category"] == category_name:
                x_pos = -0.38 + (col * 0.15)
                y_pos = 0.18 - (row * 0.09)
                
                btn = Button(text=data["name"], position=(x_pos, y_pos), scale=(0.14, 0.07), color=data["color"], parent=self.bg, on_click=Func(self.select_item, item_id))
                self.item_buttons.append(btn)
                
                col += 1
                if col >= 5:
                    col = 0
                    row += 1

    def select_item(self, item_id):
        self.selected_item_id = item_id
        item_name = voxels.BLOCK_TYPES[item_id]["name"]
        print(f"[INVENTORY] Selected item: {item_name} (ID: {item_id})")

    def toggle(self, current_gamemode="creative"):
        self.is_open = not self.is_open
        self.bg.enabled = self.is_open
