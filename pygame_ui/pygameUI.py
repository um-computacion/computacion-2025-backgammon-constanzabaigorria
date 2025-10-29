"""
Módulo de Interfaz Visual de Backgammon (Versión Clásica Renovada)

Este módulo genera un tablero de Backgammon con una estética clásica mejorada:
madera clara, triángulos suaves, botones modernos y texto limpio.
Incluye control de eventos de ratón y renderizado del estado del juego.
"""

import os
os.environ['PYGAME_HIDE_SUPPORT_PROMPT'] = "hide"
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
        pygame.init()  # type: ignore
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
            100,
            45,
            "Tirar Dados",
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

        # Dibujar dados si están disponibles
        if self.dados:
            self._dibujar_dados()

        # Dibujar información del turno
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
                    color_ficha = self.colores["ficha_blanca"] if ficha.get_color() == "white" else self.colores["ficha_negra"]
                    fichas_en_punto.append((ficha.get_color(), color_ficha))

            # Dibujar las fichas
            for idx, (_, color_ficha) in enumerate(fichas_en_punto):
                y = y_base + (y_dir * idx * (self.radio_ficha * 2))
                pygame.draw.circle(
                    self.pantalla,
                    color_ficha,
                    (x + self.ancho_punto // 2, y),
                    self.radio_ficha
                )
                # Dibujar borde especial si la ficha está seleccionada
                color_borde = self.colores["resaltado"] if self.seleccionado == punto else self.colores["borde"]
                grosor_borde = 4 if self.seleccionado == punto else 2
                pygame.draw.circle(
                    self.pantalla,
                    color_borde,
                    (x + self.ancho_punto // 2, y),
                    self.radio_ficha,
                    grosor_borde
                )

    def _dibujar_fichas_barra(self) -> None:
        """Dibuja las fichas en la barra."""
        if not self.juego:
            return
        board = self.juego.get_board()
        # Dibujar fichas blancas en la barra
        fichas_blancas_barra = board.bar["white"]
        for idx, ficha in enumerate(fichas_blancas_barra):
            x = self.x_tablero + self.ancho_tablero // 2 - self.radio_ficha
            y = self.y_tablero + self.alto_tablero // 2 - 20 - (idx * (self.radio_ficha * 2 + 5))
            pygame.draw.circle(
                self.pantalla,
                self.colores["ficha_blanca"],
                (x, y),
                self.radio_ficha
            )
            pygame.draw.circle(
                self.pantalla,
                self.colores["borde"],
                (x, y),
                self.radio_ficha,
                2
            )
        # Dibujar fichas negras en la barra
        fichas_negras_barra = board.bar["black"]
        for idx, ficha in enumerate(fichas_negras_barra):
            x = self.x_tablero + self.ancho_tablero // 2 + self.radio_ficha
            y = self.y_tablero + self.alto_tablero // 2 - 20 - (idx * (self.radio_ficha * 2 + 5))
            pygame.draw.circle(
                self.pantalla,
                self.colores["ficha_negra"],
                (x, y),
                self.radio_ficha
            )
            pygame.draw.circle(
                self.pantalla,
                self.colores["borde"],
                (x, y),
                self.radio_ficha,
                2
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
        # Manejar tanto tuplas de 2 elementos como de 1 elemento
        if len(dados_disponibles) == 2:
            dado1, dado2 = dados_disponibles
            valores_dados = [dado1, dado2]
        elif len(dados_disponibles) == 1:
            valores_dados = [dados_disponibles[0]]
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
            
            # Manejar tanto tuplas de 2 elementos como de 1 elemento
            if len(dados_disponibles) == 2:
                dado1, dado2 = dados_disponibles
            elif len(dados_disponibles) == 1:
                dado1 = dados_disponibles[0]
                dado2 = None
            else:
                return
                
            punto_seleccionado = self.seleccionado + 1
            
            # Calcular posibles destinos
            jugador_actual = self.juego.get_current_player()
            dados_a_procesar = [dado1]
            if dado2 is not None:
                dados_a_procesar.append(dado2)
                
            for dado in dados_a_procesar:
                # En Backgammon:
                # - Fichas blancas van hacia números más altos (1->24)
                # - Fichas negras van hacia números más bajos (24->1)
                if jugador_actual.get_color() == "white":
                    destino = punto_seleccionado + dado
                else:
                    destino = punto_seleccionado - dado
                    
                if 1 <= destino <= 24:
                    if self.juego.is_valid_move(punto_seleccionado, destino):
                        movimientos_validos.append(destino - 1)  # Convertir a índice 0-based
        
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
        """Calcula la coordenada x para un punto."""
        if punto < 12:
            return self.x_tablero + ((11 - punto) * self.ancho_punto)
        else:
            return self.x_tablero + self.ancho_tablero - self.ancho_bear - ((23 - punto) * self.ancho_punto)

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

        # Manejar tanto tuplas de 2 elementos como de 1 elemento
        if len(self.dados) == 2:
            dado1, dado2 = self.dados
        elif len(self.dados) == 1:
            dado1 = self.dados[0]
            dado2 = None
        else:
            return
            
        x_base = self.x_tablero + self.ancho_tablero // 2 - 50
        y_base = self.y_tablero + self.alto_tablero // 2 - 25
        lado = 40

        # Dibujar los dados
        dados_a_dibujar = [dado1]
        if dado2 is not None:
            dados_a_dibujar.append(dado2)
            
        for i, valor in enumerate(dados_a_dibujar):
            x = x_base + i * 60
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
        rect_fondo = pygame.Rect(x_info - 10, y_info - 5, texto_renderizado.get_width() + 20, texto_renderizado.get_height() + 10)
        pygame.draw.rect(self.pantalla, self.colores["punto_claro"], rect_fondo, border_radius=5)
        pygame.draw.rect(self.pantalla, self.colores["borde"], rect_fondo, 2, border_radius=5)
        
        # Dibujar el texto
        self.pantalla.blit(texto_renderizado, (x_info, y_info))
        
        # Dibujar indicador de color del jugador
        radio_indicator = 8
        color_ficha = self.colores["ficha_blanca"] if color_jugador == "white" else self.colores["ficha_negra"]
        pygame.draw.circle(self.pantalla, color_ficha, (x_info - 15, y_info + texto_renderizado.get_height() // 2), radio_indicator)
        pygame.draw.circle(self.pantalla, self.colores["borde"], (x_info - 15, y_info + texto_renderizado.get_height() // 2), radio_indicator, 2)

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

    def manejar_eventos(self, evento: pygame.event.Event) -> None:
        """Controla los clics en el tablero y el botón."""
        if self.boton_dados.manejar_evento(evento):
            if self.juego and not self.juego.has_dice_been_rolled():
                self.juego.roll_dice()
                self.actualizar_desde_juego()
                return

        if evento.type == 1025 and evento.button == 1:  # MOUSEBUTTONDOWN
            x, y = evento.pos
            
            # Verificar si se hizo clic en la barra
            if self._es_clic_en_barra(x, y):
                # Cuando se hace clic en la barra, necesitamos esperar el segundo clic para el destino
                if self.seleccionado is None:
                    # Marcar que estamos seleccionando desde la barra
                    self.seleccionado = -1  # Usar -1 para indicar selección desde barra
                else:
                    # Ya tenemos la barra seleccionada, ahora obtener el destino
                    punto_clicado = self._obtener_punto_clicado(x, y)
                    if punto_clicado is not None:
                        # Intentar mover desde la barra
                        if self.juego.make_move_from_bar(punto_clicado + 1):
                            self.actualizar_desde_juego()
                    self.seleccionado = None
                return
            
            punto_clicado = self._obtener_punto_clicado(x, y)
            if punto_clicado is not None:
                if self.seleccionado is None:
                    # Solo permitir seleccionar fichas del jugador actual
                    if self._puede_seleccionar_punto(punto_clicado):
                        self.seleccionado = punto_clicado
                elif self.seleccionado == -1:
                    # Tenemos la barra seleccionada, intentar mover desde la barra
                    if self.juego.make_move_from_bar(punto_clicado + 1):
                        self.actualizar_desde_juego()
                    self.seleccionado = None
                else:
                    # Intentar mover la ficha normal
                    if self.juego.is_valid_move(self.seleccionado + 1, punto_clicado + 1):
                        if self.juego.make_move(self.seleccionado + 1, punto_clicado + 1):
                            self.actualizar_desde_juego()
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

        pygame.quit()  # type: ignore


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
