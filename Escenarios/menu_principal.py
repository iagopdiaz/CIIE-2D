import pygame
from pygame.locals import *
from Escenarios.escena import *
from Gestores.gestor_recursos import *
from Gestores.gestor_sonido import GestorSonido
from Escenarios.fase import *
from Escenarios.menu_nivel import MenuNivel
from Escenarios.menu_settings import MenuAjustes
from Interfaz.GUIElemento import *
from Escenarios.botones import GUI, BotonJugar, BotonNivel, BotonAjuste, BotonSalir


class GUIInicial(GUI):
    def __init__(self, menu):
        GUI.__init__(self, menu, "interfaces/fondos/principal.jpg")
        botonJugar = BotonJugar(self)
        botonNivel = BotonNivel(self)
        botonAjustes = BotonAjuste(self)
        botonSalir = BotonSalir(self)
        self.GUIelementos.append(botonJugar)
        self.GUIelementos.append(botonNivel)
        self.GUIelementos.append(botonAjustes)
        self.GUIelementos.append(botonSalir)
      

class Menu(Escena):
    def __init__(self, director):
        #Llamamos al constructor de la clase padre
        Escena.__init__(self, director)
        #Creamos la lista de pantallas
        self.listaPantallas = []
        #Creamos las pantallas que vamos a tener
        #y las metemos en la lista
        self.listaPantallas.append(GUIInicial(self))
        #En que pantalla estamos actualmente
        self.mostrarPantallaInicial()
    
    def update(self, *args):
        return

    def eventos(self, lista_eventos):
        #Se mira si se quiere salir de esta escena
        for evento in lista_eventos:
            #Si se quiere salir, se le indica al director
            if evento.type == KEYDOWN:
                if evento.key == K_ESCAPE:
                    self.ejecutarSalir()
            elif evento.type == pygame.QUIT:
                self.director.salirPrograma()
        #Se pasa la lista de eventos a la pantalla actual
        self.listaPantallas[self.pantallaActual].eventos(lista_eventos)

    def dibujar(self, pantalla):
        self.listaPantallas[self.pantallaActual].dibujar(pantalla)

    def ejecutarJugar(self):
        fase = Fase(self.director, 1)
        self.director.apilarEscena(fase)
        
    def ejecutarAjustes(self):
        ajustes = MenuAjustes(self.director)
        self.director.apilarEscena(ajustes)
        
    def ejecutarNivel(self):
        menuSelect = MenuNivel(self.director)
        self.director.apilarEscena(menuSelect)

    def ejecutarSalir(self):
        self.director.salirPrograma()

    def mostrarPantallaInicial(self):
        self.pantallaActual = 0
    
    def encender_musica(self):
        GestorSonido.musica_menu_principal()      