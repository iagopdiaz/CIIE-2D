from misprite import *
from gestor_recursos import *
from observable import Observable
from gestor_sonido import *

class Puerta(MiSprite, Observable):
    def __init__(self, partituras, imagen_puerta, area_activacion, tipo):
        # Llamamos al constructor de la clase padre
        MiSprite.__init__(self)
        Observable.__init__(self)
        observers = []
        
        #Cargamos la imagen de la puerta
        imagen_puerta = GestorRecursos.CargarImagen(imagen_puerta, colorkey=(112, 136, 168))
        
    
        # Creamos una lista para almacenar cada frame de la animación
        self.frames_puerta = []

        # Cargamos las coordenadas de las puertas
        datos = GestorRecursos.CargarArchivoCoordenadas("puertas/coordpuertas.txt")
        datos = datos.split("\n")
        acum = 0

        # Dividimos la imagen en 16 partes iguales
        for i in range(16):
            # Obtenemos las coordenadas de cada frame
            coord = datos[i].split(" ")

            #Aumentamos el acumulador para saber donde empezar a recortar
            acum += int(coord[0])

            # Creamos un rectángulo que representa la porción de la imagen que queremos
            rectangulo_frame = pygame.Rect(acum , 0, int(coord[1]), imagen_puerta.get_height())
        
            # Aumentamos el acumulador para la siguiente iteración
            acum += int(coord[1])

            # Obtenemos la imagen de ese frame
            frame = imagen_puerta.subsurface(rectangulo_frame)
            
            if tipo == 1:
                frame = pygame.transform.rotate(frame, -90)  # Rotamos 90 grados en sentido antihorario
                frame = pygame.transform.scale(frame, (131, 50))  # Ajustamos el tamaño si es necesario
            else:
                frame = pygame.transform.scale(frame, (50, 131))
        
            # Añadimos el frame a la lista
            self.frames_puerta.append(frame)
    
        # Establecemos el frame inicial (puerta cerrada)
        self.frame_actual = 15
        self.image = self.frames_puerta[self.frame_actual]

        #Obtenemos el rectangulo del sprite
        self.rect = self.image.get_rect()

        #Creamos un inventario para la puerta
        self.inventario = []

        #Establecemos las partituras necesarias para abrir la puerta
        self.partituras = partituras

        #Establecemos el area de activacion de la puerta
        self.area = area_activacion

        # Establecemos si la puerta esta abierta o cerrada
        self.abierta = False

        # Establecemos el retardo de la animación
        self.contador_retardo = 0

    def añadir_partitura(self, partitura):
        if partitura in self.partituras:
            self.inventario.append(partitura)
            print("Partitura añadida a la puerta, falta:", len(self.partituras)-len(self.inventario), "partituras")
            self.notificar_observers("accion", PUERTA_PARTITURA)
            return True
        self.notificar_observers("accion", PUERTA_PARTITURA_NO)
        return False
    
    def abrir_puerta(self):
        if self.frame_actual == 15: GestorSonido.reproducir_efecto(SONIDO_PUERTA)
        self.contador_retardo += 1
        if self.contador_retardo == 10:
            self.frame_actual -= 1
            self.contador_retardo = 0
            self.frame_actual = max(0, self.frame_actual)
            self.image = self.frames_puerta[self.frame_actual]
        if self.frame_actual == 0:
            self.abierta = True

    def update(self):
        #Abrir la puerta cuando todos los nombres esten en el inventario
        if all([partitura in self.inventario for partitura in self.partituras]) and not self.abierta:
            self.notificar_observers("accion", PUERTA_ABIERTA)
            self.abrir_puerta()
            return
    
    
    def notificar_observers(self, tipo, imagen):
        for observer in self.observers:
            if (tipo == "accion"):
                observer.actualizar_observer("accion", imagen) 
            else: 
                observer.actualizar_observer(tipo, imagen)
                
    def registrar_observador(self, observador):
        self.observers.append(observador)
            
    def eliminar_observador(self, observador):
        self.observers.remove(observador)             


    def escuchar(self, id_jugador):
        # Obtenemos las partituras que aún no se han añadido al inventario
        partituras_restantes = [partitura for partitura in self.partituras if partitura not in self.inventario]
        escuchado = False
        # Si hay partituras restantes, se reproduce la del jugador
        if partituras_restantes:
            #De las restantes, busca la que le corresponde al jugador
            for partitura in partituras_restantes:
                if partitura.jugador == id_jugador:
                    GestorSonido.reproducir_partitura(partitura.musica)
                    self.notificar_observers("accion", ESCUCHANDO)
                    escuchado = True
                    return
            if not escuchado:
                self.notificar_observers("accion", PUERTA_MAS_OTRO)
            