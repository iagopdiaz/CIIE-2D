import pygame, sys, os
from pygame.locals import *
from gestor_recursos import *
from gestor_sonido import GestorSonido
from jugador import *
from escena import *
from partitura import *
from interfaz_usuario import InterfazUsuario

class Fase(Escena):
    def __init__(self, director):
        Escena.__init__(self, director)
        #self.nivel = 1
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
        self.scrolly = 0
        #  En ese caso solo hay scroll horizontal
        #  Si ademas lo hubiese vertical, seria self.scroll = (0, 0)
        self.decorado = Decorado()
        self.muros = Muros()
        self.interfazUsuario = InterfazUsuario()
        # Creamos los sprites de los jugadores
        self.jugador1 = Alchemist()
        self.jugador2 = Bartender()
        self.jugador3 = Merchant()
        #Definir los 3 jugadores con sus observadores 
        
        self.grupoJugadores = pygame.sprite.Group(self.jugador1, self.jugador2, self.jugador3)

        # Cargamos las coordenadas donde se encuentran las partituras
        datosPartituras = GestorRecursos.CargarArchivoCoordenadasPartituras('mapa/coordPartituras.txt')

        # Creamos los sprites de las partituras
        self.grupoPartituras = pygame.sprite.Group()

        # Grupo con los nombres
        nombres_partituras = ["Melodía de la Vida", "Arpegio de la Aurora", "Sinfonía del Silencio", "Rapsodia del Resplandor", "Concierto de los Cóndores", "Preludio de la Perdición", "Sonata del Susurro", "Interludio de la Ilusión", "Nocturno de la Niebla", "Fantasía de la Frontera"]

        # Creamos cada partitura individualmente con su respectiva coordenada
        for i, coords in enumerate(datosPartituras, start=1):
            x, y = map(int, coords.split())
            partitura = Partitura(i, f"partitura{i}.png", nombres_partituras[i-1]) #AQUI TIENEN QUE SER DIFERENTES IMAGENES - CORREGIR
            partitura.establecerPosicion((x, y))
            self.grupoPartituras.add(partitura)

        # Ponemos a los jugadores en sus posiciones iniciales
        self.jugador1.establecerPosicion((255, 530))

        self.jugador_activo = self.jugador1

        datosPlataformas = GestorRecursos.CargarCoordenadasPlataformas('coordPlataformas.txt')
        
        # Creamos las plataformas del decorado basándonos en las coordenadas cargadas
        self.grupoPlataformas = pygame.sprite.Group()
        for linea in datosPlataformas:
            x, y, ancho, alto = map(int, linea.split())
            plataforma = Plataforma(pygame.Rect(x, y, ancho, alto))
            self.grupoPlataformas.add(plataforma)

        # Inicializa los grupos de sprites como antes
        self.grupoSpritesDinamicos = pygame.sprite.Group(self.jugador_activo)  # Asumiendo que solo hay un jugador por simplicidad
        self.grupoSprites = pygame.sprite.Group(self.jugador_activo, self.grupoPlataformas, self.grupoPartituras)
    
    def update(self, tiempo):

        self.grupoSpritesDinamicos.update(self.grupoPlataformas, self.grupoPartituras, tiempo)
        self.actualizarScroll()

        return False

    def actualizarScroll(self):
        # Definimos el límite para el scroll como los 3/4 de la pantalla
        LIMITE_SCROLL_X = ANCHO_PANTALLA * 3 / 4
        LIMITE_SCROLL_Y = ALTO_PANTALLA * 3 / 4


        # Si el jugador se encuentra más allá del límite de la pantalla en el eje X
        if self.jugador_activo.rect.right > LIMITE_SCROLL_X:
            # Calculamos cuántos píxeles está fuera del límite
            desplazamiento_x = self.jugador_activo.rect.right - LIMITE_SCROLL_X
            # Actualizamos el scroll en el eje X
            self.scrollx = min(self.scrollx + desplazamiento_x, self.decorado.imagen.get_width() - ANCHO_PANTALLA)
        elif self.jugador_activo.rect.left < ANCHO_PANTALLA - LIMITE_SCROLL_X:
            desplazamiento_x = ANCHO_PANTALLA - LIMITE_SCROLL_X - self.jugador_activo.rect.left
            self.scrollx = max(0, self.scrollx - desplazamiento_x)

        # Si el jugador se encuentra más allá del límite de la pantalla en el eje Y
        if self.jugador_activo.rect.bottom > LIMITE_SCROLL_Y:
            # Calculamos cuántos píxeles está fuera del límite
            desplazamiento_y = self.jugador_activo.rect.bottom - LIMITE_SCROLL_Y
            # Actualizamos el scroll en el eje Y
            self.scrolly = min(self.scrolly + desplazamiento_y, self.decorado.imagen.get_height() - ALTO_PANTALLA)
        elif self.jugador_activo.rect.top < ALTO_PANTALLA - LIMITE_SCROLL_Y:
            desplazamiento_y = ALTO_PANTALLA - LIMITE_SCROLL_Y - self.jugador_activo.rect.top
            self.scrolly = max(0, self.scrolly - desplazamiento_y)


        # Actualizamos la posición en pantalla de todos los Sprites según el scroll actual
        for sprite in iter(self.grupoSprites):
            sprite.establecerPosicionPantalla((self.scrollx, self.scrolly))

        # Además, actualizamos el decorado para que se muestre una parte distinta
        self.decorado.update(self.scrollx, self.scrolly)
        self.muros.update(self.scrollx, self.scrolly)



    def dibujar(self, pantalla):
        # Luego los Sprites
        self.decorado.dibujar(pantalla)
        self.muros.dibujar(pantalla)
        self.grupoSprites.draw(pantalla)
        self.interfazUsuario.dibujar(pantalla)

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

            elif evento.type == pygame.MOUSEBUTTONDOWN:
                if evento.button == 1:  # Botón izquierdo del ratón
                # Ajustar las posiciones iniciales con el desplazamiento actual
                    self.start_pos = (evento.pos[0] + self.scrollx, evento.pos[1] + self.scrolly)
            elif evento.type == pygame.MOUSEBUTTONUP:
                if evento.button == 1:  # Botón izquierdo del ratón
                    # Ajustar las posiciones finales con el desplazamiento actual
                    self.end_pos = (evento.pos[0] + self.scrollx, evento.pos[1] + self.scrolly)
                    # Calcula las coordenadas y dimensiones del rectángulo ajustadas al desplazamiento
                    x = min(self.start_pos[0], self.end_pos[0])
                    y = min(self.start_pos[1], self.end_pos[1])
                    ancho = abs(self.start_pos[0] - self.end_pos[0])
                    alto = abs(self.start_pos[1] - self.end_pos[1])
                    print(f'x: {x}, y: {y}, ancho: {ancho}, alto: {alto}')
                    with open('./imagenes/mapa/coordPlataformas.txt', 'a') as archivo:
                        archivo.write(f'{int(x)} {int(y)} {int(ancho)} {int(alto)}\n')

        # Indicamos la acción a realizar segun la tecla pulsada para cada jugador
        teclasPulsadas = pygame.key.get_pressed()
        self.jugador_activo.mover(teclasPulsadas, K_UP, K_DOWN, K_LEFT, K_RIGHT)
        
        # No se sale del programa
        return False

    def encender_musica(self):
        GestorSonido.musica_nivel_1()

class Plataforma(MiSprite):
    def __init__(self,rectangulo):
        # Primero invocamos al constructor de la clase padre
        MiSprite.__init__(self)
        # Rectangulo con las coordenadas en pantalla que ocupara
        self.rect = rectangulo
        # Y lo situamos de forma global en esas coordenadas
        self.establecerPosicion((self.rect.left, self.rect.bottom))
        # En el caso particular de este juego, las plataformas no se van a ver, asi que no se carga ninguna imagen
        self.image = pygame.Surface((0, 0))

class Muros:
    def __init__(self):
        self.imagen = GestorRecursos.CargarImagen('mapa/mapa1paredes.png', -1)
       
        self.rect = self.imagen.get_rect()
        
        # La subimagen que estamos viendo
        self.rectSubimagen = pygame.Rect(0, 0, ANCHO_PANTALLA, ALTO_PANTALLA)
        self.rectSubimagen.left = 0 # El scroll horizontal empieza en la posicion 0 por defecto
        self.rectSubimagen.top = 0

    def update(self, scrollx, scrolly):
        # Asegúrate de que scrollx no sea menor que 0 ni mayor que la anchura de la imagen menos la anchura de la pantalla
        self.rectSubimagen.left = max(0, min(scrollx, self.imagen.get_width() - ANCHO_PANTALLA))
        # Asegúrate de que scrolly no sea menor que 0 ni mayor que la altura de la imagen menos la altura de la pantalla
        self.rectSubimagen.top = max(0, min(scrolly, self.imagen.get_height() - ALTO_PANTALLA))

    def dibujar(self, pantalla):
        pantalla.blit(self.imagen, self.rect, self.rectSubimagen)

class Decorado:
    def __init__(self):
        self.imagen = GestorRecursos.CargarImagen('mapa/mapa1decorado.png')

        self.rect = self.imagen.get_rect()
        
        # La subimagen que estamos viendo
        self.rectSubimagen = pygame.Rect(0, 0, ANCHO_PANTALLA, ALTO_PANTALLA)
        self.rectSubimagen.left = 0 # El scroll horizontal empieza en la posicion 0 por defecto
        self.rectSubimagen.top = 0

    def update(self, scrollx, scrolly):
        # Asegúrate de que scrollx no sea menor que 0 ni mayor que la anchura de la imagen menos la anchura de la pantalla
        self.rectSubimagen.left = max(0, min(scrollx, self.imagen.get_width() - ANCHO_PANTALLA))
        # Asegúrate de que scrolly no sea menor que 0 ni mayor que la altura de la imagen menos la altura de la pantalla
        self.rectSubimagen.top = max(0, min(scrolly, self.imagen.get_height() - ALTO_PANTALLA))

    def dibujar(self, pantalla):
        pantalla.blit(self.imagen, self.rect, self.rectSubimagen)
