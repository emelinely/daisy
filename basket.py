import pygame

class Basket:

    def __init__(self):
        self.img = pygame.image.load("assets/basket.png")

        self.img_dimensions = self.img.get_rect().size
        self.width = self.img_dimensions[0]
        self.height = self.img_dimensions[1]

        self.position_x = 0
        self.position_y = 570 - self.height

        self.a = 5
        # self.b = 2

    def draw(self, surface, basket):
        surface.blit(self.img, (self.position_x, self.position_y))
        if len(basket) != 0:
            for flower in basket:
                for i in range(len(basket)):
                    flower.position[0] = self.position_x + self.a*i + 15
                    flower.position[1] = self.position_y+35 #+ self.b*i
                    surface.blit(flower.img, (flower.position[0], flower.position[1]))
