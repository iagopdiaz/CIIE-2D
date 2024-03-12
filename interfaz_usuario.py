import pygame
from settings import *
from gestor_recursos import GestorRecursos
from observer import Observer
from partitura import Partitura

class InterfazUsuario(Observer):    
    def __init__(self):
        #health
        #elementos musicales
        #inventario
        #imagen inventario
        self.cargar_inventario("partitura", "partituras/partitura1.png") #Deberia ser una imagan de "no hay partitura"
        self.cargar_barra_vida()
        self.cargar_inventario_resto()
        
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
   
    def cargar_barra_vida(self):
        font = GestorRecursos.CargarFuente(self,FUENTE1, 30)  
        self.renderizado_barra_vida = font.render("BarraVida", True, (255,255,255)) #Añadir tmb nombre de partitura
        self.barra_vida_rect = self.renderizado_barra_vida.get_rect()
        self.barra_vida_rect.center = (ANCHO_PANTALLA/9, ALTO_PANTALLA/9.5) 
        
    def cargar_inventario_resto(self):
        font = GestorRecursos.CargarFuente(self,FUENTE1, 30)  
        self.renderizado_inventario_resto = font.render("Inventario Resto", True, (255,255,255)) #Añadir tmb nombre de partitura
        self.inventario_resto_rect = self.renderizado_inventario_resto.get_rect()
        self.inventario_resto_rect.center = (ANCHO_PANTALLA/1.5, ALTO_PANTALLA - ALTO_PANTALLA/10)        
    
    def dibujar(self, pantalla):
        pantalla.blit(self.inventario_surface, self.inventario_rect)
        #if (self.imagen_partitura != None and self.imagen_partitura_rect != None):
        #pantalla.blit(self.imagen_partitura, self.imagen_partitura_rect)
        pantalla.blit(self.renderizado_barra_vida, self.barra_vida_rect)  
        pantalla.blit(self.renderizado_inventario_resto, self.inventario_resto_rect)
        
    def actualizar_observer(self, tipo, imagen):
        if tipo == "partitura":
            self.cargar_inventario(tipo,imagen)
        