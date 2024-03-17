import pygame
from pygame.locals import *
from escena import *
from gestor_recursos import *
from fase import *
from menu_nivel import *
from GUIElemento import GUIElemento


class Boton(GUIElemento):
    def __init__(self, pantalla, nombreImagen, posicion):
        #Se carga la imagen del boton
        self.imagen = GestorRecursos.CargarImagen(nombreImagen, -1)
        self.rect = self.imagen.get_rect()

        #Se llama al metodo de la clase padre con el rectangulo que ocupa el boton
        GUIElemento.__init__(self, pantalla, self.rect)
        #Se coloca el rectangulo en su posicion
        self.establecerPosicion(posicion)
    
    def dibujar(self, pantalla):
        pantalla.blit(self.imagen, self.rect)


class BotonJugar(Boton):
    def __init__(self, pantalla):
        Boton.__init__(self, pantalla, BOTON_JUGAR, (100, 120))
    
    def accion(self):
        self.pantalla.menu.ejecutarJugar()


class BotonNivel(Boton):
    def __init__(self, pantalla):
        Boton.__init__(self, pantalla, BOTON_NIVEL, (100, 240))
    
    def accion(self):
        self.pantalla.menu.ejecutarNivel()


class BotonAjuste(Boton):
    def __init__(self, pantalla):
        Boton.__init__(self, pantalla, BOTON_AJUSTES, (100, 360))
    
    def accion(self):
        self.pantalla.menu.ejecutarAjustes()


class BotonSalir(Boton):
    def __init__(self, pantalla):
        Boton.__init__(self, pantalla, BOTON_SALIR, (100, 480))
    
    def accion(self):
        self.pantalla.menu.ejecutarSalir()


class BotonPantallaCompleta(Boton):
    def __init__(self, pantalla):
        Boton.__init__(self, pantalla, BOTON_PANTALLA_COMPLETA, (100, 360))
    
    def accion(self):
        self.pantalla.menu.ejecutarPantallaCompleta()


class BotonAtras(Boton):
    def __init__(self, pantalla):
        Boton.__init__(self, pantalla, BOTON_ATRAS, (100, 480))
    
    def accion(self):
        self.pantalla.menu.ejecutarAtras()


class TextoBotonVolumenMusica(Boton):
    def __init__(self, pantalla):
        Boton.__init__(self, pantalla, BOTON_VOL_MUSICA, (100, 120))
    
    def accion(self):
        # No hace nada. Realmente es un texto. Formato botón por comodidad y para mantener estética del menú
        pass


class BotonBajarMusica(Boton):
    def __init__(self, pantalla):
        Boton.__init__(self, pantalla, BOTON_BAJAR, (490, 120))
    
    def accion(self):
        self.pantalla.menu.ejecutarBajarVolumenMusica()       


class BotonSubirMusica(Boton):
    def __init__(self, pantalla):
        Boton.__init__(self, pantalla, BOTON_SUBIR, (668, 120))
    
    def accion(self):
        self.pantalla.menu.ejecutarSubirVolumenMusica()


class TextoBotonVolumenEfectos(Boton):
    def __init__(self, pantalla):
        Boton.__init__(self, pantalla, BOTON_VOL_EFECTOS, (100, 240))
    
    def accion(self):
        # No hace nada. Realmente es un texto. Formato botón por comodidad y para mantener estética del menú
        pass


class BotonBajarEfectos(Boton):
    def __init__(self, pantalla):
        Boton.__init__(self, pantalla, BOTON_BAJAR, (490, 240))
    def accion(self):
        self.pantalla.menu.ejecutarBajarVolumenEfectos()

           
class BotonSubirEfectos(Boton):
    def __init__(self, pantalla):
        Boton.__init__(self, pantalla, BOTON_SUBIR, (668, 240))
    
    def accion(self):
        self.pantalla.menu.ejecutarSubirVolumenEfectos()        


class BotonVolumenMusica(Boton):
    def __init__(self, pantalla):
        Boton.__init__(self, pantalla, NIVEL_VOLUMEN, (550, 100))
    
    def dibujar(self, pantalla):
        imagen_escalada = pygame.transform.scale(self.imagen, (int(self.imagen.get_width() * 2), int(self.imagen.get_height() * 1.5)))
        pantalla.blit(imagen_escalada, self.rect)
        fuente = GestorRecursos.CargarFuente(self, FUENTE1, 25)
        texto = fuente.render(str(GestorSonido.obtener_volumen_musica()), 1, (10, 10, 10))
        pantalla.blit(texto, (self.rect.x + 30, self.rect.y + 24))


class BotonVolumenEfectos(Boton):
    def __init__(self, pantalla):
        Boton.__init__(self, pantalla, NIVEL_VOLUMEN, (550, 220))
    
    def dibujar(self, pantalla):
        imagen_escalada = pygame.transform.scale(self.imagen, (int(self.imagen.get_width() * 2), int(self.imagen.get_height() * 1.5)))
        pantalla.blit(imagen_escalada, self.rect)
        fuente = GestorRecursos.CargarFuente(self, FUENTE1, 25)
        texto = fuente.render(str(GestorSonido.obtener_volumen_efectos()), 1, (10, 10, 10))
        pantalla.blit(texto, (self.rect.x + 30, self.rect.y + 24))
