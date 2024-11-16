import pygame
import random

# Initialize Pygame
pygame.init()

# Screen dimensions
WIDTH = 1000
HEIGHT = 800

# Colors
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
GREEN = (0, 255, 0)

# Game variables
GRAVITY = 0.5
FLAP_STRENGTH = -10
PIPE_GAP = 150
PIPE_WIDTH = 80
PIPE_SPEED = 5
BIRD_WIDTH = 40
BIRD_HEIGHT = 30

# Set up display
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Flappy Bird Clone")
clock = pygame.time.Clock()

# Load bird image (substitute with any 40x30 image or color fill)
bird_image = pygame.Surface((BIRD_WIDTH, BIRD_HEIGHT))
bird_image.fill(GREEN)

# Bird class
class Bird:
    def __init__(self):
        self.x = WIDTH // 3
        self.y = HEIGHT // 2
        self.vel_y = 0

    def flap(self):
        self.vel_y = FLAP_STRENGTH

    def update(self):
        self.vel_y += GRAVITY
        self.y += self.vel_y

    def draw(self):
        screen.blit(bird_image, (self.x, self.y))

# Pipe class
class Pipe:
    def __init__(self):
        self.x = WIDTH
        self.height = random.randint(100, 400)
        self.top_rect = pygame.Rect(self.x, 0, PIPE_WIDTH, self.height)
        self.bottom_rect = pygame.Rect(self.x, self.height + PIPE_GAP, PIPE_WIDTH, HEIGHT)

    def update(self):
        self.x -= PIPE_SPEED
        self.top_rect.x = self.x
        self.bottom_rect.x = self.x

    def draw(self):
        pygame.draw.rect(screen, GREEN, self.top_rect)
        pygame.draw.rect(screen, GREEN, self.bottom_rect)

    def off_screen(self):
        return self.x < -PIPE_WIDTH

    def collide(self, bird):
        bird_rect = pygame.Rect(bird.x, bird.y, BIRD_WIDTH, BIRD_HEIGHT)
        return bird_rect.colliderect(self.top_rect) or bird_rect.colliderect(self.bottom_rect)

# Main game loop
def main():
    bird = Bird()
    pipes = [Pipe()]
    score = 0

    running = True
    while running:
        clock.tick(30)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                    bird.flap()

        bird.update()

        # Add new pipe if the last pipe has moved a certain distance
        if pipes[-1].x < WIDTH // 2:
            pipes.append(Pipe())

        # Remove pipes that are off-screen
        if pipes[0].off_screen():
            pipes.pop(0)
            score += 1

        # Check for collisions
        if bird.y < 0 or bird.y > HEIGHT or any(pipe.collide(bird) for pipe in pipes):
            running = False  # End the game if collision occurs

        # Draw everything
        screen.fill(WHITE)
        bird.draw()
        for pipe in pipes:
            pipe.update()
            pipe.draw()

        # Display the score
        font = pygame.font.SysFont(None, 50)
        score_text = font.render(f"Score: {score}", True, BLACK)
        screen.blit(score_text, (WIDTH // 2 - score_text.get_width() // 2, 50))

        pygame.display.flip()

    pygame.quit()

if __name__ == "__main__":
    main()
