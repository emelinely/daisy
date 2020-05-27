import pygame
import random

from math_helpers import *
# import PAdLib.occluder as occluder

class Flower:
    speed = 10.0

    def __init__(self, position):
        self.position = list(position)
        self.velocity = [
            Flower.speed*random.uniform(-1.0,1.0),
            Flower.speed*random.uniform(-1.0,1.0)
        ]

        self.angle = random.uniform(0.0,360.0)
        self.spin = random.uniform(-1.0,1.0)

        self.health = 5
        self.radius = 20

        self.name = "flower"

        numof_points = random.randint(3,8)
        # self.rel_points = []
        # for i in range(numof_points):
        #     angle = (i*2*pi)/numof_points
        #     point = []
        #     point.append(  cos(angle)  )
        #     point.append(  sin(angle)  )
        #     self.rel_points.append(point)
        if numof_points == 3:
            self.img = pygame.image.load("assets/3.png")#.convert()
            self.radius = 17.5
            self.center_x = 28 #from left
            self.center_y = 18 #from top
        elif numof_points == 4:
            self.img = pygame.image.load("assets/4.png")#.convert()
            self.radius = 17
            self.center_x = 26 #from left
            self.center_y = 19 #from top
        elif numof_points == 5:
            self.img = pygame.image.load("assets/5.png")#.convert()
            self.radius = 19
            self.center_x = 26 #from left
            self.center_y = 19 #from top
        elif numof_points == 6:
            self.img = pygame.image.load("assets/6.png")#.convert()
            self.radius = 20
            self.center_x = 26 #from left
            self.center_y = 22 #from top
        elif numof_points == 7:
            self.img = pygame.image.load("assets/7.png")#.convert()
            self.radius = 19
            self.center_x = 39 #from left
            self.center_y = 31 #from top
        else:
            self.img = pygame.image.load("assets/8.png")#.convert()
            self.radius = 19
            self.center_x = 26 #from left
            self.center_y = 19 #from top


    def hit(self):
        self.health -= 1
        # self.radius -= 2

    def update(self, dt, screen_size):

        # old_angle = self.angle

        self.position[0] += self.velocity[0] * dt
        self.position[1] += self.velocity[1] * dt
        if self.position[0] < 0:
            self.position[0] = 0
            self.velocity[0] *= -1.0
        elif self.position[0] > screen_size[0]:
            self.position[0] = screen_size[0]
            self.velocity[0] *= -1.0
        if self.position[1] < 0:
            self.position[1] = 0
            self.velocity[1] *= -1.0
        elif self.position[1] > screen_size[1]-50:
            self.position[1] = screen_size[1]-50
            self.velocity[1] *= -1.0

        self.angle = (self.angle+self.spin) % 360.0

        # self.real_points = []
        # # angle_rad = radians(self.angle)
        # # for x,y in self.rel_points:
        # #     rotated = rotate_point([self.radius*x,self.radius*y],angle_rad)
        # #     self.real_points.append([
        # #         rotated[0] + self.position[0],
        # #         rotated[1] + self.position[1]
        # #     ])
        #
        # self.occluder = occluder.Occluder(self.real_points)
        # self.occluder.set_bounce(0.1)

        # angle_dif = old_angle - self.angle
        # self.img = pygame.transform.rotate(self.img, self.angle)

    def draw(self, surface):
        # pygame.draw.aalines(surface,(255,255,255),True,self.real_points
        surface.blit(pygame.transform.rotate(self.img, self.angle), self.position)
