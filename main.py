import pygame, sys, os
from pygame.locals import *
from gestor_recursos import *
from gestor_usuario import *
from jugador import *
from fase import *
from settings import *
from director import *
from menu_principal import *

if __name__ == '__main__':
    
    pygame.init()
    
    GestorUsuario.init()

    director = Director()
    menu = Menu(director)
    director.apilarEscena(menu)
    
    director.ejecutar()
    
    pygame.quit()