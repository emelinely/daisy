import pygame
import random
import math

class Bee:
    def __init__(self, screen_size):
        self.position_x = random.randint(0, screen_size[0]-50)
        self.position_y = random.randint(0, screen_size[1]-50)

        self.velocity_x = random.randint(1,4)
        self.velocity_y = random.randint(1,4)

        self.img = pygame.image.load("assets/bee.png")

        self.img_dimensions = self.img.get_rect().size
        self.width = self.img_dimensions[0]
        self.height = self.img_dimensions[1]
        self.center_x = self.position_x + self.width/2
        self.center_y = self.position_y + self.height/2

        self.angle = 10
        self.count = 0

        self.health = 7
        self.alive = True

    def help_asteroids(self, asteroids):
        for asteroid in asteroids:
            dist = sqrt(((self.center_x-(asteroid.position[0] + asteroid.center_x))**2) + ((self.center_y-(asteroid.position[1] + asteroid.center_y))**2))
            # for point in self.real_points:
            if dist <= asteroid.radius + 40:
                asteroid.health += random.randint(1,3)

    def hit(self):
        self.health -= 1

    def update(self, screen_size):
        self.position_x += self.velocity_x
        self.position_y += self.velocity_y

        if self.position_x < 0:
            self.position_x = 0
            self.velocity_x *= -1.0
        elif self.position_x > screen_size[0]-50:
            self.position_x = screen_size[0]-50
            self.velocity_x *= -1.0
        if self.position_y < 0:
            self.position_y = 0
            self.velocity_y *= -1.0
        elif self.position_y > screen_size[1]-50:
            self.position_y = screen_size[1]-50
            self.velocity_y *= -1.0

        if self.velocity_x < 0:
            self.img = pygame.image.load("assets/bee.png")
        elif self.velocity_x > 0:
            self.img = pygame.image.load("assets/bee1.png")

        self.center_x = self.position_x + self.width/2
        self.center_y = self.position_y + self.height/2

    def draw(self, surface):
        if self.count % 10 == 0:
            self.angle *= -1
        self.count += 1
        surface.blit(pygame.transform.rotate(self.img, self.angle), (self.position_x, self.position_y))
