import pygame, sys, os
from pygame.locals import *
from escena import *
from gestor_recursos import *
from menu_principal import *
from director import *

# Redundancia debido a imports circulares

class GO_GUIElemento:
    def __init__(self, pantalla, rectangulo):
        self.pantalla = pantalla
        self.rectangulo = rectangulo
    
    def establecerPosicion(self, posicion):
        (posicionx, posiciony) = posicion
        self.rect.topleft = posicionx, posiciony
    
    def posicionEnElemento(self, posicion):
        (posicionx, posiciony) = posicion
        if (posicionx >= self.rect.left) and (posicionx <= self.rect.right) and (posiciony >= self.rect.top) and (posiciony <= self.rect.bottom):
            return True
        else:
            return False
        
    def dibujar(self):
        raise NotImplemented("Metodo dibujar no implementado.")
    
    def accion(self):
        raise NotImplemented("Metodo accion no implementado.")


class GO_Boton(GO_GUIElemento):
    def __init__(self, pantalla, nombreImagen, posicion):
        #Se carga la imagen del boton
        self.imagen = GestorRecursos.CargarImagen(nombreImagen, -1)
        self.rect = self.imagen.get_rect()

        #Se llama al metodo de la clase padre con el rectangulo que ocupa el boton
        GO_GUIElemento.__init__(self, pantalla, self.rect)
        #Se coloca el rectangulo en su posicion
        self.establecerPosicion(posicion)
    
    def dibujar(self, pantalla):
        pantalla.blit(self.imagen, self.rect)


class GO_BotonAtras(GO_Boton):
    def __init__(self, pantalla):
        GO_Boton.__init__(self, pantalla, "interfaces/botones/atras.png", (100, 360))
    
    def accion(self):
        self.pantalla.menu.ejecutarAtras()


class GO_BotonSalir(GO_Boton):
    def __init__(self, pantalla):
        GO_Boton.__init__(self, pantalla, "interfaces/botones/salir.png", (100, 480))
    
    def accion(self):
        self.pantalla.menu.ejecutarSalir()


class GO_GUI:
    def __init__(self, menu, nombreImagen):
        self.menu = menu
        self.imagen = GestorRecursos.CargarImagen(nombreImagen)
        self.imagen = pygame.transform.scale(self.imagen, (ANCHO_PANTALLA, ALTO_PANTALLA))
        self.GO_GUIelementos = []

    def eventos(self, lista_eventos):
        for evento in lista_eventos:
            if evento.type == MOUSEBUTTONDOWN:
                self.elementosClic = None
                for elemento in self.GO_GUIelementos:
                    if elemento.posicionEnElemento(evento.pos):
                        self.elementosClic = elemento
            if evento.type == MOUSEBUTTONUP:
                for elemento in self.GO_GUIelementos:
                    if elemento.posicionEnElemento(evento.pos):
                        if (elemento == self.elementosClic):
                            elemento.accion()

    def dibujar(self, pantalla):
        #Dibujamos imagen de fondo
        pantalla.blit(self.imagen, self.imagen.get_rect())
        #Dibujamos botones
        for elemento in self.GO_GUIelementos:
            elemento.dibujar(pantalla)

class GameOverGUI(GO_GUI):
    def __init__(self, menu, tipoGO):
        if tipoGO == "enhorabuena":
            GO_GUI.__init__(self, menu, "interfaces/fondos/enhorabuena.jpg")
        else:
            GO_GUI.__init__(self, menu, "interfaces/fondos/muerte.jpg")
        
        go_botonSalir = GO_BotonSalir(self)
        go_botonAtras = GO_BotonAtras(self)
        self.GO_GUIelementos.append(go_botonSalir)
        self.GO_GUIelementos.append(go_botonAtras)

class GameOver(Escena):
    def __init__(self, director, tipoGO):
         #Llamamos al constructor de la clase padre
        Escena.__init__(self, director)
        #Creamos la lista de pantallas
        self.listaPantallas = []
        #Creamos las pantallas que vamos a tener
        #y las metemos en la lista
        self.listaPantallas.append(GameOverGUI(self, tipoGO))
        self.tipoGO = tipoGO

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
                    self.retrocederPantalla()
            elif evento.type == pygame.QUIT:
                self.director.salirPrograma()
        #Se pasa la lista de eventos a la pantalla actual
        self.listaPantallas[self.pantallaActual].eventos(lista_eventos)

    def dibujar(self, pantalla):
        self.listaPantallas[self.pantallaActual].dibujar(pantalla)

    def salirPrograma(self):
        self.director.salirPrograma()
    
    def retrocederPantalla(self):
        self.director.salirEscena()

    def mostrarPantallaInicial(self):
        self.pantallaActual = 0
    
    def ejecutarAtras(self):
        self.director.salirEscena()

    def ejecutarSalir(self):
        self.director.salirPrograma()

    def encender_musica(self):
        GestorSonido.musica_menu_principal()