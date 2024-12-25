import pygame
import sys
import math
import random

# Initialize Pygame
pygame.init()

# Set up display
WINDOW_WIDTH = 800
WINDOW_HEIGHT = 600
screen = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))
pygame.display.set_caption("3D Demo")

# Particle class to manage the moving pixel and its trail
class Particle:
    def __init__(self):
        # Randomize starting position
        self.x = random.randint(0, WINDOW_WIDTH)
        self.y = random.randint(0, WINDOW_HEIGHT)
        self.time = random.uniform(0, 100)  # Random starting time
        self.trail = []
        self.max_trail_length = random.randint(30, 70)  # Random trail length
        self.size = random.uniform(3, 7)  # Random size
        # Different frequency components for each particle
        self.freq1 = random.uniform(0.5, 1.5)
        self.freq2 = random.uniform(1.5, 2.5)
        self.freq3 = random.uniform(2.5, 3.5)
        # Random speed multiplier
        self.speed = random.uniform(0.01, 0.03)

    def update(self):
        self.time += self.speed
        
        # Create chaotic motion using multiple sine/cosine waves
        # with different frequencies and phases
        self.x += (math.sin(self.time * self.freq1) * 3 + 
                  math.cos(self.time * self.freq2) * 2 +
                  math.sin(self.time * self.freq3) * 1.5)
        
        self.y += (math.cos(self.time * self.freq1) * 2 +
                  math.sin(self.time * self.freq2) * 3 +
                  math.cos(self.time * self.freq3) * 1.5)
        
        # Wrap around screen edges instead of resetting
        self.x = self.x % WINDOW_WIDTH
        self.y = self.y % WINDOW_HEIGHT
        
        # Add current position to trail
        self.trail.append((self.x, self.y))
        if len(self.trail) > self.max_trail_length:
            self.trail.pop(0)

    def draw(self, surface):
        # Draw trail with fading effect
        for i, pos in enumerate(self.trail):
            alpha = int((i / len(self.trail)) * 255)
            # More yellow at the end of trail, more red at the particle
            yellow = int((i / len(self.trail)) * 255)
            color = (255, yellow, 0, alpha)
            
            size = self.size * (0.5 + i / len(self.trail))
            surf = pygame.Surface((size * 2, size * 2), pygame.SRCALPHA)
            pygame.draw.circle(surf, color, (size, size), size)
            surface.blit(surf, (pos[0] - size, pos[1] - size))
        
        # Draw current particle position
        pygame.draw.circle(surface, (255, 255, 255), (int(self.x), int(self.y)), self.size)

# Main game loop
def main():
    clock = pygame.time.Clock()
    particles = [Particle() for _ in range(100)]  # Create 100 particles
    
    while True:
        # Event handling
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            
        # Clear screen with slight fade effect for motion blur
        screen.fill((0, 0, 0, 5))  # Black background
        
        # Update and draw all particles
        for particle in particles:
            particle.update()
            particle.draw(screen)
        
        # Update display
        pygame.display.flip()
        
        # Cap the frame rate
        clock.tick(60)

if __name__ == "__main__":
    main()
