# agent.py - Agente de búsqueda para resolver el juego
from collections import deque
import time

class MemoriceAgent:
    """Agente que resuelve el juego de Memorice usando BFS"""
    
    def __init__(self, game):
        self.game = game
        self.solving = False
        self.solution_path = []
        self.current_step = 0
        self.search_time = 0
    
    def solve(self):
        """Resuelve el juego usando BFS"""
        print("Iniciando búsqueda de solución...")
        self.solving = True
        self.solution_path = []
        
        start_time = time.time()
        solution_found = self._bfs_search()
        self.search_time = time.time() - start_time
        
        if solution_found:
            print(f"Solución encontrada en {len(self.solution_path)} movimientos!")
            print(f"Tiempo de búsqueda: {self.search_time:.2f}s")
            self.current_step = 0
            return True
        else:
            print("No se encontró solución")
            self.solving = False
            return False
    
    def _bfs_search(self):
        """Implementa el algoritmo BFS para encontrar la solución"""
        # Estado inicial: todas las cartas ocultas (0)
        initial_state = tuple(0 for _ in range(36))
        
        queue = deque([(initial_state, [])])  # (estado, camino)
        visited = set([initial_state])
        
        while queue:
            current_state, path = queue.popleft()
            
            # Verificar si es estado objetivo
            if self._is_goal_state(current_state):
                self.solution_path = path
                return True
            
            # Generar estados sucesores
            for next_state, move in self._generate_successors(current_state):
                if next_state not in visited:
                    visited.add(next_state)
                    queue.append((next_state, path + [move]))
        
        return False
    
    def _is_goal_state(self, state):
        """Verifica si el estado es el objetivo (todas las cartas emparejadas)"""
        return all(s == 1 for s in state)
    
    def _generate_successors(self, state):
        """Genera todos los estados sucesores posibles"""
        successors = []
        
        # Encontrar todas las parejas posibles
        for i in range(36):
            if state[i] == 0:  # Carta no emparejada
                for j in range(i + 1, 36):
                    if state[j] == 0:  # Otra carta no emparejada
                        # Verificar si son del mismo valor
                        if self.game.cards[i].value == self.game.cards[j].value:
                            new_state = list(state)
                            new_state[i] = 1  # Emparejada
                            new_state[j] = 1  # Emparejada
                            successors.append((tuple(new_state), (i, j)))
        
        return successors
    
    def execute_next_move(self):
        """Ejecuta el siguiente movimiento de la solución"""
        if not self.solving or self.current_step >= len(self.solution_path):
            self.solving = False
            return False
        
        card1_idx, card2_idx = self.solution_path[self.current_step]
        
        # Revelar las cartas
        self.game.cards[card1_idx].revealed = True
        self.game.cards[card2_idx].revealed = True
        
        # Verificar si son pareja
        if self.game.cards[card1_idx].value == self.game.cards[card2_idx].value:
            self.game.cards[card1_idx].matched = True
            self.game.cards[card2_idx].matched = True
            self.game.matched_pairs += 1
            self.game.revealed_cards = []
        else:
            self.game.revealed_cards = [
                self.game.cards[card1_idx], 
                self.game.cards[card2_idx]
            ]
        
        self.game.moves += 1
        self.current_step += 1
        
        # Verificar si el juego terminó
        if self.game.matched_pairs == 18:
            self.game._end_game()
            self.solving = False
        
        return True
    
    def get_solution_info(self):
        """Retorna información sobre la solución"""
        return {
            'solving': self.solving,
            'steps_total': len(self.solution_path),
            'steps_current': self.current_step,
            'search_time': self.search_time
        }