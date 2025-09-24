# Agente Memorice

El objetivo de esté proyecto es usar un algoritmo de busqueda en el juego Memorice para la asignatura de inteligencia artifical.

## 🎯 Características principales

- **Juego completo de Memorice** con tablero 6x6 (18 parejas de cartas)
- **Interfaz visual atractiva** con Pygame
- **Agente de IA automático** que resuelve el juego usando BFS
- **Modo manual** para jugar tradicionalmente
- **Modo automático** donde el agente juega solo
- **Seguimiento de estadísticas** (tiempo, movimientos, parejas)

## 🧠 Explicación del Agente BFS

### ¿Cómo funciona el agente?
El agente implementa **Búsqueda en Amplitud (BFS)** para encontrar la solución óptima:

- **Estado del juego**: Representado como una tupla de 36 elementos (0 = carta oculta, 1 = carta emparejada)
- **Búsqueda sistemática**: Explora todos los movimientos posibles nivel por nivel
- **Solución óptima**: BFS garantiza encontrar la solución con el menor número de movimientos

### Complejidad del problema
- **Espacio de búsqueda**: 36! / (2^18 × 18!) estados posibles (extremadamente grande)
- **Heurística**: El agente aprovecha que conoce los valores de las cartas
- **Eficiencia**: BFS es completo y óptimo, pero puede ser costoso en memoria
