import pygame
from pygame.locals import *
from escena import *
from gestor_recursos import *
from fase import *
from menu_nivel import *


class GUIElemento:
    def __init__(self, pantalla, rectangulo):
        self.pantalla = pantalla
        self.rectangulo = rectangulo
    
    def establecerPosicion(self, posicion):
        (posicionx, posiciony) = posicion
        self.rect.left = posicionx
        self.rect.bottom = posiciony
    
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


class Boton(GUIElemento):
    def __init__(self, pantalla, nombreImagen, posicion):
        #Se carga la imagen del boton
        self.imagen = GestorRecursos.CargarImagen(nombreImagen, -1)
        self.imagen = pygame.transform.scale(self.imagen, (160, 32))
        self.rect = self.imagen.get_rect()

        #Se llama al metodo de la clase padre con el rectangulo que ocupa el boton
        GUIElemento.__init__(self, pantalla, self.rect)
        #Se coloca el rectangulo en su posicion
        self.establecerPosicion(posicion)
    
    def dibujar(self, pantalla):
        pantalla.blit(self.imagen, self.rect)


class BotonJugar(Boton):
    def __init__(self, pantalla):
        Boton.__init__(self, pantalla, "menu/boton/jugar.png", (100, 150))
    
    def accion(self):
        self.pantalla.menu.ejecutarJugar()


class BotonNivel(Boton):
    def __init__(self, pantalla):
        Boton.__init__(self, pantalla, "menu/boton/nivel.png", (100, 300))
    
    def accion(self):
        self.pantalla.menu.ejecutarNivel()


class BotonSalir(Boton):
    def __init__(self, pantalla):
        Boton.__init__(self, pantalla, "menu/boton/salir.png", (100, 450))
    
    def accion(self):
        self.pantalla.menu.ejecutarSalir()


class GUI:
    def __init__(self, menu, nombreImagen):
        self.menu = menu
        self.imagen = GestorRecursos.CargarImagen(nombreImagen)
        self.imagen = pygame.transform.scale(self.imagen, (ANCHO_PANTALLA, ALTO_PANTALLA))
        self.GUIelementos = []

    def eventos(self, lista_eventos):
        for evento in lista_eventos:
            if evento.type == MOUSEBUTTONDOWN:
                self.elementosClic = None
                for elemento in self.GUIelementos:
                    if elemento.posicionEnElemento(evento.pos):
                        self.elementosClic = elemento
            if evento.type == MOUSEBUTTONUP:
                for elemento in self.GUIelementos:
                    if elemento.posicionEnElemento(evento.pos):
                        if (elemento == self.elementosClic):
                            elemento.accion()

    def dibujar(self, pantalla):
        #Dibujamos imagen de fondo
        pantalla.blit(self.imagen, self.imagen.get_rect())
        #Dibujamos botones
        for elemento in self.GUIelementos:
            elemento.dibujar(pantalla)


class GUIInicial(GUI):
    def __init__(self, menu):
        GUI.__init__(self, menu, "menu/wallpaper.jpg")
        botonJugar = BotonJugar(self)
        botonNivel = BotonNivel(self)
        botonSalir = BotonSalir(self)
        self.GUIelementos.append(botonJugar)
        self.GUIelementos.append(botonNivel)
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
        fase = Fase(self.director)
        self.director.apilarEscena(fase)
    
    def ejecutarNivel(self):
        menuSelect = MenuNivel(self.director)
        self.director.apilarEscena(menuSelect)

    def ejecutarSalir(self):
        self.director.salirPrograma()

    def mostrarPantallaInicial(self):
        self.pantallaActual = 0