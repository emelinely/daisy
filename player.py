import pygame
from math import *
import math

import bullet

class Player:
    thrust = 300.0

    def __init__(self, position):
        self.position = list(position)
        self.velocity = [0.0,0.0]

        self.angle = 90.0

        self.img = pygame.image.load("assets/daisy_cat1.png")

        self.img_dimensions = self.img.get_rect().size
        self.width = self.img_dimensions[0]
        self.height = self.img_dimensions[1]
        self.center_x = self.position[0] + self.width/2
        self.center_y = self.position[1] + self.height/2

        self.fire = 0.0
        self.bullets = []

        #List of (angle,radius) pairs.
        self.rel_points = [[0, 20], [-140, 20], [180, 7.5], [140, 20]]
        scale = 0.5
        for i in range(len(self.rel_points)):
            self.rel_points[i] = (radians(self.rel_points[i][0]),scale*self.rel_points[i][1])

        self.thrust_append = 0

        self.alive = True
        self.health = 20
        self.dying = False
        self.lives = 3
        self.time_invincibility = 0
        self.shoot_effect = pygame.mixer.Sound("assets/kitten_mew-1.wav")
        self.score = 0

    def level_up(self, new_level):
        self.alive = True
        self.velocity = [0.0,0.0]

        self.bullets = []

        if new_level % 5 == 0:
            self.lives += 1

        self.time_invincibility = 2.5

    def shoot(self):
        if self.fire <= 0.0:
            # Play Sound

            angle_rad = radians(-self.angle+90)
            pos = [
                self.position[0] + 7.5*cos(angle_rad),
                self.position[1] + 7.5*sin(angle_rad)
            ]
            self.bullets.append(bullet.Bullet(pos,angle_rad))

            self.fire += 0.1
    def update(self, dt, screen_size):#, reset_game):
        self.position[0] += self.velocity[0] * dt
        self.position[1] += self.velocity[1] * dt

        if self.position[0] < 0:
            self.position[0] = 0
            self.velocity[0] *= -0.5
        elif self.position[0] > screen_size[0]:
            self.position[0] = screen_size[0]
            self.velocity[0] *= -0.5
        if self.position[1] < 0:
            self.position[1] = 0
            self.velocity[1] *= -0.5
        elif self.position[1] > screen_size[1]:
            self.position[1] = screen_size[1]
            self.velocity[1] *= -0.5

        if self.time_invincibility > 0.0:
            self.time_invincibility -= dt
        if self.fire > 0.0:
            self.fire -= dt
        if self.health <= 0:
            self.alive = False
            self.lives -= 1
            self.health = 6
        if self.dying != False:
            self.dying -= dt
            if self.dying < 0.0:
                self.dying = False

                self.position = [screen_size[0]/2,screen_size[1]/2]
                self.velocity = [0.0,0.0]
                self.time_invincibility = 2.5

                self.lives -= 1
                if self.lives >= 0:
                    self.alive = True
        # if self.lives <= 0:
            # reset_game()

        for b in self.bullets:
            b.update(dt)
            if b.time > 5.0:
                self.bullets.remove(b)
                continue

        self.center_x = self.position[0] + self.width/2
        self.center_y = self.position[1] + self.height/2

        self.real_points = []
        for point_angle,point_radius in self.rel_points:
            angle = radians(self.angle) + point_angle
            xp = point_radius * sin(angle)
            yp = point_radius * cos(angle)
            self.real_points.append((
                self.position[0] + xp,
                self.position[1] + yp
            ))

    # def collide_bullets(self, asteroids, particle_system, dt):
    #     for bullet in self.bullets:
    #         for asteroid in asteroids:
    #             dist = sqrt(((bullet.position[0]-(asteroid.position[0] + asteroid.center_x))**2)+((bullet.position[1]-(asteroid.position[1] + asteroid.center_y))**2))
    #             if dist <= asteroid.radius:
    #                 emitter = particle_system.emitters["hit"]
    #                 emitter.set_position(bullet.position)
    #                 emitter.set_particle_emit_density(100)
    #                 emitter._padlib_update(particle_system,dt)
    #                 emitter.set_particle_emit_density(0)
    #
    #                 asteroid.hit()
    #
    #                 self.score += 10
    #
    #                 if asteroid.health == 0:
    #                     emitter = particle_system.emitters["shock"]
    #                     emitter.set_position(asteroid.position)
    #                     emitter.set_particle_emit_density(1000)
    #                     emitter._padlib_update(particle_system,dt)
    #                     emitter.set_particle_emit_density(0)
    #
    #                     asteroids.remove(asteroid)
    #                     self.score += 100
    #
    #                 self.bullets.remove(bullet)
    #                 break

    def collide_bees_bullet(self, bees, particle_system, dt):
        for bullet in self.bullets:
            for bee in bees:
                dist = sqrt(((bullet.position[0]-bee.center_x)**2)+((bullet.position[1]-bee.center_y)**2))
                if dist <= 40:
                    emitter = particle_system.emitters["hit"]
                    emitter.set_position((bee.position_x, bee.position_y))
                    emitter.set_particle_emit_density(100)
                    emitter._padlib_update(particle_system,dt)
                    emitter.set_particle_emit_density(0)

                    bee.hit()

                    self.score += 10

                    if bee.health == 0:
                        emitter = particle_system.emitters["shock"]
                        emitter.set_position((bee.position_x, bee.position_y))
                        emitter.set_particle_emit_density(1000)
                        emitter._padlib_update(particle_system,dt)
                        emitter.set_particle_emit_density(0)

                        bees.remove(bee)
                        self.score += 100

                    self.bullets.remove(bullet)
                    break

    def collide_flowers(self, flowers, basket, particle_system):
        if self.dying: return True
        if self.time_invincibility > 0.0: return True

        for flower in flowers:
            dist = sqrt(((self.center_x-(flower.position[0] + flower.center_x))**2) + ((self.center_y-(flower.position[1] + flower.center_y))**2))
            # for point in self.real_points:
            if dist <= flower.radius + 43:
                basket.append(flower)
                flowers.remove(flower)
                self.score += 100

                particle_system.emitters["rocket"].set_particle_emit_density(0)
                particle_system.emitters["turn1"].set_particle_emit_density(0)
                particle_system.emitters["turn2"].set_particle_emit_density(0)

                # particle_system.emitters["die"].set_position(self.position)
                # particle_system.emitters["die"].set_particle_emit_density(1000)
                # particle_system.emitters["die"]._padlib_update(particle_system,0.1)
                # particle_system.emitters["die"].set_particle_emit_density(0)

                # self.dying = 1.0
                # self.alive = False

                return

    def collide_bees(self, bees, particle_system):
        if self.dying: return True
        if self.time_invincibility > 0.0: return True

        for bee in bees:

            dist = sqrt(((self.center_x-(bee.position_x + 51))**2) + ((self.center_y-(bee.position_y + 52))**2))
            # for point in self.real_points:
            if dist <= 40 + 43:

                self.health -= 1
                # self.shoot_effect.play()

                particle_system.emitters["rocket"].set_particle_emit_density(0)
                particle_system.emitters["turn1"].set_particle_emit_density(0)
                particle_system.emitters["turn2"].set_particle_emit_density(0)

                particle_system.emitters["die"].set_position(self.position)
                particle_system.emitters["die"].set_particle_emit_density(1000)
                particle_system.emitters["die"]._padlib_update(particle_system,0.1)
                particle_system.emitters["die"].set_particle_emit_density(0)


    def draw(self, surface):
        for b in self.bullets:
            b.draw(surface)

        if self.alive:
            color = (255,255,255)
            if self.time_invincibility > 0.0:
                if self.time_invincibility % 0.1 < 0.03:
                    color = (0,0,255)
            # pygame.draw.aalines(surface,color,True,self.real_points,True)
            # self.img = pygame.transform.rotate(self.img, self.angle)
            surface.blit(pygame.transform.rotate(self.img, self.angle-90), (self.position[0]-60, self.position[1]))
