import pygame
import random
from constants import GRID_WIDTH, GRID_HEIGHT, GRID_SIZE, SNAKE_COLORS

class Snake:
    """Manages each snake's state, movement, and behavior."""
    def __init__(self, color, start_pos, start_dir):
        self.body = [start_pos]
        self.direction = start_dir
        self.color = color
        self.score = 1
        self.alive = True

    def move(self):
        """Moves the snake one step in its current direction."""
        head = self.body[0]
        new_head = (head[0] + self.direction[0], head[1] + self.direction[1])
        self.body.insert(0, new_head)
        self.body.pop()

    def grow(self):
        """Grows the snake by one segment."""
        tail = self.body[-1]
        self.body.append(tail)
        self.score += 1

    def check_collision(self, other_snakes):
        """Checks for collisions with walls, self, and other snakes."""
        head = self.body[0]
        # Wall collision
        if not (0 <= head[0] < GRID_WIDTH and 0 <= head[1] < GRID_HEIGHT):
            self.alive = False
            return
        # Self-collision
        if head in self.body[1:]:
            self.alive = False
            return
        # Other snake collision
        for other in other_snakes:
            if self == other:
                continue
            if head in other.body:
                self.alive = False
                return

    def find_best_direction(self, food, all_snakes):
        """AI to decide the snake's next move."""
        head = self.body[0]
        possible_moves = [(0, 1), (0, -1), (1, 0), (-1, 0)]
        
        # Avoid immediate death
        safe_moves = []
        for move in possible_moves:
            # Avoid moving back on itself
            if len(self.body) > 1 and move[0] == -self.direction[0] and move[1] == -self.direction[1]:
                continue

            next_pos = (head[0] + move[0], head[1] + move[1])
            
            # Check wall collision
            if not (0 <= next_pos[0] < GRID_WIDTH and 0 <= next_pos[1] < GRID_HEIGHT):
                continue
            
            # Check collision with any snake
            is_safe = True
            for snake in all_snakes:
                if next_pos in snake.body:
                    is_safe = False
                    break
            if is_safe:
                safe_moves.append(move)

        if not safe_moves:
            # No safe moves, just continue in the current direction
            return

        # Find nearest food
        if food:
            closest_food = min(food, key=lambda f: abs(f[0] - head[0]) + abs(f[1] - head[1]))
            
            # Prioritize moves towards food
            best_moves = []
            min_dist = float('inf')
            for move in safe_moves:
                next_pos = (head[0] + move[0], head[1] + move[1])
                dist = abs(next_pos[0] - closest_food[0]) + abs(next_pos[1] - closest_food[1])
                if dist < min_dist:
                    min_dist = dist
                    best_moves = [move]
                elif dist == min_dist:
                    best_moves.append(move)
            
            self.direction = random.choice(best_moves)
        else:
            # No food, move randomly
            self.direction = random.choice(safe_moves)

    def draw(self, screen):
        """Draws the snake on the screen."""
        for segment in self.body:
            pygame.draw.rect(screen, self.color, (segment[0] * GRID_SIZE, segment[1] * GRID_SIZE, GRID_SIZE, GRID_SIZE))
