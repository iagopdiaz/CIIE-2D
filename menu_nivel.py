import pygame
from pygame.locals import *
from escena import *
from gestor_recursos import *
from fase import *


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


class BotonNivel1(Boton):
    def __init__(self, pantalla):
        Boton.__init__(self, pantalla, "menu/boton/nivel1.png", (100, 120))
    
    def accion(self):
        self.pantalla.menu.ejecutarNivel1()


class BotonNivel2(Boton):
    def __init__(self, pantalla):
        Boton.__init__(self, pantalla, "menu/boton/nivel2.png", (100, 240))
    
    def accion(self):
        self.pantalla.menu.ejecutarNivel2()


class BotonNivel3(Boton):
    def __init__(self, pantalla):
        Boton.__init__(self, pantalla, "menu/boton/nivel3.png", (100, 360))
    
    def accion(self):
        self.pantalla.menu.ejecutarNivel3()


class BotonAtras(Boton):
    def __init__(self, pantalla):
        Boton.__init__(self, pantalla, "menu/boton/atras.png", (100, 480))
    
    def accion(self):
        self.pantalla.menu.ejecutarAtras()


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
        #Dibujamos primero la imagen de fondo
        pantalla.blit(self.imagen, self.imagen.get_rect())
        #Despues los botones
        for elemento in self.GUIelementos:
            elemento.dibujar(pantalla)


class GUIInicial(GUI):
    def __init__(self, menu):
        GUI.__init__(self, menu, "menu/wallpaper.jpg")
        botonFase1 = BotonNivel1(self)
        botonFase2 = BotonNivel2(self)
        botonFase3 = BotonNivel3(self)
        botonAtras = BotonAtras(self)
        self.GUIelementos.append(botonFase1)
        self.GUIelementos.append(botonFase2)
        self.GUIelementos.append(botonFase3)
        self.GUIelementos.append(botonAtras)


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
        fase1 = Fase(self.director)
        self.director.cambiarEscena(fase1)
    
    def ejecutarNivel2(self):
        fase2 = Fase(self.director)
        self.director.cambiarEscena(fase2)
    
    def ejecutarNivel3(self):
        fase3 = Fase(self.director)
        self.director.cambiarEscena(fase3)
    
    def ejecutarAtras(self):
        self.director.salirEscena()
    
    def mostrarPantallaInicial(self):
        self.pantallaActual = 0