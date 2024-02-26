import pygame, sys, os
from pygame.locals import *
from GestorRecursos import *
from Jugador import *
from settings import *
###############################################################################################################
# Clase MiSprite
class MiSprite(pygame.sprite.Sprite):
    "Los Sprites que tendra este juego"
    def __init__(self):
        pygame.sprite.Sprite.__init__(self)
        self.posicion = (0, 0)
        self.velocidad = (0, 0)
        self.scroll   = (0, 0)

    def establecerPosicion(self, posicion):
        self.posicion = posicion
        self.rect.left = self.posicion[0] - self.scroll[0]
        self.rect.bottom = self.posicion[1] - self.scroll[1]

    def incrementarPosicion(self, incremento):
        (posx, posy) = self.posicion
        (incrementox, incrementoy) = incremento
        self.establecerPosicion((posx+incrementox, posy+incrementoy))

    def update(self, tiempo):
        incrementox = self.velocidad[0]*tiempo
        incrementoy = self.velocidad[1]*tiempo
        self.incrementarPosicion((incrementox, incrementoy))
        
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

    def update(self, grupoPlataformas, tiempo):

        # Las velocidades a las que iba hasta este momento
        (velocidadx, velocidady) = self.velocidad

        # Si vamos a la izquierda o a la derecha        
        if (self.movimiento == IZQUIERDA) or (self.movimiento == DERECHA):
            # Esta mirando hacia ese lado
            self.mirando = self.movimiento
            # Si vamos a la izquierda, le ponemos velocidad en esa dirección
            if self.movimiento == IZQUIERDA:
                self.numPostura = SPRITE_ANDANDO_IZQ
                velocidadx = -self.velocidadCarrera
            # Si vamos a la derecha, le ponemos velocidad en esa dirección
            else:
                self.numPostura = SPRITE_ANDANDO_DER
                velocidadx = self.velocidadCarrera
               
        # Si queremos saltar
        elif self.movimiento == ARRIBA:
            self.numPostura = SPRITE_ARRIBA
            # Le imprimimos una velocidad en el eje y
            velocidady = -self.velocidadSalto

        # Si queremos bajar
        elif self.movimiento == ABAJO:
            self.numPostura = SPRITE_ABAJO
            # Le imprimimos una velocidad en el eje y
            velocidady = self.velocidadSalto

        # Si no se ha pulsado ninguna tecla
        elif self.movimiento == QUIETO:
            self.numPostura = SPRITE_QUIETO
            velocidadx = 0
            velocidady = 0

        #  miramos si hay colision con alguna plataforma del grupo
        plataformas = pygame.sprite.spritecollide(self, grupoPlataformas,False)
        #  Ademas, esa colision solo nos interesa cuando estamos cayendo
        #  y solo es efectiva cuando caemos encima, no de lado, es decir,
        #  cuando nuestra posicion inferior esta por encima de la parte de abajo de la plataforma
        for plataforma in plataformas:
            if (plataforma != None) and (velocidady>0) and (plataforma.rect.bottom >= self.rect.bottom) and (plataforma.rect.top >= self.rect.top):
                # Lo situamos con la parte de abajo un pixel colisionando con la plataforma
                #  para poder detectar cuando se cae de ella
                self.establecerPosicion((self.posicion[0], plataforma.posicion[1] - plataforma.rect.height - 1))
                # Lo ponemos como quieto
                velocidady = 0

                    # Si hay colisión y nos estamos moviendo hacia arriba (subiendo)
            if (plataforma != None) and (velocidady < 0) and (plataforma.rect.top <= self.rect.top) and (plataforma.rect.bottom <= self.rect.bottom):
                # Ajustamos la posición para que el sprite no se "incruste" en la plataforma
                self.establecerPosicion((self.posicion[0], plataforma.posicion[1] + plataforma.rect.height + 30))
                velocidady = 0  # Cambia esto según el comportamiento deseado (rebote o detención completa)

            if (plataforma != None) and (velocidadx > 0) and (plataforma.rect.right >= self.rect.right) and (plataforma.rect.left >= self.rect.left):
                self.establecerPosicion((plataforma.posicion[0] - plataforma.rect.width - 20, self.posicion[1]))
                
                velocidadx = 0

            if (plataforma != None) and (velocidadx < 0) and (plataforma.rect.left <= self.rect.left) and (plataforma.rect.right <= self.rect.right):
                self.establecerPosicion((plataforma.posicion[0] + plataforma.rect.width + 1, self.posicion[1]))
                # Lo ponemos como quieto    
                velocidadx = 0

            

        # Actualizamos la imagen a mostrar
        self.actualizarPostura()

        # Aplicamos la velocidad en cada eje      
        self.velocidad = (velocidadx, velocidady)

        # Y llamamos al método de la superclase para que, según la velocidad y el tiempo
        #  calcule la nueva posición del Sprite
        MiSprite.update(self, tiempo)
        
        return


# -------------------------------------------------
    
class Jugador(Personaje):
    "Cualquier personaje del juego"
    def __init__(self):
        # Invocamos al constructor de la clase padre con la configuracion de este personaje concreto
        Personaje.__init__(self,'alchemist.png','coordJugador.txt', [4, 4, 4, 4, 4, 4, 4, 4], VELOCIDAD_JUGADOR, VELOCIDAD_JUGADOR, RETARDO_ANIMACION_JUGADOR)


    def mover(self, teclasPulsadas, arriba, abajo, izquierda, derecha):
        # Indicamos la acción a realizar segun la tecla pulsada para el jugador
        if teclasPulsadas[arriba]:
            Personaje.mover(self,ARRIBA)
        elif teclasPulsadas[izquierda]:
            Personaje.mover(self,IZQUIERDA)
        elif teclasPulsadas[derecha]:
            Personaje.mover(self,DERECHA)
        elif teclasPulsadas[abajo]:
            Personaje.mover(self,ABAJO)
        else:
            Personaje.mover(self,QUIETO)

