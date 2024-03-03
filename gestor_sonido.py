import pygame
from settings import *
from gestor_recursos import GestorRecursos
from gestor_usuario import GestorUsuario

class GestorSonido: 
    
    sonido_musica = 50
    
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
        self.poner_volumen_musica(self,self.sonido_musica)
        pygame.mixer.music.play(-1)

    @classmethod
    def musica_nivel_2(self):
        pygame.mixer.music.load(MUSICA_NIVEL_2)
        self.poner_volumen_musica(self,self.sonido_musica)
        pygame.mixer.music.play(-1)
    
    @classmethod
    def musica_nivel_3(self):
        pygame.mixer.music.load(MUSICA_NIVEL_3)
        self.poner_volumen_musica(self,self.sonido_musica)
        pygame.mixer.music.play(-1)
    
    @classmethod
    def musica_menu_principal(self):
        pygame.mixer.music.load(MUSICA_MENU_PRINCIPAL)
        self.poner_volumen_musica(self,self.sonido_musica)
        pygame.mixer.music.play(-1)
    
    @classmethod
    def musica_menus(self):
        pygame.mixer.music.load(MUSICA_MENUS)
        self.poner_volumen_musica(self,self.sonido_musica)
        pygame.mixer.music.play(-1)
        
    classmethod
    def poner_volumen_musica(self,volumen):
        self.sonido_musica = volumen
        pygame.mixer.music.set_volume(self.sonido_musica/100.0)