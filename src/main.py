import pygame
import asyncio
from constants import SCREEN_WIDTH, SCREEN_HEIGHT, FPS
from game import Game

async def main():
    pygame.init()
    screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
    pygame.display.set_caption("snake_case")
    game = Game(screen)
    await game.run()

if __name__ == "__main__":
    asyncio.run(main())
