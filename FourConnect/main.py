from GameManager import GameManager
from Agent import *
import pygame
import sys

    

if __name__ == "__main__":

    pygame.init()
    game_manager = GameManager(agents=[HumanAgent(), RandomAgent()])
    
    while True:
        events = pygame.event.get()
        for event in events:
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

        if not game_manager.update(events):
            pygame.quit()
            sys.exit()
