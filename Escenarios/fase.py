import pygame
from Escenarios.escena import *
from itertools import chain
from pygame.locals import *
from Escenarios.game_over import GameOver
from Gestores.gestor_recursos import *
from Gestores.gestor_sonido import GestorSonido
from Personajes.jugador import *
from Personajes.personajes import *
from Objetos.partitura import *
from Interfaz.interfaz_usuario import *
from Objetos.puerta import *
from Objetos.meta_fase import *
from Objetos.puzzle_cubo import *
from Animaciones.onda import *
from Animaciones.penumbra import *
from Objetos.pared import *
from Dialogos.dialogos import Dialogos 
from Personajes.enemigos import *
from Animaciones.onda import *
from Animaciones.animaciones import *

class Fase(Escena):
    def __init__(self, director, nivel, dialogos = True):
        # Llamamos al constructor de la clase padre
        Escena.__init__(self, director)

        # Nivel actual
        self.nivel = nivel
        
        #Definir dialogos
        self.ultimo_dialogo = False
        if(nivel == 4): 
            self.ultimo_dialogo = True 
        if(nivel == 1) : 
            dialogo = NIVEL1   
        elif(nivel == 2) :
            dialogo = NIVEL2
        elif(nivel == 3) :
            dialogo = NIVEL3 
        self.dialogos = Dialogos(dialogo, not self.ultimo_dialogo)   
         
        
        # Iniciar el scroll
        self.scrollx = 0
        self.scrolly = 0

        # Iniciar el decorado
        self.decorado = Decorado(nivel)

        # Creamos los sprites de los jugadores y los añadimos a un grupo
        self.jugador1 = PrimerPersonaje()
        if self.nivel > 1:
            self.jugador2 = SegundoPersonaje()
        if self.nivel > 2:
            self.jugador3 = TercerPersonaje()

        # Ponemos a los jugadores en sus posiciones iniciales
        self.jugador1.establecerPosicion((250, 520))
        self.jugando = False

        # Establecemos el jugador activo como el jugador1
        self.jugador_activo = self.jugador1
        self.jugador_activo.registrar_observador(self)
        self.interfazUsuario = InterfazUsuario(self.jugador_activo, self.nivel)
        self.grupoJugadorActivo = pygame.sprite.Group(self.jugador_activo)
        self.tipo_anterior = [None,None,None]

        # Creamos las paredes del decorado basándonos en las coordenadas cargadas
        datosParedes = GestorRecursos.CargarCoordenadasParedes(f'coordParedes{self.nivel}.txt')

        self.grupoParedes = pygame.sprite.Group()
        for linea in datosParedes:
            x, y, ancho, alto = map(int, linea.split())
            pared = Pared(pygame.Rect(x, y, ancho, alto))
            self.grupoParedes.add(pared)

        #Pinchos
        datosPinchos = GestorRecursos.CargarCoordenadasPinchos(f"coordPinchos{self.nivel}.txt")
        
        self.grupoPinchos = pygame.sprite.Group()
        for linea in datosPinchos:
            x, y, orientacion = map(int, linea.split())
            pincho = ParedPinchos(orientacion)
            pincho.establecerPosicion((x, y))
            self.grupoPinchos.add(pincho)

        # Partituras
        datosPartituras = GestorRecursos.CargarPartituras(f'coordPartituras{nivel}.txt')

        self.grupoPartituras = pygame.sprite.Group()
        i = 1
        for datos in datosPartituras:
            if i == 5: i = 1
            x, y = map(int, datos['coords'].split())
            partitura = Partitura(f"partituras/partitura{datos['jugador']}.png", datos['nombre'], datos['jugador'])
            partitura.establecerPosicion((x, y))
            self.grupoPartituras.add(partitura)
            i += 1

        # Meta
        if self.nivel == 2:
            meta = MetaFase(4780, 349, 'metas/metaVertical.png')
        else:
            # Misma meta para fases 1 y 3
            meta = MetaFase(5314, 190, 'metas/metaHorizontal.png')
        self.grupoMeta = pygame.sprite.Group(meta)

        # Puertas
        datosPuertas = GestorRecursos.CargarPuertas(f"coordPuertas{nivel}.txt")

        self.grupoPuertas = pygame.sprite.Group()
        
        for i, datos in enumerate(datosPuertas, start=1):
            # Obtenemos las coordenadas de la foto de la puerta
            x_foto, y_foto, tipo = map(int, datos['coords_foto'].split())
            # Obtenemos las coordenadas y dimensiones del área de activación de la puerta
            x_area, y_area, ancho, alto = map(int, datos['coords_area'].split())
            #Creamos el array de partituras
            partituras = []
            # Creamos la puerta y establecemos su posición y área de activación
            for nombre in datos['nombre']:
                #Buscar la partitura en el grupo de partituras
                for partitura in self.grupoPartituras:
                    if partitura.nombre == nombre:
                        partituras.append(partitura)
            puerta = Puerta(partituras, f"puertas/puerta.png", pygame.Rect(x_area, y_area, ancho, alto), tipo)
            puerta.establecerPosicion((x_foto, y_foto))
            self.grupoPuertas.add(puerta)
            puerta.registrar_observador(self)

        #Cubos
        datosCuboAlchemist = GestorRecursos.CargarCubos(f'coordMapaCuboSombra{self.nivel}.txt')
        self.grupoCubosSombra = pygame.sprite.Group()
        for linea in datosCuboAlchemist:
            x, y, tipoCubo = map(int, linea.split())
            if tipoCubo == 1:
                cubo = Cubo_Sombra1()
            elif tipoCubo == 2:
                cubo = Cubo_Sombra2()
            elif tipoCubo == 3:
                cubo = Cubo_Sombra3()
            cubo.establecerPosicion((x, y))
            self.grupoCubosSombra.add(cubo)
        
        datosCuboGris = GestorRecursos.CargarCubos(f'coordMapaCuboGris{self.nivel}.txt')
        self.grupoCubosGrises = pygame.sprite.Group()
        for linea in datosCuboGris:
            x, y = map(int, linea.split())
            cubo = Cubo_Gris()
            cubo.establecerPosicion((x, y))
            self.grupoCubosGrises.add(cubo)

        self.grupoCubosNegros = pygame.sprite.Group()

        #Penumbra
        self.grupoPenumbra = pygame.sprite.Group()
        if nivel == 3:
            self.grupoPenumbra.add(Penumbra())

        #Enemigos
        datosEnemigo = GestorRecursos.CargarCubos(f'coordEnemigo{self.nivel}.txt')
        self.grupoEnemigos = pygame.sprite.Group()
        for linea in datosEnemigo:
            x, y, tipo = map(int, linea.split())
            enemigo = Enemigo(tipo)
            enemigo.establecerPosicion((x, y))
            self.grupoEnemigos.add(enemigo)

        #Ataques        
        self.grupoAtaques = pygame.sprite.Group()

        #Control para la musica
        self.tocando = False

    def update(self, tiempo):
        self.grupoJugadorActivo.update(self.grupoParedes, self.grupoPinchos, self.grupoPartituras, self.grupoPuertas, self.grupoCubosNegros, self.grupoCubosGrises, self.grupoPuertas, self.grupoEnemigos, tiempo)
        self.grupoPuertas.update()
        self.grupoCubosSombra.update(self.grupoAtaques, self.grupoCubosNegros)
        self.grupoAtaques.update(self.jugador_activo, tiempo)
        self.grupoCubosNegros.update(self.jugador_activo, self.grupoParedes, self.grupoPuertas, self.grupoCubosGrises, tiempo)
        self.grupoPenumbra.update(self.jugador_activo, self.nivel)
        self.grupoEnemigos.update(self.jugador_activo, self.grupoParedes, self.grupoPuertas, self.grupoCubosGrises, tiempo)
        
        if not self.ultimo_dialogo:
            self.dialogos.actualizar_dialgo()
        else :
            self.dialogos.actualizar_accion(0)
        
        if pygame.sprite.groupcollide(self.grupoJugadorActivo, self.grupoMeta, False, False) != {}:
            if self.nivel == 1 or self.nivel == 2:
                self.director.cambiarEscena(Fase(self.director, self.nivel + 1))
            else:
                self.director.cambiarEscena(GameOver(self.director, ENHORABUENA))
        
        self.actualizarScroll()

        #Variable de control para saber cuando acaba de tocar
        if GestorSonido.canal_partitura.get_busy():
            self.tocando = True

        #Si estuvo tocando pero ahora ya no esta ocupado es que termino, por lo que ajustamos el volumen otra vez al del self del gestor
        if not GestorSonido.canal_partitura.get_busy() and self.tocando:
            GestorSonido.poner_volumen_musica(GestorSonido.obtener_volumen_musica())#AQUI ES DND NO SE QUE CARAJO FALLA
            self.tocando = False
            print("Ajustada la musica", GestorSonido.obtener_volumen_musica())


        return False
    
    def actualizar_observer(self, tipo, imagen):
        if tipo == "muerte":
            self.director.cambiarEscena(GameOver(self.director, MUERTE))
        elif tipo == "accion":
            if(imagen == PARTITURA_SOLTADA):
                self.dialogos.actualizar_accion(1)
            elif( imagen == PARTITURA_RECOGIDA):
                self.dialogos.actualizar_accion_txt(self.jugador_activo.inventario.nombre)
            elif( imagen == PARTIRUTA_TOCADA):  
                self.dialogos.actualizar_accion(3)
            elif( imagen == ABRIR_PUERTA):        
                self.dialogos.actualizar_accion(4)    
            elif( imagen == PUERTA_ABIERTA):        
                self.dialogos.actualizar_accion(5)
            elif( imagen == HABILIDAD_PERSONAJE):        
                self.dialogos.actualizar_accion(6)  
            elif( imagen == PERDER_VIDA):        
                self.dialogos.actualizar_accion(7)   
            elif (imagen == SIN_PARTITURA):
                self.dialogos.actualizar_accion(8)
            elif (imagen == PUERTA_PARTITURA):
                self.dialogos.actualizar_accion(9)
            elif (imagen == PUERTA_PARTITURA_NO):
                self.dialogos.actualizar_accion(10)  
            elif (imagen == SOLTAR_PARTITURA_NO):
                self.dialogos.actualizar_accion(11) 
            elif (imagen == ESCUCHANDO):
                self.dialogos.actualizar_accion(12) 
            elif (imagen == PUERTA_MAS_OTRO):
                self.dialogos.actualizar_accion(13)
                                   
            else:
                pass         
        elif tipo == "partitura1" or "partitura2" or "partitura3": 
            self.interfazUsuario.cargar_inventario(tipo,imagen)  
        elif tipo == "DELpartitura1" or "DELpartitura2" or "DELpartitura3":  
            self.interfazUsuario.cargar_inventario(tipo, "partituras/partituraX.png")
                 
            
    def actualizarScroll(self):
        # Definimos el límite para el scroll como los 3/5 de la pantalla
        LIMITE_SCROLL_X = ANCHO_PANTALLA * 3 / 5
        LIMITE_SCROLL_Y = ALTO_PANTALLA * 3 / 5

        #Aproximacion del centro del jugador, no se coge con .center porque sino varia con los diferentes personajes
        #En penumbra si que se coje con .center por que sino en el circulo se nota mucho el centro mal
        posicion_x = self.jugador_activo.rect.topleft[0] + 25
        posicion_y = self.jugador_activo.rect.topleft[1] + 25

        if posicion_x > LIMITE_SCROLL_X:
            # Calculamos cuántos píxeles está fuera del límite
            desplazamiento_x = posicion_x - LIMITE_SCROLL_X
            # Actualizamos el scroll en el eje X
            self.scrollx = min(self.scrollx + desplazamiento_x, self.decorado.imagen.get_width() - ANCHO_PANTALLA)
        elif posicion_x < ANCHO_PANTALLA - LIMITE_SCROLL_X:
            desplazamiento_x = ANCHO_PANTALLA - LIMITE_SCROLL_X - posicion_x
            self.scrollx = max(0, self.scrollx - desplazamiento_x)

        # Si el jugador se encuentra más allá del límite de la pantalla en el eje Y
        if posicion_y > LIMITE_SCROLL_Y:
            # Calculamos cuántos píxeles está fuera del límite
            desplazamiento_y = posicion_y - LIMITE_SCROLL_Y
            # Actualizamos el scroll en el eje Y
            self.scrolly = min(self.scrolly + desplazamiento_y, self.decorado.imagen.get_height() - ALTO_PANTALLA)
        elif posicion_y < ALTO_PANTALLA - LIMITE_SCROLL_Y:
            desplazamiento_y = ALTO_PANTALLA - LIMITE_SCROLL_Y - posicion_y
            self.scrolly = max(0, self.scrolly - desplazamiento_y)
            
        # Actualizamos la posición en pantalla de todos los Sprites según el scroll actual
        for sprite in chain(self.grupoJugadorActivo, self.grupoParedes, self.grupoPinchos, self.grupoPartituras, self.grupoCubosGrises, self.grupoCubosSombra, self.grupoPuertas, self.grupoMeta, self.grupoCubosNegros, self.grupoEnemigos):
            sprite.establecerPosicionPantalla((self.scrollx, self.scrolly))

        # Además, actualizamos el decorado para que se muestre una parte distinta
        self.decorado.update(self.scrollx, self.scrolly)

    def dibujar(self, pantalla):
        self.decorado.dibujar(pantalla)
        self.grupoParedes.draw(pantalla)
        self.grupoPinchos.draw(pantalla)
        self.grupoPartituras.draw(pantalla)
        self.grupoEnemigos.draw(pantalla)
        self.grupoCubosSombra.draw(pantalla)
        self.grupoJugadorActivo.draw(pantalla)
        self.grupoCubosGrises.draw(pantalla)
        self.grupoPuertas.draw(pantalla)
        self.grupoMeta.draw(pantalla)
        self.grupoCubosNegros.draw(pantalla)
        self.grupoAtaques.draw(pantalla)
        self.grupoPenumbra.draw(pantalla)
        self.interfazUsuario.dibujar(pantalla)
        self.dialogos.dibujar(pantalla)

    def cambiar_jugador(self):
        if self.nivel > 1:
            if (self.jugador_activo == self.jugador1):
                nuevo_jugador_activo = self.jugador2

            elif (self.jugador_activo == self.jugador2):
                nuevo_jugador_activo = self.jugador1

            if self.nivel > 2:
                if (self.jugador_activo == self.jugador2):
                    nuevo_jugador_activo = self.jugador3

                elif (self.jugador_activo == self.jugador3):
                    nuevo_jugador_activo = self.jugador1
        
            # Establece la posición del nuevo jugador activo a la posición del actual antes de cambiar
            nuevo_jugador_activo.establecerPosicion(self.jugador_activo.posicion)

            #Creamos un rectangulo con la futura posicion del jugador
            futuro_rect = pygame.Rect(nuevo_jugador_activo.posicion[0]-self.scrollx, nuevo_jugador_activo.posicion[1]-self.scrolly, nuevo_jugador_activo.rect.width, nuevo_jugador_activo.rect.height)

            #Calcular posicion futura del jugador activo, solo permitir el cambio si no hay colision con pared o puerta
            if nuevo_jugador_activo.puede_moverse(futuro_rect, self.grupoParedes, self.grupoPuertas, self.grupoCubosGrises):
                # Actualiza el grupo de sprites para que contenga al nuevo jugador activo
                # Primero, elimina el jugador activo actual de los grupos relevantes
                nuevo_jugador_activo.vida = self.jugador_activo.vida

                self.grupoJugadorActivo.remove(self.jugador_activo)

                # Luego, agrega el nuevo jugador activo a los grupos
                self.grupoJugadorActivo.add(nuevo_jugador_activo)

                # Finalmente, actualiza la referencia de jugador_activo al nuevo jugador
                self.jugador_activo = nuevo_jugador_activo
                self.interfazUsuario.actualizar_jugador(self.jugador_activo)
                self.jugador_activo.registrar_observador(self)
                
                #Creamos el humo para el cambio del jugador
                ataque = AnimacionCambio(self.jugador_activo.rect.left, self.jugador_activo.rect.top)
                self.grupoAtaques.add(ataque)

                #Ponemos el sonido del cambio de jugador
                GestorSonido.reproducir_efecto(SONIDO_CAMBIO_JUGADOR)

            else:
                print("No se puede cambiar de jugador en esta posicion")

    def eventos(self, lista_eventos):
        for evento in lista_eventos:
            if evento.type == pygame.QUIT:
                return True
            elif evento.type == pygame.KEYDOWN:
                if evento.key == pygame.K_p:
                    self.dialogos.siguiente_dialogo()
                    if (self.dialogos.final()):
                        self.jugando = True
                if self.jugando:
                    if evento.key == pygame.K_TAB:
                        self.cambiar_jugador()
                        continue
                    elif evento.key == pygame.K_t:
                        self.jugador_activo.tocar(self.grupoPuertas, self.grupoPartituras)
                    elif evento.key == pygame.K_e:
                        self.jugador_activo.escuchar(self.grupoPuertas)
                    elif evento.key == pygame.K_s:
                        self.jugador_activo.soltar_partitura(self.grupoPartituras, self.grupoParedes, self.grupoPuertas, self.grupoCubosGrises)
                    elif evento.key == pygame.K_h:
                        self.jugador_activo.habilidad1(self.grupoAtaques)
                        continue
            if self.jugando:
                # Indicamos la acción a realizar segun la tecla pulsada para cada jugador
                teclasPulsadas = pygame.key.get_pressed()
                self.jugador_activo.mover(teclasPulsadas, K_UP, K_DOWN, K_LEFT, K_RIGHT)

        return False  # No se sale del programa


    def encender_musica(self):
        if self.nivel == 1:
            GestorSonido.musica_nivel_1()
        if self.nivel == 2:
            GestorSonido.musica_nivel_2()
        if self.nivel == 3:
            GestorSonido.musica_nivel_3()


class Decorado:
    def __init__(self, nivel):
        self.nivel = nivel
        self.imagen = GestorRecursos.CargarImagen(f'mapa/mapa{self.nivel}decorado.png')

        self.rect = self.imagen.get_rect()
        
        # La subimagen que estamos viendo
        self.rectSubimagen = pygame.Rect(0, 0, ANCHO_PANTALLA, ALTO_PANTALLA)
        self.rectSubimagen.left = 0 # El scroll horizontal empieza en la posicion 0 por defecto
        self.rectSubimagen.top = 0

    def update(self, scrollx, scrolly):
        # Asegúrate de que scrollx no sea menor que 0 ni mayor que la anchura de la imagen menos la anchura de la pantalla
        self.rectSubimagen.left = max(0, min(scrollx, self.imagen.get_width() - ANCHO_PANTALLA))
        # Asegúrate de que scrolly no sea menor que 0 ni mayor que la altura de la imagen menos la altura de la pantalla
        self.rectSubimagen.top = max(0, min(scrolly, self.imagen.get_height() - ALTO_PANTALLA))

    def dibujar(self, pantalla):
        pantalla.blit(self.imagen, self.rect, self.rectSubimagen)
