import pygame

ANCHO_PANTALLA = 800
ALTO_PANTALLA = 600

class Escena:
    """Representa un escena abstracta del videojuego.
 
    Una escena es una parte visible del juego, como una pantalla
    de presentación o menú de opciones. Tiene que crear un objeto
    derivado de esta clase para crear una escena utilizable.
    
    """
 
    def __init__(self, director):
        self.director = director
 
    def update(self):
        "Actualización lógica que se llama automáticamente desde el director."
        raise NotImplemented("Tiene que implementar el método on_update.")
 
    def eventos(self, event):
        "Se llama cuando llega un evento especifico al bucle."
        raise NotImplemented("Tiene que implementar el método on_event.")
 
    def dibujar(self, screen):
        "Se llama cuando se quiere dibujar la pantalla."
        raise NotImplemented("Tiene que implementar el método on_draw.")
    def encender_musica(self):
        "Se llama cuando se quiere encender la música."
        raise NotImplemented("Tiene que implementar el método encender_musica.")
    
class EscenaPygame(Escena):

    def __init__(self, director):
        Escena.__init__(self, director)
        # Inicializamos la libreria de pygame (si no esta inicializada ya)
        pygame.init()
        # Creamos la pantalla (si no esta creada ya)
        self.screen = pygame.display.set_mode((ANCHO_PANTALLA, ALTO_PANTALLA))
