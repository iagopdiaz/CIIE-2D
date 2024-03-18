import pygame
from Ajustes.settings import *
import json

#Singleton

class GestorUsuario:
    
    configuracion = {}
    
    @classmethod
    def init(self): 
        try:
            with open(CONFIGURACION_USUARIO) as file:
                self.configuracion = json.load(file)
        except:
            pass
        
    @classmethod
    def do_update(self,key,value):     
        self.configuracion[key] = value
        with open(CONFIGURACION_USUARIO, 'w') as file:
            json.dump(self.configuracion, file)
            
    @classmethod
    def get_value(self,key):
        return self.configuracion[key]        