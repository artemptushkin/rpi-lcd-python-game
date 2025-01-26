import sys

import arcade
import time

# Constants
SCREEN_WIDTH = 1280
SCREEN_HEIGHT = 720
SCREEN_TITLE = "Dog Sprite Demo"
SPRITE_SCALING = 2.5
SPRITE_WIDTH = 64  # Update to match your sprite's width
SPRITE_HEIGHT = 64  # Update to match your sprite's height
ROWS = 8
INITIAL_POSITION_X = SCREEN_WIDTH // 4 - 150  # Initial X position
INITIAL_POSITION_Y = SCREEN_HEIGHT // 4 - 50 # Initial Y position
JUMP_MOVE_X = 50  # Horizontal movement during jump
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

def mock_lego_build_hat_input():
    # This is just a mock. Replace it with actual Lego Build Hat logic later.
    # Returns a dictionary of mock inputs for testing
    return {
        "jump": False,
        "walk_left": False,
        "walk_right": False
    }

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
    def __init__(self, is_mac):
        super().__init__(SCREEN_WIDTH, SCREEN_HEIGHT, SCREEN_TITLE)
        self.is_mac = is_mac
        self.textures_by_state_name = None
        self.dog_sprite_list = None  # SpriteList for the dog sprite
        self.dog_sprite = None  # The animated sprite
        self.sprite_data = None
        self.is_jumping = False
        self.jump_frames_remaining = 0
        self.is_walking = False
        self.facing_right = True
        self.background_texture = None
        self.start_jump_x = None
        self.jump_increment_x = None
        self.start_jump_y = None

    def setup(self):
        """Set up the game and initialize variables."""
        # Set the background color
        arcade.set_background_color(arcade.color.WHITE)

        self.background_texture = arcade.load_texture("static/background/city_winter.png")

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

        current_x = self.dog_sprite.center_x if self.dog_sprite else INITIAL_POSITION_X
        current_y = self.dog_sprite.center_y if self.dog_sprite else INITIAL_POSITION_Y

        # Create the dog sprite
        self.dog_sprite_list = arcade.SpriteList()
        self.dog_sprite = arcade.Sprite(scale=SPRITE_SCALING)
        self.dog_sprite.texture = self.sprite_data.textures[self.sprite_data.current_frame][
            0 if self.facing_right else 1]
        self.dog_sprite.center_x = current_x  # Retain the X position
        self.dog_sprite.center_y = current_y  # Retain the Y position

        self.dog_sprite_list.append(self.dog_sprite)
        self.is_walking = False

    def jump(self):
        current_textures = self.textures_by_state_name["jump"]
        total_frames = len(current_textures)

        self.sprite_data = SpriteData(0, total_frames, current_textures)

        # Retain the current position of the dog
        self.start_jump_x = self.dog_sprite.center_x if self.dog_sprite else INITIAL_POSITION_X
        self.start_jump_y = self.dog_sprite.center_y if self.dog_sprite else INITIAL_POSITION_Y

        # Calculate incremental movement per frame
        self.jump_increment_x = JUMP_MOVE_X / total_frames * (1 if self.facing_right else -1)

        # Initialize jump animation
        self.dog_sprite_list = arcade.SpriteList()
        self.dog_sprite = arcade.Sprite(scale=SPRITE_SCALING)
        self.dog_sprite.texture = self.sprite_data.textures[self.sprite_data.current_frame][
            0 if self.facing_right else 1]

        # Set the position to the current position, ensuring center_y is unchanged
        self.dog_sprite.center_x = self.start_jump_x
        self.dog_sprite.center_y = self.start_jump_y

        self.dog_sprite_list.append(self.dog_sprite)
        self.is_jumping = True
        self.jump_frames_remaining = total_frames

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
            # Update texture frame
            self.sprite_data.current_frame = (
                                                     self.sprite_data.current_frame + 1
                                             ) % self.sprite_data.length
            self.dog_sprite.texture = self.sprite_data.textures[self.sprite_data.current_frame][
                0 if self.facing_right else 1]

            # Smoothly move horizontally during the jump
            if self.is_jumping:
                self.dog_sprite.center_x += self.jump_increment_x

        # Handle jump state completion
        if self.is_jumping:
            self.jump_frames_remaining -= 1
            if self.jump_frames_remaining <= 0:
                self.is_jumping = False
                self.sit()

    def on_draw(self):
        arcade.start_render()

        # Draw the background image
        if self.background_texture:
            arcade.draw_lrwh_rectangle_textured(
                0, 0, SCREEN_WIDTH, SCREEN_HEIGHT, self.background_texture
            )

        self.dog_sprite_list.draw()

    def on_key_press(self, key, modifiers):
        if self.is_mac:
            if key == arcade.key.SPACE and not self.is_jumping:
                self.jump()
            elif key == arcade.key.LEFT:
                self.walk("left")
            elif key == arcade.key.RIGHT:
                self.walk("right")
        else:
            # Placeholder for Lego Build Hat controls
            inputs = mock_lego_build_hat_input()
            if inputs["jump"] and not self.is_jumping:
                self.jump()
            elif inputs["walk_left"]:
                self.walk("left")
            elif inputs["walk_right"]:
                self.walk("right")

    def on_key_release(self, key, modifiers):
        if self.is_mac:
            if key in (arcade.key.LEFT, arcade.key.RIGHT):
                self.dog_sprite.change_x = 0
                self.is_walking = False

                # Switch to the sit animation
                self.sit()
        else:
            # Placeholder for Lego Build Hat controls
            self.dog_sprite.change_x = 0
            self.is_walking = False
            self.sit()

def main():
    is_mac = '--mac' in sys.argv
    dog = DogSpriteDemo(is_mac)
    dog.setup()
    arcade.run()


if __name__ == "__main__":
    main()
