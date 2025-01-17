import arcade

# Constants
SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600
SCREEN_TITLE = "Dog Sprite Demo"
SPRITE_SCALING = 2.5
SPRITE_WIDTH = 64  # Update to match your sprite's width
SPRITE_HEIGHT = 64  # Update to match your sprite's height
ROWS = 8
first_col_width = 100
states_columns = {
    "jump": 11,
    "idle1": 5,
    "idle2": 5,
    "sit": 9,
    "walk": 5,
    "run": 8,
    "sniff": 8,
    "sniff_walk": 8,
}
FRAME_DELAY = 0.1  # Time in seconds between frame changes


def load_textures_by_state(sprite_sheet_path, sprite_width, sprite_height, rows):
    # Iterate through rows and columns
    # Iterate through rows and columns
    textures_by_state = {str: [arcade.Texture]}

    # Validate that the number of states matches the number of rows
    if len(states_columns) != rows:
        raise ValueError("The number of states must match the number of rows in the sprite sheet.")

    # Iterate through rows and columns, assign textures to states
    row = 0
    for state, columns in states_columns.items():
        textures = []
        for col in range(1, columns):  # Start from column 1 to skip the first column
            x = first_col_width + (col - 1) * sprite_width  # Account for wider first column
            y = row * sprite_height
            texture = arcade.load_texture(sprite_sheet_path, x, y, sprite_width, sprite_height)
            textures.append(texture)
        row = row + 1
        textures_by_state.update({state: textures})

    return textures_by_state


class TexturesData:
    def __init__(self, textures: [arcade.Texture]):
        self.textures = textures


class SpriteData:
    def __init__(self, initial_frame, length, textures):
        self.current_frame = initial_frame
        self.length = length
        self.textures = textures


class DogSpriteDemo(arcade.Window):
    def __init__(self):
        super().__init__(SCREEN_WIDTH, SCREEN_HEIGHT, SCREEN_TITLE)
        self.textures_by_state_name = None
        self.dog_sprite_list = None  # SpriteList for the dog sprite
        self.dog_sprite = None  # The animated sprite
        self.sprite_data = None

    def setup(self):
        """Set up the game and initialize variables."""
        # Set the background color
        arcade.set_background_color(arcade.color.WHITE)

        # Load sprite sheet and textures
        sprite_sheet_path = "static/welsh-corgi-sprites/corgi-asset.png"  # Path to the sprite sheet
        self.textures_by_state_name = load_textures_by_state(
            sprite_sheet_path,
            SPRITE_WIDTH,
            SPRITE_HEIGHT,
            ROWS,
        )

        # Schedule the animation update
        arcade.schedule(self.update_texture, FRAME_DELAY)

    def sit(self):
        current_textures = self.textures_by_state_name["sit"]
        self.sprite_data = SpriteData(0, len(current_textures), current_textures)

        # Create the dog sprite
        self.dog_sprite_list = arcade.SpriteList()
        self.dog_sprite = arcade.Sprite(scale=SPRITE_SCALING)
        self.dog_sprite.texture = self.sprite_data.textures[self.sprite_data.current_frame]
        self.dog_sprite.center_x = SCREEN_WIDTH // 2
        self.dog_sprite.center_y = SCREEN_HEIGHT // 2

        self.dog_sprite_list.append(self.dog_sprite)

    def jump(self):
        current_textures = self.textures_by_state_name["jump"]
        self.sprite_data = SpriteData(0, len(current_textures), current_textures)

        # Create the dog sprite
        self.dog_sprite_list = arcade.SpriteList()
        self.dog_sprite = arcade.Sprite(scale=SPRITE_SCALING)
        self.dog_sprite.texture = self.sprite_data.textures[self.sprite_data.current_frame]
        self.dog_sprite.center_x = SCREEN_WIDTH // 2
        self.dog_sprite.center_y = SCREEN_HEIGHT // 2

        self.dog_sprite_list.append(self.dog_sprite)

    def update_texture(self, delta_time):
        """Update the sprite texture every FRAME_DELAY seconds."""
        self.sprite_data.current_frame = (
                                                 self.sprite_data.current_frame + 1) % self.sprite_data.length  # Cycle between frames 0 to frame
        self.dog_sprite.texture = self.sprite_data.textures[self.sprite_data.current_frame]

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
    dog = DogSpriteDemo()
    dog.setup()
    dog.sit()
    arcade.run()

if __name__ == "__main__":
    main()
