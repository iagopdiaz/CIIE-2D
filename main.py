import pygame
import sys
from Ajustes.settings import *
from Gestores.director import Director
from Escenarios.menu_principal import *
from Gestores.gestor_usuario import GestorUsuario
from Gestores.gestor_sonido import GestorSonido

if __name__ == '__main__':
 
    sys.path.insert(0, './')
    GestorUsuario.init()
    GestorSonido.init()

    director = Director()
    menu = Menu(director)
    director.apilarEscena(menu)
    
    director.ejecutar()
