import pygame
from game import Game

pygame.init()
pygame.mixer.init()
pygame.display.set_caption("FUCK THE SUN")

game = Game()
game.run_game_loop()

pygame.quit()
quit()