import pygame
from pygame.locals import *
from Escenarios.escena import *
from Gestores.gestor_recursos import *
from Gestores.gestor_sonido import GestorSonido
from Escenarios.fase import *
from Interfaz.GUIElemento import *
from Escenarios.botones import *


class GUIInicial(GUI):
    def __init__(self, menu):
        GUI.__init__(self, menu, "interfaces/fondos/ajustes.jpg")
        textoBotonVolumenMusica = TextoBotonVolumenMusica(self)
        botonBajarVolumenMusica = BotonBajarMusica(self)
        botonSubirVolumenMusica = BotonSubirMusica(self)
        textoBotonVolumenEfectos = TextoBotonVolumenEfectos(self)
        botonBajarVolumenEfectos = BotonBajarEfectos(self)
        botonSubirVolumenEfectos = BotonSubirEfectos(self)
        botonVolumenMusica = BotonVolumenMusica(self)
        botonVolumenEfectos = BotonVolumenEfectos(self)        
        botonAtras = BotonAtras(self)
        
        self.GUIelementos.append(textoBotonVolumenMusica)
        self.GUIelementos.append(botonBajarVolumenMusica)
        self.GUIelementos.append(botonSubirVolumenMusica)
        self.GUIelementos.append(textoBotonVolumenEfectos)
        self.GUIelementos.append(botonBajarVolumenEfectos)
        self.GUIelementos.append(botonSubirVolumenEfectos)        
        self.GUIelementos.append(botonVolumenMusica)
        self.GUIelementos.append(botonVolumenEfectos)
        self.GUIelementos.append(botonAtras)


class MenuAjustes(Escena):
    
    def __init__(self, director):
        #Llamamos al constructor de la clase padre
        Escena.__init__(self, director)
        #Creamos la lista de pantallas
        self.listaPantallas = []
        #Creamos las pantallas que vamos a tener
        #y las metemos en la lista
        self.listaPantallas.append(GUIInicial(self))

        #En que pantalla estamos actualmente
        self.mostrarPantallaInicial()

    def update(self, *args):
        return

    def eventos(self, lista_eventos):
        #Se mira si se quiere salir de esta escena
        for evento in lista_eventos:
            #Si se quiere salir, se le indica al director
            if evento.type == KEYDOWN:
                if evento.key == K_ESCAPE:
                    self.ejecutarAtras()
            elif evento.type == pygame.QUIT:
                self.director.salirPrograma()
        #Se pasa la lista de eventos a la pantalla actual
        self.listaPantallas[self.pantallaActual].eventos(lista_eventos)

    def dibujar(self, pantalla):
        self.listaPantallas[self.pantallaActual].dibujar(pantalla)
    
    def ejecutarSalir(self):
        self.director.salirPrograma()
    
    def ejecutarAtras(self):
        self.director.salirEscena()
    
    def ejecutarBajarVolumenMusica(self):
        GestorSonido.bajar_volumen_musica(10) 
        GestorUsuario.do_update("volumen_musica", GestorSonido.obtener_volumen_musica())
        
    def ejecutarSubirVolumenMusica(self):
        GestorSonido.subir_volumen_musica(10) 
        GestorUsuario.do_update("volumen_musica", GestorSonido.obtener_volumen_musica())
    
    def ejecutarBajarVolumenEfectos(self):
        GestorSonido.bajar_volumen_efectos(10) 
        GestorUsuario.do_update("volumen_efectos", GestorSonido.obtener_volumen_efectos())
    
    def ejecutarSubirVolumenEfectos(self):
        GestorSonido.subir_volumen_efectos(10)
        GestorUsuario.do_update("volumen_efectos", GestorSonido.obtener_volumen_efectos())
    
    def mostrarPantallaInicial(self):
        self.pantallaActual = 0
        
    def encender_musica(self):
        GestorSonido.musica_menus()
