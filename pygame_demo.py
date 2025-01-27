import os
import sys
import pygame
import time
from build_hat_controller import lego_build_hat_input

os.environ["DISPLAY"] = ":0"  # Only for RPI

# Constants
SCREEN_WIDTH = 1280
SCREEN_HEIGHT = 720
SPRITE_SCALING = 4
SPRITE_WIDTH = 64
SPRITE_HEIGHT = 64
SPAWN_POINTS = {
    "street": {"x": 0.10, "y": 0.55},    # 20% from left, 70% from top
    "bench": {"x": 0.5, "y": 0.65},      # middle of screen
    "park_entrance": {"x": 0.8, "y": 0.7} # 80% from left
}
JUMP_MOVE_X = 50
FPS = 60
FRAME_DELAY = 100  # milliseconds between frame changes

# State configurations
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

class SpriteSheet:
    def __init__(self, filename):
        self.sheet = pygame.image.load(filename).convert_alpha()
        self.first_col_width = 100

    def get_sprite(self, x, y, width, height, flip=False):
        sprite = pygame.Surface((width, height), pygame.SRCALPHA)
        sprite.blit(self.sheet, (0, 0), (x, y, width, height))
        if flip:
            sprite = pygame.transform.flip(sprite, True, False)
        return sprite

def load_textures_by_state(sprite_sheet, sprite_width, sprite_height):
    textures_by_state = {}
    row = 0
    for state, columns in states_columns.items():
        textures = []
        for col in range(1, columns):
            x = sprite_sheet.first_col_width + (col - 1) * sprite_width
            y = row * sprite_height
            texture = sprite_sheet.get_sprite(x, y, sprite_width, sprite_height)
            flipped_texture = sprite_sheet.get_sprite(x, y, sprite_width, sprite_height, flip=True)
            textures.append((texture, flipped_texture))
        row += 1
        textures_by_state[state] = textures
    return textures_by_state

class DogSprite(pygame.sprite.Sprite):
    def __init__(self, textures_by_state, initial_x, initial_y):
        super().__init__()
        self.textures_by_state = textures_by_state
        self.current_state = "sit"
        self.current_frame = 0
        self.facing_right = True
        self.is_jumping = False
        self.is_walking = False
        self.jump_frames_remaining = 0
        self.change_x = 0
        
        # Set initial image and position
        self.image = self.textures_by_state["sit"][0][0]
        self.image = pygame.transform.scale(self.image, 
                                         (int(SPRITE_WIDTH * SPRITE_SCALING), 
                                          int(SPRITE_HEIGHT * SPRITE_SCALING)))
        self.rect = self.image.get_rect()
        self.rect.x = initial_x
        self.rect.y = initial_y
        
        self.last_update = pygame.time.get_ticks()
        
    def sit(self):
        self.current_state = "sit"
        self.current_frame = 0
        self.is_walking = False
        self.change_x = 0
        
    def jump(self):
        if not self.is_jumping:
            self.current_state = "jump"
            self.current_frame = 0
            self.is_jumping = True
            total_frames = len(self.textures_by_state["jump"])
            self.jump_frames_remaining = total_frames
            # Calculate horizontal movement per frame during jump
            self.jump_x_per_frame = JUMP_MOVE_X / total_frames * (1 if self.facing_right else -1)
            
    def walk(self, direction):
        self.current_state = "walk"
        self.facing_right = direction == "right"
        self.change_x = 10 if self.facing_right else -10
        self.is_walking = True
        
    def update(self):
        now = pygame.time.get_ticks()
        if now - self.last_update > FRAME_DELAY:
            self.last_update = now
            
            # Update position - include jump movement if jumping
            if self.is_jumping:
                self.rect.x += self.jump_x_per_frame
            self.rect.x += self.change_x
            
            # Update animation frame
            textures = self.textures_by_state[self.current_state]
            self.current_frame = (self.current_frame + 1) % len(textures)
            
            # Update image based on direction
            texture = textures[self.current_frame][0 if self.facing_right else 1]
            self.image = pygame.transform.scale(texture,
                                             (int(SPRITE_WIDTH * SPRITE_SCALING),
                                              int(SPRITE_HEIGHT * SPRITE_SCALING)))
            
            # Handle jump completion
            if self.is_jumping:
                self.jump_frames_remaining -= 1
                if self.jump_frames_remaining <= 0:
                    self.is_jumping = False
                    self.sit()

class Game:
    def __init__(self, is_mac):
        pygame.init()
        self.screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
        pygame.display.set_caption("Dog Sprite Demo")
        self.clock = pygame.time.Clock()
        self.is_mac = is_mac
        
        # Load background
        self.background = pygame.image.load("static/background/city_winter.png").convert()
        self.background = pygame.transform.scale(self.background, (SCREEN_WIDTH, SCREEN_HEIGHT))

         # Calculate spawn position (using "street" as default spawn point)
        spawn_point = SPAWN_POINTS["street"]
        initial_x = int(SCREEN_WIDTH * spawn_point["x"])
        initial_y = int(SCREEN_HEIGHT * spawn_point["y"])
        
        # Load sprite sheet and create dog sprite
        sprite_sheet = SpriteSheet("static/welsh-corgi-sprites/corgi-asset.png")
        textures = load_textures_by_state(sprite_sheet, SPRITE_WIDTH, SPRITE_HEIGHT)
        
        # Create sprite group and add dog
        self.all_sprites = pygame.sprite.Group()
        self.dog = DogSprite(textures, initial_x, initial_y)
        self.all_sprites.add(self.dog)
        
    def handle_input(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return False
            if self.is_mac:
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_SPACE and not self.dog.is_jumping:
                        self.dog.jump()
                    elif event.key == pygame.K_LEFT:
                        self.dog.walk("left")
                    elif event.key == pygame.K_RIGHT:
                        self.dog.walk("right")
                elif event.type == pygame.KEYUP:
                    if event.key in (pygame.K_LEFT, pygame.K_RIGHT):
                        self.dog.sit()
        
        if not self.is_mac:
            direction = lego_build_hat_input()
            if direction["left"]:
                self.dog.walk("left")
            elif direction["right"]:
                self.dog.walk("right")
            elif self.dog.is_walking:
                self.dog.sit()
                
        return True
    
    def update(self):
        self.all_sprites.update()
        
    def draw(self):
        self.screen.blit(self.background, (0, 0))
        self.all_sprites.draw(self.screen)
        pygame.display.flip()
        
    def run(self):
        running = True
        while running:
            running = self.handle_input()
            self.update()
            self.draw()
            self.clock.tick(FPS)
            
def main():
    is_mac = '--mac' in sys.argv
    game = Game(is_mac)
    game.run()
    pygame.quit()

if __name__ == "__main__":
    main() 