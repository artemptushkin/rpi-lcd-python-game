import arcade

# Constants
SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600
SCREEN_TITLE = "Dog Sprite Demo"
SPRITE_SCALING = 2.5
SPRITE_WIDTH = 64  # Update to match your sprite's width
SPRITE_HEIGHT = 64  # Update to match your sprite's height
COLUMNS = 11
ROWS = 8
first_col_width = 100
states = ["jump", "idle1", "idle2", "sit", "walk", "run", "sniff", "sniff_walk"]
FRAME_DELAY = 0.2  # Time in seconds between frame changes

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
        self.dog_sprite_list = None  # SpriteList for the dog sprite
        self.dog_sprite = None       # The animated sprite
        self.current_frame = 0       # Tracks the current frame for animation
        self.sprite_textures = []    # Holds textures for the animation

    def setup(self):
        """Set up the game and initialize variables."""
        # Set the background color
        arcade.set_background_color(arcade.color.WHITE)

        # Load sprite sheet and textures
        sprite_sheet_path = "static/welsh-corgi-sprites/corgi-asset.png"  # Path to the sprite sheet
        self.sprite_textures = load_textures_by_state(
            sprite_sheet_path,
            SPRITE_WIDTH,
            SPRITE_HEIGHT,
            COLUMNS,
            ROWS,
        )["run"]

        # Create the dog sprite
        self.dog_sprite_list = arcade.SpriteList()
        self.dog_sprite = arcade.Sprite(scale=SPRITE_SCALING)
        self.dog_sprite.texture = self.sprite_textures[self.current_frame]  # Start with the first frame
        self.dog_sprite.center_x = SCREEN_WIDTH // 2
        self.dog_sprite.center_y = SCREEN_HEIGHT // 2

        # Add the sprite to the list
        self.dog_sprite_list.append(self.dog_sprite)

        # Schedule the animation update
        arcade.schedule(self.update_texture, FRAME_DELAY)

    def update_texture(self, delta_time):
        """Update the sprite texture every FRAME_DELAY seconds."""
        self.current_frame = (self.current_frame + 1) % 8  # Cycle between frames 0 to 9
        self.dog_sprite.texture = self.sprite_textures[self.current_frame]

    def on_draw(self):
        arcade.start_render()

        self.dog_sprite_list.draw()
        for sprite in self.dog_sprite_list:
            arcade.draw_rectangle_outline(
                center_x=sprite.center_x,
                center_y=sprite.center_y,
                width=sprite.width,
                height=sprite.height,
                color=arcade.color.BLACK,
                border_width=2  # Thickness of the border
            )

def main():
    window = DogSpriteDemo()
    window.setup()
    arcade.run()

if __name__ == "__main__":
    main()
