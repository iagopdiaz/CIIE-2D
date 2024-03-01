from misprite import *
from gestor_recursos import *

class Partitura(MiSprite):
    def __init__(self, id, imagen_partitura, nombre):
        #Invocamos al constructor de la clase padre
        MiSprite.__init__(self)

        #Cargamos la imagen de la partitura
        self.image = GestorRecursos.CargarImagen(imagen_partitura, -1)
        self.image = pygame.transform.scale(self.image, (18, 30))  # Escala la imagen

        #Obtenemos el rectangulo del sprite
        self.rect = self.image.get_rect()

        #Establecemos el id de la partitura
        self.id = id

        #Establecemos el nombre de la partitura
        self.nombre = nombre

        #Falta la musica de la partitura
        #self.musica = GestorRecursos.CargarMusica(musica_partitura)




        