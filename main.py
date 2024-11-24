import sys
import pygame

# Initialization
pygame.init()

# Constants
SCREEN_WIDTH = 400
SCREEN_HEIGHT = 300
CIRCLE_RADIUS = 20
CIRCLE_COLOR = (255, 255, 0)  # Yellow
BACKGROUND_COLOR = (0, 0, 255)  # Blue
FPS = 60

# Circle starting position
circle_x = SCREEN_WIDTH // 2
circle_y = SCREEN_HEIGHT // 2

# Movement step size
STEP_SIZE = 5

# Parse arguments
use_keyboard = len(sys.argv) > 1 and sys.argv[1] == "mac"

# Mock LEGO Build HAT API for macOS testing
class LegoBuildHatMock:
    def read(self):
        return None  # Replace with mock data like "left" or "right" if testing this part.

from abc import ABC, abstractmethod

# Abstract base class for input handling
class InputHandler(ABC):
    @abstractmethod
    def get_action(self):
        """Return 'left', 'right', or None based on input"""
        pass

# Keyboard input handler (macOS)
class KeyboardInputHandler(InputHandler):
    def get_action(self):
        keys = pygame.key.get_pressed()
        if keys[pygame.K_LEFT]:
            return "left"
        if keys[pygame.K_RIGHT]:
            return "right"
        return None

# LEGO Build HAT input handler (Raspberry Pi)
class LegoHatInputHandler(InputHandler):
    def __init__(self, lego_hat):
        self.lego_hat = lego_hat

    def get_action(self):
        # Replace with real LEGO Build HAT input reading logic
        return self.lego_hat.read()

# Factory to choose the correct input handler
def create_input_handler(use_keyboard):
    if use_keyboard:
        return KeyboardInputHandler()
    else:
        return LegoHatInputHandler(lego_hat)


lego_hat = LegoBuildHatMock() if use_keyboard else None

# Initialize screen
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("Circle Game")

# Clock for controlling frame rate
clock = pygame.time.Clock()

# Game loop

input_handler = create_input_handler(use_keyboard)

running = True
while running:
    screen.fill(BACKGROUND_COLOR)

    # Handle events
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    # Get action from input handler
    action = input_handler.get_action()
    if action == "left" and circle_x - CIRCLE_RADIUS > 0:
        circle_x -= STEP_SIZE
    elif action == "right" and circle_x + CIRCLE_RADIUS < SCREEN_WIDTH:
        circle_x += STEP_SIZE

    # Draw the circle
    pygame.draw.circle(screen, CIRCLE_COLOR, (circle_x, circle_y), CIRCLE_RADIUS)

    # Update the display
    pygame.display.flip()

    # Cap the frame rate
    clock.tick(FPS)

# Quit the game
pygame.quit()
