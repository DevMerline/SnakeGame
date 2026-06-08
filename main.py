import pygame
import random
import math

# Initialisation
pygame.init()
pygame.mixer.init()

# Configuration
WINDOW_X, WINDOW_Y = 800, 600
CELL_SIZE = 20
GRID_WIDTH = WINDOW_X // CELL_SIZE
GRID_HEIGHT = WINDOW_Y // CELL_SIZE
FPS = 12

# Palette de couleurs
COLORS = {
    'bg_dark': (15, 15, 35),
    'bg_grid': (25, 25, 50),
    'snake_head': (0, 230, 118),
    'snake_body': (0, 200, 100),
    'snake_tail': (0, 170, 80),
    'snake_outline': (0, 100, 50),
    'fruit': (255, 82, 82),
    'fruit_glow': (255, 120, 120),
    'text': (255, 255, 255),
    'text_shadow': (0, 0, 0),
    'score_bg': (40, 40, 80),
    'game_over_bg': (20, 20, 40, 200),
}

# Fenêtre
screen = pygame.display.set_mode((WINDOW_X, WINDOW_Y))
pygame.display.set_caption('🐍 Snake Modern')
clock = pygame.time.Clock()

# Polices
font_score = pygame.font.Font(None, 36)
font_title = pygame.font.Font(None, 72)
font_subtitle = pygame.font.Font(None, 36)


class Particle:
    """Particule pour les effets visuels."""
    def __init__(self, x, y, color):
        self.x = x
        self.y = y
        self.color = color
        self.vx = random.uniform(-3, 3)
        self.vy = random.uniform(-3, 3)
        self.life = 1.0
        self.decay = random.uniform(0.02, 0.05)

    def update(self):
        self.x += self.vx
        self.y += self.vy
        self.life -= self.decay
        return self.life > 0

    def draw(self, surface):
        alpha = int(255 * self.life)
        size = int(6 * self.life)
        if size > 0:
            color = (*self.color[:3], alpha)
            s = pygame.Surface((size * 2, size * 2), pygame.SRCALPHA)
            pygame.draw.circle(s, color, (size, size), size)
            surface.blit(s, (self.x - size, self.y - size))


class Snake:
    def __init__(self):
        self.reset()

    def reset(self):
        start_x = GRID_WIDTH // 2
        start_y = GRID_HEIGHT // 2
        self.body = [
            [start_x, start_y],
            [start_x - 1, start_y],
            [start_x - 2, start_y],
            [start_x - 3, start_y],
        ]
        self.direction = 'RIGHT'
        self.next_direction = 'RIGHT'
        self.growing = False

    def change_direction(self, new_dir):
        opposites = {'UP': 'DOWN', 'DOWN': 'UP', 'LEFT': 'RIGHT', 'RIGHT': 'LEFT'}
        if new_dir != opposites.get(self.direction):
            self.next_direction = new_dir

    def move(self):
        self.direction = self.next_direction
        head = self.body[0].copy()

        moves = {'UP': (0, -1), 'DOWN': (0, 1), 'LEFT': (-1, 0), 'RIGHT': (1, 0)}
        dx, dy = moves[self.direction]
        head[0] += dx
        head[1] += dy

        self.body.insert(0, head)
        if not self.growing:
            self.body.pop()
        self.growing = False

    def grow(self):
        self.growing = True

    def check_collision(self):
        head = self.body[0]
        # Murs
        if head[0] < 0 or head[0] >= GRID_WIDTH or head[1] < 0 or head[1] >= GRID_HEIGHT:
            return True
        # Corps
        if head in self.body[1:]:
            return True
        return False

    def draw(self, surface, time_offset):
        for i, segment in enumerate(self.body):
            x = segment[0] * CELL_SIZE
            y = segment[1] * CELL_SIZE

            # Dégradé de couleur tête → queue
            ratio = i / max(len(self.body) - 1, 1)
            if i == 0:
                color = COLORS['snake_head']
                size_mod = 2
            else:
                color = (
                    int(COLORS['snake_body'][0] * (1 - ratio * 0.3)),
                    int(COLORS['snake_body'][1] * (1 - ratio * 0.3)),
                    int(COLORS['snake_body'][2] * (1 - ratio * 0.3)),
                )
                size_mod = 0

            # Animation subtile
            wave = math.sin(time_offset * 5 + i * 0.3) * 1

            # Rectangle arrondi
            rect = pygame.Rect(
                x + 2 - size_mod + wave,
                y + 2 - size_mod,
                CELL_SIZE - 4 + size_mod * 2,
                CELL_SIZE - 4 + size_mod * 2
            )
            pygame.draw.rect(surface, color, rect, border_radius=6)

            # Contour subtil
            pygame.draw.rect(surface, COLORS['snake_outline'], rect, 1, border_radius=6)

            # Yeux sur la tête
            if i == 0:
                self._draw_eyes(surface, x, y)

    def _draw_eyes(self, surface, x, y):
        eye_offsets = {
            'UP': [(6, 6), (12, 6)],
            'DOWN': [(6, 12), (12, 12)],
            'LEFT': [(6, 6), (6, 12)],
            'RIGHT': [(12, 6), (12, 12)],
        }
        for ox, oy in eye_offsets[self.direction]:
            pygame.draw.circle(surface, (255, 255, 255), (x + ox, y + oy), 3)
            pygame.draw.circle(surface, (0, 0, 0), (x + ox, y + oy), 1)


