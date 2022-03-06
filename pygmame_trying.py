from argon2 import PasswordHasher
import pygame
import pygame_gui


class pygame_Window:
    def __init__(self):
        Window_width = 700
        Window_heigth = 500
        self.size = (Window_width, Window_heigth)

    def start(self):
        pygame.init()
        pygame.display.set_caption('First Game')
        self.screen = pygame.display.set_mode(self.size)

        finish = False
        while not finish:
            self.screen.fill((255, 0, 255))
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    finish = True

            pygame.display.flip()
        pygame.quit()
