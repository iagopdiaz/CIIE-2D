import pygame
from settings import *
from gestor_recursos import GestorRecursos
from gestor_usuario import GestorUsuario

#Singleton

class GestorSonido: 
    
    volumen_musica = 50
    volumen_sonido = 50
    
    
    @classmethod
    def init(self):
        pygame.mixer.pre_init(44100, -16, 2, 2048)
        pygame.mixer.init()
        try: 
            self.volumen_musica = GestorUsuario.get_value("volumen_musica")
        except:
            pass    
        try :
            self.volumen_sonido = GestorUsuario.get_value("volumen_sonido")
        except:
            pass
        
        self.canal_sonido = pygame.mixer.Channel(1)
        self.canal_musica = pygame.mixer.Channel(2)
        self.canal_partitura = pygame.mixer.Channel(3)

    @classmethod
    def musica_nivel_1(self):
        self.canal_musica.play(pygame.mixer.Sound(MUSICA_NIVEL_1))  # Usar el canal de música
        self.poner_volumen_musica(self.volumen_musica)

    @classmethod
    def musica_nivel_2(self):
        self.canal_musica.play(pygame.mixer.Sound(MUSICA_NIVEL_2))
        self.poner_volumen_musica(self.volumen_musica)


    @classmethod
    def musica_nivel_3(self):
        self.canal_musica.play(pygame.mixer.Sound(MUSICA_NIVEL_3))
        self.poner_volumen_musica(self.volumen_musica)
    
    @classmethod
    def musica_menu_principal(self):
        self.canal_musica.play(pygame.mixer.Sound(MUSICA_MENU_PRINCIPAL))
        self.poner_volumen_musica(self.volumen_musica)
    
    @classmethod
    def musica_menus(self):
        self.canal_musica.play(pygame.mixer.Sound(MUSICA_MENUS))
        self.poner_volumen_musica(self.volumen_musica)

    @classmethod
    def poner_volumen_musica(self,volumen):
        self.volumen_musica = volumen
        self.canal_musica.set_volume(self.volumen_musica/100.0)
    
    @classmethod
    def poner_volumen_sonido(self,volumen):
        self.volumen_sonido = volumen
        self.canal_sonido.set_volume(self.volumen_sonido/100.0)
        
    @classmethod
    def subir_volumen_musica(self,volumen):
        self.volumen_musica += volumen
        if self.volumen_musica > 100:
            self.volumen_musica = 100
        self.poner_volumen_musica(self.volumen_musica) 
    
    @classmethod
    def bajar_volumen_musica(self,volumen):
        self.volumen_musica -= volumen
        if self.volumen_musica < 0:
            self.volumen_musica = 0
        self.poner_volumen_musica(self.volumen_musica)       
    
    @classmethod    
    def subir_volumen_sonido(self,volumen):
        self.volumen_sonido += volumen
        if self.volumen_sonido > 100:
            self.volumen_sonido = 100
        self.poner_volumen_sonido(self.volumen_sonido)
    
    @classmethod
    def bajar_volumen_sonido(self,volumen):
        self.volumen_sonido -= volumen
        if self.volumen_sonido < 0:
            self.volumen_sonido = 0
        self.poner_volumen_sonido(self.volumen_sonido)
    
    @classmethod
    def obtener_volumen_musica(self):
        return self.volumen_musica
    
    @classmethod
    def obtener_volumen_sonido(self):
        return self.volumen_sonido

    @classmethod
    def get_partitura(self, nombre):
        return pygame.mixer.Sound("musica/partituras/" + nombre + ".ogg")
    
    @classmethod
    def reproducir_partitura(self, partitura):
        #Paramos el resto de las partituras q estaban sonando
        self.canal_partitura.stop() 

        #Ponemos esta a funcionar
        self.canal_partitura.play(partitura)  

        #Bajamos el volumen de las musicas(asi para evitar tocar el self y volver a subir el volumen al q estaba al terminar de tocar la partitura)
        self.canal_musica.set_volume((self.volumen_musica/2)/100)
