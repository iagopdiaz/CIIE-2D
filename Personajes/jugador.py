import pygame, sys, os
from pygame.locals import *
from Gestores.gestor_recursos import *
from Ajustes.settings import *
from Personajes.misprite import *
from Personajes.personajes import *
from Animaciones.onda import *
from Observador.observable import Observable
from Gestores.gestor_sonido import *

class Jugador(Personaje, Observable):
    "Cualquier personaje del juego"
    def __init__(self, archivoImagen, archivoCoordenadas, numImagenes, velocidadX, velocidadY, retardoAnimacion, idJugador):
        # Invocamos al constructor de la clase padre con la configuracion de este personaje concreto
        Personaje.__init__(self, archivoImagen, archivoCoordenadas, numImagenes, velocidadX, velocidadY, retardoAnimacion, idJugador)
        self.inventario = None
        self.soltando = False
        self.id = idJugador
        self.vida = 5
        self.tiempo_ultimo_dano = 0  # Inicializa el tiempo desde el último daño a 0
        self.cooldown_dano = 1500  # Establece un cooldown de daño de 1500 milisegundos

    
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

    def tocar(self, grupoPuertas, grupoPartituras):
        if self.inventario != None:
            print("Tocando: " + str(self.inventario.nombre))
            GestorSonido.reproducir_partitura(self.inventario.musica)
            en_area_activacion = False  # Variable para rastrear si el jugador está en el área de activación de alguna puerta
            for puerta in grupoPuertas:
                # Crea un rectángulo para el área de activación del personaje
                area_activacion_personaje = pygame.Rect(self.posicion[0], self.posicion[1], self.rect.width, self.rect.height)

                if (puerta.area.colliderect(area_activacion_personaje)):                    
                    en_area_activacion = True  # El jugador está en el área de activación de una puerta
                    if (puerta.añadir_partitura(self.inventario)):
                        grupoPartituras.remove(self.inventario)
                        self.inventario = None
                        self.notificar_observers("DELpartitura", "partituras\partituraX.png")  # Notifica a la interfaz que ha soltado una partitura
                        self.notificar_observers("accion", PUERTA_PARTITURA)  
                        return
                    else:
                        self.notificar_observers("accion", PUERTA_PARTITURA_NO) 
                        print("La partitura no abre esta puerta")
            if not en_area_activacion:
                self.notificar_observers("accion", ABRIR_PUERTA) 
                print("No hay puerta en el area de activacion")
        else:
            self.notificar_observers("accion", SIN_PARTITURA)
            print("No hay partitura en el inventario")

    
    def escuchar(self, grupoPuertas):
        for puerta in grupoPuertas:
                area_activacion_personaje = pygame.Rect(self.posicion[0], self.posicion[1], self.rect.width, self.rect.height)
                if (puerta.area.colliderect(area_activacion_personaje)):
                    puerta.escuchar(self.id)
                    return
                

    def recoger_partitura(self, partitura, grupoPartituras, grupoParedes, grupoPuertas, grupoCubosGrises):
        if self.id == partitura.jugador:
            if self.inventario:  # Si ya tiene una partitura en el inventario
                self.soltar_partitura(grupoPartituras, grupoParedes, grupoPuertas, grupoCubosGrises)
            #partitura.desaparecer() # La partitura desaparece del mapa
            grupoPartituras.remove(partitura)  # La partitura desaparece del grupo de partituras
            self.inventario = partitura  # Recoge la nueva partitura
        imagen = partitura.archivoImagen
        self.notificar_observers("partitura", imagen)  # Notifica a la interfaz que ha recogido una partitura
        self.notificar_observers("accion", PARTITURA_RECOGIDA)  # Notifica a la interfaz que ha recogido una partitura
        GestorSonido.reproducir_efecto(SONIDO_COGER_PARTITURA)
        
    def soltar_partitura(self, grupoPartituras, grupoParedes, grupoPuertas, grupoCubosGrises):
        if self.inventario:
            # Definición de las posiciones en función de la dirección
            posiciones_por_direccion = {
                IZQUIERDA : (70, 0),    # Si está mirando a la derecha, mueve 50 unidades en el eje x
                DERECHA : (-70, 0),   # Si está mirando a la izquierda, mueve -50 unidades en el eje x
                ARRIBA : (0, 70),      # Si está mirando arriba, mueve -50 unidades en el eje y
                ABAJO : (0, -70)       # Si está mirando abajo, mueve 50 unidades en el eje y
            }

            # Obtén las coordenadas según la dirección actual
            dx, dy = posiciones_por_direccion.get(self.mirando, (0, 0))
            nueva_posicion = (self.posicion[0] + dx, self.posicion[1] + dy)

            # Prueba en la dirección actual
            if self.puede_soltar_partitura(nueva_posicion, grupoParedes, grupoPuertas, grupoCubosGrises):
                self.soltando = False
                grupoPartituras.add(self.inventario)
                self.inventario = None
                self.notificar_observers("DELpartitura", "partituras\partituraX.png")  # Notifica a la interfaz que ha soltado una partitura
                self.notificar_observers("accion", PARTITURA_SOLTADA)  # Notifica a la interfaz que ha soltado una partitura
                GestorSonido.reproducir_efecto(SONIDO_SOLTAR_PARTITURA)
                print("Partitura soltada en la dirección actual")
                return

            # Prueba en las otras direcciones
            for direccion in posiciones_por_direccion:
                if direccion != self.mirando:
                    dx, dy = posiciones_por_direccion[direccion]
                    nueva_posicion = (self.posicion[0] + dx, self.posicion[1] + dy)
                    if self.puede_soltar_partitura(nueva_posicion, grupoParedes, grupoPuertas, grupoCubosGrises):
                        self.soltando = False
                        grupoPartituras.add(self.inventario)
                        self.inventario = None
                        print("Partitura soltada en otra")
                        self.notificar_observers("DELpartitura", "partituras\partituraX.png")  # Notifica a la interfaz que ha soltado una partitura
                        self.notificar_observers("accion", PARTITURA_SOLTADA)  # Notifica a la interfaz que ha soltado una partitura
                        GestorSonido.reproducir_efecto(SONIDO_SOLTAR_PARTITURA)
                        return

            print("No se puede soltar la partitura aqui, soltando true")
            self.soltando = True
            self.notificar_observers("accion", SOLTAR_PARTITURA_NO)  # Notifica a la interfaz que no se puede soltar la partitura aquí
        else:
            self.notificar_observers("accion", SIN_PARTITURA)
            print("No hay partitura en el inventario")

    def puede_soltar_partitura(self, posicion, grupoParedes, grupoPuertas, grupoCubosGrises):
        # Ajusta las coordenadas de la partitura en función del desplazamiento de la pantalla
        posicion_ajustada = (posicion[0] - self.scroll[0], posicion[1] - self.scroll[1])

        # Crea un rectángulo en la posible posición
        futuro_rect = pygame.Rect(posicion_ajustada[0], posicion_ajustada[1], self.rect.width, self.rect.height)

        # Comprueba si el rectángulo colisiona con alguna pared o puerta
        if not any(futuro_rect.colliderect(pared.rect) for pared in grupoParedes) and not any(futuro_rect.colliderect(puerta.rect) for puerta in grupoPuertas) and not any(futuro_rect.colliderect(cubo.rect) for cubo in grupoCubosGrises):
            # Si no colisiona, establece la posición de la partitura y la suelta
            self.inventario.establecerPosicion(posicion)
            #aqui no se notifica
            self.notificar_observers("accion", SOLTAR_PARTITURA_NO)
            return True  
        else:
            return False

    # Metodo para actualizar el estado del personaje
    def update(self, grupoParedes, grupoPinchos, grupoPartituras, grupoPuertas, grupoCubos_negros, grupoCubosGrises, grupoMeta, grupoEnemigos, tiempo):

        velocidadx, velocidady = 0, 0

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
        
        if not self.puede_moverse(futuro_rect, grupoParedes, grupoPuertas, grupoCubosGrises):
            velocidadx, velocidady = 0, 0

        # Comprobamos si choca con un pincho
        for pincho in grupoPinchos:
            if futuro_rect.colliderect(pincho.rect):
                tiempo_actual = pygame.time.get_ticks()
                if tiempo_actual - self.tiempo_ultimo_dano > self.cooldown_dano:
                    self.vida -= pincho.damage  # Restamos un punto de vida
                    self.notificar_observers("accion", PERDER_VIDA)  # Notifica a la interfaz que ha perdido vida
                    self.tiempo_ultimo_dano = tiempo_actual
                    GestorSonido.reproducir_efecto(SONIDO_PERDER_VIDA)

        # Comprobamos si puede recoger una partitura
        for partitura in grupoPartituras:
            if futuro_rect.colliderect(partitura.rect) and self.id == partitura.jugador:
                self.recoger_partitura(partitura, grupoPartituras, grupoParedes, grupoPuertas, grupoCubosGrises)

        for enemigo in grupoEnemigos:
            if futuro_rect.colliderect(enemigo.rect):
                tiempo_actual = pygame.time.get_ticks()
                if tiempo_actual - self.tiempo_ultimo_dano > self.cooldown_dano:
                    self.vida -= enemigo.damage  # Restamos un punto de vida
                    self.tiempo_ultimo_dano = tiempo_actual
                    GestorSonido.reproducir_efecto(SONIDO_PERDER_VIDA)

        # Comprobamos si puede soltar una partitura
        if self.soltando:
            print("Soltando partitura")
            self.soltar_partitura(grupoPartituras)            
            self.notificar_observers("DELpartitura", "partituras\partituraX.png") 
            self.notificar_observers("accion", PARTITURA_SOLTADA)  # Notifica a la interfaz que no se puede soltar la partitura aquí
            return

        # Actualizamos su posicion
        self.actualizarPostura()
        self.velocidad = (velocidadx, velocidady)
        MiSprite.update(self, tiempo)

        # Muerte del personaje
        if self.vida <= 0:
            self.notificar_observers("muerte", "imagenes\interfaces\fondos\muerte.jpg")
            GestorSonido.reproducir_efecto(SONIDO_PERDER)

    def habilidad1():
        raise NotImplemented("jugador sin habilidad1")

class PrimerPersonaje(Jugador, Observable):#and Observable
    def __init__(self):#and Observers
        # Invocamos al constructor de la clase padre con la configuracion de este personaje concreto
        Jugador.__init__(self,'personajes/jugador1.png','personajes/coordJugador1.txt', [4, 4, 4, 4, 4, 4, 4, 4], VELOCIDAD_JUGADORX, VELOCIDAD_JUGADORY, RETARDO_ANIMACION_JUGADOR, 0)
        Observable.__init__(self)
        observers = []
        
    def notificar_observers(self, tipo, imagen):
        for observer in self.observers:
            if (tipo == "partitura"):
                observer.actualizar_observer("partitura1", imagen)
            elif (tipo == "DELpartitura"):                    
                observer.actualizar_observer("DELpartitura1", imagen)
            elif (tipo == "accion"):
                observer.actualizar_observer("accion", imagen)    
            else: 
                observer.actualizar_observer(tipo, imagen)
    
    def registrar_observador(self, observador):
        self.observers.append(observador)
            
    def eliminar_observador(self, observador):
        self.observers.remove(observador) 
        
    def habilidad1(self, ataques):
        ataque = Onda1(self.rect.left, self.rect.top)
        ataques.add(ataque)
        self.notificar_observers("accion", HABILIDAD_PERSONAJE) 

class SegundoPersonaje(Jugador,Observable):
    def __init__(self):
        # Invocamos al constructor de la clase padre con la configuracion de este personaje concreto
        Jugador.__init__(self,'personajes/jugador2.png','personajes/coordJugador2.txt', [4, 4, 4, 4, 4, 4, 4, 4], VELOCIDAD_JUGADORX, VELOCIDAD_JUGADORY, RETARDO_ANIMACION_JUGADOR, 1)
        Observable.__init__(self)
        observers = []
        
    def notificar_observers(self, tipo, imagen):
        for observer in self.observers:
            if (tipo == "partitura"):
                observer.actualizar_observer("partitura2", imagen)
            elif (tipo == "DELpartitura"):                    
                observer.actualizar_observer("partitura2", imagen)
            else: 
                observer.actualizar_observer(tipo, imagen)
              
    def registrar_observador(self, observador):
        self.observers.append(observador)

    def eliminar_observador(self, observador):
        self.observers.remove(observador)

    def habilidad1(self, ataques):
        ataque = Onda2(self.rect.center[0], self.rect.center[1])
        ataques.add(ataque)
        self.notificar_observers("accion", HABILIDAD_PERSONAJE) 

class TercerPersonaje(Jugador,Observable):
    def __init__(self):#and Observers
        # Invocamos al constructor de la clase padre con la configuracion de este personaje concreto
        Jugador.__init__(self,'personajes/jugador3.png','personajes/coordJugador3.txt', [4, 4, 4, 4, 4, 4, 4, 4], VELOCIDAD_JUGADORX, VELOCIDAD_JUGADORY, RETARDO_ANIMACION_JUGADOR, 2)
        Observable.__init__(self)
        observers = []
        
    def notificar_observers(self, tipo, imagen):
        for observer in self.observers:
            if (tipo == "partitura"):
                observer.actualizar_observer("partitura3", imagen)
            elif (tipo == "DELpartitura"):                    
                observer.actualizar_observer("DELpartitura3", imagen)
            else: 
                observer.actualizar_observer(tipo, imagen)
               
    def registrar_observador(self, observador):
        self.observers.append(observador)

    def eliminar_observador(self, observador):
        self.observers.remove(observador)
        
    def habilidad1(self, ataques):
        ataque = Onda3(self.rect.center[0], self.rect.center[1])
        ataques.add(ataque)
        self.notificar_observers("accion", HABILIDAD_PERSONAJE) 
