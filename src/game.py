import pygame
import random
import os
import asyncio
import sys
from constants import SCREEN_WIDTH, SCREEN_HEIGHT, GRID_WIDTH, GRID_HEIGHT, GRID_SIZE, FPS, BLACK, WHITE, RED, GRAY, LIGHT_GRAY, SNAKE_COLORS, MENU, PLAYING, GAME_OVER
from snake import Snake

class Game:
    """Manages the overall game state and logic."""
    def __init__(self, screen):
        self.screen = screen
        self.clock = pygame.time.Clock()
        self.font_large = pygame.font.SysFont("arial", 48)
        self.font_medium = pygame.font.SysFont("arial", 24)
        self.font_small = pygame.font.SysFont("arial", 18)
        self.state = MENU
        self.currency = 0
        self.score = 0
        self.high_score = 0
        self.snakes = []
        self.food = []
        self.snake_cost = 10
        self.max_snakes = 10
        self.speed_boost = False
        self.snakes_used = 0
        self.should_quit = False

        # Load high score
        # When bundled with PyInstaller, sys.executable points to the .exe
        # We want highscore.txt to be in the same directory as the .exe
        if getattr(sys, 'frozen', False): # Check if running as a bundled executable
            self.highscore_file = os.path.join(os.path.dirname(sys.executable), "highscore.txt")
        else:
            # For development, use the original path
            self.highscore_file = os.path.join(os.path.dirname(os.path.dirname(__file__)), "highscore.txt")
        try:
            with open(self.highscore_file, "r") as f:
                self.high_score = int(f.read())
        except (FileNotFoundError, ValueError):
            self.high_score = 0

        # Sound
        try:
            pygame.mixer.init()
            print(f"Mixer initialized: {pygame.mixer.get_init()}")
            
            music_path = os.path.join(getattr(sys, '_MEIPASS', os.path.abspath(".")), "assets", "pac-man.mp3")
            munch_path = os.path.join(getattr(sys, '_MEIPASS', os.path.abspath(".")), "assets", "munch-sound-effect.mp3")
            death_path = os.path.join(getattr(sys, '_MEIPASS', os.path.abspath(".")), "assets", "lego-yoda-death-sound-effect.mp3")

            print(f"Attempting to load music from: {music_path}")
            pygame.mixer.music.load(music_path)
            pygame.mixer.music.set_volume(0.1)
            pygame.mixer.music.play(-1)
            
            print(f"Attempting to load munch sound from: {munch_path}")
            self.munch_sound = pygame.mixer.Sound(munch_path)
            self.munch_sound.set_volume(0.3)
            
            print(f"Attempting to load death sound from: {death_path}")
            self.death_sound = pygame.mixer.Sound(death_path)
            self.death_sound.set_volume(0.5)
            self.sounds_loaded = True
        except pygame.error as e:
            self.sounds_loaded = False
            print(f"Warning: Could not load sound files. Error: {e}")

    def reset_game(self):
        """Resets the game to its initial state."""
        self.currency = 0
        self.score = 0
        self.snakes = []
        self.food = []
        self.snakes_used = 0
        self.snake_cost = 10
        self.speed_boost = False
        self.add_snake()
        self.spawn_food()
        self.state = PLAYING

    def get_random_empty_pos(self):
        """Gets a random empty position on the grid."""
        all_occupied_pos = set()
        for snake in self.snakes:
            for segment in snake.body:
                all_occupied_pos.add(segment)
        for f in self.food:
            all_occupied_pos.add(f)

        while True:
            pos = (random.randint(0, GRID_WIDTH - 1), random.randint(0, GRID_HEIGHT - 1))
            if pos not in all_occupied_pos:
                return pos

    def add_snake(self):
        """Adds a new snake to the game."""
        if len(self.snakes) < self.max_snakes:
            start_pos = self.get_random_empty_pos()
            available_colors = [c for c in SNAKE_COLORS if c not in [s.color for s in self.snakes]]
            if not available_colors:
                available_colors = SNAKE_COLORS # Reuse colors if all are taken
            color = random.choice(available_colors)
            direction = random.choice([(0, 1), (0, -1), (1, 0), (-1, 0)])
            self.snakes.append(Snake(color, start_pos, direction))
            self.snakes_used += 1

    def spawn_food(self):
        """Spawns food on the grid."""
        while len(self.food) < 1 + len(self.snakes) // 2 and len(self.food) < 5:
            pos = self.get_random_empty_pos()
            self.food.append(pos)

    def draw_text(self, text, font, color, x, y, center=False):
        """Helper function to draw text on the screen."""
        text_surface = font.render(text, True, color)
        text_rect = text_surface.get_rect()
        if center:
            text_rect.center = (x, y)
        else:
            text_rect.topleft = (x, y)
        self.screen.blit(text_surface, text_rect)

    def draw_button(self, rect, text, base_color, hover_color):
        """Draws a clickable button."""
        mouse_pos = pygame.mouse.get_pos()
        is_hovered = rect.collidepoint(mouse_pos)
        color = hover_color if is_hovered else base_color
        
        pygame.draw.rect(self.screen, color, rect)
        self.draw_text(text, self.font_medium, BLACK, rect.centerx, rect.centery, center=True)
        
        return is_hovered

    def run_menu(self, events):
        """Runs the main menu state."""
        self.screen.fill(BLACK)
        self.draw_text("snake_case", self.font_large, WHITE, SCREEN_WIDTH // 2, SCREEN_HEIGHT // 4, center=True)

        start_button = pygame.Rect(SCREEN_WIDTH // 2 - 100, SCREEN_HEIGHT // 2, 200, 50)
        quit_button = pygame.Rect(SCREEN_WIDTH // 2 - 100, SCREEN_HEIGHT // 2 + 70, 200, 50)

        start_hovered = self.draw_button(start_button, "Start Game", GRAY, LIGHT_GRAY)
        quit_hovered = self.draw_button(quit_button, "Quit", GRAY, LIGHT_GRAY)

        for event in events:
            if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                if start_hovered:
                    self.reset_game()
                if quit_hovered:
                    self.should_quit = True
        # No return value, main loop handles 'running'

    def run_playing(self, events):
        """Runs the main gameplay state."""
        # Event handling
        for event in events:
            if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                buy_snake_rect = pygame.Rect(SCREEN_WIDTH - 220, 10, 200, 40)
                speed_boost_rect = pygame.Rect(SCREEN_WIDTH - 220, 60, 200, 40)
                if self.currency >= self.snake_cost and len(self.snakes) < self.max_snakes and buy_snake_rect.collidepoint(event.pos):
                    self.currency -= self.snake_cost
                    self.add_snake()
                    self.snake_cost = int(self.snake_cost * 1.5)
                if speed_boost_rect.collidepoint(event.pos):
                    self.speed_boost = not self.speed_boost

        # Update snakes
        all_snake_bodies = []
        for s in self.snakes:
            all_snake_bodies.extend(s.body)

        for snake in self.snakes:
            snake.find_best_direction(self.food, self.snakes)
            snake.move()
            snake.check_collision(self.snakes)

        # Check for eating food
        for snake in self.snakes:
            if snake.alive and snake.body[0] in self.food:
                self.food.remove(snake.body[0])
                snake.grow()
                self.currency += 1
                self.score += 1
                if self.sounds_loaded:
                    self.munch_sound.play()
                self.spawn_food()

        # Handle dead snakes
        dead_snakes = [s for s in self.snakes if not s.alive]
        for snake in dead_snakes:
            if self.sounds_loaded:
                self.death_sound.play()
            self.snakes.remove(snake)
        
        # Check for game over condition
        if not self.snakes and self.currency < self.snake_cost:
            if self.score > self.high_score:
                self.high_score = self.score
                try:
                    with open(self.highscore_file, "w") as f:
                        f.write(str(self.high_score))
                except IOError:
                    print("Warning: Could not save high score.")
            self.state = GAME_OVER

        # Drawing
        self.screen.fill(BLACK)
        for snake in self.snakes:
            snake.draw(self.screen)
        for f in self.food:
            pygame.draw.rect(self.screen, WHITE, (f[0] * GRID_SIZE, f[1] * GRID_SIZE, GRID_SIZE, GRID_SIZE))

        # UI
        self.draw_text(f"Currency: {self.currency}", self.font_medium, WHITE, 10, 10)
        self.draw_text(f"Snakes: {len(self.snakes)}/{self.max_snakes}", self.font_medium, WHITE, 10, 40)
        self.draw_text(f"Score: {self.score}", self.font_medium, WHITE, 10, 70)
        
        buy_snake_rect = pygame.Rect(SCREEN_WIDTH - 220, 10, 200, 40)
        can_afford = self.currency >= self.snake_cost and len(self.snakes) < self.max_snakes
        button_color = GRAY if can_afford else (50, 50, 50)
        hover_color = LIGHT_GRAY if can_afford else (50, 50, 50)
        self.draw_button(buy_snake_rect, f"Buy Snake ({self.snake_cost})", button_color, hover_color)

        speed_boost_rect = pygame.Rect(SCREEN_WIDTH - 220, 60, 200, 40)
        boost_text = "Speed: 10x" if self.speed_boost else "Speed: 1x"
        self.draw_button(speed_boost_rect, boost_text, GRAY, LIGHT_GRAY)

        # No return value, main loop handles 'running'

    def run_game_over(self, events):
        """Runs the game over state."""
        self.screen.fill(BLACK)
        self.draw_text("Game Over", self.font_large, RED, SCREEN_WIDTH // 2, SCREEN_HEIGHT // 4, center=True)
        self.draw_text(f"Score: {self.score}", self.font_medium, WHITE, SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2 - 30, center=True)
        self.draw_text(f"High Score: {self.high_score}", self.font_medium, WHITE, SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2, center=True)
        self.draw_text(f"Snakes Used: {self.snakes_used}", self.font_medium, WHITE, SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2 + 30, center=True)

        restart_button = pygame.Rect(SCREEN_WIDTH // 2 - 100, SCREEN_HEIGHT // 2 + 80, 200, 50)
        menu_button = pygame.Rect(SCREEN_WIDTH // 2 - 100, SCREEN_HEIGHT // 2 + 150, 200, 50)

        restart_hovered = self.draw_button(restart_button, "Restart", GRAY, LIGHT_GRAY)
        menu_hovered = self.draw_button(menu_button, "Back to Menu", GRAY, LIGHT_GRAY)

        for event in events:
            if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                if restart_hovered:
                    self.reset_game()
                if menu_hovered:
                    self.state = MENU
        # No return value, main loop handles 'running'

    async def run(self):
        """The main game loop, compatible with asyncio for Pyodide."""
        running = True
        while running and not self.should_quit:
            events = pygame.event.get()
            for event in events:
                if event.type == pygame.QUIT:
                    running = False

            if self.state == MENU:
                self.run_menu(events)
            elif self.state == PLAYING:
                self.run_playing(events)
            elif self.state == GAME_OVER:
                self.run_game_over(events)

            pygame.display.flip()
            current_fps = 100 if self.speed_boost else FPS
            self.clock.tick(current_fps)
            await asyncio.sleep(0) # Yield control to the browser event loop

        pygame.quit()
