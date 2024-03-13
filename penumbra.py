import pygame
import numpy as np
from scipy.ndimage.filters import gaussian_filter
from settings import *
import pygame.surfarray as surfarray

class Penumbra:
    def __init__(self):
        self.penumbra = pygame.Surface((ANCHO_PANTALLA, ALTO_PANTALLA), pygame.SRCALPHA)
        self.penumbra.fill((0, 0, 0, 0))
    

    def update(self, jugador, nivel):
        if nivel == 4:# Solo se aplica la penumbra en el nivel 3 DE MOOMENTO EN FASE DE PRUEBAS
            radio_luz = 100 if jugador.id == 3 else 50
            valor_max = 1 if jugador.id == 3 else 0.5
            valor_min = 0.2 if jugador.id == 3 else 0.1

            # Creamos una matriz con las distancias al jugador
            y = np.arange(ALTO_PANTALLA)
            x = np.arange(ANCHO_PANTALLA)
            distancias = np.sqrt((x[:, np.newaxis]-jugador.rect.center[0])**2 + (y-jugador.rect.center[1])**2)

            # Creamos la matriz de luz
            matriz = np.exp(-distancias**2 / (2*radio_luz**2))
            matriz = ((matriz - matriz.min()) * (1/(matriz.max() - matriz.min()) * (valor_max - valor_min))) + valor_min

            # Aplicamos la matriz actualizada al canal alfa de la penumbra
            alpha_array = surfarray.pixels_alpha(self.penumbra)
            alpha_array[:,:] = (matriz*255).astype(np.int64)
        else:
            self.penumbra.fill((0, 0, 0, 0))



    def dibujar(self, pantalla):
        # Dibujamos la penumbra en la pantalla
        pantalla.blit(self.penumbra, (0, 0))
