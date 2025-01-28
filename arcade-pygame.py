import os
import sys
import pygame
import time
from build_hat_controller import lego_build_hat_input

# Constants
SCREEN_WIDTH = 1280
SCREEN_HEIGHT = 720
SCREEN_TITLE = "Dog Sprite Demo"
SPRITE_SCALING = 2.5
SPRITE_WIDTH = 64  # Update to match your sprite's width
SPRITE_HEIGHT = 64  # Update to match your sprite's height
ROWS = 8
INITIAL_POSITION_X = SCREEN_WIDTH // 4 - 150  # Initial X position
INITIAL_POSITION_Y = SCREEN_HEIGHT // 4 - 50  # Initial Y position
JUMP_MOVE_X = 50  # Horizontal movement during jump
FIRST_COL_WIDTH = 100
STATES_COLUMNS = {
    "jump": 11,
    "idle1": 5,
    "idle2": 5,
    "sit": 9,
    "walk": 5,
    "run": 8,
    "sniff": 8,
    "sniff_walk": 8,
}
FRAME_DELAY = 100  # Time in milliseconds between frame changes


def load_textures_by_state(sprite_sheet_path, sprite_width, sprite_height, rows):
    textures_by_state = {}

    # Validate that the number of states matches the number of rows
    if len(STATES_COLUMNS) != rows:
        raise ValueError("The number of states must match the number of rows in the sprite sheet.")

    # Load the sprite sheet
    sprite_sheet = pygame.image.load(sprite_sheet_path).convert_alpha()

    # Iterate through rows and columns, assign textures to states
    row = 0
    for state, columns in STATES_COLUMNS.items():
        textures = []
        for col in range(1, columns):  # Start from column 1 to skip the first column
            x = FIRST_COL_WIDTH + (col - 1) * sprite_width  # Account for wider first column
            y = row * sprite_height
            texture = sprite_sheet.subsurface(pygame.Rect(x, y, sprite_width, sprite_height))
            mirror_texture = pygame.transform.flip(texture, True, False)
            textures.append((texture, mirror_texture))
        row += 1
        textures_by_state[state] = textures

    return textures_by_state


class SpriteData:
    def __init__(self, initial_frame, length, textures):
        self.current_frame = initial_frame
        self.length = length
        self.textures = textures


class DogSpriteDemo:
    def __init__(self, is_mac):
        pygame.init()
        self.is_mac = is_mac
        self.screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
        pygame.display.set_caption(SCREEN_TITLE)
        self.clock = pygame.time.Clock()
        self.textures_by_state_name = None
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
        self.current_x = INITIAL_POSITION_X
        self.current_y = INITIAL_POSITION_Y

    def setup(self):
        # Load the background
        self.background_texture = pygame.image.load("static/background/city_winter.png").convert()

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

    def sit(self):
        current_textures = self.textures_by_state_name["sit"]
        self.sprite_data = SpriteData(0, len(current_textures), current_textures)
        self.is_walking = False

    def jump(self):
        current_textures = self.textures_by_state_name["jump"]
        total_frames = len(current_textures)

        self.sprite_data = SpriteData(0, total_frames, current_textures)

        # Retain the current position of the dog
        self.start_jump_x = self.current_x
        self.start_jump_y = self.current_y

        # Calculate incremental movement per frame
        self.jump_increment_x = JUMP_MOVE_X / total_frames * (1 if self.facing_right else -1)

        self.is_jumping = True
        self.jump_frames_remaining = total_frames

    def walk(self, direction):
        current_textures = self.textures_by_state_name["walk"]
        self.sprite_data = SpriteData(0, len(current_textures), current_textures)

        self.facing_right = direction == "right"
        self.is_walking = True

    def update(self):
        # Smoothly move horizontally during the jump
        if self.is_jumping:
            self.current_x += self.jump_increment_x

        # Handle jump state completion
        if self.is_jumping:
            self.jump_frames_remaining -= 1
            if self.jump_frames_remaining <= 0:
                self.is_jumping = False
                self.sit()

        # Handle walking
        if self.is_walking:
            self.current_x += 2 if self.facing_right else -2

    def update_texture(self):
        if self.sprite_data:
            # Update texture frame
            self.sprite_data.current_frame = (
                self.sprite_data.current_frame + 1
            ) % self.sprite_data.length

    def draw(self):
        # Draw the background
        self.screen.blit(self.background_texture, (0, 0))

        # Draw the dog sprite
        if self.sprite_data:
            texture = self.sprite_data.textures[self.sprite_data.current_frame][
                0 if self.facing_right else 1
            ]
            self.screen.blit(texture, (self.current_x, self.current_y))

    def run(self):
        running = True
        while running:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False

                if self.is_mac:
                    if event.type == pygame.KEYDOWN:
                        if event.key == pygame.K_SPACE and not self.is_jumping:
                            self.jump()
                        elif event.key == pygame.K_LEFT:
                            self.walk("left")
                        elif event.key == pygame.K_RIGHT:
                            self.walk("right")

                    elif event.type == pygame.KEYUP:
                        if event.key in (pygame.K_LEFT, pygame.K_RIGHT):
                            self.is_walking = False
                            self.sit()

            if not self.is_mac:  # Handle Lego Build HAT controls
                direction = lego_build_hat_input()  # Get the direction from the motor
                if direction == "left":
                    self.walk("left")
                elif direction == "right":
                    self.walk("right")
                else:
                    self.is_walking = False
                    self.sit()

            self.update()
            self.update_texture()
            self.draw()
            pygame.display.flip()
            self.clock.tick(60)

        pygame.quit()


def main():
    is_mac = '--mac' in sys.argv
    game = DogSpriteDemo(is_mac)
    game.setup()
    game.run()


if __name__ == "__main__":
    main()
