import pygame
import sys
from game import MemoriceGame
from agent import MemoriceAgent
from config import *

class GameController:
    """Controlador principal del juego"""
    
    def __init__(self):
        pygame.init()
        self.screen = pygame.display.set_mode((WIDTH, HEIGHT))
        pygame.display.set_caption("Memorice - Agente de Búsqueda")
        
        self.game = MemoriceGame()
        self.agent = MemoriceAgent(self.game)
        self.clock = pygame.time.Clock()
        self.running = True
        
        # Fuentes
        self.font = pygame.font.SysFont('Arial', FONT_SIZE)
        self.large_font = pygame.font.SysFont('Arial', LARGE_FONT_SIZE)
    
    def run(self):
        """Bucle principal del juego"""
        while self.running:
            self._handle_events()
            self._update()
            self._render()
            self.clock.tick(60)
        
        pygame.quit()
        sys.exit()
    
    def _handle_events(self):
        """Maneja los eventos del juego"""
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.running = False
            
            elif event.type == pygame.MOUSEBUTTONDOWN:
                self._handle_mouse_click(event.pos)
            
            elif event.type == pygame.USEREVENT:
                # Evento para ocultar cartas no emparejadas
                if not self.agent.solving and len(self.game.revealed_cards) == 2:
                    self.game.hide_unmatched_cards()
    
    def _handle_mouse_click(self, pos):
        """Maneja los clics del mouse"""
        x, y = pos
        
        # Botón Reiniciar
        if (WIDTH//2 - 75 <= x <= WIDTH//2 + 75 and 
            HEIGHT - 100 <= y <= HEIGHT - 50):
            self._reset_game()
        
        # Botón Resolver (izquierdo)
        elif (50 <= x <= 200 and HEIGHT - 100 <= y <= HEIGHT - 50):
            if not self.agent.solving and not self.game.game_over:
                self.agent.solve()
        
        # Botón Paso a Paso (derecho)
        elif (WIDTH - 200 <= x <= WIDTH - 50 and HEIGHT - 100 <= y <= HEIGHT - 50):
            if self.agent.solving and not self.game.game_over:
                self.agent.execute_next_move()
        
        # Clic en cartas (solo en modo manual)
        elif (not self.agent.solving and not self.game.game_over and 
              150 <= y <= 150 + GRID_SIZE * (CARD_SIZE + MARGIN)):
            self._handle_card_click(x, y)
    
    def _handle_card_click(self, x, y):
        """Maneja el clic en una carta"""
        col = (x - 50 - MARGIN) // (CARD_SIZE + MARGIN)
        row = (y - 150 - MARGIN) // (CARD_SIZE + MARGIN)
        
        if 0 <= row < GRID_SIZE and 0 <= col < GRID_SIZE:
            if self.game.reveal_card(row, col):
                # Si se revelaron dos cartas, programar para ocultarlas si no son pareja
                if (len(self.game.revealed_cards) == 2 and 
                    self.game.revealed_cards[0].value != self.game.revealed_cards[1].value):
                    pygame.time.set_timer(pygame.USEREVENT, 1000, True)
    
    def _reset_game(self):
        """Reinicia el juego"""
        self.game.reset_game()
        self.agent = MemoriceAgent(self.game)
    
    def _update(self):
        """Actualiza el estado del juego"""
        # Actualización automática del agente
        if self.agent.solving and not self.game.game_over:
            current_time = pygame.time.get_ticks()
            if (hasattr(self, 'last_agent_move_time') and 
                current_time - self.last_agent_move_time > MOVE_DELAY):
                self.agent.execute_next_move()
                self.last_agent_move_time = current_time
                # Programar para ocultar cartas si es necesario
                if (len(self.game.revealed_cards) == 2 and 
                    self.game.revealed_cards[0].value != self.game.revealed_cards[1].value):
                    pygame.time.set_timer(pygame.USEREVENT, 1000, True)
            elif not hasattr(self, 'last_agent_move_time'):
                self.last_agent_move_time = current_time
    
    def _render(self):
        """Renderiza el juego"""
        self.game.draw(self.screen)
        self._draw_agent_controls()
        self._draw_agent_info()
        pygame.display.flip()
    
    def _draw_agent_controls(self):
        """Dibuja los controles del agente"""
        # Botón Resolver (izquierdo)
        color = GREEN if not self.agent.solving and not self.game.game_over else GRAY
        pygame.draw.rect(self.screen, color, (50, HEIGHT - 100, 150, 50))
        solve_text = self.font.render("Resolver (BFS)", True, BLACK)
        self.screen.blit(solve_text, (65, HEIGHT - 85))
        
        # Botón Paso a Paso (derecho)
        color = BLUE if self.agent.solving and not self.game.game_over else GRAY
        pygame.draw.rect(self.screen, color, (WIDTH - 200, HEIGHT - 100, 150, 50))
        step_text = self.font.render("Paso a Paso", True, BLACK)
        self.screen.blit(step_text, (WIDTH - 185, HEIGHT - 85))
    
    def _draw_agent_info(self):
        """Dibuja la información del agente"""
        if self.agent.solving:
            info = self.agent.get_solution_info()
            status_text = self.font.render(
                f"Agente resolviendo... Paso {info['steps_current']}/{info['steps_total']}", 
                True, GREEN
            )
            self.screen.blit(status_text, (WIDTH//2 - status_text.get_width()//2, 110))
            
            if info['search_time'] > 0:
                time_text = self.font.render(
                    f"Búsqueda: {info['search_time']:.2f}s", 
                    True, BLACK
                )
                self.screen.blit(time_text, (WIDTH//2 - time_text.get_width()//2, 140))

if __name__ == "__main__":
    controller = GameController()

    controller.run()
