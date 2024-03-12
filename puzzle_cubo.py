from misprite import *
from settings import *

class Cubo(MiSprite):
    "Cualquier personaje del juego"

    # Parametros pasados al constructor de esta clase:
    #  Archivo con la hoja de Sprites
    #  Archivo con las coordenadoas dentro de la hoja
    #  Numero de imagenes en cada postura
    #  Velocidad de caminar y de salto
    #  Retardo para mostrar la animacion del personaje
    
    def __init__(self, archivoImagen):

        # Primero invocamos al constructor de la clase padre
        MiSprite.__init__(self)
        # Se carga la hoja
        self.image = GestorRecursos.CargarImagen(archivoImagen, -1)
        self.rect = self.image.get_rect()
        
    
class Cubo_Negro(Cubo):#and Observable
    "Cubo Sombra"
    def __init__(self):#and Observers
        # Invocamos al constructor de la clase padre con la configuracion de este personaje concreto
        Cubo.__init__(self,'cubo_negro.png')
        
        self.velocidadX = VELOCIDAD_JUGADORX
        self.velocidadY = VELOCIDAD_JUGADORY

    
    def update(self, jugador_activo, grupoPlataformas, grupoPuertas, grupoCubosGris, tiempo):
        velocidadx, velocidady = 0, 0

        if (self.rect.colliderect(jugador_activo.rect)):
            if jugador_activo.movimiento == IZQUIERDA:
                velocidadx = -self.velocidadX
            elif jugador_activo.movimiento == DERECHA:
                velocidadx = self.velocidadX
            elif jugador_activo.movimiento == ARRIBA:
                velocidady = -self.velocidadY
            elif jugador_activo.movimiento == ABAJO:
                velocidady = self.velocidadY

        futura_posicion_x = self.posicion[0] + velocidadx * tiempo - self.scroll[0]
        futura_posicion_y = self.posicion[1] + velocidady * tiempo - self.scroll[1]

        # Y creamos un rectangulo con ella
        futuro_rect = pygame.Rect(futura_posicion_x, futura_posicion_y, self.rect.width, self.rect.height)

        if any(futuro_rect.colliderect(plataforma.rect) for plataforma in grupoPlataformas):
            velocidadx, velocidady = 0, 0

        for puerta in grupoPuertas:
            if (futuro_rect.colliderect(puerta.rect)) and (not puerta.abierta):
                velocidadx, velocidady = 0, 0
        
        for cubo_gris in grupoCubosGris:
            if self.rect.colliderect(cubo_gris.rect):
                self.eliminar()  
                cubo_gris.eliminar() 

        self.velocidad = (velocidadx, velocidady)
        MiSprite.update(self, tiempo)

    def eliminar(self):
        self.kill()

class Cubo_Gris(Cubo):#and Observable
    "Posicion Objetivo"
    def __init__(self):#and Observers
        # Invocamos al constructor de la clase padre con la configuracion de este personaje concreto
        Cubo.__init__(self,'cubo_gris.png')
        ##Observable.__init__(self, observers)

    def eliminar(self):
        self.kill()

class Cubo_Sombra(Cubo):#and Observable
    "Posicion Objetivo"
    def __init__(self):#and Observers
        # Invocamos al constructor de la clase padre con la configuracion de este personaje concreto
        Cubo.__init__(self,'cubo_sombra.png')
        ##Observable.__init__(self, observers)

    def update(self, grupoAtaques, grupoCubosNegros):
        for ataque in grupoAtaques:
            if (self.rect.colliderect(ataque.rect)):
                cuboNegro = Cubo_Negro()
                cuboNegro.establecerPosicion((self.posicion[0], self.posicion[1]))

                grupoCubosNegros.add(cuboNegro)

                self.eliminar()

    def eliminar(self):
        self.kill()