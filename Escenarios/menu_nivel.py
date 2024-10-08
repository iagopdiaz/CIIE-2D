import pygame
from pygame.locals import *
from Escenarios.escena import *
from Gestores.gestor_recursos import *
from Gestores.gestor_sonido import GestorSonido
from Escenarios.fase import *
from Escenarios.game_over import *
from Interfaz.GUIElemento import *
from Escenarios.botones import GUI, Boton


class GUIInicial(GUI):
    def __init__(self, menu):
        GUI.__init__(self, menu, "interfaces/fondos/ajustes.jpg")
        botonFase1 = BotonNivel1(self)
        botonFase2 = BotonNivel2(self)
        botonFase3 = BotonNivel3(self)
        botonAtras = BotonAtras(self)
        self.GUIelementos.append(botonFase1)
        self.GUIelementos.append(botonFase2)
        self.GUIelementos.append(botonFase3)
        self.GUIelementos.append(botonAtras)


class BotonNivel1(Boton):
    def __init__(self, pantalla):
        Boton.__init__(self, pantalla, BOTON_NIVEL1, (100, 120))
    
    def accion(self):
        self.pantalla.menu.ejecutarNivel1()


class BotonNivel2(Boton):
    def __init__(self, pantalla):
        Boton.__init__(self, pantalla, BOTON_NIVEL2 , (100, 240))
    
    def accion(self):
        self.pantalla.menu.ejecutarNivel2()


class BotonNivel3(Boton):
    def __init__(self, pantalla):
        Boton.__init__(self, pantalla,  BOTON_NIVEL3, (100, 360))
    
    def accion(self):
        self.pantalla.menu.ejecutarNivel3()


class BotonAtras(Boton):
    def __init__(self, pantalla):
        Boton.__init__(self, pantalla, BOTON_ATRAS, (100, 480))
    
    def accion(self):
        self.pantalla.menu.ejecutarAtras()


class MenuNivel(Escena):
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
                    self.ejecutarAtras()
            elif evento.type == pygame.QUIT:
                self.director.salirPrograma()
        #Se pasa la lista de eventos a la pantalla actual
        self.listaPantallas[self.pantallaActual].eventos(lista_eventos)

    def dibujar(self, pantalla):
        self.listaPantallas[self.pantallaActual].dibujar(pantalla)
    
    def ejecutarSalir(self):
        self.director.salirPrograma()

    def ejecutarNivel1(self):
        fase1 = Fase(self.director, 1)
        self.director.cambiarEscena(fase1)
    
    def ejecutarNivel2(self):
        fase2 = Fase(self.director, 2)
        self.director.cambiarEscena(fase2)
    
    def ejecutarNivel3(self):
        fase3 = Fase(self.director, 3)
        self.director.cambiarEscena(fase3)
    
    def ejecutarAtras(self):
        self.director.salirEscena()
    
    def mostrarPantallaInicial(self):
        self.pantallaActual = 0
        
    def encender_musica(self):
        GestorSonido.musica_menus()

