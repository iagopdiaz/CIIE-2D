import pygame, sys, os
from pygame.locals import *
from gestor_recursos import *
from settings import *
from misprite import *
from personaje import *
from onda import *
from observable import Observable

class Jugador(Personaje, Observable):
    "Cualquier personaje del juego"
    def __init__(self, archivoImagen, archivoCoordenadas, numImagenes, velocidadX, velocidadY, retardoAnimacion, idJugador):
        # Invocamos al constructor de la clase padre con la configuracion de este personaje concreto
        Personaje.__init__(self, archivoImagen, archivoCoordenadas, numImagenes, velocidadX, velocidadY, retardoAnimacion, idJugador)
        self.inventario = None
        self.soltando = False
        
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

    # Metodo para actualizar el estado del personaje
    def update(self, grupoPlataformas, grupoPartituras, grupoPuertas, grupoCubos_negros, grupoCubos_grises, grupoMeta, tiempo):
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

        if any(self.rect.colliderect(cubo.rect) for cubo in grupoCubos_negros):
            velocidadx, velocidady = 0, 0

        # Calculamos la futura posicion del Sprite
        futura_posicion_x = self.posicion[0] + velocidadx * tiempo - self.scroll[0]
        futura_posicion_y = self.posicion[1] + velocidady * tiempo - self.scroll[1]
    
        # Y creamos un rectangulo con ella
        futuro_rect = pygame.Rect(futura_posicion_x, futura_posicion_y, self.rect.width, self.rect.height)

        # Comprobamos si puede moverse a esa posicion
        if not self.puede_moverse(futuro_rect, grupoPlataformas, grupoPuertas, grupoCubos_grises):
            velocidadx, velocidady = 0, 0
        
        # Comprobamos si puede recoger una partitura
        for partitura in grupoPartituras:
            if futuro_rect.colliderect(partitura.rect):
                self.recoger_partitura(partitura)

        # Actualizamos su posicion
        self.actualizarPostura()
        self.velocidad = (velocidadx, velocidady)
        MiSprite.update(self, tiempo)

    def habilidad1():
        raise NotImplemented("jugador sin habilidad1")

class PrimerPersonaje(Jugador):#and Observable
    def __init__(self):#and Observers
        # Invocamos al constructor de la clase padre con la configuracion de este personaje concreto
        Jugador.__init__(self,'personajes/jugador1.png','personajes/coordJugador1.txt', [4, 4, 4, 4, 4, 4, 4, 4], VELOCIDAD_JUGADORX, VELOCIDAD_JUGADORY, RETARDO_ANIMACION_JUGADOR, 0)
        Observable.__init__(self)
        observers = []
        
    def notificar_observers(self, tipo, imagen):
        for observer in self.observers:
            observer.actualizar_observer(tipo, imagen)
            
    def registrar_observador(self, observador):
        self.observers.append(observador)

    def eliminar_observador(self, observador):
        self.observers.remove(observador) 
        
    def habilidad1(self, ataques):
        ataque = Onda1(self.rect.left - 20, self.rect.top - 20)
        ataques.add(ataque)

class SegundoPersonaje(Jugador,Observable):
    def __init__(self):
        # Invocamos al constructor de la clase padre con la configuracion de este personaje concreto
        Jugador.__init__(self,'personajes/jugador2.png','personajes/coordJugador2.txt', [4, 4, 4, 4, 4, 4, 4, 4], VELOCIDAD_JUGADORX, VELOCIDAD_JUGADORY, RETARDO_ANIMACION_JUGADOR, 1)
        Observable.__init__(self)
        observers = []
        
    def notificar_observers(self, tipo, imagen):
        for observer in self.observers:
            observer.actualizar_observer(tipo, imagen)
            
    def registrar_observador(self, observador):
        self.observers.append(observador)

    def eliminar_observador(self, observador):
        self.observers.remove(observador)

    def habilidad1(self, ataques):
        ataque = Onda2(self.rect.left - 20, self.rect.top - 20)
        ataques.add(ataque)

class TercerPersonaje(Jugador,Observable):
    def __init__(self):#and Observers
        # Invocamos al constructor de la clase padre con la configuracion de este personaje concreto
        Jugador.__init__(self,'personajes/jugador3.png','personajes/coordJugador3.txt', [4, 4, 4, 4, 4, 4, 4, 4], VELOCIDAD_JUGADORX, VELOCIDAD_JUGADORY, RETARDO_ANIMACION_JUGADOR, 2)
        Observable.__init__(self)
        observers = []
        
    def notificar_observers(self, tipo, imagen):
        for observer in self.observers:
            observer.actualizar_observer(tipo, imagen)
            
    def registrar_observador(self, observador):
        self.observers.append(observador)

    def eliminar_observador(self, observador):
        self.observers.remove(observador)
        
    def habilidad1(self, ataques):
        ataque = Onda3(self.rect.left - 20, self.rect.top - 20)
        ataques.add(ataque)
