from settings import * 
from personaje import *

class Enemigo(Personaje):
    "Personajes¡ enemigo"
    
    def __init__(self, tipo):
        Personaje.__init__(self, "personajes/slime.png", "personajes/coordSlime.txt", [4, 4], VELOCIDAD_ENEMIGOX, VELOCIDAD_ENEMIGOY, RETARDO_ANIMACION_ENEMIGO, 3)
        
        self.damage = 1
        self.tipo = tipo
        if tipo == 0:
            self.movimiento = ABAJO
        elif tipo == 1:
            self.movimiento = IZQUIERDA

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

            if (self.movimiento == DERECHA) or (self.movimiento == ABAJO):
                self.image = pygame.transform.flip(self.hoja.subsurface(self.coordenadasHoja[self.numPostura][self.numImagenPostura]), 1, 0)
            else:
                self.image = self.hoja.subsurface(self.coordenadasHoja[self.numPostura][self.numImagenPostura])


    def update(self, jugadorActivo, grupoParedes, grupoPuertas, tiempo):
        
        velocidadx, velocidady = 0, 0

        if self.movimiento == ATAQUE:
            if self.numImagenPostura == len(self.coordenadasHoja[self.numPostura]) - 1:
                self.movimiento = self.mirando  # Restablecer a la postura de mirando después de atacar
                self.numImagenPostura = 0  # Reiniciar el índice de la imagen de postura


        # Segun el movimiento que este realizando, actualizamos su velocidad
        if self.movimiento in [IZQUIERDA, DERECHA, ARRIBA, ABAJO]:
            self.mirando = self.movimiento

            if self.movimiento == IZQUIERDA:
                self.numPostura = ENEMIGO_ANDANDO_IZQ
                velocidadx = -self.velocidadX
            elif self.movimiento == DERECHA:
                self.numPostura = ENEMIGO_ANDANDO_IZQ
                velocidadx = self.velocidadX
            elif self.movimiento == ARRIBA:
                self.numPostura = ENEMIGO_ANDANDO_IZQ
                velocidady = -self.velocidadY
            elif self.movimiento == ABAJO:
                self.numPostura = ENEMIGO_ANDANDO_IZQ
                velocidady = self.velocidadY

        futura_posicion_x = self.posicion[0] + velocidadx * tiempo - self.scroll[0]
        futura_posicion_y = self.posicion[1] + velocidady * tiempo - self.scroll[1]
        futuro_rect = pygame.Rect(futura_posicion_x, futura_posicion_y, self.rect.width, self.rect.height)

        if any(futuro_rect.colliderect(pared.rect) for pared in grupoParedes) or any(futuro_rect.colliderect(puerta.rect) for puerta in grupoPuertas):
            if self.movimiento == IZQUIERDA:
                self.numPostura = ENEMIGO_ANDANDO_IZQ
                self.movimiento = DERECHA
                velocidadx = self.velocidadX

            elif self.movimiento == DERECHA:
                self.numPostura = ENEMIGO_ANDANDO_IZQ
                self.movimiento = IZQUIERDA
                velocidadx = -self.velocidadX

            elif self.movimiento == ARRIBA:
                self.numPostura = ENEMIGO_ANDANDO_IZQ
                self.movimiento = ABAJO
                velocidady = self.velocidadY

            elif self.movimiento == ABAJO:
                self.numPostura = ENEMIGO_ANDANDO_IZQ
                self.movimiento = ARRIBA
                velocidady = -self.velocidadY

        if self.rect.colliderect(jugadorActivo.rect):
            self.numPostura = ENEMIGO_ATAQUE
            self.movimiento = ATAQUE
            velocidadx, velocidady = 0, 0

        # Actualizamos su posicion
        self.actualizarPostura()
        self.velocidad = (velocidadx, velocidady)
        MiSprite.update(self, tiempo)

