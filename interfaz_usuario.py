import pygame
from settings import *
from gestor_recursos import GestorRecursos
from observer import Observer
from partitura import Partitura

class InterfazUsuario(Observer):    
    def __init__(self, personaje):
        #health
        #elementos musicales
        #inventario
        #imagen inventario
        self.personaje = personaje
        self.cargar_inventario("partitura", "partituras/partituraX.png") 
        self.cargar_marco()
        self.cargar_vida1llena()
        self.cargar_vida2media()
        self.cargar_vida3vacia()
        
    def cargar_inventario(self, tipo, imagen_partitura):
        self.imagen_partitura = GestorRecursos.CargarImagen(imagen_partitura, -1)    
        self.partitura_surface = self.imagen_partitura.get_rect() 
        print("mal")
        if (tipo == "partitura1"):
            self.partitura_surface.topleft = (60, 60)
        elif (tipo == "partitura2"):  
            self.partitura_surface.topleft = (60, 110)
        elif (tipo == "partitura3"): 
            self.partitura_surface.topleft = (60, 160)  
        elif (tipo == "DELpartitura1"):
            self.partitura_surface.topleft = (60, 60)
        elif (tipo == "DELpartitura2"):  
            self.partitura_surface.topleft = (60, 110)
        elif (tipo == "DELpartitura3"): 
            self.partitura_surface.topleft = (60, 160)         
        else: 
            self.partitura_surface.topleft = (6000, 16000)  
            print("Error al cargar la partitura") 
            
    def cargar_marco(self):
        self.marco1 = GestorRecursos.CargarImagen("interfaces/inventario/inventarioPersonaje1.png", -1)
        self.marco2 = GestorRecursos.CargarImagen("interfaces/inventario/inventarioPersonaje2.png", -1)
        self.marco3 = GestorRecursos.CargarImagen("interfaces/inventario/inventarioPersonaje3.png", -1)
        self.marco1_rect = self.marco1.get_rect()
        self.marco2_rect = self.marco2.get_rect()
        self.marco3_rect = self.marco3.get_rect()
        self.marco1_rect.topleft = (50, 50)
        self.marco2_rect.topleft = (50, 100)
        self.marco3_rect.topleft = (50, 150)
    
    def cargar_vida1llena(self):
        self.vida1 = GestorRecursos.CargarImagen("interfaces/vida/vida1llena.png", -1)
        self.vida1_rect = self.vida1.get_rect()
        self.vida1_rect.center = (ANCHO_PANTALLA/2, 50)

    def cargar_vida2media(self):
        self.vida2 = GestorRecursos.CargarImagen("interfaces/vida/vida2media.png", -1)
        self.vida2_rect = self.vida2.get_rect()
        self.vida2_rect.center = (ANCHO_PANTALLA/2, 50)
    
    def cargar_vida3vacia(self):
        self.vida3 = GestorRecursos.CargarImagen("interfaces/vida/vida3baja.png", -1)
        self.vida3_rect = self.vida3.get_rect()
        self.vida3_rect.center = (ANCHO_PANTALLA/2, 50)

    def actualizar_jugador(self, jugador):
        self.personaje = jugador
        # Aquí puedes agregar cualquier lógica adicional necesaria para actualizar la interfaz de usuario
    
    def dibujar(self, pantalla):
        pantalla.blit(self.marco1, self.marco1_rect)
        pantalla.blit(self.marco2, self.marco2_rect)
        pantalla.blit(self.marco3, self.marco3_rect)
        pantalla.blit(self.imagen_partitura, self.partitura_surface)
        if self.personaje.vida > 0:
            if self.personaje.vida == 3:
                pantalla.blit(self.vida1, self.vida1_rect)
            elif self.personaje.vida == 2:
                pantalla.blit(self.vida2, self.vida2_rect)
            else:
                pantalla.blit(self.vida3, self.vida3_rect)
        
    def actualizar_observer(self, tipo, imagen):
        if tipo == "partitura":
            self.cargar_inventario(tipo,imagen)
        