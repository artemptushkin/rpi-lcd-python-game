import arcade

# Constants
SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600
SCREEN_TITLE = "Dog Sprite Demo"
SPRITE_SCALING = 1.0
SPRITE_WIDTH = 64  # Update to match your sprite's width
SPRITE_HEIGHT = 64  # Update to match your sprite's height
COLUMNS = 11
ROWS = 8
first_col_width = 100
states = ["jump", "idle1", "idle2", "sit", "walk", "run", "sniff", "sniff_walk"]

def load_textures_by_state(sprite_sheet_path, sprite_width, sprite_height, columns, rows):

    # Iterate through rows and columns
    # Iterate through rows and columns
    textures_by_state = {state: [] for state in states}

    # Validate that the number of states matches the number of rows
    if len(states) != rows:
        raise ValueError("The number of states must match the number of rows in the sprite sheet.")

    # Iterate through rows and columns, assign textures to states
    for row in range(rows):
        state = states[row]  # Each row corresponds to a state
        for col in range(1, columns):  # Start from column 1 to skip the first column
            x = first_col_width + (col - 1) * sprite_width  # Account for wider first column
            y = row * sprite_height
            texture = arcade.load_texture(sprite_sheet_path, x, y, sprite_width, sprite_height)
            textures_by_state[state].append(texture)

    return textures_by_state


class DogSpriteDemo(arcade.Window):
    def __init__(self):
        super().__init__(SCREEN_WIDTH, SCREEN_HEIGHT, SCREEN_TITLE)
        self.dog_sprite_list = None

    def setup(self):
        arcade.set_background_color(arcade.color.WHITE)
        # Load sprite sheet and create dog sprite
        sprite_sheet_path = "static/welsh-corgi-sprites/corgi-asset.png"  # Path to the sprite sheet
        textures_by_state = load_textures_by_state(
            sprite_sheet_path,
            SPRITE_WIDTH,
            SPRITE_HEIGHT,
            COLUMNS,
            ROWS,
        )

        self.dog_sprite_list = arcade.SpriteList()

        # Example: Access textures for a specific state
        jump_textures = textures_by_state.get("run", [])
        if not jump_textures:
            print("No textures loaded for 'jump' state. Check the sprite sheet and parameters.")
            return

        print(f"Loaded {len(jump_textures)} textures for 'jump' state.")

        # Example: Assign jump textures to a sprite
        sprite = arcade.Sprite()
        sprite.textures = jump_textures
        sprite.set_texture(0)  # Set the initial texture
        sprite.center_x = SCREEN_WIDTH // 2
        sprite.center_y = SCREEN_HEIGHT // 2
        self.dog_sprite_list.append(sprite)

    def on_draw(self):
        arcade.start_render()

        self.dog_sprite_list.draw()

def main():
    window = DogSpriteDemo()
    window.setup()
    arcade.run()

if __name__ == "__main__":
    main()
