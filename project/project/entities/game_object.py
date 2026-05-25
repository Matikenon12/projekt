from abc import ABC,abstractmethod

#Klasa abstrakcyjna GameObject fundament dla wszystkich obiektow w grze
class GameObject(ABC):
    def __init__(self,x,y):
        self.x=x
        self.y=y
        self.sprite=None
        self.hitbox=None

    
    #Metoda akualizujaca logike obiektu 
    @abstractmethod
    def update(self):
        pass
   
    #Metoda odpowiedzialna za renderowanie obiektu
    @abstractmethod
    def draw(self):
        pass


