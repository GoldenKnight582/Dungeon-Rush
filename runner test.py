import pygame
import level_manager as level_manager

pygame.init()
win_dim = (800, 800)
win = pygame.display.set_mode(win_dim)
done = False
LM = level_manager.LevelManager(win, "Runner")
while not done:
    LM.update()
    done = LM.handle_input()
    LM.draw()

pygame.quit()