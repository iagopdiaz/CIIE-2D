import pygame
from settings import *
from director import Director
from menu_principal import Menu
from gestor_usuario import GestorUsuario
from gestor_sonido import GestorSonido

if __name__ == '__main__':
    
    pygame.init()
    
    GestorUsuario.init()
    GestorSonido.init()

    director = Director()
    menu = Menu(director)
    director.apilarEscena(menu)
    
    director.ejecutar()
    
    pygame.quit()