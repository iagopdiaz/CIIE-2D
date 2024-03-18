import pygame
from Ajustes.settings import *
from Gestores.gestor_recursos import GestorRecursos
from Gestores.gestor_usuario import GestorUsuario

#Singleton

class GestorSonido: 
    
    volumen_musica = 50
    volumen_efectos = 50
    
    
    
    @classmethod
    def init(self):
        pygame.mixer.pre_init(44100, -16, 2, 2048)
        pygame.mixer.init()
        try: 
            self.volumen_musica = GestorUsuario.get_value("volumen_musica")
        except:
            pass    
        try :
            self.volumen_efectos = GestorUsuario.get_value("volumen_efectos")
        except:
            pass
        
        self.canal_efectos = pygame.mixer.Channel(1)
        self.canal_musica = pygame.mixer.Channel(2)
        self.canal_partitura = pygame.mixer.Channel(3)

    @classmethod
    def musica_nivel_1(self):
        self.canal_musica.play(pygame.mixer.Sound(MUSICA_NIVEL_1), loops=-1)  # Usar el canal de música
        self.poner_volumen_musica(self.volumen_musica)
        self.poner_volumen_partitura(self.volumen_musica)


    @classmethod
    def musica_nivel_2(self):
        self.canal_musica.play(pygame.mixer.Sound(MUSICA_NIVEL_2), loops=-1)
        self.poner_volumen_musica(self.volumen_musica)
        self.poner_volumen_partitura(self.volumen_musica)

    @classmethod
    def musica_nivel_3(self):
        self.canal_musica.play(pygame.mixer.Sound(MUSICA_NIVEL_3), loops=-1)
        self.poner_volumen_musica(self.volumen_musica)
        self.poner_volumen_partitura(self.volumen_musica)

    @classmethod
    def musica_menu_principal(self):
        self.canal_musica.play(pygame.mixer.Sound(MUSICA_MENU_PRINCIPAL), loops=-1)
        self.poner_volumen_musica(self.volumen_musica)

    @classmethod
    def musica_menus(self):
        self.canal_musica.play(pygame.mixer.Sound(MUSICA_MENUS), loops=-1)
        self.poner_volumen_musica(self.volumen_musica)


    @classmethod
    def poner_volumen_musica(self,volumen):
        self.volumen_musica = volumen
        self.canal_musica.set_volume(self.volumen_musica/100.0)
    
    @classmethod
    def poner_volumen_efectos(self,volumen):
        self.volumen_efectos = volumen
        self.canal_efectos.set_volume(self.volumen_efectos/100.0)

    @classmethod
    def poner_volumen_partitura(self,volumen):
        self.canal_partitura.set_volume(volumen/100.0)
        
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
    def subir_volumen_efectos(self,volumen):
        self.volumen_efectos += volumen
        if self.volumen_efectos > 100:
            self.volumen_efectos = 100
        self.poner_volumen_efectos(self.volumen_efectos)
    
    @classmethod
    def bajar_volumen_efectos(self,volumen):
        self.volumen_efectos -= volumen
        if self.volumen_efectos < 0:
            self.volumen_efectos = 0
        self.poner_volumen_efectos(self.volumen_efectos)
    
    @classmethod
    def obtener_volumen_musica(self):
        return self.volumen_musica
    
    @classmethod
    def obtener_volumen_efectos(self):
        return self.volumen_efectos

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
        self.canal_musica.set_volume((self.volumen_musica/4)/100)

    @classmethod
    def reproducir_efecto(self, nombre):
        self.canal_efectos.play(pygame.mixer.Sound(nombre))
        self.poner_volumen_efectos(self.volumen_efectos)