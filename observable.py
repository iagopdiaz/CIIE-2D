#Patron Observador

class Observable:
    def __init__(self):
        self.observers = []
    
    def notify_observers(self):
        for observer in self.observers:
            observer.update(self)