import pygame
from pygame.locals import *
from gestor_recursos import *
from misprite import *

class Animaciones(MiSprite):
    def __init__(self, archivoImagen, archivoCoordenadas, numImagenes, retardoAnimacion, left, top):

        # Primero invocamos al constructor de la clase padre
        MiSprite.__init__(self)

        self.count = 0
        self.img_num = numImagenes[0]
        # Se carga la hoja
        self.hoja = GestorRecursos.CargarImagenAtaque(archivoImagen, -1)

        self.hoja = self.hoja.convert_alpha()

        # Leemos las coordenadas de un archivo de texto
        datos = GestorRecursos.CargarCoordenadasAtaque(archivoCoordenadas)
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

class AnimacionCambio(Animaciones):
    "Cambio de jugador"
    def __init__(self, left, top):
        Animaciones.__init__(self, 'onda4.png', 'coordOnda4.txt', [8], RETARDO_ANIMACION_ONDA, left, top)
        self.tipo = 4

    def update(self, jugador_activo, tiempo):
        if self.count + 1 < self.img_num:
            # Actualizamos la posición de la onda para que coincida con la del jugador
            self.rect.centerx = jugador_activo.rect.centerx
            self.rect.centery = jugador_activo.rect.centery-10
            self.actualizarPostura()
            MiSprite.update(self, tiempo)
        else:
            self.kill()