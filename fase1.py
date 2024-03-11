import pygame, sys, os
from pygame.locals import *
from gestor_recursos import *
from gestor_sonido import GestorSonido
from jugador import *
from escena import *
from partitura import *
from interfaz_usuario import InterfazUsuario
from puerta import *
from meta_fase import *
from fase2 import *

class Fase1(Escena):
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
        self.interfazUsuario = InterfazUsuario()
        # Creamos los sprites de los jugadores
        self.jugador1 = PrimerPersonaje()
        self.jugador2 = SegundoPersonaje()
        self.jugador3 = TercerPersonaje()
        #Definir los 3 jugadores con sus observadores 
        
        self.grupoJugadores = pygame.sprite.Group(self.jugador1, self.jugador2, self.jugador3)


        # Ponemos a los jugadores en sus posiciones iniciales
        self.jugador1.establecerPosicion((255, 530))

        # Establecemos el jugador activo como el jugador1
        self.jugador_activo = self.jugador1


        # Creamos las plataformas del decorado basándonos en las coordenadas cargadas
        datosPlataformas = GestorRecursos.CargarCoordenadasPlataformas('coordParedes1.txt')
        
        self.grupoPlataformas = pygame.sprite.Group()
        for linea in datosPlataformas:
            x, y, ancho, alto = map(int, linea.split())
            plataforma = Plataforma(pygame.Rect(x, y, ancho, alto))
            self.grupoPlataformas.add(plataforma)



        # Creamos las partituras del decorado basándonos en las coordenadas cargadas
        datosPartituras = GestorRecursos.CargarPartituras('coordPartituras.txt')

        self.grupoPartituras = pygame.sprite.Group()
        for i, datos in enumerate(datosPartituras, start=1):
            x, y = map(int, datos['coords'].split())
            partitura = Partitura(f"partitura{i}.png", datos['nombre'], datos['jugador'])
            partitura.establecerPosicion((x, y))
            self.grupoPartituras.add(partitura)

        meta = MetaFase(5115, 188, 'metaHorizontal.png')

        # Creamos las puertas del decorado basándonos en las coordenadas cargadas
        datosPuertas = GestorRecursos.CargarPuertas('coordPuertas.txt')

        self.grupoPuertas = pygame.sprite.Group()

        for i, datos in enumerate(datosPuertas, start=1):
            # Obtenemos las coordenadas de la foto de la puerta
            x_foto, y_foto = map(int, datos['coords_foto'].split())
            # Obtenemos las coordenadas y dimensiones del área de activación de la puerta
            x_area, y_area, ancho, alto = map(int, datos['coords_area'].split())
            # Creamos la puerta y establecemos su posición y área de activación
            puerta = Puerta(datos['nombre'], f"BossDoor.png", pygame.Rect(x_area, y_area, ancho, alto))
            puerta.establecerPosicion((x_foto, y_foto))
            self.grupoPuertas.add(puerta)

        # Inicializa los grupos de sprites como antes
        self.grupoSpritesDinamicos = pygame.sprite.Group(self.jugador_activo, self.grupoPuertas)  # Asumiendo que solo hay un jugador por simplicidad
        self.grupoSprites = pygame.sprite.Group(self.jugador_activo, self.grupoPlataformas, self.grupoPartituras, self.grupoPuertas, meta)
        self.metaSprites = pygame.sprite.Group(meta)

    def update(self, tiempo):

        self.grupoSpritesDinamicos.update(self.grupoPlataformas, self.grupoPartituras, self.grupoPuertas, tiempo)
        self.actualizarScroll()

        # Comprueba si el jugador ha llegado a la meta
        if pygame.sprite.groupcollide(self.grupoJugadores, self.metaSprites, False, False) != {}:
            self.director.cambiarEscena(Fase2(self.director))

        return False

    def actualizarScroll(self):
        # Definimos el límite para el scroll como los 3/4 de la pantalla
        LIMITE_SCROLL_X = ANCHO_PANTALLA * 3 / 4
        LIMITE_SCROLL_Y = ALTO_PANTALLA * 3 / 4

        ##COMO NO TIENEN TODOS LOS SPRITES EL MISMO TAMAÑO, VAMOS A COGER SIEMPRE LA MISMA MEDIDA
        #Esta puesto 25 como ejemplo de la media de tamaño de los personajes hacia el centro
        posicion_x = self.jugador_activo.rect.left+25
        posicion_y = self.jugador_activo.rect.top+25

        if posicion_x > LIMITE_SCROLL_X:
            # Calculamos cuántos píxeles está fuera del límite
            desplazamiento_x = posicion_x - LIMITE_SCROLL_X
            # Actualizamos el scroll en el eje X
            self.scrollx = min(self.scrollx + desplazamiento_x, self.decorado.imagen.get_width() - ANCHO_PANTALLA)
        elif posicion_x < ANCHO_PANTALLA - LIMITE_SCROLL_X:
            desplazamiento_x = ANCHO_PANTALLA - LIMITE_SCROLL_X - posicion_x
            self.scrollx = max(0, self.scrollx - desplazamiento_x)

        # Si el jugador se encuentra más allá del límite de la pantalla en el eje Y
        if posicion_y > LIMITE_SCROLL_Y:
            # Calculamos cuántos píxeles está fuera del límite
            desplazamiento_y = posicion_y - LIMITE_SCROLL_Y
            # Actualizamos el scroll en el eje Y
            self.scrolly = min(self.scrolly + desplazamiento_y, self.decorado.imagen.get_height() - ALTO_PANTALLA)
        elif posicion_y < ALTO_PANTALLA - LIMITE_SCROLL_Y:
            desplazamiento_y = ALTO_PANTALLA - LIMITE_SCROLL_Y - posicion_y
            self.scrolly = max(0, self.scrolly - desplazamiento_y)
            


        # Actualizamos la posición en pantalla de todos los Sprites según el scroll actual
        for sprite in iter(self.grupoSprites):
            sprite.establecerPosicionPantalla((self.scrollx, self.scrolly))

        #print(f'scrollx: {self.scrollx}, scrolly: {self.scrolly}, posicion_x: {posicion_x}, posicion_y: {posicion_y}')
        # Además, actualizamos el decorado para que se muestre una parte distinta
        self.decorado.update(self.scrollx, self.scrolly)



    def dibujar(self, pantalla):
        # Luego los Sprites
        self.decorado.dibujar(pantalla)
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

        #Creamos un rectangulo con la futura posicion del jugador
        futuro_rect = pygame.Rect(nuevo_jugador_activo.posicion[0]-self.scrollx, nuevo_jugador_activo.posicion[1]-self.scrolly, nuevo_jugador_activo.rect.width, nuevo_jugador_activo.rect.height)

        #Calcular posicion futura del jugador activo, solo permitir el cambio si no hay colision con pared o puerta
        if nuevo_jugador_activo.puede_moverse(futuro_rect, self.grupoPlataformas, self.grupoPuertas):
            # Actualiza el grupo de sprites para que contenga al nuevo jugador activo
            # Primero, elimina el jugador activo actual de los grupos relevantes
            self.grupoSpritesDinamicos.remove(self.jugador_activo)
            self.grupoSprites.remove(self.jugador_activo)

            # Luego, agrega el nuevo jugador activo a los grupos
            self.grupoSpritesDinamicos.add(nuevo_jugador_activo)
            self.grupoSprites.add(nuevo_jugador_activo)

            # Finalmente, actualiza la referencia de jugador_activo al nuevo jugador
            self.jugador_activo = nuevo_jugador_activo
        else:
            print("No se puede cambiar de jugador en esta posicion")

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
                elif evento.key == pygame.K_t:
                    self.jugador_activo.tocar()
                elif evento.key == pygame.K_p:
                    print(self.jugador_activo.posicion)
                elif evento.key == pygame.K_e:
                    self.jugador_activo.escuchar()
                elif evento.key == pygame.K_s:
                    self.jugador_activo.soltar_partitura()

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
                    with open('./imagenes/mapa/coordParedes1.txt', 'a') as archivo:
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
        self.establecerPosicion((self.rect.left, self.rect.top))
        # En el caso particular de este juego, las plataformas no se van a ver, asi que no se carga ninguna imagen
        self.image = pygame.Surface((0, 0))

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
