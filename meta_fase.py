import pygame, sys, os
from misprite import *
from gestor_recursos import *

class MetaFase (MiSprite):
    def __init__(self, coordx, coordy, metaTipo):
        MiSprite.__init__(self)
        self.image = GestorRecursos.CargarImagen(metaTipo, -1)
        self.image.convert_alpha()
        self.rect = self.image.get_rect()
        self.establecerPosicion((coordx, coordy))