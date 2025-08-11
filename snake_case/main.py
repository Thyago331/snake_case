import pygame
from .core.constants import SCREEN_WIDTH, SCREEN_HEIGHT
from .core.game import Game

def main() -> None:
    pygame.init()
    screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
    pygame.display.set_caption("snake_case")
    game = Game(screen)
    game.run()

if __name__ == "__main__":
    main()
