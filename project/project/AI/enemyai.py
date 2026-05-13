import random
from constants import KIERUNEK_GORA, KIERUNEK_DOL, KIERUNEK_LEWO, KIERUNEK_PRAWO

def wybierz_kierunek_ai(x, y, baza_x, baza_y, gracz_x, gracz_y):
    # Priorytet: Baza (70%), Gracz (30%)
    if random.randint(1, 100) > 70:
        cel_x, cel_y = gracz_x, gracz_y
    else:
        cel_x, cel_y = baza_x, baza_y

    roznica_x = cel_x - x
    roznica_y = cel_y - y

    # Jeœli AI jest ju¿ blisko celu w osi X (ta sama kolumna) -> JedŸ góra/dó³ ¿eby strzeliæ!
    if abs(roznica_x) < 32:
        return KIERUNEK_DOL if roznica_y > 0 else KIERUNEK_GORA
        
    # Jeœli AI jest ju¿ blisko w osi Y (ten sam rz¹d) -> JedŸ lewo/prawo ¿eby strzeliæ!
    if abs(roznica_y) < 32:
        return KIERUNEK_PRAWO if roznica_x > 0 else KIERUNEK_LEWO

    # Jeœli jest daleko, wybiera d³u¿sz¹ trasê, ¿eby jak najszybciej wejœæ w liniê strza³u
    if abs(roznica_x) > abs(roznica_y):
        return KIERUNEK_PRAWO if roznica_x > 0 else KIERUNEK_LEWO
    else:
        return KIERUNEK_DOL if roznica_y > 0 else KIERUNEK_GORA