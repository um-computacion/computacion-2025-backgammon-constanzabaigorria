"""
Módulo de Interfaz Visual de Backgammon (Versión Clásica Renovada)

Este módulo genera un tablero de Backgammon con una estética clásica mejorada:
madera clara, triángulos suaves, botones modernos y texto limpio.
Incluye control de eventos de ratón y renderizado del estado del juego.
"""

import os
from typing import Tuple, Optional, List

os.environ['PYGAME_HIDE_SUPPORT_PROMPT'] = "hide"
import pygame  # pylint: disable=wrong-import-position
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

        # Ajustar tamaño de fuente para que el texto quepa perfectamente
        ancho_boton = self.rect.width
        alto_boton = self.rect.height
        padding_texto = 6  # Padding mínimo dentro del botón

        # Empezar con un tamaño más grande y reducir hasta que quepa
        tamano_fuente = 28
        fuente = pygame.font.Font(None, tamano_fuente)
        texto = fuente.render(self.texto, True, self.color_texto)

        # Reducir tamaño de fuente si el texto es demasiado ancho
        while texto.get_width() > (ancho_boton - padding_texto) and tamano_fuente > 20:
            tamano_fuente -= 1
            fuente = pygame.font.Font(None, tamano_fuente)
            texto = fuente.render(self.texto, True, self.color_texto)

        # Asegurar que también quepa en altura
        while texto.get_height() > (alto_boton - padding_texto) and tamano_fuente > 20:
            tamano_fuente -= 1
            fuente = pygame.font.Font(None, tamano_fuente)
            texto = fuente.render(self.texto, True, self.color_texto)

        # Centrar perfectamente el texto dentro del botón
        texto_rect = texto.get_rect(center=self.rect.center)
        superficie.blit(texto, texto_rect)

    def manejar_evento(self, evento: pygame.event.Event) -> bool:
        """Devuelve True si el botón fue presionado."""
        if evento.type == 1024:  # MOUSEMOTION
            self.hover = self.rect.collidepoint(evento.pos)
        elif evento.type == 1025 and evento.button == 1:  # MOUSEBUTTONDOWN
            if self.rect.collidepoint(evento.pos):
                return True
        return False


class TableroBackgammon:
    """Clase que representa visualmente el tablero de Backgammon."""

    def __init__(self, ancho: int = 950, alto: int = 650) -> None:
        """Inicializa la ventana y los parámetros visuales del tablero."""
        pygame.init()  # pylint: disable=no-member
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
            "ficha_blanca": (240, 240, 240),
            "ficha_negra": (40, 40, 40),
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
            self.ancho_bear - 10,
            45,
            "Tirar Dado",
        )

        # Estado del juego
        self.juego: Optional[BackgammonGame] = None
        self.estado_tablero = None
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

    def dibujar_tablero(self) -> None:
        """Dibuja el tablero completo."""
        self.pantalla.fill(self.colores["fondo"])
        # Dibuja el marco del tablero
        pygame.draw.rect(
            self.pantalla,
            self.colores["madera"],
            (self.x_tablero, self.y_tablero, self.ancho_tablero, self.alto_tablero),
        )
        pygame.draw.rect(
            self.pantalla,
            self.colores["borde"],
            (self.x_tablero, self.y_tablero, self.ancho_tablero, self.alto_tablero),
            self.borde,
        )

        # Dibuja los triángulos
        self._dibujar_puntos()

        # Área de "bear off"
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
        # Dibujar fichas bear off
        if self.juego:
            board = self.juego.get_board()
            # BLANCAS (arriba)
            blancas_off = board.bear_off["white"]
            total_blancas = len(blancas_off)
            fichas_blancas_a_dibujar = min(total_blancas, 6)
            x_blancas = self.x_bear + self.ancho_bear // 2
            for idx in range(fichas_blancas_a_dibujar):
                y = self.y_bear + 50 + idx * (self.radio_ficha * 2 + 2)
                pygame.draw.circle(
                    self.pantalla, self.colores["ficha_blanca"], (x_blancas, y), self.radio_ficha
                )
                pygame.draw.circle(
                    self.pantalla, self.colores["borde"], (x_blancas, y), self.radio_ficha, 2
                )
            # Si hay más de 6 fichas blancas, mostrar número
            if total_blancas > 6:
                fuente_numero = pygame.font.Font(None, 20)
                texto_numero = fuente_numero.render(
                    str(total_blancas), True, self.colores["texto"]
                )
                y_num_blancas = self.y_bear + 50 + 6 * (self.radio_ficha * 2 + 2)
                x_num_blancas = x_blancas - texto_numero.get_width() // 2
                # Fondo para el número
                pygame.draw.circle(
                    self.pantalla, (255, 255, 255), (x_blancas, y_num_blancas),
                    self.radio_ficha - 2
                )
                self.pantalla.blit(
                    texto_numero,
                    (x_num_blancas, y_num_blancas - texto_numero.get_height() // 2)
                )
            # NEGRAS (abajo)
            negras_off = board.bear_off["black"]
            total_negras = len(negras_off)
            fichas_negras_a_dibujar = min(total_negras, 6)
            x_negras = self.x_bear + self.ancho_bear // 2
            for idx in range(fichas_negras_a_dibujar):
                y = self.y_bear + self.alto_tablero - 50 - idx * (self.radio_ficha * 2 + 2)
                pygame.draw.circle(
                    self.pantalla, self.colores["ficha_negra"], (x_negras, y), self.radio_ficha
                )
                pygame.draw.circle(
                    self.pantalla, self.colores["borde"], (x_negras, y), self.radio_ficha, 2
                )
            # Si hay más de 6 fichas negras, mostrar número
            if total_negras > 6:
                fuente_numero = pygame.font.Font(None, 20)
                texto_numero = fuente_numero.render(str(total_negras), True, self.colores["texto"])
                y_num_negras = self.y_bear + self.alto_tablero - 50 - 6 * (self.radio_ficha * 2 + 2)
                x_num_negras = x_negras - texto_numero.get_width() // 2
                # Fondo para el número
                pygame.draw.circle(
                    self.pantalla, (255, 255, 255), (x_negras, y_num_negras),
                    self.radio_ficha - 2
                )
                self.pantalla.blit(
                    texto_numero,
                    (x_num_negras, y_num_negras - texto_numero.get_height() // 2)
                )

        # Dibujar fichas si hay juego activo
        if self.juego:
            self._dibujar_fichas()
            self._dibujar_fichas_barra()
            # Dibujar movimientos válidos si hay una ficha seleccionada
            if self.seleccionado is not None:
                if self.seleccionado == -1:
                    # Barra seleccionada, dibujar indicación y movimientos válidos
                    self._dibujar_barra_seleccionada()
                    self._dibujar_movimientos_validos_desde_barra()
                else:
                    self._dibujar_movimientos_validos()

        # Etiquetas en zona de bear off
        # Calcular tamaño de fuente que quepa en el ancho disponible
        ancho_disponible = self.ancho_bear - 8  # Dejar 4 píxeles de padding a cada lado
        fuente_tamano = 26  # Tamaño inicial más grande
        fuente_bold = pygame.font.Font(None, fuente_tamano)
        # Probar si el texto más largo cabe, si no reducir fuente
        texto_prueba = fuente_bold.render("BLANCAS: 99", True, self.colores["texto"])
        while texto_prueba.get_width() > ancho_disponible and fuente_tamano > 18:
            fuente_tamano -= 1
            fuente_bold = pygame.font.Font(None, fuente_tamano)
            texto_prueba = fuente_bold.render("BLANCAS: 99", True, self.colores["texto"])

        fuente = pygame.font.Font(None, fuente_tamano - 2)
        # Mostrar la cantidad de fichas retiradas (bear off)
        if self.juego:
            board = self.juego.get_board()
            num_blancas = len(board.bear_off["white"])
            num_negras = len(board.bear_off["black"])
            texto1 = fuente_bold.render(
                f"BLANCAS: {num_blancas}", True, self.colores["texto"]
            )
            texto2 = fuente_bold.render(
                f"NEGRAS: {num_negras}", True, self.colores["texto"]
            )

            # Usar todo el ancho disponible menos un pequeño padding
            padding_x = 4
            rect1_w = self.ancho_bear - 2 * padding_x
            rect2_w = self.ancho_bear - 2 * padding_x
            rect1_x = self.x_bear + padding_x
            rect2_x = self.x_bear + padding_x

            # Dibujar fondo para mejor visibilidad
            rect1 = pygame.Rect(
                rect1_x, self.y_bear + self.alto_tablero // 4 - 15,
                rect1_w, texto1.get_height() + 8
            )
            rect2 = pygame.Rect(
                rect2_x, self.y_bear + 3 * self.alto_tablero // 4 - 15,
                rect2_w, texto2.get_height() + 8
            )
            pygame.draw.rect(self.pantalla, (240, 230, 200), rect1, border_radius=5)
            pygame.draw.rect(self.pantalla, self.colores["borde"], rect1, 2, border_radius=5)
            pygame.draw.rect(self.pantalla, (240, 230, 200), rect2, border_radius=5)
            pygame.draw.rect(self.pantalla, self.colores["borde"], rect2, 2, border_radius=5)

            # Centrar perfectamente el texto dentro del fondo
            texto1_x = rect1_x + (rect1_w - texto1.get_width()) // 2
            texto2_x = rect2_x + (rect2_w - texto2.get_width()) // 2
        else:
            texto1 = fuente.render("BLANCAS", True, self.colores["texto"])
            texto2 = fuente.render("NEGRAS", True, self.colores["texto"])
            texto1_x = self.x_bear + (self.ancho_bear - texto1.get_width()) // 2
            texto2_x = self.x_bear + (self.ancho_bear - texto2.get_width()) // 2
        self.pantalla.blit(
            texto1,
            (texto1_x, self.y_bear + self.alto_tablero // 4 - 12),
        )
        self.pantalla.blit(
            texto2,
            (texto2_x, self.y_bear + 3 * self.alto_tablero // 4 - 12),
        )

        # Botón de tirar dados
        self.boton_dados.dibujar(self.pantalla)

        # Dibujar dados si están disponibles
        if self.dados:
            self._dibujar_dados()

        # Dibujar información del turno o victoria
        if self.juego and self.juego.is_finished():
            self._dibujar_victoria()
        else:
            self._dibujar_info_turno()

        pygame.display.flip()

    def _dibujar_puntos(self) -> None:
        """Dibuja los triángulos del tablero."""
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
            self._dibujar_triangulo(
                x, self.y_tablero, self.ancho_punto, self.alto_punto,
                color_arriba, abajo=True
            )
            self._dibujar_triangulo(
                x, self.y_tablero + self.alto_tablero - self.alto_punto,
                self.ancho_punto, self.alto_punto, color_abajo, abajo=False
            )

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
            self._dibujar_triangulo(
                x, self.y_tablero, self.ancho_punto, self.alto_punto,
                color_arriba, abajo=True
            )
            self._dibujar_triangulo(
                x, self.y_tablero + self.alto_tablero - self.alto_punto,
                self.ancho_punto, self.alto_punto, color_abajo, abajo=False
            )

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

    def _dibujar_triangulo(
        self, x: int, y: int, ancho: int, alto: int,
        color: Tuple[int, int, int], abajo: bool
    ) -> None:
        """Dibuja un triángulo."""
        if abajo:
            puntos = [(x, y), (x + ancho, y), (x + ancho // 2, y + alto)]
        else:
            puntos = [(x, y + alto), (x + ancho, y + alto), (x + ancho // 2, y)]
        pygame.draw.polygon(self.pantalla, color, puntos)
        pygame.draw.polygon(self.pantalla, (80, 60, 40), puntos, 1)

    def _dibujar_fichas(self) -> None:
        """Dibuja las fichas en el tablero."""
        if not self.juego:
            return

        # Obtener las fichas directamente desde el tablero del juego
        board = self.juego.get_board()

        # Para cada punto en el tablero
        for punto in range(24):
            x = self._calcular_x_punto(punto)
            y_base = self._calcular_y_base(punto)
            y_dir = 1 if punto >= 12 else -1

            # Obtener fichas en este punto desde el tablero
            fichas_en_punto = []
            if board.points[punto]:  # Si hay fichas en este punto
                for ficha in board.points[punto]:
                    if ficha.get_color() == "white":
                        color_ficha = self.colores["ficha_blanca"]
                    else:
                        color_ficha = self.colores["ficha_negra"]
                    fichas_en_punto.append((ficha.get_color(), color_ficha))

            # Dibujar las fichas (máximo 6 visualmente)
            total_fichas = len(fichas_en_punto)
            fichas_a_dibujar = min(total_fichas, 6)
            # Espaciado adecuado para evitar superposiciones
            espaciado_fichas = self.radio_ficha * 2 + 2
            for idx in range(fichas_a_dibujar):
                _, color_ficha = fichas_en_punto[idx]
                y = y_base + (y_dir * idx * espaciado_fichas)
                pygame.draw.circle(
                    self.pantalla,
                    color_ficha,
                    (x + self.ancho_punto // 2, y),
                    self.radio_ficha
                )
                # Dibujar borde especial si la ficha está seleccionada
                if self.seleccionado == punto:
                    color_borde = self.colores["resaltado"]
                    grosor_borde = 4
                else:
                    color_borde = self.colores["borde"]
                    grosor_borde = 2
                pygame.draw.circle(
                    self.pantalla,
                    color_borde,
                    (x + self.ancho_punto // 2, y),
                    self.radio_ficha,
                    grosor_borde
                )
            # Si hay más de 6 fichas, dibujar un número indicando la cantidad
            if total_fichas > 6:
                fuente_numero = pygame.font.Font(None, 20)
                texto_numero = fuente_numero.render(str(total_fichas), True, self.colores["texto"])
                x_num = x + self.ancho_punto // 2
                y_num = y_base + (y_dir * 6 * espaciado_fichas)
                x_num_texto = x_num - texto_numero.get_width() // 2
                # Fondo para el número
                pygame.draw.circle(
                    self.pantalla,
                    (255, 255, 255),
                    (x_num, y_num),
                    self.radio_ficha - 2
                )
                self.pantalla.blit(
                    texto_numero,
                    (x_num_texto, y_num - texto_numero.get_height() // 2)
                )

    def _dibujar_fichas_barra(self) -> None:
        """Dibuja las fichas en la barra."""
        if not self.juego:
            return
        board = self.juego.get_board()
        espaciado_barra = self.radio_ficha * 2 + 3  # Espaciado adecuado para fichas en la barra
        # Dibujar fichas blancas en la barra
        fichas_blancas_barra = board.bar["white"]
        total_blancas_barra = len(fichas_blancas_barra)
        fichas_blancas_a_dibujar = min(total_blancas_barra, 6)
        x_blancas_barra = self.x_tablero + self.ancho_tablero // 2 - self.radio_ficha
        for idx in range(fichas_blancas_a_dibujar):
            y = self.y_tablero + self.alto_tablero // 2 - 20 - (idx * espaciado_barra)
            pygame.draw.circle(
                self.pantalla,
                self.colores["ficha_blanca"],
                (x_blancas_barra, y),
                self.radio_ficha
            )
            pygame.draw.circle(
                self.pantalla,
                self.colores["borde"],
                (x_blancas_barra, y),
                self.radio_ficha,
                2
            )
        # Si hay más de 6 fichas blancas en la barra, mostrar número
        if total_blancas_barra > 6:
            fuente_numero = pygame.font.Font(None, 18)
            texto_numero = fuente_numero.render(
                str(total_blancas_barra), True, self.colores["texto"]
            )
            y_num = self.y_tablero + self.alto_tablero // 2 - 20 - (6 * espaciado_barra)
            x_num_texto = x_blancas_barra - texto_numero.get_width() // 2
            pygame.draw.circle(
                self.pantalla, (255, 255, 255), (x_blancas_barra, y_num),
                self.radio_ficha - 2
            )
            self.pantalla.blit(
                texto_numero, (x_num_texto, y_num - texto_numero.get_height() // 2)
            )
        # Dibujar fichas negras en la barra
        fichas_negras_barra = board.bar["black"]
        total_negras_barra = len(fichas_negras_barra)
        fichas_negras_a_dibujar = min(total_negras_barra, 6)
        x_negras_barra = self.x_tablero + self.ancho_tablero // 2 + self.radio_ficha
        for idx in range(fichas_negras_a_dibujar):
            y = self.y_tablero + self.alto_tablero // 2 - 20 - (idx * espaciado_barra)
            pygame.draw.circle(
                self.pantalla,
                self.colores["ficha_negra"],
                (x_negras_barra, y),
                self.radio_ficha
            )
            pygame.draw.circle(
                self.pantalla,
                self.colores["borde"],
                (x_negras_barra, y),
                self.radio_ficha,
                2
            )
        # Si hay más de 6 fichas negras en la barra, mostrar número
        if total_negras_barra > 6:
            fuente_numero = pygame.font.Font(None, 18)
            texto_numero = fuente_numero.render(
                str(total_negras_barra), True, self.colores["texto"]
            )
            y_num = self.y_tablero + self.alto_tablero // 2 - 20 - (6 * espaciado_barra)
            x_num_texto = x_negras_barra - texto_numero.get_width() // 2
            pygame.draw.circle(
                self.pantalla, (255, 255, 255), (x_negras_barra, y_num),
                self.radio_ficha - 2
            )
            self.pantalla.blit(
                texto_numero, (x_num_texto, y_num - texto_numero.get_height() // 2)
            )

    def _dibujar_barra_seleccionada(self) -> None:
        """Dibuja una indicación visual cuando la barra está seleccionada."""
        barra_x_centro = self.x_tablero + self.ancho_tablero // 2
        barra_y_centro = self.y_tablero + self.alto_tablero // 2
        # Dibujar un círculo dorado alrededor de la barra
        pygame.draw.circle(
            self.pantalla,
            (255, 215, 0),  # Color dorado
            (barra_x_centro, barra_y_centro),
            60,
            3
        )

    def _dibujar_movimientos_validos_desde_barra(self) -> None:
        """Dibuja los movimientos válidos desde la barra."""
        if not self.juego:
            return
        jugador_actual = self.juego.get_current_player()
        color_jugador = jugador_actual.get_color()
        board = self.juego.get_board()
        # Verificar que el jugador tenga fichas en la barra
        if not board.bar[color_jugador]:
            return
        # Obtener los valores de dados disponibles
        dados_disponibles = self.juego.get_last_dice_roll()
        if not dados_disponibles:
            return
        # Manejar tuplas de cualquier longitud (dobles tienen 4 elementos)
        if len(dados_disponibles) >= 1:
            # Dobles: (2,2,2,2) o normales: (2,5) o parcial: (2,)
            valores_dados = list(dados_disponibles)
        else:
            return
        # Calcular puntos válidos según el color del jugador
        puntos_validos = []
        for valor_dado in valores_dados:
            if color_jugador == "white":
                # Fichas blancas reingresan en el lado del oponente (puntos 1-6)
                punto_destino = valor_dado
            else:
                # Fichas negras reingresan en el lado del oponente (puntos 19-24)
                punto_destino = 25 - valor_dado
            # Verificar que el punto sea válido según las reglas de reingreso
            if color_jugador == "white":
                # Fichas blancas solo pueden reingresar en puntos 1-6
                if punto_destino < 1 or punto_destino > 6:
                    continue
            else:
                # Fichas negras solo pueden reingresar en puntos 19-24
                if punto_destino < 19 or punto_destino > 24:
                    continue
            punto_idx = punto_destino - 1
            # Verificar si el punto está bloqueado por el oponente
            if board.points[punto_idx]:
                primera_ficha = board.points[punto_idx][0]
                if primera_ficha.get_owner() != jugador_actual:
                    # Si hay más de una ficha del oponente, está bloqueado
                    if len(board.points[punto_idx]) > 1:
                        continue  # Punto bloqueado
            puntos_validos.append(punto_idx)
        # Dibujar círculos verdes en los puntos válidos
        for punto_idx in puntos_validos:
            self._dibujar_circulo_movimiento_valido(punto_idx)

    def _dibujar_circulo_movimiento_valido(self, punto_idx: int) -> None:
        """Dibuja un círculo verde en un punto válido para movimiento."""
        # Usar la misma lógica que _calcular_x_punto y _calcular_y_base
        x = self._calcular_x_punto(punto_idx)
        y_base = self._calcular_y_base(punto_idx)

        # Dibujar círculo verde
        pygame.draw.circle(
            self.pantalla,
            (0, 255, 0),  # Verde
            (x + self.ancho_punto // 2, y_base),
            15,
            3
        )

    def _dibujar_movimientos_validos(self) -> None:
        """Dibuja los movimientos válidos para la ficha seleccionada."""
        if self.seleccionado is None or not self.juego:
            return

        # Obtener movimientos válidos desde el punto seleccionado
        movimientos_validos = []
        if self.juego.has_dice_been_rolled():
            dados_disponibles = self.juego.get_last_dice_roll()

            # Manejar tuplas de cualquier longitud (dobles tienen 4 elementos)
            if len(dados_disponibles) >= 1:
                # Dobles: (2,2,2,2) o normales: (2,5) o parcial: (2,)
                dados_a_procesar = list(dados_disponibles)
            else:
                return

            punto_seleccionado = self.seleccionado + 1

            # Calcular posibles destinos
            jugador_actual = self.juego.get_current_player()

            color = jugador_actual.get_color()
            can_bear = self.juego.can_bear_off(jugador_actual)

            for dado in dados_a_procesar:
                # En Backgammon:
                # - Fichas blancas van hacia números más altos (1->24)
                # - Fichas negras van hacia números más bajos (24->1)
                if jugador_actual.get_color() == "white":
                    destino = punto_seleccionado + dado
                else:
                    destino = punto_seleccionado - dado

                # Movimientos normales en el tablero
                if 1 <= destino <= 24:
                    if self.juego.is_valid_move(punto_seleccionado, destino):
                        movimientos_validos.append(destino - 1)  # Convertir a índice 0-based

            # Bear off: verificar SIEMPRE si puede sacar fichas (fuera del bucle de dados)
            if can_bear:
                if color == "white" and 19 <= punto_seleccionado <= 24:
                    # Verificar si el bear off es válido con los dados disponibles
                    if self.juego.is_valid_move(punto_seleccionado, 25):
                        # Dibujar indicador de bear off en zona de bear off para BLANCAS (arriba)
                        x_bear = self.x_bear + self.ancho_bear // 2
                        # Posición para blancas: en el cuarto superior del área de bear off
                        y_bear = self.y_bear + self.alto_tablero // 4
                        pygame.draw.circle(
                            self.pantalla,
                            self.colores["mov_valido"],
                            (x_bear, y_bear),
                            self.radio_ficha + 8,
                            3
                        )
                        # También dibujar un círculo más grande para mejor visibilidad
                        pygame.draw.circle(
                            self.pantalla,
                            self.colores["mov_valido"],
                            (x_bear, y_bear),
                            self.radio_ficha + 12,
                            2
                        )
                elif color == "black" and 1 <= punto_seleccionado <= 6:
                    # Verificar si el bear off es válido con los dados disponibles
                    if self.juego.is_valid_move(punto_seleccionado, 0):
                        # Dibujar indicador de bear off en zona de bear off
                        x_bear = self.x_bear + self.ancho_bear // 2
                        y_bear = self.y_bear + 3 * self.alto_tablero // 4
                        pygame.draw.circle(
                            self.pantalla,
                            self.colores["mov_valido"],
                            (x_bear, y_bear),
                            self.radio_ficha + 8,
                            3
                        )

        # Dibujar círculos de destino válidos
        for destino_idx in movimientos_validos:
            x = self._calcular_x_punto(destino_idx)
            y_base = self._calcular_y_base(destino_idx)

            # Dibujar círculo de destino válido
            pygame.draw.circle(
                self.pantalla,
                self.colores["mov_valido"],
                (x + self.ancho_punto // 2, y_base),
                self.radio_ficha + 5,
                3
                )

    def _calcular_x_punto(self, punto: int) -> int:
        """Calcula la coordenada x para un punto (0-23) mapeando a 6 columnas por lado."""
        inicio_derecha = self.x_tablero + self.ancho_mitad + self.ancho_centro
        # Lado izquierdo (6 columnas)
        if 6 <= punto <= 11:  # inferior izquierda: 11..6
            col = 11 - punto
            return self.x_tablero + col * self.ancho_punto
        if 12 <= punto <= 17:  # superior izquierda: 12..17
            col = punto - 12
            return self.x_tablero + col * self.ancho_punto
        # Lado derecho (6 columnas)
        if 0 <= punto <= 5:  # inferior derecha: 5..0
            col = 5 - punto
            return inicio_derecha + col * self.ancho_punto
        if 18 <= punto <= 23:  # superior derecha: 18..23
            col = punto - 18
            return inicio_derecha + col * self.ancho_punto
        # Fallback (no debería ocurrir)
        return self.x_tablero

    def _calcular_y_base(self, punto: int) -> int:
        """Calcula la coordenada y base para un punto."""
        if punto < 12:
            return self.y_tablero + self.alto_tablero - self.radio_ficha
        else:
            return self.y_tablero + self.radio_ficha

    def _dibujar_dados(self) -> None:
        """Dibuja los dados."""
        if not self.dados:
            return

        # Manejar tuplas de cualquier longitud
        # Dobles: (2,2,2,2) inicialmente, luego (2,2,2), (2,2), (2), ()
        # Normales: (2,5) inicialmente, luego (5) o (2), luego ()
        if len(self.dados) >= 2:
            # Mostrar todos los dados disponibles (máximo 4 para dobles)
            dados_a_dibujar = list(self.dados[:4])
        elif len(self.dados) == 1:
            dados_a_dibujar = [self.dados[0]]
        else:
            return

        x_base = self.x_tablero + self.ancho_tablero // 2 - 50
        y_base = self.y_tablero + self.alto_tablero // 2 - 25
        lado = 40

        # Ajustar posición inicial si hay más de 2 dados
        if len(dados_a_dibujar) > 2:
            x_base = x_base - (len(dados_a_dibujar) - 2) * 30

        for i, valor in enumerate(dados_a_dibujar):
            x = x_base + i * (60 if len(dados_a_dibujar) <= 2 else 50)
            # Cuadrado del dado
            pygame.draw.rect(
                self.pantalla,
                (255, 255, 255),
                (x, y_base, lado, lado)
            )
            pygame.draw.rect(
                self.pantalla,
                self.colores["borde"],
                (x, y_base, lado, lado),
                2
            )
            # Puntos del dado
            self._dibujar_puntos_dado(x, y_base, lado, valor)

    def _dibujar_puntos_dado(self, x: int, y: int, lado: int, valor: int) -> None:
        """Dibuja los puntos de un dado."""
        puntos = []
        radio = 4
        if valor in [1, 3, 5]:
            puntos.append((x + lado // 2, y + lado // 2))  # Centro
        if valor >= 2:
            puntos.extend([
                (x + lado // 4, y + lado // 4),          # Arriba izquierda
                (x + 3 * lado // 4, y + 3 * lado // 4)   # Abajo derecha
            ])
        if valor >= 4:
            puntos.extend([
                (x + 3 * lado // 4, y + lado // 4),      # Arriba derecha
                (x + lado // 4, y + 3 * lado // 4)       # Abajo izquierda
            ])
        if valor == 6:
            puntos.extend([
                (x + lado // 4, y + lado // 2),          # Medio izquierda
                (x + 3 * lado // 4, y + lado // 2)       # Medio derecha
            ])
        for punto in puntos:
            pygame.draw.circle(self.pantalla, self.colores["texto"], punto, radio)

    def _dibujar_info_turno(self) -> None:
        """Dibuja la información del turno actual."""
        if not self.juego:
            return
        # Posición arriba a la derecha
        x_info = self.ancho - 200
        y_info = 20
        # Obtener información del jugador actual
        jugador_actual = self.juego.get_current_player()
        nombre_jugador = jugador_actual.get_name()
        color_jugador = jugador_actual.get_color()
        # Crear texto del turno
        fuente = pygame.font.Font(None, 28)
        texto_turno = f"Turno: {nombre_jugador}"
        texto_renderizado = fuente.render(texto_turno, True, self.colores["texto"])
        # Dibujar fondo para el texto
        rect_fondo = pygame.Rect(
            x_info - 10, y_info - 5,
            texto_renderizado.get_width() + 20, texto_renderizado.get_height() + 10
        )
        pygame.draw.rect(
            self.pantalla, self.colores["punto_claro"], rect_fondo, border_radius=5
        )
        pygame.draw.rect(
            self.pantalla, self.colores["borde"], rect_fondo, 2, border_radius=5
        )
        # Dibujar el texto
        self.pantalla.blit(texto_renderizado, (x_info, y_info))
        # Dibujar indicador de color del jugador
        radio_indicator = 8
        if color_jugador == "white":
            color_ficha = self.colores["ficha_blanca"]
        else:
            color_ficha = self.colores["ficha_negra"]
        centro_y = y_info + texto_renderizado.get_height() // 2
        pygame.draw.circle(
            self.pantalla, color_ficha, (x_info - 15, centro_y), radio_indicator
        )
        pygame.draw.circle(
            self.pantalla, self.colores["borde"], (x_info - 15, centro_y),
            radio_indicator, 2
        )

    def _dibujar_victoria(self) -> None:
        """Dibuja el mensaje de victoria cuando el juego termina."""
        if not self.juego:
            return

        ganador = self.juego.get_winner()
        if not ganador:
            return

        # Centro del tablero (no de toda la pantalla para evitar tapar el botón)
        x_centro = self.x_tablero + self.ancho_tablero // 2
        # Posicionar un poco más arriba para no tapar el botón que está en el centro vertical
        y_centro = self.y_tablero + self.alto_tablero // 3

        # Crear mensaje de victoria (tamaño más compacto)
        fuente_grande = pygame.font.Font(None, 42)
        fuente_pequena = pygame.font.Font(None, 28)

        nombre_ganador = ganador.get_name()
        color_ganador = ganador.get_color()
        if color_ganador == "white":
            color_ficha = self.colores["ficha_blanca"]
        else:
            color_ficha = self.colores["ficha_negra"]

        texto_victoria = f"¡{nombre_ganador} GANA!"
        texto_renderizado = fuente_grande.render(texto_victoria, True, (255, 215, 0))

        # Dibujar texto de derrota para el otro jugador
        if ganador == self.juego.get_player2():
            jugador_perdedor = self.juego.get_player1()
        else:
            jugador_perdedor = self.juego.get_player2()
        nombre_perdedor = jugador_perdedor.get_name()
        texto_perdedor = f"{nombre_perdedor} ha perdido"
        texto_perdedor_renderizado = fuente_pequena.render(
            texto_perdedor, True, self.colores["texto"]
        )

        # Calcular dimensiones del panel (más compacto)
        ancho_panel = max(
            texto_renderizado.get_width(), texto_perdedor_renderizado.get_width()
        ) + 50
        alto_panel = texto_renderizado.get_height() + texto_perdedor_renderizado.get_height() + 60

        x_panel = x_centro - ancho_panel // 2
        y_panel = y_centro - alto_panel // 2

        # Verificar que no tape el botón
        # (que está en y: self.y_tablero + self.alto_tablero // 2 - 25)
        boton_y_top = self.y_tablero + self.alto_tablero // 2 - 25
        panel_y_bottom = y_panel + alto_panel

        # Si el panel está cerca del botón, moverlo más arriba
        if panel_y_bottom > boton_y_top - 10:
            y_panel = boton_y_top - alto_panel - 20

        # Dibujar fondo del panel con semi-transparencia (simulado con color más claro)
        pygame.draw.rect(
            self.pantalla, (250, 240, 210),
            (x_panel, y_panel, ancho_panel, alto_panel), border_radius=12
        )
        pygame.draw.rect(
            self.pantalla, self.colores["borde"],
            (x_panel, y_panel, ancho_panel, alto_panel), 3, border_radius=12
        )

        # Dibujar texto de victoria
        x_texto_victoria = x_centro - texto_renderizado.get_width() // 2
        y_texto_victoria = y_panel + 20
        self.pantalla.blit(texto_renderizado, (x_texto_victoria, y_texto_victoria))

        # Dibujar círculo con el color del ganador
        radio_ganador = 18
        y_circulo = y_texto_victoria + texto_renderizado.get_height() + 15
        pygame.draw.circle(
            self.pantalla, color_ficha, (x_centro, y_circulo), radio_ganador
        )
        pygame.draw.circle(
            self.pantalla, self.colores["borde"], (x_centro, y_circulo),
            radio_ganador, 2
        )

        # Dibujar texto de derrota
        x_texto_perdedor = x_centro - texto_perdedor_renderizado.get_width() // 2
        y_texto_perdedor = y_texto_victoria + texto_renderizado.get_height() + 40
        self.pantalla.blit(texto_perdedor_renderizado, (x_texto_perdedor, y_texto_perdedor))

    def establecer_juego(self, juego: BackgammonGame) -> None:
        """Vincula una instancia del juego lógico al tablero."""
        self.juego = juego
        self.actualizar_desde_juego()

    def actualizar_desde_juego(self) -> None:
        """Refresca el estado visual según la lógica del juego."""
        if not self.juego:
            return
        if self.juego.has_dice_been_rolled():
            self.dados = self.juego.get_last_dice_roll()
        else:
            self.dados = None
            self.seleccionado = None  # Limpiar selección cuando cambia el turno

    def _tiene_reingreso_disponible(self) -> bool:
        """Devuelve True si el jugador actual puede reingresar desde la barra
        con los dados actuales."""
        if not self.juego:
            return False
        jugador_actual = self.juego.get_current_player()
        color_jugador = jugador_actual.get_color()
        board = self.juego.get_board()
        # Debe tener fichas en barra
        if not board.bar[color_jugador]:
            return False
        dados_disponibles = self.juego.get_last_dice_roll()
        if not dados_disponibles:
            return False
        # Manejar tuplas de cualquier longitud (dobles tienen 4 elementos)
        if len(dados_disponibles) >= 1:
            # Dobles: (2,2,2,2) o normales: (2,5) o parcial: (2,)
            valores_dados = list(dados_disponibles)
        else:
            valores_dados = []
        puntos_validos = []
        for valor_dado in valores_dados:
            if color_jugador == "white":
                punto_destino = valor_dado
                if punto_destino < 1 or punto_destino > 6:
                    continue
            else:
                punto_destino = 25 - valor_dado
                if punto_destino < 19 or punto_destino > 24:
                    continue
            idx = punto_destino - 1
            if board.points[idx]:
                primera = board.points[idx][0]
                if primera.get_owner() != jugador_actual and len(board.points[idx]) > 1:
                    continue
            puntos_validos.append(idx)
        return len(puntos_validos) > 0

    def manejar_eventos(self, evento: pygame.event.Event) -> None:
        """Controla los clics en el tablero y el botón."""
        # No procesar eventos si el juego ha terminado
        if self.juego and self.juego.is_finished():
            return

        if self.boton_dados.manejar_evento(evento):
            if self.juego and not self.juego.has_dice_been_rolled():
                self.juego.roll_dice()
                self.actualizar_desde_juego()
                # Verificar si hay movimientos disponibles, si no, pasar turno
                if self.juego.has_dice_been_rolled():
                    movimientos_disponibles = self.juego.get_available_moves()
                    # También verificar si tiene fichas en barra y puede reingresar
                    tiene_reingreso = self._tiene_reingreso_disponible()
                    if not movimientos_disponibles and not tiene_reingreso:
                        # No hay movimientos disponibles, pasar turno automáticamente
                        self.juego.end_turn()
                        self.actualizar_desde_juego()
                return

        if evento.type == 1025 and evento.button == 1:  # MOUSEBUTTONDOWN
            x, y = evento.pos
            if self._es_clic_en_barra(x, y):
                if self.seleccionado is None:
                    # Si no hay reingresos posibles, perder turno
                    if not self._tiene_reingreso_disponible():
                        self.juego.end_turn()
                        self.actualizar_desde_juego()
                        return
                    self.seleccionado = -1
                else:
                    punto_clicado = self._obtener_punto_clicado(x, y)
                    if punto_clicado is not None:
                        if self.juego.make_move_from_bar(punto_clicado + 1):
                            self.actualizar_desde_juego()
                        else:
                            # Solo perder turno si no hay ningún reingreso posible
                            if not self._tiene_reingreso_disponible():
                                self.juego.end_turn()
                                self.actualizar_desde_juego()
                    self.seleccionado = None
                return

            # Verificar PRIMERO si el clic es en bear off (cuando hay una ficha seleccionada)
            if self.seleccionado is not None and self.seleccionado != -1:
                if self._es_clic_en_bear_off(x, y):
                    color = self.juego.get_current_player().get_color()
                    bear_destino = 25 if color == "white" else 0
                    from_point = self.seleccionado + 1
                    # Validar antes de intentar el movimiento
                    if self.juego.is_valid_move(from_point, bear_destino):
                        if self.juego.make_move(from_point, bear_destino):
                            self.actualizar_desde_juego()
                        # Si el movimiento falló pero era válido, podría ser un error
                    self.seleccionado = None
                    return

            punto_clicado = self._obtener_punto_clicado(x, y)
            if punto_clicado is not None:
                if self.seleccionado is None:
                    if self._puede_seleccionar_punto(punto_clicado):
                        self.seleccionado = punto_clicado
                elif self.seleccionado == -1:
                    if self.juego.make_move_from_bar(punto_clicado + 1):
                        self.actualizar_desde_juego()
                    else:
                        if not self._tiene_reingreso_disponible():
                            self.juego.end_turn()
                            self.actualizar_desde_juego()
                    self.seleccionado = None
                else:
                    # Movimiento normal en el tablero
                    if self.juego.is_valid_move(self.seleccionado + 1, punto_clicado + 1):
                        if self.juego.make_move(self.seleccionado + 1, punto_clicado + 1):
                            self.actualizar_desde_juego()
                    # Nota: no saltamos turno en invalidaciones normales
                    self.seleccionado = None

    def _obtener_punto_clicado(self, x: int, y: int) -> Optional[int]:
        """Determina qué punto del tablero fue clicado."""
        if x < self.x_tablero or x > self.x_tablero + self.ancho_tablero:
            return None

        # Determinar si está en la mitad superior o inferior
        mitad_superior = y < self.y_tablero + self.alto_tablero // 2

        # Calcular el índice del punto
        x_rel = x - self.x_tablero
        if x_rel > self.ancho_mitad + self.ancho_centro:
            # Lado derecho del tablero
            x_rel -= (self.ancho_mitad + self.ancho_centro)
            punto = x_rel // self.ancho_punto
            if mitad_superior:
                return 18 + punto if punto < 6 else None
            return 5 - punto if punto < 6 else None
        elif x_rel < self.ancho_mitad:
            # Lado izquierdo del tablero
            punto = x_rel // self.ancho_punto
            if mitad_superior:
                return 12 + punto if punto < 6 else None
            return 11 - punto if punto < 6 else None
        return None

    def _es_clic_en_bear_off(self, x: int, y: int) -> bool:
        """Verifica si el clic fue en la zona de bear off."""
        if not self.juego:
            return False
        # Verificar si está dentro del área de bear off
        # (hacer el área más amplia para facilitar el clic)
        if self.x_bear <= x <= self.x_bear + self.ancho_bear:
            if self.y_bear <= y <= self.y_bear + self.alto_tablero:
                jugador_actual = self.juego.get_current_player()
                color = jugador_actual.get_color()

                # Calcular áreas más grandes para facilitar el clic
                # Para blancas: zona superior (hasta el punto medio del área de bear off)
                # Para negras: zona inferior (desde el punto medio del área de bear off)
                mitad_y = self.y_bear + self.alto_tablero // 2

                if color == "white":
                    # Área ampliada: desde el inicio hasta un poco más allá de la mitad
                    # para incluir el círculo verde que está en y_bear + alto_tablero // 4
                    return y <= mitad_y + 50  # Extender un poco más abajo
                else:
                    # Área ampliada: desde un poco antes de la mitad hacia abajo
                    return y >= mitad_y - 50  # Extender un poco más arriba
        return False

    def _es_clic_en_barra(self, x: int, y: int) -> bool:
        """Verifica si el clic fue en la barra central."""
        if not self.juego:
            return False

        # Verificar si el jugador actual tiene fichas en la barra
        jugador_actual = self.juego.get_current_player()
        color_jugador = jugador_actual.get_color()
        board = self.juego.get_board()

        if not board.bar[color_jugador]:
            return False

        # Verificar si el clic está en el área de la barra
        barra_x_centro = self.x_tablero + self.ancho_tablero // 2
        barra_y_centro = self.y_tablero + self.alto_tablero // 2

        # Área de clic en la barra (más amplia para facilitar el clic)
        area_clic = 50

        return (abs(x - barra_x_centro) < area_clic and
                abs(y - barra_y_centro) < area_clic)

    def _puede_seleccionar_punto(self, punto_idx: int) -> bool:
        """Verifica si el punto puede ser seleccionado por el jugador actual."""
        if not self.juego:
            return False

        # Si el jugador tiene fichas en la barra, debe moverlas primero
        jugador_actual = self.juego.get_current_player()
        color_jugador = jugador_actual.get_color()
        board = self.juego.get_board()

        if board.bar[color_jugador]:
            return False  # No puede seleccionar fichas normales si tiene fichas en la barra

        # Verificar que el punto tenga fichas
        if not board.points[punto_idx]:
            return False

        # Verificar que la primera ficha pertenezca al jugador actual
        primera_ficha = board.points[punto_idx][0]
        return primera_ficha.get_owner() == jugador_actual

    def ejecutar(self) -> None:
        """Bucle principal del tablero."""
        reloj = pygame.time.Clock()
        corriendo = True

        while corriendo:
            for evento in pygame.event.get():
                if evento.type == 256:  # QUIT
                    corriendo = False
                elif evento.type == 768 and evento.key == 27:  # KEYDOWN, K_ESCAPE
                    corriendo = False
                else:
                    self.manejar_eventos(evento)

            # Redibujar tablero
            self.dibujar_tablero()

            # Actualizar pantalla
            pygame.display.flip()
            reloj.tick(60)

        pygame.quit()  # pylint: disable=no-member


def main() -> None:
    """Ejecuta el tablero visual clásico renovado."""
    tablero = TableroBackgammon()
    juego = BackgammonGame()
    juego.setup_initial_position()
    juego.start_game()  # Iniciar el juego
    tablero.establecer_juego(juego)
    tablero.ejecutar()


if __name__ == "__main__":
    main()
