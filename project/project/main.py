import sys
import os
import ctypes
import pygame


glowny_folder = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, glowny_folder)

try:
    ctypes.windll.user32.SetProcessDPIAware()
except AttributeError:
    pass

from environment import Environment


if __name__ == "__main__":
    gra = Environment()
    gra.uruchom()