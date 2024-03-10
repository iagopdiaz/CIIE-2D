import pygame, sys, os
from pygame.locals import *
from gestor_recursos import *
from settings import *
from misprite import *
from observable import Observable

class Personaje(MiSprite, Observable):
    "Cualquier personaje del juego"

    # Parametros pasados al constructor de esta clase:
    #  Archivo con la hoja de Sprites
    #  Archivo con las coordenadoas dentro de la hoja
    #  Numero de imagenes en cada postura
    #  Velocidad de caminar y de salto
    #  Retardo para mostrar la animacion del personaje
    
    def __init__(self, archivoImagen, archivoCoordenadas, numImagenes, velocidadX, velocidadY, retardoAnimacion, id):

        # Primero invocamos al constructor de la clase padre
        MiSprite.__init__(self)
        # Se carga la hoja
        self.hoja = GestorRecursos.CargarImagen(archivoImagen, -1)

        self.hoja = self.hoja.convert_alpha()
        # El movimiento que esta realizando
        self.movimiento = QUIETO
        # Lado hacia el que esta mirando
        self.mirando = IZQUIERDA

        # El id del personaje para saber que personaje es
        self.id = id

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
        self.velocidadX = velocidadX
        self.velocidadY = velocidadY

        # El retardo en la animacion del personaje (podria y deberia ser distinto para cada postura)
        self.retardoAnimacion = retardoAnimacion

        # Y actualizamos la postura del Sprite inicial, llamando al metodo correspondiente
        self.actualizarPostura()


    # Metodo base para realizar el movimiento: simplemente se le indica cual va a hacer, y lo almacena
    def mover(self, movimiento):
        self.movimiento = movimiento

    def tocar(self):
        if self.inventario != None:
            print("Tocando: " + str(self.inventario.nombre))
            for puerta in self.grupoPuertas:
                # Crea un rectángulo para el área de activación del personaje
                area_activacion_personaje = pygame.Rect(self.posicion[0], self.posicion[1], self.rect.width, self.rect.height)

                if (puerta.area.colliderect(area_activacion_personaje)):                    
                    if (puerta.añadir_partitura(self.inventario)):
                        self.inventario = None
                        return
                    else:
                        print("La partitura no abre esta puerta")
                else:
                    print("No hay puerta en el area de activacion")
        else:
            print("No hay partitura en el inventario")
    
    def escuchar(self):
        for puerta in self.grupoPuertas:
                area_activacion_personaje = pygame.Rect(self.posicion[0], self.posicion[1], self.rect.width, self.rect.height)
                if (puerta.area.colliderect(area_activacion_personaje)):
                    print("Escuchando: " + str(puerta.nombres))


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
        if self.id == partitura.jugador:
            if self.inventario:  # Si ya tiene una partitura en el inventario
                self.soltar_partitura()  
            partitura.desaparecer() # La partitura desaparece del mapa
            self.inventario = partitura  # Recoge la nueva partitura
        imagen = partitura.archivoImagen
        self.notificar_observers("partitura", imagen)  # Notifica a la interfaz que ha recogido una partitura

    def soltar_partitura(self):
        if self.inventario:
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
            if self.puede_soltar_partitura(nueva_posicion):
                self.soltando = False
                print("Partitura soltada")
                return

            # Prueba en las otras direcciones
            for direccion in posiciones_por_direccion:
                if direccion != self.mirando:
                    dx, dy = posiciones_por_direccion[direccion]
                    nueva_posicion = (self.posicion[0] + dx, self.posicion[1] + dy)
                    if self.puede_soltar_partitura(nueva_posicion):
                        self.soltando = False
                        return

            print("No se puede soltar la partitura aqui")
            self.soltando = True
        else:
            print("No hay partitura en el inventario")

    def puede_soltar_partitura(self, posicion):
        # Ajusta las coordenadas de la partitura en función del desplazamiento de la pantalla
        posicion_ajustada = (posicion[0] - self.scroll[0], posicion[1] - self.scroll[1])

        # Crea un rectángulo en la posible posición
        futuro_rect = pygame.Rect(posicion_ajustada[0], posicion_ajustada[1], self.rect.width, self.rect.height)

        # Comprueba si el rectángulo colisiona con alguna plataforma o puerta
        if not any(futuro_rect.colliderect(plataforma.rect) for plataforma in self.grupoPlataformas) and not any(futuro_rect.colliderect(puerta.rect) for puerta in self.grupoPuertas):
            # Si no colisiona, establece la posición de la partitura y la suelta
            self.inventario.establecerPosicion(posicion)
            self.inventario = None
            print("Partitura soltada")
            return True  # Devuelve True si pudo soltar la partitura
        
        return False
    
    #A esta se le pasan como argumentos plataformas y puertas ya que se le llama antes de actualizar los personajes cuando se cambian
    def puede_moverse(self, futuro_rect, grupoPlataformas, grupoPuertas):
        # Comprueba si el rectángulo colisiona con alguna plataforma
        if any(futuro_rect.colliderect(plataforma.rect) for plataforma in grupoPlataformas):
            return False

        # Compueba si el rectángulo colisiona con alguna puerta cerrada
        for puerta in grupoPuertas:
            if futuro_rect.colliderect(puerta.rect) and not puerta.abierta:
                return False

        return True


    # Metodo para actualizar el estado del personaje
    def update(self, grupoPlataformas, grupoPartituras, grupoPuertas, tiempo):
        self.grupoPlataformas = grupoPlataformas
        self.grupoPuertas = grupoPuertas
        
        velocidadx, velocidady = 0, 0

        #Comprobamos si el personaje quiere soltar una partitura
        if self.soltando:
            self.soltar_partitura()
            return

        # Segun el movimiento que este realizando, actualizamos su velocidad
        if self.movimiento in [IZQUIERDA, DERECHA, ARRIBA, ABAJO]:
            self.mirando = self.movimiento

            if self.movimiento == IZQUIERDA:
                self.numPostura = SPRITE_ANDANDO_IZQ
                velocidadx = -self.velocidadX
            elif self.movimiento == DERECHA:
                self.numPostura = SPRITE_ANDANDO_DER
                velocidadx = self.velocidadX
            elif self.movimiento == ARRIBA:
                self.numPostura = SPRITE_ARRIBA
                velocidady = -self.velocidadY
            elif self.movimiento == ABAJO:
                self.numPostura = SPRITE_ABAJO
                velocidady = self.velocidadY

        elif self.movimiento == QUIETO:
            self.numPostura = SPRITE_QUIETO if self.mirando == SPRITE_ABAJO else self.mirando

        # Calculamos la futura posicion del Sprite
        futura_posicion_x = self.posicion[0] + velocidadx * tiempo - self.scroll[0]
        futura_posicion_y = self.posicion[1] + velocidady * tiempo - self.scroll[1]
    
        # Y creamos un rectangulo con ella
        futuro_rect = pygame.Rect(futura_posicion_x, futura_posicion_y, self.rect.width, self.rect.height)

        # Comprobamos si puede moverse a esa posicion
        if not self.puede_moverse(futuro_rect, grupoPlataformas, grupoPuertas):
            velocidadx, velocidady = 0, 0
        
        # Comprobamos si puede recoger una partitura
        for partitura in grupoPartituras:
            if futuro_rect.colliderect(partitura.rect):
                self.recoger_partitura(partitura)
        

        # Actualizamos su posicion
        self.actualizarPostura()
        self.velocidad = (velocidadx, velocidady)
        MiSprite.update(self, tiempo)

