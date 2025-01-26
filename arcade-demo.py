import arcade
import time

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
    textures_by_state = {}

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
            mirror_texture = arcade.load_texture(sprite_sheet_path, x, y, sprite_width, sprite_height, mirrored=True)
            textures.append((texture, mirror_texture))
        row += 1
        textures_by_state[state] = textures

    return textures_by_state


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
        self.is_jumping = False
        self.jump_frames_remaining = 0
        self.is_walking = False
        self.facing_right = True

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

        # Initialize the dog in the sit state
        self.sit()

        # Schedule the animation update
        arcade.schedule(self.update_texture, FRAME_DELAY)

    def sit(self):
        current_textures = self.textures_by_state_name["sit"]
        self.sprite_data = SpriteData(0, len(current_textures), current_textures)

        # Create the dog sprite
        self.dog_sprite_list = arcade.SpriteList()
        self.dog_sprite = arcade.Sprite(scale=SPRITE_SCALING)
        self.dog_sprite.texture = self.sprite_data.textures[self.sprite_data.current_frame][0 if self.facing_right else 1]
        self.dog_sprite.center_x = SCREEN_WIDTH // 2
        self.dog_sprite.center_y = SCREEN_HEIGHT // 2

        self.dog_sprite_list.append(self.dog_sprite)
        self.is_walking = False

    def jump(self):
        current_textures = self.textures_by_state_name["jump"]
        self.sprite_data = SpriteData(0, len(current_textures), current_textures)

        # Create the dog sprite
        self.dog_sprite_list = arcade.SpriteList()
        self.dog_sprite = arcade.Sprite(scale=SPRITE_SCALING)
        self.dog_sprite.texture = self.sprite_data.textures[self.sprite_data.current_frame][0 if self.facing_right else 1]
        self.dog_sprite.center_x = SCREEN_WIDTH // 2
        self.dog_sprite.center_y = SCREEN_HEIGHT // 2

        self.dog_sprite_list.append(self.dog_sprite)
        self.is_jumping = True
        self.jump_frames_remaining = len(current_textures)

    def walk(self, direction):
        current_textures = self.textures_by_state_name["walk"]
        self.sprite_data = SpriteData(0, len(current_textures), current_textures)

        self.facing_right = direction == "right"
        self.dog_sprite.texture = self.sprite_data.textures[self.sprite_data.current_frame][
            0 if self.facing_right else 1]

        # Set movement direction
        self.dog_sprite.change_x = 2 if self.facing_right else -2
        self.is_walking = True

    def update(self, delta_time):
        """Update game logic."""
        if self.dog_sprite:
            self.dog_sprite.center_x += self.dog_sprite.change_x

    def update_texture(self, delta_time):
        """Update the sprite texture every FRAME_DELAY seconds."""
        if self.sprite_data:
            self.sprite_data.current_frame = (
                self.sprite_data.current_frame + 1
            ) % self.sprite_data.length  # Cycle between frames 0 to frame
            self.dog_sprite.texture = self.sprite_data.textures[self.sprite_data.current_frame][0 if self.facing_right else 1]

        # Handle jump state completion
        if self.is_jumping:
            self.jump_frames_remaining -= 1
            if self.jump_frames_remaining <= 0:
                self.is_jumping = False
                self.sit()

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

    def on_key_press(self, key, modifiers):
        if key == arcade.key.SPACE and not self.is_jumping:
            self.jump()
        elif key == arcade.key.LEFT:
            self.walk("left")
        elif key == arcade.key.RIGHT:
            self.walk("right")

    def on_key_release(self, key, modifiers):
        if key in (arcade.key.LEFT, arcade.key.RIGHT):
            self.dog_sprite.change_x = 0
            self.is_walking = False


def main():
    dog = DogSpriteDemo()
    dog.setup()
    arcade.run()


if __name__ == "__main__":
    main()
