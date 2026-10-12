from ursina import *
import random

BLOCK_TYPES = {
    # Building Blocks
    1: {"name": "Grass", "color": color.rgb(80, 160, 60), "category": "Building", "type": "block"},
    2: {"name": "Dirt", "color": color.rgb(120, 80, 40), "category": "Building", "type": "block"},
    3: {"name": "Stone", "color": color.rgb(120, 120, 120), "category": "Building", "type": "block"},
    4: {"name": "Bedrock", "color": color.rgb(30, 30, 30), "category": "Building", "type": "block"},
    5: {"name": "Cobblestone", "color": color.rgb(90, 90, 90), "category": "Building", "type": "block"},
    6: {"name": "Oak Planks", "color": color.rgb(160, 115, 65), "category": "Building", "type": "block"},
    7: {"name": "Glass", "color": color.rgb(200, 230, 255), "category": "Building", "type": "block"},
    8: {"name": "Obsidian", "color": color.rgb(20, 15, 30), "category": "Building", "type": "block"},
    
    # Ores & Minerals
    9: {"name": "Coal Ore", "color": color.rgb(60, 60, 60), "category": "Ores", "type": "block"},
    10: {"name": "Iron Ore", "color": color.rgb(180, 150, 130), "category": "Ores", "type": "block"},
    11: {"name": "Gold Ore", "color": color.rgb(220, 190, 70), "category": "Ores", "type": "block"},
    12: {"name": "Diamond Ore", "color": color.rgb(80, 220, 240), "category": "Ores", "type": "block"},
    
    # Natural Blocks
    13: {"name": "Oak Wood", "color": color.rgb(100, 60, 30), "category": "Natural", "type": "block"},
    14: {"name": "Oak Leaves", "color": color.rgb(40, 140, 40), "category": "Natural", "type": "block"},
    15: {"name": "Sand", "color": color.rgb(220, 210, 140), "category": "Natural", "type": "block"},
    
    # Functional
    16: {"name": "Crafting Table", "color": color.rgb(150, 100, 50), "category": "Functional", "type": "block"},
    17: {"name": "Furnace", "color": color.rgb(80, 80, 80), "category": "Functional", "type": "block"},
    18: {"name": "Chest", "color": color.rgb(180, 120, 40), "category": "Functional", "type": "block"},
    19: {"name": "Command Block", "color": color.rgb(190, 110, 60), "category": "Functional", "type": "block"},

    # Weapons & Combat
    20: {"name": "Wooden Sword", "color": color.rgb(130, 90, 50), "category": "Combat", "type": "weapon"},
    21: {"name": "Iron Sword", "color": color.rgb(200, 200, 200), "category": "Combat", "type": "weapon"},
    22: {"name": "Diamond Sword", "color": color.rgb(100, 240, 220), "category": "Combat", "type": "weapon"},
    23: {"name": "Bow", "color": color.rgb(110, 75, 40), "category": "Combat", "type": "weapon"},

    # Tools & Utilities
    24: {"name": "Wooden Pickaxe", "color": color.rgb(130, 90, 50), "category": "Tools", "type": "tool"},
    25: {"name": "Iron Pickaxe", "color": color.rgb(200, 200, 200), "category": "Tools", "type": "tool"},
    26: {"name": "Diamond Pickaxe", "color": color.rgb(100, 240, 220), "category": "Tools", "type": "tool"},
    27: {"name": "Flint and Steel", "color": color.rgb(80, 80, 80), "category": "Tools", "type": "tool"},

    # Food & Consumables
    28: {"name": "Apple", "color": color.rgb(220, 40, 40), "category": "Food", "type": "food"},
    29: {"name": "Golden Apple", "color": color.rgb(250, 220, 50), "category": "Food", "type": "food"},
    30: {"name": "Bread", "color": color.rgb(190, 140, 70), "category": "Food", "type": "food"},
    31: {"name": "Cooked Beef", "color": color.rgb(110, 60, 30), "category": "Food", "type": "food"}
}

class Voxel(Button):
    def __init__(self, position=(0,0,0), block_id=1):
        self.block_id = block_id
        self.block_info = BLOCK_TYPES.get(block_id, BLOCK_TYPES[1])
        
        super().__init__(
            parent=scene,
            position=position,
            model='cube',
            origin_y=0.5,
            texture='white_cube',
            color=self.block_info["color"],
            highlight_color=color.lime
        )

def generate_world(size=10):
    print("[WORLD GEN] Generating terrain...")
    for x in range(-size, size):
        for z in range(-size, size):
            Voxel(position=(x, 0, z), block_id=1)
            Voxel(position=(x, -1, z), block_id=2)
            Voxel(position=(x, -2, z), block_id=2)
            for y in range(-5, -2):
                if random.random() < 0.1:
                    Voxel(position=(x, y, z), block_id=12)
                else:
                    Voxel(position=(x, y, z), block_id=3)
            Voxel(position=(x, -6, z), block_id=4)
            if random.random() < 0.04 and (abs(x) > 2 or abs(z) > 2):
                spawn_tree(x, 1, z)

def spawn_tree(x, y, z):
    for trunk_y in range(y, y + 4):
        Voxel(position=(x, trunk_y, z), block_id=13)
    for leaf_x in range(x - 1, x + 2):
        for leaf_z in range(z - 1, z + 2):
            for leaf_y in range(y + 3, y + 5):
                if not (leaf_x == x and leaf_z == z and leaf_y < y + 4):
                    Voxel(position=(leaf_x, leaf_y, leaf_z), block_id=14)

def mine_block():
    if mouse.hovered_entity and isinstance(mouse.hovered_entity, Voxel):
        if mouse.hovered_entity.block_id != 4:
            destroy(mouse.hovered_entity)

def place_block(block_id=1):
    # Only place if it's a valid block type
    if block_id in BLOCK_TYPES and BLOCK_TYPES[block_id]["type"] == "block":
        if mouse.hovered_entity and isinstance(mouse.hovered_entity, Voxel):
            hit_position = mouse.hovered_entity.position + mouse.normal
            Voxel(position=hit_position, block_id=block_id)
