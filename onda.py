import pygame, sys, os
from pygame.locals import *
from gestor_recursos import *
from misprite import *

class Ataque(MiSprite):
    "Ataque"

    def __init__(self, archivoImagen, archivoCoordenadas, numImagenes, retardoAnimacion, left, top):

        # Primero invocamos al constructor de la clase padre
        MiSprite.__init__(self)

        self.count = 0
        self.img_num = numImagenes[0]
        # Se carga la hoja
        self.hoja = GestorRecursos.CargarImagen(archivoImagen, -1)

        self.hoja = self.hoja.convert_alpha()

        # Leemos las coordenadas de un archivo de texto
        datos = GestorRecursos.CargarArchivoCoordenadas(archivoCoordenadas)
        datos = datos.split()
        self.numPostura = 0
        self.numImagenPostura = 0
        cont = 0
        self.coordenadasHoja = []
        for linea in range(0, 1):
            self.coordenadasHoja.append([])
            tmp = self.coordenadasHoja[linea]
            for postura in range(1, numImagenes[linea]+1):
                tmp.append(pygame.Rect((int(datos[cont]), int(datos[cont+1])), (int(datos[cont+2]), int(datos[cont+3]))))
                cont += 4

        # El retardo a la hora de cambiar la imagen del Sprite (para que no se mueva demasiado rápido)
        self.retardoMovimiento = 0

        # El rectangulo del Sprite
        self.rect = pygame.Rect(left, top, self.coordenadasHoja[self.numPostura][self.numImagenPostura][2], self.coordenadasHoja[self.numPostura][self.numImagenPostura][3])

        self.retardoAnimacion = retardoAnimacion
        self.establecerPosicion((left, top))

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
            self.count += 1
            



class Onda1(Ataque):
    "Ataque con forma de onda de jugador 1"

    def __init__(self, left, top):
        Ataque.__init__(self, 'Onda.png', 'coordOnda.txt', [6], RETARDO_ANIMACION_ONDA, left, top)
        self.tipo = 1

    def update(self, jugador_activo, tiempo):
        summ = 0
        if self.count < self.img_num:
            summ = 10 * self.count
            self.rect = pygame.Rect(jugador_activo.rect.left - summ, jugador_activo.rect.top- summ , self.coordenadasHoja[self.numPostura][self.numImagenPostura][2], self.coordenadasHoja[self.numPostura][self.numImagenPostura][3])
            self.actualizarPostura()
            MiSprite.update(self, tiempo)
        else:
            self.kill()

class Onda2(Ataque):
    "Ataque con forma de onda de jugador 2"

    def __init__(self, left, top):
        Ataque.__init__(self, 'Onda.png', 'coordOnda.txt', [6], RETARDO_ANIMACION_ONDA, left, top)
        self.tipo = 2

    def update(self, jugador_activo, tiempo):
        summ = 0
        if self.count < self.img_num:
            summ = 10 * self.count
            self.rect = pygame.Rect(jugador_activo.rect.left - summ, jugador_activo.rect.top- summ , self.coordenadasHoja[self.numPostura][self.numImagenPostura][2], self.coordenadasHoja[self.numPostura][self.numImagenPostura][3])
            self.actualizarPostura()
            MiSprite.update(self, tiempo)
        else:
            self.kill()

class Onda3(Ataque):
    "Ataque con forma de onda de jugador 3"

    def __init__(self, left, top):
        Ataque.__init__(self, 'Onda.png', 'coordOnda.txt', [6], RETARDO_ANIMACION_ONDA, left, top)
        self.tipo = 3

    def update(self, jugador_activo, tiempo):
        summ = 0
        if self.count < self.img_num:
            summ = 10 * self.count
            self.rect = pygame.Rect(jugador_activo.rect.left - summ, jugador_activo.rect.top- summ , self.coordenadasHoja[self.numPostura][self.numImagenPostura][2], self.coordenadasHoja[self.numPostura][self.numImagenPostura][3])     
            self.actualizarPostura()
            MiSprite.update(self, tiempo)
        else:
            self.kill()