import arcade

from sprites import load_textures_by_state

SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600
SCREEN_TITLE = "Dog Sprite game"  # todo rename
SPRITE_SCALING = 1.0
SPRITE_WIDTH = 64  # Update to match your sprite's width
SPRITE_HEIGHT = 64  # Update to match your sprite's height
COLUMNS = 11
ROWS = 8
DOG_STATES = ["jump", "idle1", "idle2", "sit", "walk", "run", "sniff", "sniff_walk"]


class DogSpriteDemo(arcade.Window):
    def __init__(self, sprite_sheet_path):
        super().__init__(SCREEN_WIDTH, SCREEN_HEIGHT, SCREEN_TITLE)
        self.sprite_sheet_path = sprite_sheet_path
        self.dog_sprite_list = None
        self.initial_state = "idle1"

    def setup(self):
        self.dog_sprite_list = arcade.SpriteList()
        arcade.set_background_color(arcade.color.WHITE)
        # Load sprite sheet and create dog sprite
        textures_by_state = load_textures_by_state(
            self.sprite_sheet_path,
            SPRITE_WIDTH,
            SPRITE_HEIGHT,
            COLUMNS,
            ROWS,
            DOG_STATES
        )

        # Example: Access textures for a specific state
        jump_textures = textures_by_state.get(self.initial_state, [])
        if not jump_textures:
            print("No textures loaded for 'jump' state. Check the sprite sheet and parameters.")
            return

        # Example: Assign jump textures to a sprite
        sprite = arcade.Sprite(scale=2.5)
        sprite.textures = jump_textures
        sprite.set_texture(0)  # Set the initial texture
        sprite.center_x = SCREEN_WIDTH // 2
        sprite.center_y = SCREEN_HEIGHT // 2
        self.dog_sprite_list.append(sprite)

    def on_draw(self):
        arcade.start_render()

        self.dog_sprite_list.draw()
