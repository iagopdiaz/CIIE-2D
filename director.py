import pygame, sys
from escena import *
from pygame.locals import *
from settings import *
from gestor_usuario import *

class Director:
    """Representa el objeto principal del juego.
    
    En lugar de gestionar en nuestro archivo main el bucle del 
    juego lo que vamos a hacer es crear un clase director que 
    será la encargada de gestionar nuestro bucle de juego, este 
    bucle recibirá una escena cualquiera y se encargará de 
    ejecutar sus métodos de actualizar, eventos y dibujar  
 
    Tiene que utilizar este objeto en conjunto con objetos
    derivados de Scene.  
    
    """
 
    def __init__(self):
        self.screen = pygame.display.set_mode((ANCHO_PANTALLA, ALTO_PANTALLA))
        pygame.display.set_caption(TITULO)
        
        #Configuracion Pantalla Completa
        self.pantallaCompleta = False
        try: 
            self.pantallaCompleta = GestorUsuario.get('pantalla_completa')
        except:
            pass       
        if self.pantallaCompleta:
            pygame.display.toggle_fullscreen()
            
        self.pila = []
        self.salir_escena = False
        #Musica
        self.reloj = pygame.time.Clock()
 
    def loop(self, escena):
        "Pone en funcionamiento el juego."
        self.salir_escena = False
        #Eliminamos todos los eventos producidos antes de entrar en el bucle
        pygame.event.clear()
        while not self.salir_escena:
            #Si se produce un evento de salir del juego, salimos ------------> ESTO NO VA AQUI HAY QUE CAMBIARLO
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.salirPrograma()
            #Sincronizar el juego a 60 fps
            tiempo_pasado = self.reloj.tick(60)
            #Pasamos los eventos a la escena
            escena.eventos(pygame.event.get())
            #Actualiza la escena 
            escena.update(tiempo_pasado)
            #Se dibuja en pantalla
            escena.dibujar(self.screen)
            pygame.display.flip()
    
    def pantallaCompleta(self):
        pygame.display.toggle_fullscreen()
        self.pantallaCompleta = not self.pantallaCompleta
        GestorUsuario.do_update('pantalla_completa',self.pantallaCompleta)
    
    def es_pantalla_completa(self):
        return self.pantallaCompleta
    
    def ejecutar(self):
        #Mientras haya escenas en la pila, ejecutamos la de arriba
        while (len(self.pila) > 0):
            #Se coge la escena a ejecutar como la que este en la cima de la pila
            escena = self.pila[len(self.pila) - 1]
            #if musica
            #Ejecutamos el bucle de eventos hasta que termine la escena
            self.loop(escena)

    def salirEscena(self):#(self,updateMuscia = True)
        #Indicamos en el flag que se quiere salir de la escena
        #update music
        self.salir_escena = True
        #Eliminamos la escena actual de la pila. La popeamos
        if (len(self.pila) > 0):
            self.pila.pop()
            if len(self.pila) == 0:
                self.salirEscena = True
                return
        
    def salirPrograma(self):
        #Vaciamos la lista de escenas pendientes
        self.pila = []
        self.salir_escena = True

    def cambiarEscena(self, escena):
        #update music
        self.salirEscena()
        #Ponemos la escena en la cima de la pila eliminando la anterior
        self.pila.append(escena)

    def apilarEscena(self, escena):
        #update music
        self.salir_escena = True
        #Ponemos la escena en la cima de la pila sin eliminar la anterior
        self.pila.append(escena)

