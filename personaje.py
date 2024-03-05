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

    def tocar(self, grupoPuertas):
        if self.inventario != None:
            print("Tocando: " + str(self.inventario.nombre))
            for puerta in grupoPuertas:
                # Crea un rectángulo para el área de activación del personaje
                area_activacion_personaje = pygame.Rect(self.posicion[0], self.posicion[1], self.rect.width, self.rect.height)

                if (puerta.area.colliderect(area_activacion_personaje)):
                    if (puerta.nombre == self.inventario.nombre):
                        puerta.abierta = True
                        print("Puerta abierta")
                        self.soltar_partitura()
                        return
                    else:
                        print("La partitura no abre esta puerta")
                else:
                    print("No hay puerta en el area de activacion")
        else:
            print("No hay partitura en el inventario")


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
        posicion_fuera_pantalla = [-1000, -1000]  # Posición fuera de la pantalla     ---------------------   CORREGIR ESTO NO CREO QUE SEA ASI
        partitura.establecerPosicion(posicion_fuera_pantalla) # La partitura desaparece del mapa
        self.inventario = partitura  # Recoge la nueva partitura
        #self.notify("partirura", self.inventario)

    def soltar_partitura(self):
        # Definición de las posiciones en función de la dirección
        posiciones_por_direccion = {
            IZQUIERDA : (50, 0),    # Si está mirando a la derecha, mueve 50 unidades en el eje x
            DERECHA : (-50, 0),   # Si está mirando a la izquierda, mueve -50 unidades en el eje x
            ARRIBA : (0, 50),      # Si está mirando arriba, mueve -50 unidades en el eje y
            ABAJO : (0, -50)       # Si está mirando abajo, mueve 50 unidades en el eje y
        }

        # Obtén las coordenadas según la dirección actual
        dx, dy = posiciones_por_direccion.get(self.mirando, (0, 0))
        nueva_posicion = (self.posicion[0] + dx, self.posicion[1] + dy)

        # Prueba en la dirección actual
        if self._puede_soltar_partitura(nueva_posicion):
            return

        # Prueba en las otras direcciones
        for direccion in posiciones_por_direccion:
            if direccion != self.mirando:
                dx, dy = posiciones_por_direccion[direccion]
                nueva_posicion = (self.posicion[0] + dx, self.posicion[1] + dy)
                if self._puede_soltar_partitura(nueva_posicion):
                    return

        # Si todas las posibles posiciones están bloqueadas, no suelta la partitura
        print("No se puede soltar la partitura, todas las posiciones están bloqueadas.")  # Caso improbable por cómo tenemos las paredes colocadas

    def _puede_soltar_partitura(self, posicion):
        # Ajusta las coordenadas de la partitura en función del desplazamiento de la pantalla
        posicion_ajustada = (posicion[0] - self.scroll[0], posicion[1] - self.scroll[1])

        # Crea un rectángulo en la posible posición
        futuro_rect = pygame.Rect(posicion_ajustada[0], posicion_ajustada[1], self.rect.width, self.rect.height)

        # Comprueba si el rectángulo colisiona con alguna plataforma
        if not any(futuro_rect.colliderect(plataforma.rect) for plataforma in self.grupoPlataformas):
            # Si no colisiona, establece la posición de la partitura y la suelta
            self.inventario.establecerPosicion(posicion)
            self.inventario = None
            return True  # Devuelve True si pudo soltar la partitura

        return False


    # Metodo para actualizar el estado del personaje
    def update(self, grupoPlataformas, grupoPartituras, grupoPuertas, tiempo):
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
        futuro_rect = pygame.Rect(futura_posicion_x, futura_posicion_y, self.rect.width, self.rect.height)


        # Comprobamos si al moverse se va a chocar con algun borde del mapa
        if any(futuro_rect.colliderect(plataforma.rect) for plataforma in grupoPlataformas):
            velocidadx, velocidady = 0, 0

        # Comprobamos si al moverse se va a chocar con una puerta activa
        for puerta in grupoPuertas:
            if futuro_rect.colliderect(puerta.rect):
                if not puerta.abierta:
                    velocidadx, velocidady = 0, 0

        # Comprobamos si toca con alguna partitura
        for partitura in grupoPartituras:
            if futuro_rect.colliderect(partitura.rect):
                self.recoger_partitura(partitura)


        # Actualizamos su posicion
        self.actualizarPostura()
        self.velocidad = (velocidadx, velocidady)
        MiSprite.update(self, tiempo)

