import pygame, sys, os
from pygame.locals import *
from gestor_recursos import *
from settings import *
from misprite import *


class Personaje(MiSprite):
    "Cualquier personaje del juego"

    # Parametros pasados al constructor de esta clase:
    #  Archivo con la hoja de Sprites
    #  Archivo con las coordenadoas dentro de la hoja
    #  Numero de imagenes en cada postura
    #  Velocidad de caminar y de salto
    #  Retardo para mostrar la animacion del personaje
    
    def __init__(self, archivoImagen, archivoCoordenadas, numImagenes, velocidadCarrera, velocidadSalto, retardoAnimacion):

        # Primero invocamos al constructor de la clase padre
        MiSprite.__init__(self)

        # Se carga la hoja
        self.hoja = GestorRecursos.CargarImagen(archivoImagen, -1)

        self.hoja = self.hoja.convert_alpha()
        # El movimiento que esta realizando
        self.movimiento = QUIETO
        # Lado hacia el que esta mirando
        self.mirando = IZQUIERDA

        # Leemos las coordenadas de un archivo de texto
        datos = GestorRecursos.CargarArchivoCoordenadas(archivoCoordenadas)
        datos = datos.split()
        self.numPostura = 1
        self.numImagenPostura = 0
        cont = 0
        self.coordenadasHoja = []
        for linea in range(0, 8):
            self.coordenadasHoja.append([])
            tmp = self.coordenadasHoja[linea]
            for postura in range(1, numImagenes[linea]+1):
                tmp.append(pygame.Rect((int(datos[cont]), int(datos[cont+1])), (int(datos[cont+2]), int(datos[cont+3]))))
                cont += 4

        # El retardo a la hora de cambiar la imagen del Sprite (para que no se mueva demasiado rápido)
        self.retardoMovimiento = 0

        # En que postura esta inicialmente
        self.numPostura = QUIETO

        # El rectangulo del Sprite
        self.rect = pygame.Rect(100,100,self.coordenadasHoja[self.numPostura][self.numImagenPostura][2],self.coordenadasHoja[self.numPostura][self.numImagenPostura][3])

        # Las velocidades de caminar y salto
        self.velocidadCarrera = velocidadCarrera
        self.velocidadSalto = velocidadSalto

        # El retardo en la animacion del personaje (podria y deberia ser distinto para cada postura)
        self.retardoAnimacion = retardoAnimacion

        # Y actualizamos la postura del Sprite inicial, llamando al metodo correspondiente
        self.actualizarPostura()


    # Metodo base para realizar el movimiento: simplemente se le indica cual va a hacer, y lo almacena
    def mover(self, movimiento):
        self.movimiento = movimiento

    def actualizarPostura(self):
        self.retardoMovimiento -= 1
        # Miramos si ha pasado el retardo para dibujar una nueva postura
        if (self.retardoMovimiento < 0):
            self.retardoMovimiento = self.retardoAnimacion
            # Si ha pasado, actualizamos la postura
            self.numImagenPostura += 1
            if self.numImagenPostura >= len(self.coordenadasHoja[self.numPostura]):
                self.numImagenPostura = 0
            if self.numImagenPostura < 0:
                self.numImagenPostura = len(self.coordenadasHoja[self.numPostura])-1
            self.image = self.hoja.subsurface(self.coordenadasHoja[self.numPostura][self.numImagenPostura])

            # Si esta mirando a la izquiera, cogemos la porcion de la hoja
            if self.mirando == IZQUIERDA:
                self.image = self.hoja.subsurface(self.coordenadasHoja[self.numPostura][self.numImagenPostura])
            #  Si no, si mira a la derecha, invertimos esa imagen
            elif self.mirando == DERECHA:
                self.image = self.hoja.subsurface(self.coordenadasHoja[self.numPostura][self.numImagenPostura])

            elif self.mirando == ARRIBA:
                self.image = self.hoja.subsurface(self.coordenadasHoja[self.numPostura][self.numImagenPostura])

            elif self.mirando == ABAJO:
                self.image = self.hoja.subsurface(self.coordenadasHoja[self.numPostura][self.numImagenPostura])

    
    def recoger_partitura(self, partitura):
        if self.inventario:  # Si ya tiene una partitura en el inventario
            self.soltar_partitura()  
        posicion_fuera_pantalla = [-1000, -1000]  # Posición fuera de la pantalla
        partitura.establecerPosicion(posicion_fuera_pantalla) # La partitura desaparece del mapa
        self.inventario = partitura  # Recoge la nueva partitura
        

    def soltar_partitura(self):
        # Define las posibles posiciones donde soltar la partitura
        posibles_posiciones = [
            (self.posicion[0] + 50, self.posicion[1]),      # Derecha
            (self.posicion[0] - 50, self.posicion[1]),      # Izquierda
            (self.posicion[0], self.posicion[1] - 50),      # Arriba
            (self.posicion[0], self.posicion[1] + 50)       # Abajo
        ]

        for posicion in posibles_posiciones:
            # Crea un rectángulo en la posible posición
            futuro_rect = pygame.Rect(posicion[0], posicion[1], self.rect.width, self.rect.height)

            # Comprueba si el rectángulo colisiona con alguna plataforma
            if not any(futuro_rect.colliderect(plataforma.rect) for plataforma in self.grupoPlataformas):
                # Si no colisiona, establece la posición de la partitura y la suelta
                self.inventario.establecerPosicion(posicion)
                self.inventario = None
                return  # Devuelve la partitura soltada para que se pueda añadir al mapa

        # Si todas las posibles posiciones están bloqueadas, no suelta la partitura
        print("No se puede soltar la partitura, todas las posiciones están bloqueadas.") # Caso improbable por como tenemos las paredes colocadas


    # Metodo para actualizar el estado del personaje
    def update(self, grupoPlataformas, grupoPartituras, tiempo):
        self.grupoPlataformas = grupoPlataformas
        
        velocidadx, velocidady = 0, 0

        # Segun el movimiento que este realizando, actualizamos su velocidad
        if self.movimiento in [IZQUIERDA, DERECHA, ARRIBA, ABAJO]:
            self.mirando = self.movimiento

            if self.movimiento == IZQUIERDA:
                self.numPostura = SPRITE_ANDANDO_IZQ
                velocidadx = -self.velocidadCarrera
            elif self.movimiento == DERECHA:
                self.numPostura = SPRITE_ANDANDO_DER
                velocidadx = self.velocidadCarrera
            elif self.movimiento == ARRIBA:
                self.numPostura = SPRITE_ARRIBA
                velocidady = -self.velocidadSalto
            elif self.movimiento == ABAJO:
                self.numPostura = SPRITE_ABAJO
                velocidady = self.velocidadSalto

        elif self.movimiento == QUIETO:
            self.numPostura = SPRITE_QUIETO if self.mirando == SPRITE_ABAJO else self.mirando

        # Calculamos la futura posicion del Sprite
        futura_posicion_x = self.posicion[0] + velocidadx * tiempo - self.scroll[0]
        futura_posicion_y = self.posicion[1] + velocidady * tiempo - self.scroll[1]

        # Y creamos un rectangulo con ella
        futuro_rect = pygame.Rect(futura_posicion_x, futura_posicion_y - self.rect.height, self.rect.width, self.rect.height)


        # Comprobamos si al moverse se va a chocar con alguna plataforma
        if any(futuro_rect.colliderect(plataforma.rect) for plataforma in grupoPlataformas):
            velocidadx, velocidady = 0, 0

        # Comprobamos si toca con alguna partitura
        for partitura in grupoPartituras:
            if futuro_rect.colliderect(partitura.rect):
                if partitura != self.inventario:
                    self.recoger_partitura(partitura)
                    print("Partitura recogida")


        # Si no, actualizamos su posicion
        self.actualizarPostura()
        self.velocidad = (velocidadx, velocidady)
        MiSprite.update(self, tiempo)

