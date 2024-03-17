import pygame
from settings import *
from gestor_recursos import GestorRecursos
from observer import Observer
from partitura import Partitura

class InterfazUsuario(Observer):    
    def __init__(self, personaje):
        #Inicializamos la interfaz de usuario   
        self.personaje = personaje
        self.partituras_surfaces = {}
        self.cargar_inventario("partituraX", "partituras/partituraX.png") 
        self.cargar_marco()
        self.cargar_vida1()
        self.cargar_vida2()
        self.cargar_vida3()
        self.cargar_vida4()
        self.cargar_vida5()

    #Carga sobre los marcos del inventario las partirutas disponibles de cada personaje
    def cargar_inventario(self, tipo, imagen_partitura):
        self.imagen_partitura = GestorRecursos.CargarImagen(imagen_partitura, -1)
        self.partitura_surface = self.imagen_partitura.get_rect()
        if tipo == "partitura1" or tipo == "DELpartitura1":
            self.partitura_surface.topleft = (60, 60)
        elif tipo == "partitura2" or tipo == "DELpartitura2":  
            self.partitura_surface.topleft = (60, 110)
        elif tipo == "partitura3" or tipo == "DELpartitura3": 
            self.partitura_surface.topleft = (60, 160)   
        else: #Primer caso inventario vacio
            self.partitura_surface.topleft = (16000, 16000)
            
        if tipo.startswith("DEL"):
            tipo_real = tipo[3:]  
            self.partituras_surfaces[tipo_real] = (GestorRecursos.CargarImagen("partituras/partituraX.png", -1), self.partitura_surface)
        else:
            self.partituras_surfaces[tipo] = (self.imagen_partitura, self.partitura_surface)   
        
    #Carga el marco sobre el que se dibujarán las partituras            
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
    
    #Carga las vida del personaje
    def cargar_vida1(self):
        self.vida11 = GestorRecursos.CargarImagen(VIDA, -1)
        self.vida12 = GestorRecursos.CargarImagen(VIDA, -1)        
        self.vida13 = GestorRecursos.CargarImagen(VIDA, -1)
        self.vida12_rect = self.vida12.get_rect()
        self.vida12_rect.center = (ANCHO_PANTALLA/2, 50)
        self.vida13_rect = self.vida13.get_rect()
        self.vida13_rect.center = (ANCHO_PANTALLA/2+40, 50)
        self.vida11_rect = self.vida11.get_rect()
        self.vida11_rect.center = (ANCHO_PANTALLA/2-40, 50)
    
    #Carga las vida del personaje
    def cargar_vida2(self):
        self.vida21 = GestorRecursos.CargarImagen(VIDA, -1)
        self.vida22 = GestorRecursos.CargarImagen(VIDA, -1)
        self.vida21_rect = self.vida21.get_rect()
        self.vida21_rect.center = (ANCHO_PANTALLA/2-20, 50)
        self.vida22_rect = self.vida22.get_rect()
        self.vida22_rect.center = (ANCHO_PANTALLA/2+20, 50)
    
    #Carga las vida del personaje
    def cargar_vida3(self):
        self.vida3 = GestorRecursos.CargarImagen(VIDA, -1)
        self.vida3_rect = self.vida3.get_rect()
        self.vida3_rect.center = (ANCHO_PANTALLA/2, 50)

    def cargar_vida4(self):
        self.vida41 = GestorRecursos.CargarImagen(VIDA, -1)
        self.vida42 = GestorRecursos.CargarImagen(VIDA, -1)
        self.vida43 = GestorRecursos.CargarImagen(VIDA, -1)
        self.vida44 = GestorRecursos.CargarImagen(VIDA, -1)
        self.vida41_rect = self.vida41.get_rect()
        self.vida41_rect.center = (ANCHO_PANTALLA/2-60, 50)
        self.vida42_rect = self.vida42.get_rect()
        self.vida42_rect.center = (ANCHO_PANTALLA/2-20, 50)
        self.vida43_rect = self.vida43.get_rect()
        self.vida43_rect.center = (ANCHO_PANTALLA/2+20, 50)
        self.vida44_rect = self.vida44.get_rect()
        self.vida44_rect.center = (ANCHO_PANTALLA/2+60, 50)
        
    def cargar_vida5(self):
        self.vida51 = GestorRecursos.CargarImagen(VIDA, -1)
        self.vida52 = GestorRecursos.CargarImagen(VIDA, -1)
        self.vida53 = GestorRecursos.CargarImagen(VIDA, -1)
        self.vida54 = GestorRecursos.CargarImagen(VIDA, -1)
        self.vida55 = GestorRecursos.CargarImagen(VIDA, -1)
        self.vida51_rect = self.vida51.get_rect()
        self.vida51_rect.center = (ANCHO_PANTALLA/2-80, 50)
        self.vida52_rect = self.vida52.get_rect()
        self.vida52_rect.center = (ANCHO_PANTALLA/2-40, 50)
        self.vida53_rect = self.vida53.get_rect()
        self.vida53_rect.center = (ANCHO_PANTALLA/2, 50)
        self.vida54_rect = self.vida54.get_rect()
        self.vida54_rect.center = (ANCHO_PANTALLA/2+40, 50)
        self.vida55_rect = self.vida55.get_rect()
        self.vida55_rect.center = (ANCHO_PANTALLA/2+80, 50)
        
        
        
    def actualizar_jugador(self, jugador):
       self.personaje = jugador
    
       
    def dibujar(self, pantalla):
        pantalla.blit(self.marco1, self.marco1_rect)
        pantalla.blit(self.marco2, self.marco2_rect)
        pantalla.blit(self.marco3, self.marco3_rect)
        
        #Dibujamos las partituras para cada uno de los personajes
        for (imagen, surface) in self.partituras_surfaces.values():
            pantalla.blit(imagen, surface)
        
        #Dibujamos la vida del personaje
        if self.personaje.vida > 0:
            if self.personaje.vida == 5:
                pantalla.blit(self.vida51, self.vida51_rect)
                pantalla.blit(self.vida52, self.vida52_rect)
                pantalla.blit(self.vida53, self.vida53_rect)
                pantalla.blit(self.vida54, self.vida54_rect)
                pantalla.blit(self.vida55, self.vida55_rect) 
            elif self.personaje.vida == 4:
                pantalla.blit(self.vida41, self.vida41_rect)
                pantalla.blit(self.vida42, self.vida42_rect)
                pantalla.blit(self.vida43, self.vida43_rect)
                pantalla.blit(self.vida44, self.vida44_rect)      
            elif self.personaje.vida == 3:
                pantalla.blit(self.vida11, self.vida11_rect)
                pantalla.blit(self.vida12, self.vida12_rect)
                pantalla.blit(self.vida13, self.vida13_rect)
            elif self.personaje.vida == 2:
                pantalla.blit(self.vida21, self.vida21_rect)
                pantalla.blit(self.vida22, self.vida22_rect)
            else:
                pantalla.blit(self.vida3, self.vida3_rect)