"""Archivo principal para ejecutar el CLI de Backgammon.

Este archivo permite iniciar el CLI desde la raíz del proyecto.
"""

from cli.cli import run_cli

def main() -> None:
    """
    Ejecuta el CLI de Backgammon.
    """
    run_cli()

if __name__ == "__main__":
    main()
