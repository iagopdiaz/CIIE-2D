from misprite import *
from gestor_recursos import *

class Puerta(MiSprite):
    def __init__(self, nombre, imagen_puerta, area_activacion):
        # Llamamos al constructor de la clase padre
        MiSprite.__init__(self)

        #Cargamos la imagen de la puerta
        imagen_puerta = GestorRecursos.CargarImagen(imagen_puerta, colorkey=(112, 136, 168))

        # Calculamos el ancho de cada frame de la animación
        ancho_frame = imagen_puerta.get_width() // 16
    
        # Creamos una lista para almacenar cada frame de la animación
        self.frames_puerta = []
    
        # Dividimos la imagen en 16 partes iguales
        for i in range(16):
            # Creamos un rectángulo que representa la porción de la imagen que queremos
            rectangulo_frame = pygame.Rect(i * ancho_frame, 0, ancho_frame, imagen_puerta.get_height())
        
            # Obtenemos la imagen de ese frame
            frame = imagen_puerta.subsurface(rectangulo_frame)
            frame = pygame.transform.scale(frame, (50, 131))
        
            # Añadimos el frame a la lista
            self.frames_puerta.append(frame)
    
        # Establecemos el frame inicial (puerta cerrada)
        self.frame_actual = 15
        self.image = self.frames_puerta[self.frame_actual]

        #Obtenemos el rectangulo del sprite
        self.rect = self.image.get_rect()

        #Establecemos el nombre de la puerta (para saber que partitura la desbloquea)
        self.nombre = nombre

        #Establecemos el area de activacion de la puerta
        self.area = area_activacion

        # Establecemos si la puerta esta abierta o cerrada
        self.abierta = False

        # Establecemos el retardo de la animación
        self.retardo_animacion = 7
        self.contador_retardo = 0


    def update(self, tiempo):#CORREGIR -> No se si la animacion va aqui creo que no
        # Si la puerta está abierta no hacemos nada                           #CORREGIR: abierto=True cuando acaba la animacion
        if self.abierta:
            # Disminuimos el frame actual para abrir la puerta
            self.contador_retardo += 1
            
            if self.contador_retardo == self.retardo_animacion:
                self.frame_actual -= 1
                self.contador_retardo = 0
                # Nos aseguramos de que el frame actual no sea menor que 0
                self.frame_actual = max(0, self.frame_actual)
                
                # Actualizamos la imagen de la puerta con el frame actual de la animación
                self.image = self.frames_puerta[self.frame_actual]

