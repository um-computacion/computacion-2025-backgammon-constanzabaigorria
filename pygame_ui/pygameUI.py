"""
Módulo de Interfaz Visual de Backgammon (Versión Clásica Renovada)

Este módulo genera un tablero de Backgammon con una estética clásica mejorada:
madera clara, triángulos suaves, botones modernos y texto limpio.
Incluye control de eventos de ratón y renderizado del estado del juego.
"""

import pygame
from typing import Tuple, Optional, List
from core.backgammongame import BackgammonGame


class Boton:
    """Clase simple para manejar botones con estilo clásico renovado."""

    def __init__(
        self,
        x: int,
        y: int,
        ancho: int,
        alto: int,
        texto: str,
        *,
        color_base: Tuple[int, int, int] = (180, 140, 90),
        color_hover: Tuple[int, int, int] = (200, 160, 110),
        color_texto: Tuple[int, int, int] = (30, 20, 10),
    ) -> None:
        """Inicializa el botón con posición, dimensiones y estilo."""
        self.rect = pygame.Rect(x, y, ancho, alto)
        self.texto = texto
        self.color_base = color_base
        self.color_hover = color_hover
        self.color_texto = color_texto
        self.hover = False

    def dibujar(self, superficie: pygame.Surface) -> None:
        """Dibuja el botón en pantalla."""
        color_actual = self.color_hover if self.hover else self.color_base
        pygame.draw.rect(superficie, color_actual, self.rect, border_radius=10)
        pygame.draw.rect(superficie, (80, 60, 40), self.rect, 2, border_radius=10)

        fuente = pygame.font.Font(None, 30)
        texto = fuente.render(self.texto, True, self.color_texto)
        superficie.blit(texto, texto.get_rect(center=self.rect.center))

    def manejar_evento(self, evento: pygame.event.Event) -> bool:
        """Devuelve True si el botón fue presionado."""
        if evento.type == pygame.MOUSEMOTION:
            self.hover = self.rect.collidepoint(evento.pos)
        elif evento.type == pygame.MOUSEBUTTONDOWN and evento.button == 1:
            if self.rect.collidepoint(evento.pos):
                return True
        return False


class TableroBackgammon:
    """Clase que representa visualmente el tablero de Backgammon."""

    def __init__(self, ancho: int = 950, alto: int = 650) -> None:
        """Inicializa la ventana y los parámetros visuales del tablero."""
        pygame.init()
        self.ancho, self.alto = ancho, alto
        self.pantalla = pygame.display.set_mode((ancho, alto))
        pygame.display.set_caption("Backgammon Clásico Renovado")

        # Paleta de colores más cálida y suave
        self.colores = {
            "fondo": (210, 180, 140),
            "madera": (186, 140, 90),
            "borde": (100, 70, 40),
            "punto_claro": (235, 205, 150),
            "punto_oscuro": (170, 110, 60),
            "texto": (30, 20, 10),
            "resaltado": (255, 215, 0),
            "mov_valido": (60, 180, 75),
        }

        # Márgenes y proporciones
        self.margen = 30
        self.borde = 15
        self.ancho_centro = 40
        self.ancho_bear = 70
        self.radio_ficha = 18

        # Cálculo de áreas
        self._calcular_dimensiones()

        # Botón de lanzar dados
        self.boton_dados = Boton(
            self.x_bear + 5,
            self.y_tablero + self.alto_tablero // 2 - 25,
            100,
            45,
            "Tirar Dados",
        )

        # Estado del juego: inicialmente no hay juego vinculado, inicializar en vacío
        self.juego: Optional[BackgammonGame] = None
        self.estado_tablero = []  # estado por defecto vacío hasta vincular juego
        self.dados = None
        self.seleccionado: Optional[int] = None
        self.destinos: Optional[List[int]] = None

    def _calcular_dimensiones(self) -> None:
        """Calcula el tamaño de las áreas principales del tablero."""
        self.ancho_tablero = self.ancho - 2 * self.margen - self.ancho_bear
        self.alto_tablero = self.alto - 2 * self.margen
        self.x_tablero = self.margen
        self.y_tablero = self.margen
        self.x_bear = self.x_tablero + self.ancho_tablero
        self.y_bear = self.y_tablero
        self.ancho_mitad = (self.ancho_tablero - self.ancho_centro) // 2
        self.ancho_punto = self.ancho_mitad // 6
        self.alto_punto = (self.alto_tablero - 40) // 2

    # ---------------------------------------------------------
    # DIBUJO DE ELEMENTOS VISUALES
    # ---------------------------------------------------------

    def dibujar_tablero(self) -> None:
        """Dibuja el fondo, puntos y zonas principales del tablero."""
        self.pantalla.fill(self.colores["fondo"])
        pygame.draw.rect(
            self.pantalla,
            self.colores["borde"],
            (self.x_tablero, self.y_tablero, self.ancho_tablero, self.alto_tablero),
            self.borde,
        )

        # Triángulos alternos arriba/abajo
        self._dibujar_puntos()

        # Área de “bear off”
        pygame.draw.rect(
            self.pantalla,
            (200, 170, 130),
            (self.x_bear, self.y_bear, self.ancho_bear, self.alto_tablero),
        )
        pygame.draw.rect(
            self.pantalla,
            self.colores["borde"],
            (self.x_bear, self.y_bear, self.ancho_bear, self.alto_tablero),
            3,
        )

        # Etiquetas en zona de bear off
        fuente = pygame.font.Font(None, 24)
        texto1 = fuente.render("BLANCAS", True, self.colores["texto"])
        texto2 = fuente.render("NEGRAS", True, self.colores["texto"])
        self.pantalla.blit(
            texto1,
            (self.x_bear + 5, self.y_bear + self.alto_tablero // 4 - 12),
        )
        self.pantalla.blit(
            texto2,
            (self.x_bear + 5, self.y_bear + 3 * self.alto_tablero // 4 - 12),
        )

        # Botón de tirar dados
        self.boton_dados.dibujar(self.pantalla)

    def _dibujar_puntos(self) -> None:
        """Dibuja los triángulos del tablero de forma alternada."""
        for i in range(6):
            x = self.x_tablero + i * self.ancho_punto
            color_arriba = (
                self.colores["punto_oscuro"]
                if i % 2 == 0
                else self.colores["punto_claro"]
            )
            color_abajo = (
                self.colores["punto_claro"]
                if i % 2 == 0
                else self.colores["punto_oscuro"]
            )
            self._dibujar_triangulo(x, self.y_tablero, self.ancho_punto, self.alto_punto, color_arriba, abajo=True)
            self._dibujar_triangulo(x, self.y_tablero + self.alto_tablero - self.alto_punto, self.ancho_punto, self.alto_punto, color_abajo, abajo=False)

        # Lado derecho
        inicio_derecha = self.x_tablero + self.ancho_mitad + self.ancho_centro
        for i in range(6):
            x = inicio_derecha + i * self.ancho_punto
            color_arriba = (
                self.colores["punto_claro"]
                if i % 2 == 0
                else self.colores["punto_oscuro"]
            )
            color_abajo = (
                self.colores["punto_oscuro"]
                if i % 2 == 0
                else self.colores["punto_claro"]
            )
            self._dibujar_triangulo(x, self.y_tablero, self.ancho_punto, self.alto_punto, color_arriba, abajo=True)
            self._dibujar_triangulo(x, self.y_tablero + self.alto_tablero - self.alto_punto, self.ancho_punto, self.alto_punto, color_abajo, abajo=False)

        # Barra central
        pygame.draw.rect(
            self.pantalla,
            (150, 110, 70),
            (
                self.x_tablero + self.ancho_mitad,
                self.y_tablero,
                self.ancho_centro,
                self.alto_tablero,
            ),
        )

    def _dibujar_triangulo(self, x: int, y: int, ancho: int, alto: int, color: Tuple[int, int, int], abajo: bool) -> None:
        """Dibuja un triángulo apuntando hacia arriba o hacia abajo."""
        if abajo:
            puntos = [(x, y), (x + ancho, y), (x + ancho // 2, y + alto)]
        else:
            puntos = [(x, y + alto), (x + ancho, y + alto), (x + ancho // 2, y)]
        pygame.draw.polygon(self.pantalla, color, puntos)
        pygame.draw.polygon(self.pantalla, (80, 60, 40), puntos, 1)

    # ---------------------------------------------------------
    # FUNCIONES DE ESTADO Y EVENTOS
    # ---------------------------------------------------------

    def establecer_juego(self, juego: BackgammonGame) -> None:
        """Vincula una instancia del juego lógico al tablero."""
        self.juego = juego
        self.actualizar_desde_juego()

    def actualizar_desde_juego(self) -> None:
        """Refresca el estado visual según la lógica del juego."""
        if not self.juego:
            return
        self.estado_tablero = self.juego.board.get_board_state()
        if self.juego.last_roll:
            self.dados = self.juego.last_roll

    def manejar_eventos(self, evento: pygame.event.Event) -> None:
        """Controla los clics en el tablero y el botón."""
        if self.boton_dados.manejar_evento(evento):
            if self.juego and (self.juego.last_roll is None or not self.juego.available_moves):
                self.juego.roll_dice()
                self.actualizar_desde_juego()

    def ejecutar(self) -> None:
        """Bucle principal del tablero."""
        reloj = pygame.time.Clock()
        corriendo = True

        while corriendo:
            for evento in pygame.event.get():
                if evento.type == pygame.QUIT:
                    corriendo = False
                elif evento.type == pygame.KEYDOWN and evento.key == pygame.K_ESCAPE:
                    corriendo = False
                else:
                    self.manejar_eventos(evento)

            # Redibujar tablero
            self.dibujar_tablero()

            # Actualizar pantalla
            pygame.display.flip()
            reloj.tick(60)

        pygame.quit()


def main() -> None:
    """Ejecuta el tablero visual clásico renovado."""
    tablero = TableroBackgammon()
    juego = BackgammonGame()
    juego.setup_initial_position()
    tablero.establecer_juego(juego)
    tablero.ejecutar()


if __name__ == "__main__":
    main()
