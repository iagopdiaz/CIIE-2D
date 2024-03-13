import pygame
from settings import *
from gestor_recursos import GestorRecursos
from observer import Observer
from partitura import Partitura
from fase import *

class InterfazUsuario(Observer):    
    def __init__(self, fase):
        #health
        #elementos musicales
        #inventario
        #imagen inventario
        self.fase = fase
        self.cargar_inventario("partitura", "partituras/partitura1.png") #Deberia ser una imagan de "no hay partitura"
        self.cargar_marco()
        self.cargar_vida()
        
    def cargar_inventario(self, tipo, imagen_partitura):
        if (tipo == "partitura"):
            font = GestorRecursos.CargarFuente(self, FUENTE1, 15)
            imagen_partitura = GestorRecursos.CargarImagen(imagen_partitura, -1)
            texto_surface = font.render("Inventario", True, (255, 255, 255))
            texto_rect = texto_surface.get_rect()
            lado_cuadrado = int(texto_rect.width * 0.75)
            nueva_imagen = pygame.transform.scale(imagen_partitura, (lado_cuadrado, lado_cuadrado))
            posicion_x = texto_rect.x
            posicion_y = texto_rect.y + texto_rect.height
            nueva_surface = pygame.Surface((texto_rect.width + lado_cuadrado + 10, max(texto_rect.height, lado_cuadrado)))
            nueva_surface.blit(texto_surface, (0, 0))
            nueva_surface.blit(nueva_imagen, (texto_rect.width + 10, 0))
            self.inventario_surface = nueva_surface
            self.inventario_rect = self.inventario_surface.get_rect()
            self.inventario_rect.topleft = (10, ALTO_PANTALLA - 50)
    
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
    
    def cargar_vida(self):
        if self.fase.vida_jugador == 3:
            self.vida = GestorRecursos.CargarImagen("interfaces/vida/vida1llena.png", -1)
        elif self.fase.vida_jugador == 2:
            self.vida = GestorRecursos.CargarImagen("interfaces/vida/vida2media.png", -1)
        elif self.fase.vida_jugador == 1:
            self.vida = GestorRecursos.CargarImagen("interfaces/vida/vida3baja.png", -1)
        self.vida_rect = self.vida.get_rect()
        self.vida_rect.center = (ANCHO_PANTALLA/2, 50)
    
    def dibujar(self, pantalla):
        pantalla.blit(self.inventario_surface, self.inventario_rect)
        #if (self.imagen_partitura != None and self.imagen_partitura_rect != None):
        #pantalla.blit(self.imagen_partitura, self.imagen_partitura_rect)
        pantalla.blit(self.marco1, self.marco1_rect)
        pantalla.blit(self.marco2, self.marco2_rect)
        pantalla.blit(self.marco3, self.marco3_rect)
        if self.fase.vida_jugador > 0:
            pantalla.blit(self.vida, self.vida_rect)
        
    def actualizar_observer(self, tipo, imagen):
        if tipo == "partitura":
            self.cargar_inventario(tipo,imagen)
        