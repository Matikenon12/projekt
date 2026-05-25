import sys
import os
import ctypes
import pygame
from environment import Environment


#Konfiguracja sciezek   
#Ustawienie glownego katalogu projektu jako sciezki dostepnej dla interpretera
#Pozwala poprawnie iportowac moduly z podfolderow
#ROZWIAZANIE ZAPROPONOWANE PRZEZ AI ALE BEZ TEGO TEZ DZIALA
glowny_folder = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, glowny_folder)



#Optymalizacja wyswietlania
#Instrukcja dla systemu Windowds aby gra nie byla rozmyta
#ROZWIAZANIE ZAPROPONOWANE PRZEZ AI ALE BEZ TEGO TEZ DZIALA TYLKO JEST LEKKO ROZMYTE
try:
    ctypes.windll.user32.SetProcessDPIAware()
except AttributeError:
    pass

#Uruchamianie aplikacji 
if __name__ == "__main__":
    gra = Environment() #Glowna instancja srodowiska gry
    gra.uruchom()       #Rozpoczecie glownej petli gry