import pygame
import sys

# Inicialización de Pygame
pygame.init()

# Configuración de la ventana
screen = pygame.display.set_mode((800, 600))
pygame.display.set_caption("Herramienta de Selección de Plataformas")

color_fondo = (173, 216, 230)  # Azul claro (Light Blue)

# Cargar la imagen de fondo
fondo = pygame.image.load('./imagenes/mapa1paredes.png')  # Cambia 'tuImagenDeFondo.png' al nombre de tu archivo

# Variables de control
start_pos = None  # Posición inicial del rectángulo
end_pos = None    # Posición final del rectángulo
running = True

while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.MOUSEBUTTONDOWN:
            start_pos = event.pos
        elif event.type == pygame.MOUSEBUTTONUP:
            end_pos = event.pos
            # Calcula las coordenadas y dimensiones del rectángulo
            x = min(start_pos[0], end_pos[0])
            y = min(start_pos[1], end_pos[1])
            ancho = abs(start_pos[0] - end_pos[0])
            alto = abs(start_pos[1] - end_pos[1])
            print(f'x: {x}, y: {y}, ancho: {ancho}, alto: {alto}')
            # Aquí podrías agregar una función para guardar estas coordenadas en un archivo

    # Dibujo de la imagen de fondo
    screen.blit(fondo, (0, 0))

    # Dibujo del rectángulo de selección
    if start_pos and end_pos:
        rect_color = (255, 0, 0)  # Color rojo
        width = 2  # Ancho de la línea del rectángulo
        pygame.draw.rect(screen, rect_color, pygame.Rect(start_pos, (end_pos[0] - start_pos[0], end_pos[1] - start_pos[1])), width)

    pygame.display.flip()

pygame.quit()
sys.exit()