# game.py - Lógica del juego y componentes visuales
import pygame
import random
import time
from config import *

class Card:
    """Representa una carta individual en el tablero"""
    
    def __init__(self, value, row, col):
        self.value = value
        self.row = row
        self.col = col
        self.revealed = False
        self.matched = False
        self.color = COLORS[value]
        self.id = row * GRID_SIZE + col
    
    def draw(self, screen, font):
        """Dibuja la carta en la pantalla"""
        x = self.col * (CARD_SIZE + MARGIN) + MARGIN + 50
        y = self.row * (CARD_SIZE + MARGIN) + MARGIN + 150
        
        if self.matched:
            self._draw_matched(screen, font, x, y)
        elif self.revealed:
            self._draw_revealed(screen, font, x, y)
        else:
            self._draw_hidden(screen, font, x, y)
    
    def _draw_matched(self, screen, font, x, y):
        """Dibuja una carta emparejada"""
        pygame.draw.rect(screen, self.color, (x, y, CARD_SIZE, CARD_SIZE))
        pygame.draw.rect(screen, BLACK, (x, y, CARD_SIZE, CARD_SIZE), 2)
        text = font.render(str(self.value + 1), True, WHITE)
        screen.blit(text, (x + CARD_SIZE//2 - 5, y + CARD_SIZE//2 - 10))
    
    def _draw_revealed(self, screen, font, x, y):
        """Dibuja una carta revelada"""
        pygame.draw.rect(screen, self.color, (x, y, CARD_SIZE, CARD_SIZE))
        pygame.draw.rect(screen, BLACK, (x, y, CARD_SIZE, CARD_SIZE), 2)
        text = font.render(str(self.value + 1), True, WHITE)
        screen.blit(text, (x + CARD_SIZE//2 - 5, y + CARD_SIZE//2 - 10))
    
    def _draw_hidden(self, screen, font, x, y):
        """Dibuja una carta oculta"""
        pygame.draw.rect(screen, DARK_GRAY, (x, y, CARD_SIZE, CARD_SIZE))
        pygame.draw.rect(screen, BLACK, (x, y, CARD_SIZE, CARD_SIZE), 2)
        text = font.render("?", True, WHITE)
        screen.blit(text, (x + CARD_SIZE//2 - 5, y + CARD_SIZE//2 - 10))

class MemoriceGame:
    """Clase principal que maneja la lógica del juego"""
    
    def __init__(self):
        self.reset_game()
        self.font = pygame.font.SysFont('Arial', FONT_SIZE)
        self.large_font = pygame.font.SysFont('Arial', LARGE_FONT_SIZE)
    
    def reset_game(self):
        """Reinicia el juego a su estado inicial"""
        self._initialize_cards()
        self.revealed_cards = []
        self.matched_pairs = 0
        self.moves = 0
        self.game_over = False
        self.start_time = time.time()
        self.end_time = None
    
    def _initialize_cards(self):
        """Inicializa las cartas del juego"""
        self.cards = []
        values = list(range(18)) * 2  # 18 parejas
        random.shuffle(values)
        
        for i in range(GRID_SIZE):
            for j in range(GRID_SIZE):
                idx = i * GRID_SIZE + j
                if idx < len(values):
                    self.cards.append(Card(values[idx], i, j))
    
    def reveal_card(self, row, col):
        """Revela una carta en la posición especificada"""
        if self.game_over:
            return False
        
        index = row * GRID_SIZE + col
        card = self.cards[index]
        
        if card.revealed or card.matched:
            return False
        
        card.revealed = True
        self.revealed_cards.append(card)
        
        if len(self.revealed_cards) == 2:
            self._process_card_pair()
            return True
        
        return False
    
    def _process_card_pair(self):
        """Procesa un par de cartas reveladas"""
        self.moves += 1
        card1, card2 = self.revealed_cards
        
        if card1.value == card2.value:
            self._handle_matched_pair(card1, card2)
        else:
            self._handle_unmatched_pair()
    
    def _handle_matched_pair(self, card1, card2):
        """Maneja cuando se encuentra una pareja"""
        card1.matched = True
        card2.matched = True
        self.matched_pairs += 1
        self.revealed_cards = []
        
        if self.matched_pairs == 18:
            self._end_game()
    
    def _handle_unmatched_pair(self):
        """Maneja cuando las cartas no son pareja"""
        # Las cartas se ocultarán después de un tiempo en la lógica principal
        pass
    
    def _end_game(self):
        """Finaliza el juego"""
        self.game_over = True
        self.end_time = time.time()
    
    def hide_unmatched_cards(self):
        """Oculta las cartas que no son pareja"""
        for card in self.revealed_cards:
            if not card.matched:
                card.revealed = False
        self.revealed_cards = []
    
    def get_elapsed_time(self):
        """Retorna el tiempo transcurrido"""
        if self.game_over:
            return self.end_time - self.start_time
        return time.time() - self.start_time
    
    def draw(self, screen):
        """Dibuja todo el juego en la pantalla"""
        self._draw_background(screen)
        self._draw_game_info(screen)
        self._draw_cards(screen)
        self._draw_buttons(screen)
    
    def _draw_background(self, screen):
        """Dibuja el fondo de la pantalla"""
        screen.fill(WHITE)
    
    def _draw_game_info(self, screen):
        """Dibuja la información del juego"""
        # Título
        title = self.large_font.render("MEMORICE - AGENTE DE BÚSQUEDA", True, BLUE)
        screen.blit(title, (WIDTH//2 - title.get_width()//2, 20))
        
        # Información del juego
        elapsed_time = self.get_elapsed_time()
        time_text = self.font.render(f"Tiempo: {elapsed_time:.1f}s", True, BLACK)
        moves_text = self.font.render(f"Movimientos: {self.moves}", True, BLACK)
        pairs_text = self.font.render(f"Parejas: {self.matched_pairs}/18", True, BLACK)
        
        screen.blit(time_text, (50, 80))
        screen.blit(moves_text, (250, 80))
        screen.blit(pairs_text, (450, 80))
        
        # Estado del juego
        if self.game_over:
            status_text = self.font.render("¡JUEGO TERMINADO!", True, RED)
            screen.blit(status_text, (WIDTH//2 - status_text.get_width()//2, 110))
    
    def _draw_cards(self, screen):
        """Dibuja todas las cartas"""
        for card in self.cards:
            card.draw(screen, self.font)
    
    def _draw_buttons(self, screen):
        """Dibuja los botones de control"""
        # Botón Reiniciar
        pygame.draw.rect(screen, YELLOW, (WIDTH//2 - 75, HEIGHT - 100, 150, 50))
        reset_text = self.font.render("Reiniciar", True, BLACK)
        screen.blit(reset_text, (WIDTH//2 - reset_text.get_width()//2, HEIGHT - 85))