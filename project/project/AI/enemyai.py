import random
from constants import KIERUNEK_GORA, KIERUNEK_DOL, KIERUNEK_LEWO, KIERUNEK_PRAWO

#Funkcja systemu sztucznej inteligencji enemy czolgu decyduje o kierunku poruszania sie 
def wybierz_kierunek_ai(x, y, baza_x, baza_y, gracz_x, gracz_y):

    #Priorytet: Baza (70%), Gracz (30%)
    if random.randint(1, 100) > 70:
        cel_x, cel_y = gracz_x, gracz_y
    else:
        cel_x, cel_y = baza_x, baza_y

    roznica_x = cel_x - x
    roznica_y = cel_y - y

    #Logika celowania
    #Jesli AI jest w tej samej kolumnie co cel porusza sie w pionie aby wyrownac os ognia
    if abs(roznica_x) < 32:
        return KIERUNEK_DOL if roznica_y > 0 else KIERUNEK_GORA
        
    #Jesli AI jest w tym samym rzedzie co cel porusza sie w poziomie aby wyrownac os ognia
    if abs(roznica_y) < 32:
        return KIERUNEK_PRAWO if roznica_x > 0 else KIERUNEK_LEWO

    #Jesli AI jest daleko, wybiera dluzsza trase, zeby jak najszybciej wejsc w liniê strzalu
    if abs(roznica_x) > abs(roznica_y):
        return KIERUNEK_PRAWO if roznica_x > 0 else KIERUNEK_LEWO
    else:
        return KIERUNEK_DOL if roznica_y > 0 else KIERUNEK_GORA