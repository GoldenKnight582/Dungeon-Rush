import pygame
import level_manager

pygame.init()
win_dim = (800, 800)
win = pygame.display.set_mode(win_dim)
done = False
LM = level_manager.LevelManager(win, "Title")
while not done:
    LM.update()
    done = LM.handle_input()
    win.fill((0, 0, 0))
    LM.draw()

pygame.quit()
