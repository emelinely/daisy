import random
import pygame

class Cloud:

    def __init__(self, screen_size):
        self.type = random.randint(1,2)
        self.alive = True
        self.position_y = random.randint(0, (screen_size[1]-200))
        if self.type == 1:
            self.position_x = 0
            self.img = pygame.image.load("assets/cloud_fr_left.png")
            self.velocity = random.randint(1, 6)
        else:
            self.position_x = screen_size[0]-1
            self.img = pygame.image.load("assets/cloud_fr_right.png")
            self.velocity = random.randint(1, 15)*(-1)

    def update(self, screen_size):
        if self.type == 1:
            if self.position_x > screen_size[0]:
                self.position_x = 0
            else:
                self.position_x += self.velocity
        else:
            if self.position_x < 0:
                self.position_x = screen_size[0]-1
            else:
                self.position_x += self.velocity

    def draw(self, surface):
        surface.blit(self.img, (self.position_x, self.position_y))
