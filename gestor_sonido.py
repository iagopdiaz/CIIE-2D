import pygame
from settings import *
from gestor_recursos import GestorRecursos
from gestor_usuario import GestorUsuario

#Singleton

class GestorSonido: 
    
    nivel_musica = 50
    nivel_sonido = 50
    
    @classmethod
    def init(self):
        pygame.mixer.pre_init(44100, -16, 2, 2048)
        pygame.mixer.init()
        try: 
            self.sonido_musica = GestorUsuario.get_value("volumen_musica")
        except:
            pass    
        
    @classmethod
    def musica_nivel_1(self):
        pygame.mixer.music.load(MUSICA_NIVEL_1)
        self.poner_volumen_musica(self,self.nivel_musica)
        pygame.mixer.music.play(-1)

    @classmethod
    def musica_nivel_2(self):
        pygame.mixer.music.load(MUSICA_NIVEL_2)
        self.poner_volumen_musica(self,self.nivel_musica)
        pygame.mixer.music.play(-1)
    
    @classmethod
    def musica_nivel_3(self):
        pygame.mixer.music.load(MUSICA_NIVEL_3)
        self.poner_volumen_musica(self,self.nivel_musica)
        pygame.mixer.music.play(-1)
    
    @classmethod
    def musica_menu_principal(self):
        pygame.mixer.music.load(MUSICA_MENU_PRINCIPAL)
        self.poner_volumen_musica(self,self.nivel_musica)
        pygame.mixer.music.play(-1)
    
    @classmethod
    def musica_menus(self):
        pygame.mixer.music.load(MUSICA_MENUS)
        self.poner_volumen_musica(self,self.sonido_musica)
        pygame.mixer.music.play(-1)
        
    @classmethod
    def poner_volumen_musica(self,volumen):
        self.sonido_musica = volumen
        pygame.mixer.music.set_volume(self.sonido_musica/100.0)
    
    @classmethod
    def poner_volumen_sonido(self,volumen):
        self.sonido_sonido = volumen
        for sonido in pygame.mixer.get_init():
            sonido.set_volume(self.sonido_sonido/100.0)
    
    @classmethod
    def subir_volumen_musica(self,volumen):
        self.sonido_musica += volumen
        if self.sonido_musica > 100:
            self.sonido_musica = 100
        self.poner_volumen_musica(self,self.sonido_musica) 
    
    @classmethod
    def bajar_volumen_musica(self,volumen):
        self.sonido_musica -= volumen
        if self.sonido_musica < 0:
            self.sonido_musica = 0
        self.poner_volumen_musica(self,self.sonido_musica)       
    
    @classmethod    
    def subir_volumen_sonido(self,volumen):
        self.sonido_sonido += volumen
        if self.sonido_sonido > 100:
            self.sonido_sonido = 100
        self.poner_volumen_sonido(self,self.sonido_sonido)
    
    @classmethod
    def bajar_volumen_sonido(self,volumen):
        self.sonido_sonido -= volumen
        if self.sonido_sonido < 0:
            self.sonido_sonido = 0
        self.poner_volumen_sonido(self,self.sonido_sonido)
            
        