from entities.game_object import GameObject

#Klasa bazowa dla wszystkich czolgow (PlayerTank,EnemyTank)
#Rozszerza klase GameObject o statystyki bojowe i parametry ruchu
class Tank(GameObject):
    def __init__(self,x,y,hp,kierunek,predkosc,cooldown_strzalu,poziom,liczba_zyc):
        super().__init__(x,y)

        #Parametry bojowe i ruchu
        self.hp=hp                              #Punkty zycia                         
        self.kierunek=kierunek                  #Aktualny zwrot czolgu
        self.predkosc=predkosc                  #Wartosc predkosci
        self.cooldown_strzalu=cooldown_strzalu  #Minimalny czas pomiedzy strzalami

        #Statystyki ogolne
        self.poziom=poziom                      #Poziom ulepszenia
        self.liczba_zyc=liczba_zyc              #Liczba zyc









