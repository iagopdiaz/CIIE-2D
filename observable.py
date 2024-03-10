#Patron Observador

class Observable:
    def __init__(self):
        self.observers = []
    
    def notificar_observers(self,tipo, imagen):
        for observer in self.observers:
            observer.actualizar_observer(tipo, imagen)
            
    def registrar_observador(self, observador):
        self.observers.append(observador)

    def eliminar_observador(self, observador):
        self.observers.remove(observador)
     
            