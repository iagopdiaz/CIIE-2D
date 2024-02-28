# Módulos
import pygame
import sys
 
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
        self.screen = pygame.display.set_mode((640, 480))
        pygame.display.set_caption("Nombre Proyecto")
        self.scene = None
        self.quit_flag = False
        self.clock = pygame.time.Clock()
 
    def loop(self):
        "Pone en funcionamiento el juego."
 
        while not self.quit_flag:
            time = self.clock.tick(60)
             
            # Eventos de Salida
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.quit()
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_ESCAPE:
                        self.quit()
 
            # detecta eventos
            self.scene.on_event()
 
            # actualiza la escena
            self.scene.on_update()
 
            # dibuja la pantalla
            self.scene.on_draw(self.screen)
            pygame.display.flip()
 
    def change_scene(self, scene):
        "Altera la escena actual."
        self.scene = scene
 
    def quit(self):
        self.quit_flag = True
        
        
        
        
""""
main.py


import pygame
import director
import escena_implementada (menu,pausa,menu_inicio,configuracion,gameover, la partida en si)
 
def main():
    dir = director.Director()
    scene = scene_home.SceneHome(dir)
    dir.change_scene(scene)
    dir.loop()
 
if __name__ == '__main__':
    pygame.init()
    main()



"""