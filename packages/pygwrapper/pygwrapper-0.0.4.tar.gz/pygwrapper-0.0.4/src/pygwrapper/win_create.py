import pygame
import pymunk
from win32api import GetSystemMetrics
pygame.init()

def nothing():
    pass
class GameInstance:
    def __init__(self):
        self.win_size = (GetSystemMetrics(0), int(GetSystemMetrics(1)*0.9))
        self.win = pygame.display.set_mode((self.win_size))
        self.clock = pygame.time.Clock()
        self.space = pymunk.Space()

    def start_window(self,caption,mainloop,get_event=nothing,on_quit=nothing):
        pygame.display.set_caption(caption)
        self.space.gravity = (0,500)
        run = True
        while run:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    run = False
                    on_quit()
                get_event()
            mainloop()
            pygame.display.update()
            self.clock.tick(120)
            self.space.step(1/120)
        pygame.quit()
