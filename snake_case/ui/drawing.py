"""User interface helper functions."""
from __future__ import annotations
import pygame
from ..core.constants import BLACK


def draw_text(screen: pygame.Surface, text: str, font: pygame.font.Font, color, x: int, y: int, center: bool = False) -> None:
    surface = font.render(text, True, color)
    rect = surface.get_rect()
    if center:
        rect.center = (x, y)
    else:
        rect.topleft = (x, y)
    screen.blit(surface, rect)


def draw_button(screen: pygame.Surface, rect: pygame.Rect, text: str, font: pygame.font.Font, base_color, hover_color):
    mouse_pos = pygame.mouse.get_pos()
    is_hovered = rect.collidepoint(mouse_pos)
    color = hover_color if is_hovered else base_color
    pygame.draw.rect(screen, color, rect)
    draw_text(screen, text, font, BLACK, rect.centerx, rect.centery, center=True)
    return is_hovered
