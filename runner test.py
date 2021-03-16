import pygame
import level_manager as level_manager

pygame.init()
win_dim = (800, 800)
win = pygame.display.set_mode(win_dim)
done = False
<<<<<<< HEAD:combat test.py
LM = level_manager.LevelManager(win, "Combat")
=======
LM = level_manager.LevelManager(win, "Runner")
>>>>>>> origin/main:runner test.py
while not done:
    LM.update()
    done = LM.handle_input()
    LM.draw()

pygame.quit()