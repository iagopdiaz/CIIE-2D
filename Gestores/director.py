import pygame, sys
from Ajustes.settings import *
from Gestores.gestor_usuario import *
from Escenarios.escena import *
import time
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
        pygame.init()
        self.screen = pygame.display.set_mode((ANCHO_PANTALLA, ALTO_PANTALLA))
        pygame.display.set_caption(TITULO)
             
        self.pila = []
        self.salir_escena = False
        self.musica = True
        self.reloj = pygame.time.Clock()
 
    def loop(self, escena):
        "Pone en funcionamiento el juego."
        self.salir_escena = False
        #Eliminamos todos los eventos producidos antes de entrar en el bucle
        pygame.event.clear()
        while not self.salir_escena:
            #Sincronizar el juego a 60 fps
            tiempo_pasado = self.reloj.tick(60)
            if (escena.eventos(pygame.event.get())):
                self.salirPrograma()
            # Actualiza la escena
            # Devuelve si se debe parar o no el juego
            if (escena.update(tiempo_pasado)):
                self.salirPrograma()
            #Se dibuja en pantalla
            escena.dibujar(self.screen)
            pygame.display.flip()
    
    
    def ejecutar(self):
        #Mientras haya escenas en la pila, ejecutamos la de arriba
            
        while (len(self.pila) > 0):
            #Se coge la escena a ejecutar como la que este en la cima de la pila
            escena = self.pila[len(self.pila) - 1]
            if self.musica:
                escena.encender_musica()
                escena.musica = False
                
            self.loop(escena)

        pygame.quit()
        sys.exit()

    def salirEscena(self, actualizarMusica = True):
        #Indicamos en el flag que se quiere salir de la escena
        self.musica = actualizarMusica
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


    def cambiarEscena(self, escena, actualizarMusica=True):
        self.musica = actualizarMusica
        self.salirEscena()
        self.apilarEscena(escena)



    def apilarEscena(self, escena, actualizarMusica = True):
        self.musica = actualizarMusica
        self.salir_escena = True
        #Ponemos la escena en la cima de la pila sin eliminar la anterior
        self.pila.append(escena)
        
    def volumenMusica(self):
        pass
    
    def volumenEfectos(self):
        pass    

