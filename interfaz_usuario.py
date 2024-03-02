import pygame
from settings import *
from gestor_recursos import GestorRecursos
from observer import Observer

class InterfazUsuario(Observer):
    def __init__(self):
        #health
        #elementos musicales
        #inventario
        self.cargar_inventario()
        self.cargar_barra_vida()
        self.cargar_inventario_resto()
        
    def cargar_inventario(self):
        font = GestorRecursos.CargarFuente(self,FUENTE1, 15)  
        self.renderizado_inventario = font.render("Inventario", True, (255,255,255)) #Añadir tmb nombre de partitura
        self.inventario_rect = self.renderizado_inventario.get_rect()
        self.inventario_rect.center = (ANCHO_PANTALLA/9, ALTO_PANTALLA - ALTO_PANTALLA/10)  
        
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
        pantalla.blit(self.renderizado_inventario, self.inventario_rect)  
        pantalla.blit(self.renderizado_barra_vida, self.barra_vida_rect)  
        pantalla.blit(self.renderizado_inventario_resto, self.inventario_resto_rect)
        