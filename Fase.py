import pygame, sys, os
from pygame.locals import *
from GestorRecursos import *
from Jugador import *
from Plataforma import *

class Fase:
    def __init__(self):

        # Habria que pasarle como parámetro el número de fase, a partir del cual se cargue
        #  un fichero donde este la configuracion de esa fase en concreto, con cosas como
        #   - Nombre del archivo con el decorado
        #   - Posiciones de las plataformas
        #   - Posiciones de los enemigos
        #   - Posiciones de inicio de los jugadores
        #  etc.
        # Y cargar esa configuracion del archivo en lugar de ponerla a mano, como aqui abajo
        # De esta forma, se podrian tener muchas fases distintas con esta clase

        # Que parte del decorado estamos visualizando
        self.scrollx = 0
        #  En ese caso solo hay scroll horizontal
        #  Si ademas lo hubiese vertical, seria self.scroll = (0, 0)
        self.decorado = Decorado()
        # Creamos los sprites de los jugadores
        self.jugador1 = Alchemist()
        self.jugador2 = Bartender()
        self.jugador3 = Merchant()
        self.grupoJugadores = pygame.sprite.Group(self.jugador1, self.jugador2, self.jugador3)

        # Ponemos a los jugadores en sus posiciones iniciales
        self.jugador1.establecerPosicion((200, 462))
        self.jugador2.establecerPosicion((200, 462))
        self.jugador3.establecerPosicion((200, 462))

        self.jugador_activo = self.jugador1

        # Cargar las coordenadas de las plataformas
        datosPlataformas = GestorRecursos.CargarCoordenadasPlataformas('coordPlataformas.txt')
        
        # Creamos las plataformas del decorado basándonos en las coordenadas cargadas
        self.grupoPlataformas = pygame.sprite.Group()
        for linea in datosPlataformas:
            x, y, ancho, alto = map(int, linea.split())
            plataforma = Plataforma(pygame.Rect(x, y, ancho, alto))
            self.grupoPlataformas.add(plataforma)

        # Inicializa los grupos de sprites como antes
        self.grupoSpritesDinamicos = pygame.sprite.Group(self.jugador_activo)  # Asumiendo que solo hay un jugador por simplicidad
        self.grupoSprites = pygame.sprite.Group(self.jugador_activo, self.grupoPlataformas)

    
    def update(self, tiempo):

        self.grupoSpritesDinamicos.update(self.grupoPlataformas, tiempo)

        return False
    
    def dibujar(self, pantalla):
        # Luego los Sprites
        self.decorado.dibujar(pantalla)
        self.grupoSprites.draw(pantalla)

    def cambiar_jugador(self):
        
        if (self.jugador_activo == self.jugador1):
            nuevo_jugador_activo = self.jugador2

        elif (self.jugador_activo == self.jugador2):
            nuevo_jugador_activo = self.jugador3

        elif (self.jugador_activo == self.jugador3):
            nuevo_jugador_activo = self.jugador1

        # Establece la posición del nuevo jugador activo a la posición del actual antes de cambiar
        nuevo_jugador_activo.establecerPosicion(self.jugador_activo.posicion)

        # Actualiza el grupo de sprites para que contenga al nuevo jugador activo
        # Primero, elimina el jugador activo actual de los grupos relevantes
        self.grupoSpritesDinamicos.remove(self.jugador_activo)
        self.grupoSprites.remove(self.jugador_activo)

        # Luego, agrega el nuevo jugador activo a los grupos
        self.grupoSpritesDinamicos.add(nuevo_jugador_activo)
        self.grupoSprites.add(nuevo_jugador_activo)

        # Finalmente, actualiza la referencia de jugador_activo al nuevo jugador
        self.jugador_activo = nuevo_jugador_activo

    def eventos(self, lista_eventos):
        # Miramos a ver si hay algun evento de salir del programa
        for evento in lista_eventos:
            # Si se sale del programa
            if evento.type == pygame.QUIT:
                return True
            elif evento.type == pygame.KEYDOWN:
                # Si la tecla presionada es TAB
                if evento.key == pygame.K_TAB:
                    self.cambiar_jugador()
                    # No necesitas continuar el bucle después de cambiar de jugador
                    continue

        # Indicamos la acción a realizar segun la tecla pulsada para cada jugador
        teclasPulsadas = pygame.key.get_pressed()
        self.jugador_activo.mover(teclasPulsadas, K_UP, K_DOWN, K_LEFT, K_RIGHT)
        
        # No se sale del programa
        return False
    

class Decorado:
    def __init__(self):
        self.imagen = GestorRecursos.CargarImagen('mapa.png', -1)
        #self.imagen = pygame.transform.scale(self.imagen, (1200, 300))

        self.rect = self.imagen.get_rect()
        self.rect.bottom = ALTO_PANTALLA

        # La subimagen que estamos viendo
        self.rectSubimagen = pygame.Rect(0, 0, ANCHO_PANTALLA, ALTO_PANTALLA)
        self.rectSubimagen.left = 0 # El scroll horizontal empieza en la posicion 0 por defecto

    def update(self, scrollx):
        self.rectSubimagen.left = scrollx

    def dibujar(self, pantalla):
        pantalla.blit(self.imagen, self.rect, self.rectSubimagen)