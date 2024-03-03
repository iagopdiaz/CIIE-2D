import pygame
import sys

pygame.init()

# Configuración de la ventana
window_size = (1600, 1024)
screen = pygame.display.set_mode(window_size)
pygame.display.set_caption("Herramienta de Selección de Plataformas")

color_fondo = (173, 216, 230)  # Azul claro (Light Blue)

# Cargar la imagen de fondo
fondo = pygame.image.load('./imagenes/mapa/mapa1paredes.png')  # Asegúrate de que el camino a la imagen es correcto
rect = fondo.get_rect()
# La subimagen que estamos viendo
rectSubimagen = pygame.Rect(0, 0, 1600, 1024)
rectSubimagen.left = 0 # El scroll horizontal empieza en la posicion 0 por defecto
rectSubimagen.top = 0
# Variables de control
start_pos = None  # Posición inicial del rectángulo
end_pos = None    # Posición final del rectángulo
scroll = [0, 0]   # Desplazamiento actual de la vista
running = True
pressed = False
colorFondo = (255, 255, 255)  # Color fondo

while running:
    screen.fill(colorFondo)
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.MOUSEBUTTONDOWN:
            if event.button == 1:  # Botón izquierdo del ratón
                # Ajustar las posiciones iniciales con el desplazamiento actual
                start_pos = (event.pos[0] + scroll[0], event.pos[1] + scroll[1])
        elif event.type == pygame.MOUSEBUTTONUP:
            if event.button == 1:  # Botón izquierdo del ratón
                # Ajustar las posiciones finales con el desplazamiento actual
                end_pos = (event.pos[0] + scroll[0], event.pos[1] + scroll[1])
                # Calcula las coordenadas y dimensiones del rectángulo ajustadas al desplazamiento
                x = min(start_pos[0], end_pos[0])
                y = min(start_pos[1], end_pos[1])
                ancho = abs(start_pos[0] - end_pos[0])
                alto = abs(start_pos[1] - end_pos[1])
                print(f'x: {x}, y: {y}, ancho: {ancho}, alto: {alto}')
                # Aquí podrías agregar una función para guardar estas coordenadas en un archivo

    # Manejo de desplazamiento con las teclas
    keys = pygame.key.get_pressed()
    if keys[pygame.K_LEFT]:
        scroll[0] -= 5
        pressed = True
    if keys[pygame.K_RIGHT]:
        scroll[0] += 5
        pressed = True
    if keys[pygame.K_UP]:
        scroll[1] -= 5
        pressed = True
    if keys[pygame.K_DOWN]:
        scroll[1] += 5
        pressed = True

    if pressed: 
        # Asegúrate de que scrollx no sea menor que 0 ni mayor que la anchura de la imagen menos la anchura de la pantalla
        rectSubimagen.left = max(0, min(scroll[0], fondo.get_width() - 800))
        # Asegúrate de que scrolly no sea menor que 0 ni mayor que la altura de la imagen menos la altura de la pantalla
        rectSubimagen.top = max(0, min(scroll[1], fondo.get_height() - 600))

    # Dibujo del rectángulo de selección ajustado al desplazamiento
    if start_pos and end_pos:
        rect_color = (255, 0, 0)  # Color rojo
        width = 2  # Ancho de la línea del rectángulo
        rect = pygame.Rect(start_pos[0] - scroll[0], start_pos[1] - scroll[1], end_pos[0] - start_pos[0], end_pos[1] - start_pos[1])
        pygame.draw.rect(screen, rect_color, rect, width)

    pressed = False
    screen.blit(fondo, rect, rectSubimagen)
    pygame.display.flip()

pygame.quit()
sys.exit()
"""
elif evento.type == pygame.MOUSEBUTTONDOWN:
                if evento.button == 1:  # Botón izquierdo del ratón
                # Ajustar las posiciones iniciales con el desplazamiento actual
                    self.start_pos = (evento.pos[0] + self.scrollx, evento.pos[1] + self.scrolly)
            elif evento.type == pygame.MOUSEBUTTONUP:
                if evento.button == 1:  # Botón izquierdo del ratón
                    # Ajustar las posiciones finales con el desplazamiento actual
                    self.end_pos = (evento.pos[0] + self.scrollx, evento.pos[1] + self.scrolly)
                    # Calcula las coordenadas y dimensiones del rectángulo ajustadas al desplazamiento
                    x = min(self.start_pos[0], self.end_pos[0])
                    y = min(self.start_pos[1], self.end_pos[1])
                    ancho = abs(self.start_pos[0] - self.end_pos[0])
                    alto = abs(self.start_pos[1] - self.end_pos[1])
                    print(f'x: {x}, y: {y}, ancho: {ancho}, alto: {alto}')
                    with open('./imagenes/coordPlataformas.txt', 'a') as archivo:
                        archivo.write(f'{int(x)} {int(y)} {int(ancho)} {int(alto)}\n')
                    # Aquí podrías agregar una función para guardar estas coordenadas en un archivo

"""