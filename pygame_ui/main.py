"""
Archivo principal para ejecutar la interfaz gráfica de Backgammon.
"""

from pygameUI import PygameUI


def main():
    """Función principal para ejecutar la interfaz gráfica."""
    try:
        ui = PygameUI()
        ui.run()
    except Exception as e:
        print(f"Error al ejecutar la interfaz gráfica: {e}")
        import pygame
        pygame.quit()


if __name__ == "__main__":
    main()
