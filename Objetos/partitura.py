from Personajes.misprite import *
from Gestores.gestor_recursos import *
from Gestores.gestor_sonido import *

class Partitura(MiSprite):
    def __init__(self, imagen_partitura, nombre, id_jugador):
        #Invocamos al constructor de la clase padre
        MiSprite.__init__(self)

        #Cargamos la imagen de la partitura
        self.image = GestorRecursos.CargarImagen(imagen_partitura, -1)
        self.image = pygame.transform.scale(self.image, (40, 40))  # Escala la imagen
        self.archivoImagen = imagen_partitura
        #Obtenemos el rectangulo del sprite
        self.rect = self.image.get_rect()

        #Establecemos a que jugador pertenece la partitura
        self.jugador = id_jugador

        #Establecemos el nombre de la partitura
        self.nombre = nombre

        #Falta la musica de la partitura
        self.musica = GestorSonido.get_partitura(nombre)