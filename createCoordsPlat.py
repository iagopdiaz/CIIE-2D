import pygame, os
from pygame.locals import *

class GestorRecursos:
    
    recursos = {}
            
    @classmethod
    def CargarImagen(cls, nombre, colorkey=None):
        # Si el nombre de archivo está entre los recursos ya cargados
        if nombre in cls.recursos:
            # Se devuelve ese recurso
            return cls.recursos[nombre]
        # Si no ha sido cargado anteriormente
        else:
            # Se carga la imagen indicando la carpeta en la que está
            fullname = os.path.join('imagenes', nombre)
            try:
                imagen = pygame.image.load(fullname)
            except pygame.error as message:
                print (f'Cannot load image: {fullname}')
                raise SystemExit(message)
            if colorkey != None:
                if colorkey == -1:
                    colorkey = imagen.get_at((0,0))
                imagen.set_colorkey(colorkey, RLEACCEL)
            # Se almacena
            cls.recursos[nombre] = imagen
            # Se devuelve

            return imagen
        
    @classmethod
    def guardar_imagen(cls, imagen, nombre_archivo):
        """Guarda una imagen en disco como PNG."""
        # Define la ruta completa donde quieres guardar la imagen
        ruta_completa = os.path.join('imagenes', f"{nombre_archivo}.png")
        try:
            # Guarda la imagen en la ruta especificada
            pygame.image.save(imagen, ruta_completa)
            print(f"Imagen guardada como: {ruta_completa}")
        except pygame.error as e:
            print(f"No se pudo guardar la imagen: {ruta_completa}")
            raise SystemExit(e)
        
imagen = GestorRecursos.CargarImagen("sonido.png", -1)
GestorRecursos.guardar_imagen(imagen, "sonido_vacio.png")

"""
elif evento.type == pygame.MOUSEBUTTONDOWN:
                if evento.button == 1:  # Botón izquierdo del ratón
                # Ajustar las posiciones iniciales con el desplazamiento actual
                    self.start_pos = (evento.pos[0] + self.scrollx, evento.pos[1] + self.scrolly)
            elif evento.type == pygame.MOUSEBUTTONUP:
                if evento.button == 1:  # Botón izquierdo del ratón
                    # Ajustar las posiciones finales con el desplazamiento actual
                    self.end_pos = (evento.pos[0] + self.scrollx, evento.pos[1] + self.scrolly)
                    # Calcula las coordenadas y dimensiones del rectángulo ajustadas al desplazamiento
                    x = min(self.start_pos[0], self.end_pos[0])
                    y = min(self.start_pos[1], self.end_pos[1])
                    ancho = abs(self.start_pos[0] - self.end_pos[0])
                    alto = abs(self.start_pos[1] - self.end_pos[1])
                    print(f'x: {x}, y: {y}, ancho: {ancho}, alto: {alto}')
                    with open('./imagenes/coordPlataformas.txt', 'a') as archivo:
                        archivo.write(f'{int(x)} {int(y)} {int(ancho)} {int(alto)}\n')
                    # Aquí podrías agregar una función para guardar estas coordenadas en un archivo

"""