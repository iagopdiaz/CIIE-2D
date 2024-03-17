import pygame
import datetime as datetime
from gestor_recursos import GestorRecursos
from observer import Observer
from settings import *

class Dialogos(Observer):
    def __init__(self, nivel, habilitado=True):
        # Cargar fondo del diálogo
        self.imagen = GestorRecursos.CargarImagen(CAJA_DIALOGO, -1)
        self.imagen = pygame.transform.scale(self.imagen, (250,100))
        self.rect = self.imagen.get_rect()
        # Posicionar el diálogo, lo habilitamos y le damos valores iniciales  
        self.rect.bottomright = (ANCHO_PANTALLA, ALTO_PANTALLA)   
        self.habilitado = habilitado
        self.reiniciar()
        self.ultimo_tiempo = pygame.time.get_ticks()
        self.lista_dialogos = GestorRecursos.CargarDialogo(nivel)
        self.acciones = GestorRecursos.CargarDialogo(CABECERA)
        self.fuente_nombre = GestorRecursos.CargarFuente(self,FUENTE1, TAMAÑO_FUENTE_NOMBRE)
        self.fuente_frase = GestorRecursos.CargarFuente(self,FUENTE1, TAMAÑO_FUENTE_FRASE)
        # Posicionamos los elementos del diálogo
        self.posicion_nombre()
        self.posicion_texto()
        self.posicion_cabecera()
        # Posicionamos el indicador "TECLA P" siguiente diálogo
        fuente_pequena = GestorRecursos.CargarFuente(self,FUENTE1, TAMAÑO_FUENTE_ENTER)
        self.superficie_indicacion = fuente_pequena.render(TEXTO_P, True, DARK_GRAY)
        self.rect_indicacion = self.superficie_indicacion.get_rect()
        xf, yf = self.rect.bottomleft
        self.rect_indicacion.bottomleft = (xf + 15, yf - 8)

        
        # Inicializar texto del diálogo si no ha terminado
        if not self.final():
            self.cargar_cabecera()    
            self.cargar_accion(0)
            self.cargar_nombre()
            self.cargar_frase()
        else: # al acabar el diálogo, mostramos la cabecera para mostrar avisos
            self.cargar_cabecera()    
            self.cargar_accion(0)
            
    def reiniciar(self):
        self.inicio_palabra = 0
        self.palabra = 0
        self.lineas = []
        self.lineas_acion = []
        self.dialogo_actual = 0
    
    # Nos da el nombre del personaje que habla    
    def nombre_habla(self):
        return self.lista_dialogos[self.dialogo_actual][0]
    
    # Nos da el texto de la cabecera
    def texto_cabecera(self):
        return self.acciones[0][0]
    
    # Nos da el texto de la acción sobre la que hay que mostrar un aviso
    def texto_accion(self,num):
        return self.acciones[num][1]

    # Nos da el texto que dice el personaje
    def frase_dice(self):
        return self.lista_dialogos[self.dialogo_actual][1]
    
    # Carga el nombre en la caja del diálogo        
    def cargar_nombre(self):
        self.superficie_nombre = self.fuente_nombre.render(self.nombre_habla(), True, MARROON)
        self.rect_nombre = self.superficie_nombre.get_rect()
        self.rect_nombre.topleft = (self.nombre_x, self.nombre_y)
    
    # Carga la cabecera en la caja del diálogo
    def cargar_cabecera(self):
        self.superficie_cabecera = self.fuente_nombre.render(self.texto_cabecera(), True, MARROON)
        self.rect_cabecera = self.superficie_cabecera.get_rect()
        self.rect_cabecera.topleft = (self.cabecera_x, self.cabecera_y)  
    
    # Posiciona el nombre el la caja del diálogo 
    def posicion_nombre(self):
        x , y = self.rect.topleft       
        self.nombre_x = x + 15
        self.nombre_y = y + 10
    
    # Posiciona la cabecera en la caja del diálogo
    def posicion_cabecera(self):
        x , y = self.rect.topleft       
        self.cabecera_x = x + 15
        self.cabecera_y = y + 10
    
    # Posiciona el texto en la caja del diálogo        
    def posicion_texto(self):
        x, y = self.rect.topleft   
        self.texto_x = x + 15
        self.texto_y = y + 25
    
    # Carga la acción en la caja del diálogo    
    def cargar_accion(self,accion):
        caja_dialogo = self.rect.width - 22 , self.rect.height - 10
        frase = self.texto_accion(accion)
        acciones = frase.split(' ')
        linea_actual = ''
        self.lineas_accion = []
        for palabra in acciones:
            if self.fuente_frase.size(linea_actual + palabra)[0] > caja_dialogo[0]:
                superficie_linea_accion = self.fuente_frase.render(linea_actual, True, DARK_GRAY)
                self.lineas_accion.append(superficie_linea_accion)
                linea_actual = palabra + ' '
            else:
                linea_actual += palabra + ' '
        superficie_linea_accion = self.fuente_frase.render(linea_actual, True, DARK_GRAY)
        self.lineas_accion.append(superficie_linea_accion)
    
    # Carga la frase en la caja del diálogo    
    def cargar_frase(self):
        caja_dialogo = self.rect.width - 22 , self.rect.height - 10
        frase = self.frase_dice()
        palabras = frase.split(' ')
        linea_actual = ''
        self.lineas = []
        for palabra in palabras: 
            #Si añadir la palabra sobrepasa el tamaño disponible
            if self.fuente_frase.size(linea_actual + palabra)[0] > caja_dialogo[0]:
                #Renderizamos la linea actual y la añadimos a la lista de lineas
                #Añadimos la palabra a la siguiente linea
                superficie_linea = self.fuente_frase.render(linea_actual, True, DARK_GRAY)
                self.lineas.append(superficie_linea)
                linea_actual = palabra + ' '
            else:
                linea_actual += palabra + ' '
        superficie_linea = self.fuente_frase.render(linea_actual, True, DARK_GRAY)
        self.lineas.append(superficie_linea)


    def habilitar(self):
        self.habilitado = True
    
    def siguiente_dialogo(self):
        self.dialogo_actual += 1
        self.inicio_palabra = 0
        self.palabra = 0
        self.lineas = []
        self.lineas_accion = []
    
    def final(self):
        if (len(self.lista_dialogos) - 1 < self.dialogo_actual) or not self.habilitado:
            return True
        

    def actualizar_dialgo(self):
        if not self.final():
            self.cargar_nombre()
            self.cargar_frase()
            
    def actualizar_accion(self,accion): 
        self.cargar_cabecera()  
        self.cargar_accion(accion)  

        
    def dibujar(self, pantalla):
        distancia_lineas = 0
        distancia_lineas_accion = 0
        if (not self.final()):
            pantalla.blit(self.imagen, self.rect)
            pantalla.blit(self.superficie_nombre, self.rect_nombre)
            for linea in self.lineas:
                pantalla.blit(linea, pygame.Rect(self.texto_x, self.texto_y + distancia_lineas, 230, 90))
                distancia_lineas += 12                    
            pantalla.blit(self.superficie_indicacion, self.rect_indicacion)
        else:             
            pantalla.blit(self.imagen, self.rect)            
            pantalla.blit(self.superficie_cabecera, self.rect_cabecera)
            for linea in self.lineas_accion:
                pantalla.blit(linea, pygame.Rect(self.texto_x, self.texto_y + distancia_lineas_accion, 230, 90))
                distancia_lineas_accion += 12                    
            pantalla.blit(self.superficie_indicacion, self.rect_indicacion)
                
