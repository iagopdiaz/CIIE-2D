import pygame, os
from pygame.locals import *

# Singleton
class GestorRecursos:
    
    recursos = {}

    dialogo_0 = "\dialogos\nivel_0.txt"  
    
            
    @classmethod
    def CargarImagen(cls, nombre, colorkey=None):
        # Si el nombre de archivo está entre los recursos ya cargados
        if nombre in cls.recursos:
            # Se devuelve ese recurso
            return cls.recursos[nombre]
        # Si no ha sido cargado anteriormente
        else:
            # Se carga la imagen indicando la carpeta en la que está
            fullname = os.path.join('imagenes/', nombre)
            try:
                imagen = pygame.image.load(fullname)
            except pygame.error as message:
                print (f'Cannot load image: {fullname}')
                raise SystemExit(message)
            imagen = imagen.convert()
            if colorkey != None:
                if colorkey == -1:
                    colorkey = imagen.get_at((0,0))
                imagen.set_colorkey(colorkey, RLEACCEL)
            # Se almacena
            cls.recursos[nombre] = imagen
            # Se devuelve
            return imagen

    @classmethod
    def CargarArchivoCoordenadas(cls, nombre):
        # Si el nombre de archivo está entre los recursos ya cargados
        if nombre in cls.recursos:
            # Se devuelve ese recurso
            return cls.recursos[nombre]
        # Si no ha sido cargado anteriormente
        else:
            # Se carga el recurso indicando el nombre de su carpeta
            fullname = os.path.join('imagenes', nombre)
            pfile=open(fullname,'r')
            datos=pfile.read()
            pfile.close()
            # Se almacena
            cls.recursos[nombre] = datos
            # Se devuelve
            return datos
        
    @classmethod    
    def CargarCoordenadasParedes(cls, nombre):
        if nombre in cls.recursos:
            return cls.recursos[nombre]
        else:
            fullname = os.path.join('imagenes/mapa', nombre)  # Asegúrate de que el archivo esté en la carpeta correcta
            with open(fullname, 'r') as pfile:
                datos = pfile.readlines()
            cls.recursos[nombre] = datos
            return datos    
    
    
    @classmethod
    def CargarPartituras(cls, nombre):
        # Si el nombre de archivo está entre los recursos ya cargados
        if nombre in cls.recursos:
            # Se devuelve ese recurso
            return cls.recursos[nombre]
        # Si no ha sido cargado anteriormente
        else:
            # Se carga el recurso indicando el nombre de su carpeta
            fullname = os.path.join('imagenes/mapa', nombre)
            with open(fullname, 'r') as pfile:
                lineas = pfile.read().splitlines()
                datos = []
                for i in range(0, len(lineas), 2):
                    # Split the name and player field
                    nombre, jugador = lineas[i].split(' - ')
                    coords = lineas[i+1]
                    datos.append({'nombre': nombre, 'coords': coords, 'jugador': int(jugador)})
            # Se almacena
            cls.recursos[nombre] = datos
            # Se devuelve
            return datos
        
    @classmethod
    def CargarPuertas(cls, nombre):
        # Si el nombre de archivo está entre los recursos ya cargados
        if nombre in cls.recursos:
            # Se devuelve ese recurso
            return cls.recursos[nombre]
        # Si no ha sido cargado anteriormente
        else:
            # Se carga el recurso indicando el nombre de su carpeta
            fullname = os.path.join('imagenes/mapa', nombre)
            with open(fullname, 'r') as pfile:
                lineas = pfile.read().splitlines()
                datos = []
                for i in range(0, len(lineas), 3):
                    # Extract the names from the brackets and split by '][' to get a list of names
                    nombres = lineas[i].strip('[]').split('][')
                    coords_foto = lineas[i+1]
                    coords_area = lineas[i+2]
                    datos.append({'nombre': nombres, 'coords_foto': coords_foto, 'coords_area': coords_area})
            # Se almacena
            cls.recursos[nombre] = datos
            # Se devuelve
            return datos

    @classmethod
    def CargarCubos(cls, nombre):
        if nombre in cls.recursos:
            return cls.recursos[nombre]
        else:
            fullname = os.path.join('imagenes/mapa', nombre)  # Asegúrate de que el archivo esté en la carpeta correcta
            with open(fullname, 'r') as pfile:
                datos = pfile.readlines()
            cls.recursos[nombre] = datos
            return datos    
       
        
    @classmethod
    def CargarImagenCubos(cls, nombre, colorkey=None):
        # Si el nombre de archivo está entre los recursos ya cargados
        if nombre in cls.recursos:
            # Se devuelve ese recurso
            return cls.recursos[nombre]
        # Si no ha sido cargado anteriormente
        else:
            # Se carga la imagen indicando la carpeta en la que está
            fullname = os.path.join('imagenes/cubos', nombre)
            try:
                imagen = pygame.image.load(fullname)
            except pygame.error as message:
                print (f'Cannot load image: {fullname}')
                raise SystemExit(message)
            imagen = imagen.convert()
            if colorkey != None:
                if colorkey == -1:
                    colorkey = imagen.get_at((0,0))
                imagen.set_colorkey(colorkey, RLEACCEL)
            # Se almacena
            cls.recursos[nombre] = imagen
            # Se devuelve
            return imagen 
        
    @classmethod
    def CargarImagenAtaque(cls, nombre, colorkey=None):
        # Si el nombre de archivo está entre los recursos ya cargados
        if nombre in cls.recursos:
            # Se devuelve ese recurso
            return cls.recursos[nombre]
        # Si no ha sido cargado anteriormente
        else:
            # Se carga la imagen indicando la carpeta en la que está
            fullname = os.path.join('imagenes/ataques', nombre)
            try:
                imagen = pygame.image.load(fullname)
            except pygame.error as message:
                print (f'Cannot load image: {fullname}')
                raise SystemExit(message)
            imagen = imagen.convert()
            if colorkey != None:
                if colorkey == -1:
                    colorkey = imagen.get_at((0,0))
                imagen.set_colorkey(colorkey, RLEACCEL)
            # Se almacena
            cls.recursos[nombre] = imagen
            # Se devuelve
            return imagen 
        
    @classmethod
    def CargarCoordenadasAtaque(cls, nombre):
        # Si el nombre de archivo está entre los recursos ya cargados
        if nombre in cls.recursos:
            # Se devuelve ese recurso
            return cls.recursos[nombre]
        # Si no ha sido cargado anteriormente
        else:
            # Se carga el recurso indicando el nombre de su carpeta
            fullname = os.path.join('imagenes/ataques', nombre)
            pfile=open(fullname,'r')
            datos=pfile.read()
            pfile.close()
            # Se almacena
            cls.recursos[nombre] = datos
            # Se devuelve
            return datos
        
    @classmethod
    def CargarImagenPinchos(cls, orientacion, colorkey=None):
        # Si el nombre de archivo está entre los recursos ya cargados
        nombre = "spritePinchos" + str(orientacion) + ".png"
        if nombre in cls.recursos:
            # Se devuelve ese recurso
            return cls.recursos[nombre]
        # Si no ha sido cargado anteriormente
        else:
            # Se carga la imagen indicando la carpeta en la que está
            fullname = os.path.join('imagenes/pinchos', nombre)
            try:
                imagen = pygame.image.load(fullname)
            except pygame.error as message:
                print (f'Cannot load image: {fullname}')
                raise SystemExit(message)
            imagen = imagen.convert()
            if colorkey != None:
                if colorkey == -1:
                    colorkey = imagen.get_at((0,0))
                imagen.set_colorkey(colorkey, RLEACCEL)
            # Se almacena
            cls.recursos[nombre] = imagen
            # Se devuelve
            return imagen 
        
    @classmethod
    def CargarCoordenadasPinchos(cls, nombre):
        if nombre in cls.recursos:
            return cls.recursos[nombre]
        else:
            fullname = os.path.join('imagenes/mapa', nombre)  # Asegúrate de que el archivo esté en la carpeta correcta
            with open(fullname, 'r') as pfile:
                datos = pfile.readlines()
            cls.recursos[nombre] = datos
            return datos  
        
    def CargarFuente(self,fuente,tamano):
        #Cargar fuente y tamaño. Habria que comprobar si ya ha sido cargada
        try:
            fuente = pygame.font.Font(fuente,tamano)
        except (pygame.error):
            print('Cannot load font: ', fuente)
            raise SystemExit
        
        return fuente
        
    @classmethod
    def CargarDialogo(cls, nombre):
        # Si el nombre de archivo está entre los recursos ya cargados
        if nombre in cls.recursos:
            # Se devuelve ese recurso
            return cls.recursos[nombre]
        # Si no ha sido cargado anteriormente
        else:
            # Se carga el recurso indicando el nombre de su carpeta
            fullname = os.path.join('dialogos', nombre)
            with open(fullname, 'r', encoding='utf-8') as pfile:
                lineas = pfile.read().splitlines()
                datos = []
                for linea in lineas:
                    # Divide la línea en nombre y frase
                    nombre, frase = linea.split(' && ')
                    datos.append((nombre, frase))
            # Se almacena
            cls.recursos[nombre] = datos
            # Se devuelve
            return datos
    