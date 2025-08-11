import pygame
import random
from .constants import (
    SCREEN_WIDTH,
    SCREEN_HEIGHT,
    GRID_WIDTH,
    GRID_HEIGHT,
    GRID_SIZE,
    FPS,
    BLACK,
    WHITE,
    RED,
    GRAY,
    LIGHT_GRAY,
    SNAKE_COLORS,
    MENU,
    PLAYING,
    GAME_OVER,
)
from .snake import Snake
from ..audio.sound import SoundManager
from ..ui.drawing import draw_text, draw_button
from ..persistence import highscore
from .. import steam_integration


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
        self.high_score = highscore.load_highscore()
        self.snakes = []
        self.food = []
        self.snake_cost = 10
        self.max_snakes = 10
        self.speed_boost = False
        self.snakes_used = 0
        self.should_quit = False

        self.sounds = SoundManager()
        self.sounds.play_music()
        steam_integration.init()

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
        """Gets a random empty position on the grid or ``None`` if full."""
        all_positions = {
            (x, y)
            for x in range(GRID_WIDTH)
            for y in range(GRID_HEIGHT)
        }

        occupied = set()
        for snake in self.snakes:
            occupied.update(snake.body)
        occupied.update(self.food)

        empty_positions = list(all_positions - occupied)
        if not empty_positions:
            return None
        return random.choice(empty_positions)

    def add_snake(self):
        """Adds a new snake to the game."""
        if len(self.snakes) < self.max_snakes:
            start_pos = self.get_random_empty_pos()
            if start_pos is None:
                return
            available_colors = [
                c for c in SNAKE_COLORS if c not in [s.color for s in self.snakes]
            ]
            if not available_colors:
                available_colors = SNAKE_COLORS
            color = random.choice(available_colors)
            direction = random.choice([(0, 1), (0, -1), (1, 0), (-1, 0)])
            self.snakes.append(Snake(color, start_pos, direction))
            self.snakes_used += 1

    def spawn_food(self):
        """Spawns food on the grid."""
        while len(self.food) < 1 + len(self.snakes) // 2 and len(self.food) < 5:
            pos = self.get_random_empty_pos()
            if pos is None:
                break
            self.food.append(pos)

    def run_menu(self, events):
        """Runs the main menu state."""
        self.screen.fill(BLACK)
        draw_text(
            self.screen,
            "snake_case",
            self.font_large,
            WHITE,
            SCREEN_WIDTH // 2,
            SCREEN_HEIGHT // 4,
            center=True,
        )

        start_button = pygame.Rect(
            SCREEN_WIDTH // 2 - 100, SCREEN_HEIGHT // 2, 200, 50
        )
        quit_button = pygame.Rect(
            SCREEN_WIDTH // 2 - 100, SCREEN_HEIGHT // 2 + 70, 200, 50
        )

        start_hovered = draw_button(
            self.screen, start_button, "Start Game", self.font_medium, GRAY, LIGHT_GRAY
        )
        quit_hovered = draw_button(
            self.screen, quit_button, "Quit", self.font_medium, GRAY, LIGHT_GRAY
        )

        for event in events:
            if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                if start_hovered:
                    self.reset_game()
                if quit_hovered:
                    self.should_quit = True

    def run_playing(self, events):
        """Runs the main gameplay state."""
        for event in events:
            if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                buy_snake_rect = pygame.Rect(SCREEN_WIDTH - 220, 10, 200, 40)
                speed_boost_rect = pygame.Rect(SCREEN_WIDTH - 220, 60, 200, 40)
                if (
                    self.currency >= self.snake_cost
                    and len(self.snakes) < self.max_snakes
                    and buy_snake_rect.collidepoint(event.pos)
                ):
                    self.currency -= self.snake_cost
                    self.add_snake()
                    self.snake_cost = int(self.snake_cost * 1.5)
                if speed_boost_rect.collidepoint(event.pos):
                    self.speed_boost = not self.speed_boost

        for snake in self.snakes:
            snake.find_best_direction(self.food, self.snakes)
            snake.move()
            snake.check_collision(self.snakes)

        for snake in self.snakes:
            if snake.alive and snake.body[0] in self.food:
                self.food.remove(snake.body[0])
                snake.grow()
                self.currency += 1
                self.score += 1
                self.sounds.play_munch()
                self.spawn_food()

        dead_snakes = [s for s in self.snakes if not s.alive]
        for snake in dead_snakes:
            self.sounds.play_death()
            self.snakes.remove(snake)

        if not self.snakes and self.currency < self.snake_cost:
            if self.score > self.high_score:
                self.high_score = self.score
                highscore.save_highscore(self.high_score)
                steam_integration.record_highscore(self.high_score)
            self.state = GAME_OVER

        self.screen.fill(BLACK)
        for snake in self.snakes:
            snake.draw(self.screen)
        for f in self.food:
            pygame.draw.rect(
                self.screen,
                WHITE,
                (f[0] * GRID_SIZE, f[1] * GRID_SIZE, GRID_SIZE, GRID_SIZE),
            )

        draw_text(
            self.screen,
            f"Currency: {self.currency}",
            self.font_medium,
            WHITE,
            10,
            10,
        )
        draw_text(
            self.screen,
            f"Snakes: {len(self.snakes)}/{self.max_snakes}",
            self.font_medium,
            WHITE,
            10,
            40,
        )
        draw_text(
            self.screen,
            f"Score: {self.score}",
            self.font_medium,
            WHITE,
            10,
            70,
        )

        buy_snake_rect = pygame.Rect(SCREEN_WIDTH - 220, 10, 200, 40)
        can_afford = self.currency >= self.snake_cost and len(self.snakes) < self.max_snakes
        button_color = GRAY if can_afford else (50, 50, 50)
        hover_color = LIGHT_GRAY if can_afford else (50, 50, 50)
        draw_button(
            self.screen,
            buy_snake_rect,
            f"Buy Snake ({self.snake_cost})",
            self.font_medium,
            button_color,
            hover_color,
        )

        speed_boost_rect = pygame.Rect(SCREEN_WIDTH - 220, 60, 200, 40)
        boost_text = "Speed: 10x" if self.speed_boost else "Speed: 1x"
        draw_button(
            self.screen,
            speed_boost_rect,
            boost_text,
            self.font_medium,
            GRAY,
            LIGHT_GRAY,
        )

    def run_game_over(self, events):
        """Runs the game over state."""
        self.screen.fill(BLACK)
        draw_text(
            self.screen,
            "Game Over",
            self.font_large,
            RED,
            SCREEN_WIDTH // 2,
            SCREEN_HEIGHT // 4,
            center=True,
        )
        draw_text(
            self.screen,
            f"Score: {self.score}",
            self.font_medium,
            WHITE,
            SCREEN_WIDTH // 2,
            SCREEN_HEIGHT // 2 - 30,
            center=True,
        )
        draw_text(
            self.screen,
            f"High Score: {self.high_score}",
            self.font_medium,
            WHITE,
            SCREEN_WIDTH // 2,
            SCREEN_HEIGHT // 2,
            center=True,
        )
        draw_text(
            self.screen,
            f"Snakes Used: {self.snakes_used}",
            self.font_medium,
            WHITE,
            SCREEN_WIDTH // 2,
            SCREEN_HEIGHT // 2 + 30,
            center=True,
        )

        restart_button = pygame.Rect(
            SCREEN_WIDTH // 2 - 100, SCREEN_HEIGHT // 2 + 80, 200, 50
        )
        menu_button = pygame.Rect(
            SCREEN_WIDTH // 2 - 100, SCREEN_HEIGHT // 2 + 150, 200, 50
        )

        restart_hovered = draw_button(
            self.screen, restart_button, "Restart", self.font_medium, GRAY, LIGHT_GRAY
        )
        menu_hovered = draw_button(
            self.screen, menu_button, "Back to Menu", self.font_medium, GRAY, LIGHT_GRAY
        )

        for event in events:
            if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                if restart_hovered:
                    self.reset_game()
                if menu_hovered:
                    self.state = MENU

    def run(self):
        """The main game loop."""
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

        pygame.quit()
