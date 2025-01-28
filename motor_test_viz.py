import pygame
import sys
from buildhat import Motor
import threading
import time

# Initialize Pygame
pygame.init()

# Set up the display
WINDOW_WIDTH = 800  # Made wider to show movement better
WINDOW_HEIGHT = 400  # Made taller to accommodate everything
screen = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))
pygame.display.set_caption("LEGO Motor Position Monitor")

# Colors
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
GRAY = (150, 150, 150)
RED = (255, 0, 0)

# Font setup
font = pygame.font.Font(None, 36)

class MotorMonitor:
    def __init__(self):
        self.current_position = 0
        self.previous_position = 0
        self.motor = Motor('A')
        self.running = True
        self.MIN_CHANGE_THRESHOLD = 15  # Minimum change in position to register
        
        # Add speed tracking
        self.current_speed = 0  # degrees per second
        self.last_update_time = time.time()
        
        # Object parameters
        self.object_width = 50
        self.object_height = 50
        self.base_x = WINDOW_WIDTH // 2 - self.object_width // 2
        self.current_x = self.base_x
        
        # Start motor monitoring
        self.monitor_thread = threading.Thread(target=self.monitor_motor)
        self.monitor_thread.start()
    
    def calculate_speed(self, new_position):
        current_time = time.time()
        time_diff = current_time - self.last_update_time
        if time_diff > 0:
            position_diff = new_position - self.current_position
            self.current_speed = position_diff / time_diff
        self.last_update_time = current_time
    
    def monitor_motor(self):
        while self.running:
            new_position = self.motor.get_position()
            # Only update if the change is significant enough
            if abs(new_position - self.current_position) >= self.MIN_CHANGE_THRESHOLD:
                self.previous_position = self.current_position
                self.calculate_speed(new_position)
                self.current_position = new_position
                
                # Calculate movement based on current position
                movement = (self.current_position / 100.0) * 300
                self.current_x = self.base_x + movement
                self.current_x = max(0, min(self.current_x, WINDOW_WIDTH - self.object_width))
            time.sleep(0.1)
    
    def draw_speed_gauge(self, screen):
        # Draw speed gauge background
        gauge_width = 200
        gauge_height = 20
        gauge_x = WINDOW_WIDTH - gauge_width - 20
        gauge_y = 50
        
        pygame.draw.rect(screen, GRAY, (gauge_x, gauge_y, gauge_width, gauge_height), 2)
        
        # Calculate speed percentage (assuming max speed of 360 degrees/second)
        MAX_SPEED = 360
        speed_ratio = min(abs(self.current_speed) / MAX_SPEED, 1.0)
        filled_width = int(gauge_width * speed_ratio)
        
        # Draw filled portion
        if filled_width > 0:
            color = RED if self.current_speed > 0 else (0, 0, 255)  # Red for clockwise, Blue for counter-clockwise
            pygame.draw.rect(screen, color, (gauge_x, gauge_y, filled_width, gauge_height))
    
    def run(self):
        clock = pygame.time.Clock()
        
        while True:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.running = False
                    self.monitor_thread.join()
                    pygame.quit()
                    sys.exit()
            
            screen.fill(BLACK)
            
            # Update direction text
            direction = "RIGHT" if self.current_position > 0 else "LEFT"
            direction_color = WHITE
            
            # Draw all the text and visuals
            current_text = font.render(f"Current Position: {self.current_position}°", True, WHITE)
            screen.blit(current_text, (20, 50))
            
            previous_text = font.render(f"Previous Position: {self.previous_position}°", True, GRAY)
            screen.blit(previous_text, (20, 100))
            
            speed_text = font.render(f"Speed: {self.current_speed:.1f}°/s", True, WHITE)
            screen.blit(speed_text, (20, 150))
            
            movement_text = font.render(f"Moving: {direction}", True, direction_color)
            screen.blit(movement_text, (20, 200))

            # Draw threshold indicator text
            threshold_text = font.render(f"Min Change Threshold: {self.MIN_CHANGE_THRESHOLD}°", True, GRAY)
            screen.blit(threshold_text, (20, 250))
            
            # Draw speed gauge
            self.draw_speed_gauge(screen)
            
            # Draw the movable object
            pygame.draw.rect(screen, RED, (self.current_x, WINDOW_HEIGHT - 100, 
                                         self.object_width, self.object_height))
            
            # Draw center line
            pygame.draw.line(screen, GRAY, (WINDOW_WIDTH//2, WINDOW_HEIGHT - 120),
                           (WINDOW_WIDTH//2, WINDOW_HEIGHT - 80), 2)
            
            pygame.display.flip()
            clock.tick(60)

if __name__ == "__main__":
    monitor = MotorMonitor()
    monitor.run()