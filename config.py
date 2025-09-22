# config.py - Configuración del juego
import pygame

# Dimensiones y configuración visual
WIDTH, HEIGHT = 700, 800
CARD_SIZE = 80
GRID_SIZE = 6
MARGIN = 10
FONT_SIZE = 24
LARGE_FONT_SIZE = 36

# Colores
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
GRAY = (200, 200, 200)
DARK_GRAY = (100, 100, 100)
BLUE = (0, 100, 255)
RED = (255, 0, 0)
GREEN = (0, 200, 0)
YELLOW = (255, 255, 0)

# Colores para las cartas (18 parejas)
COLORS = [
    (255, 0, 0), (0, 255, 0), (0, 0, 255), (255, 255, 0),
    (255, 0, 255), (0, 255, 255), (128, 0, 0), (0, 128, 0),
    (0, 0, 128), (128, 128, 0), (128, 0, 128), (0, 128, 128),
    (255, 128, 0), (255, 0, 128), (128, 255, 0), (0, 255, 128),
    (128, 0, 255), (0, 128, 255)
]

# Configuración del agente
MOVE_DELAY = 500  # ms entre movimientos del agente