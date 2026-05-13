from entities.game_object import GameObject


class Tank(GameObject):
    def __init__(self,x,y,hp,kierunek,predkosc,cooldown_strzalu,poziom,liczba_zyc):
        super().__init__(x,y)
        self.hp=hp
        self.kierunek=kierunek
        self.predkosc=predkosc
        self.cooldown_strzalu=cooldown_strzalu
        self.poziom=poziom
        self.liczba_zyc=liczba_zyc