import pygame
import random

class Application:
    def __init__(self):
        pygame.init()
        self.screen = pygame.display.set_mode((400, 600))
        self.clock = pygame.time.Clock()
        self.bird_y = 250
        self.bird_velocity = 0
        self.gravity = 0.5
        self.game_over = False
        self.score = 0
        self.pipes = []
        self.frame_counter = 0
        self.punishment_duration = 3  # Punishment delay in seconds
        self.punishment_start_time = 0
        
        # Font for displaying scores
        self.font = pygame.font.Font(None, 36)
        self.add_pipe()

    def run(self):
        while True:
            self.handle_input()
            if not self.game_over:
                self.update()
            self.render()
            self.clock.tick(60)

    def handle_input(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                exit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE and not self.game_over:
                    self.bird_velocity = -10
                if self.game_over and (pygame.time.get_ticks() - self.punishment_start_time) // 1000 >= self.punishment_duration:
                    self.reset_game()

    def update(self):
        self.bird_velocity += self.gravity
        self.bird_y += self.bird_velocity
        
        if self.bird_y >= 600:
            self.game_over = True
            self.apply_punishment()
        
        if self.bird_y < 0:
            self.bird_y = 0
        
        self.frame_counter += 1
        if self.frame_counter % 100 == 0:  # Add a new pipe every 100 frames
            self.add_pipe()
        
        for pipe in self.pipes:
            pipe['x'] -= 5  # Move pipes to the left
            if pipe['x'] < -50:  # Remove off-screen pipes
                self.pipes.remove(pipe)
                self.score += 1  # Increase score when a pipe is passed

        if self.check_collisions():
            self.game_over = True
            self.apply_punishment()

    def render(self):
        self.screen.fill((135, 206, 235))  # Sky color
        pygame.draw.rect(self.screen, (255, 215, 0), (50, self.bird_y, 30, 30))  # Bird
        
        for pipe in self.pipes:
            pygame.draw.rect(self.screen, (0, 255, 0), (pipe['x'], 0, 50, pipe['height']))  # Top pipe
            pygame.draw.rect(self.screen, (0, 255, 0), (pipe['x'], pipe['height'] + 150, 50, 600 - pipe['height'] - 150))  # Bottom pipe
            
        score_surface = self.font.render(f'Score: {self.score}', True, (255, 255, 255))
        self.screen.blit(score_surface, (10, 10))
        
        if self.game_over:
            game_over_surface = self.font.render('Game Over! Press SPACE to restart', True, (255, 0, 0))
            self.screen.blit(game_over_surface, (50, 300))
        
        pygame.display.flip()

    def check_collisions(self):
        bird_rect = pygame.Rect(50, self.bird_y, 30, 30)
        for pipe in self.pipes:
            top_pipe_rect = pygame.Rect(pipe['x'], 0, 50, pipe['height'])
            bottom_pipe_rect = pygame.Rect(pipe['x'], pipe['height'] + 150, 50, 600 - pipe['height'] - 150)
            if bird_rect.colliderect(top_pipe_rect) or bird_rect.colliderect(bottom_pipe_rect):
                return True
        return False

    def apply_punishment(self):
        self.punishment_start_time = pygame.time.get_ticks()

    def reset_game(self):
        self.bird_y = 250
        self.bird_velocity = 0
        self.game_over = False
        self.score = 0
        self.pipes.clear()
        self.add_pipe()  # Restart with one pipe

    def add_pipe(self):
        height = random.randint(100, 400)
        self.pipes.append({'x': 400, 'height': height})

if __name__ == "__main__":
    app = Application()
    app.run()