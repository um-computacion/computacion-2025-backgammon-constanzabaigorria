"""Punto de entrada para lanzar el juego de Backgammon."""

from cli.cli import run_cli
# from pygame_ui.pygame_ui import main as run_pygame_ui


def main() -> None:
    """Ejecuta el juego de Backgammon.
    
    Presenta un menú al usuario para elegir entre CLI o Pygame UI.
    """
    print("=" * 60)
    print("\n BACKGAMMON")
    print("\nElige una interfaz:")
    print("  1. CLI (Línea de comandos)")
    print("  2. Pygame UI (Interfaz gráfica)")
    print("\nIngresa tu elección (1 o 2): ", end="")
    
    choice = input().strip()
    
    if choice == "1":
        print("\nIniciando modo CLI...\n")
        run_cli()
    elif choice == "2":
        print("\nIniciando modo Pygame UI...\n")
        try:
            from pygame_ui.pygame_ui import main as run_pygame_ui
            run_pygame_ui()
        except ImportError:
            print("Pygame UI no disponible. Usa CLI (opción 1).")
    else:
        print("\nOpción inválida. Ejecuta el programa nuevamente y elige 1 o 2.")


if __name__ == "__main__":
    main()