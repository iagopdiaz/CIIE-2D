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
        self.partituras_surfaces = {}
        self.cargar_inventario("partituraX", "partituras/partituraX.png") 
        self.cargar_marco()
        self.cargar_vida1llena()
        self.cargar_vida2media()
        self.cargar_vida3vacia()
    
    def eliminar_partitura(self, tipo):
        if tipo is None:
            return
        if tipo in self.partitura_surfaces:
            del self.partitura_surfaces[tipo]


    def cargar_inventario(self, tipo, imagen_partitura):
        self.imagen_partitura = GestorRecursos.CargarImagen(imagen_partitura, -1)
        self.partitura_surface = self.imagen_partitura.get_rect()
        print("--------**ENTRADA IF CASOS***------------")  
        print(imagen_partitura)
        if (tipo == "partitura1" or "DELpartitura1"):
            print(tipo)
            print("1")
            self.partitura_surface.topleft = (60, 60)
        elif (tipo == "partitura2" or "DELpartitura2"):  
            print(tipo)
            print("2")
            self.partitura_surface.topleft = (60, 110)
        elif (tipo == "partitura3" or "DELpartitura3"): 
            self.partitura_surface.topleft = (60, 160)   
        else: #Primer caso
            self.partitura_surface.topleft = (16000, 16000)
            
        if tipo.startswith("DEL"):
            tipo_real = tipo[3:]  # Eliminar el prefijo "DEL"
            self.partituras_surfaces[tipo_real] = (GestorRecursos.CargarImagen("partituras/partituraX.png", -1), self.partitura_surface)
        else:
            self.partituras_surfaces[tipo] = (self.imagen_partitura, self.partitura_surface)   
        
        print("--------------------")
        print(self.partituras_surfaces.values())
        print("--------------------")  
        
                
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
        #Aquí puedes agregar cualquier lógica adicional necesaria para actualizar la interfaz de usuario
    
    def dibujar(self, pantalla):
        pantalla.blit(self.marco1, self.marco1_rect)
        pantalla.blit(self.marco2, self.marco2_rect)
        pantalla.blit(self.marco3, self.marco3_rect)
        
        print("no printeo por otra cosa")        
        for (imagen, surface) in self.partituras_surfaces.values():
            pantalla.blit(imagen, surface)
        
        #pantalla.blit(self.imagen_partitura, self.partitura_surface)
        if self.personaje.vida > 0:
            if self.personaje.vida == 3:
                pantalla.blit(self.vida1, self.vida1_rect)
            elif self.personaje.vida == 2:
                pantalla.blit(self.vida2, self.vida2_rect)
            else:
                pantalla.blit(self.vida3, self.vida3_rect)