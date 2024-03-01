import pygame, sys, os
from pygame.locals import *
from gestor_recursos import *
from jugador import *
from fase import *
from settings import *
from director import *
from menu_principal import *

if __name__ == '__main__':
    
    pygame.init()

    director = Director()
    escena = Menu(director)
    director.apilarEscena(escena)
    
    director.ejecutar()
    
    pygame.quit()