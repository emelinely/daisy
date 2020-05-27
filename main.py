import pygame
from pygame.locals import *
import sys, os, traceback
if sys.platform in ["win32","win64"]: os.environ["SDL_VIDEO_CENTERED"]="1"
import random
from math import *

import flower, player, cloud, bee, basket
from math_helpers import *

import PAdLib.occluder as occluder
import PAdLib.particles as particles

pygame.display.init()
pygame.font.init()
pygame.mixer.init()
# LOAD THE SOUND TO THE player object
# player.shoot_sound = pygame.mixer.Sound('Cat 1.wav')

screen_size = [800,600]
icon = pygame.Surface((1,1)); icon.set_alpha(0); pygame.display.set_icon(icon)
pygame.display.set_caption("Asteroids II - The Vector - v.4.0.0 - Ian Mallett - 2013")
surface = pygame.display.set_mode(screen_size)

# clouds = []
# for i in range(5):
#     clouds.append(cloud.Cloud(screen_size))

num_bees = 1

font1 = pygame.font.Font("assets/FrederickatheGreat-Regular.ttf", 16)
font2 = pygame.font.Font("assets/FrederickatheGreat-Regular.ttf", 32)

# fonts = {
#     16 : pygame.font.SysFont("Times New Roman",16,True),
#     32 : pygame.font.SysFont("Times New Roman",32,True)
# }

colors = [(220, 246, 172), (211, 254, 255), (255, 232, 211), (220, 246, 172), (202, 255, 231), (210, 223, 255), (249, 225, 238)]
color = colors[random.randint(0, len(colors)-1)]

fire_colors = [(255,0,0),(255,255,0),(255,200,0),(255,128,0),(128,0,0),(0,0,0)]

emitter_rocket = particles.Emitter()
emitter_rocket.set_particle_emit_density(0)
emitter_rocket.set_particle_emit_speed([350.0,550.0])
emitter_rocket.set_particle_emit_life([1.0,2.0])
emitter_rocket.set_particle_emit_colors(fire_colors)

emitter_turn1 = particles.Emitter()
emitter_turn1.set_particle_emit_density(0)
emitter_turn1.set_particle_emit_speed([50.0,250.0])
emitter_turn1.set_particle_emit_life([0.05,0.05])
emitter_turn1.set_particle_emit_colors(fire_colors)

emitter_turn2 = particles.Emitter()
emitter_turn2.set_particle_emit_density(0)
emitter_turn2.set_particle_emit_speed([50.0,250.0])
emitter_turn2.set_particle_emit_life([0.05,0.05])
emitter_turn2.set_particle_emit_colors(fire_colors)

emitter_shock = particles.Emitter()
emitter_shock.set_particle_emit_density(0)
emitter_shock.set_particle_emit_angle(0.0,360.0)
emitter_shock.set_particle_emit_speed([50.0,400.0])
emitter_shock.set_particle_emit_life([0.5,1.0])
emitter_shock.set_particle_emit_colors([(255,255,255),(0,0,0)])

emitter_hit = particles.Emitter()
emitter_hit.set_particle_emit_density(0)
emitter_hit.set_particle_emit_angle(0.0,360.0)
emitter_hit.set_particle_emit_speed([100.0,100.0])
emitter_hit.set_particle_emit_life([0.5,1.0])
emitter_hit.set_particle_emit_colors([(255,255,255),(255,255,0),(0,0,255),(0,0,0)])

emitter_die = particles.Emitter()
emitter_die.set_particle_emit_density(0)
emitter_die.set_particle_emit_angle(0.0,360.0)
emitter_die.set_particle_emit_speed([50.0,100.0])
emitter_die.set_particle_emit_life([0.5,2.0])
emitter_die.set_particle_emit_colors(fire_colors)

particle_system = particles.ParticleSystem()
particle_system.add_emitter(emitter_rocket,"rocket")
particle_system.add_emitter(emitter_turn1,"turn1")
particle_system.add_emitter(emitter_turn2,"turn2")
particle_system.add_emitter(emitter_shock,"shock")
particle_system.add_emitter(emitter_hit,"hit")
particle_system.add_emitter(emitter_die,"die")

level_text_brightness = 0

def load_hs():
    global hs
    try:
        f = open("hs.txt","rb")
        hs = int(f.read())
        f.close()
    except:
        hs = 0
def write_hs():
    f = open("hs.txt","wb")
    f.write(str(hs).encode())
    f.close()

def reset_game():
    global level, player1
    level = 0
    # clouds = []
    player1 = player.Player([screen_size[0]/2.0,screen_size[1]/2.0])

    next_level()
def next_level():
    global flowers, bullets, level, level_text_brightness, clouds, bees, num_bees, baske, ba

    level += 1

    player1.level_up(level)

    ba = basket.Basket()
    baske = []

    clouds = []
    for i in range(random.randint(4,8)):
        clouds.append(cloud.Cloud(screen_size))

    flowers = []
    for i in range(2*level):
        flowers.append(flower.Flower([
            random.randint(0,screen_size[0]),
            random.randint(0,screen_size[1])
        ]))

    bees = []
    for i in range(num_bees):
        bees.append(bee.Bee(screen_size))
    if level%7 == 0:
        num_bees += 1

    level_text_brightness = 1.0

turning = None
count = 0
def get_input(dt):
    global turning, count
    keys_pressed = pygame.key.get_pressed()
    mouse_buttons = pygame.mouse.get_pressed()
    mouse_position = pygame.mouse.get_pos()
    mouse_rel = pygame.mouse.get_rel()
    for event in pygame.event.get():
        if   event.type == QUIT: return False
        elif event.type == KEYDOWN:
            if   event.key == K_ESCAPE: return False
            elif event.key == K_F2 and not player1.alive:
                reset_game()
            elif event.key == K_1:
                next_level()
            elif event.key == K_2:
                player1.alive = True
            elif event.key == K_3:
                bees = []

    if player1.alive:
        def reset():
            for emitter in [emitter_turn1,emitter_turn2]:
                emitter._padlib_update(particle_system,dt)
                emitter.set_particle_emit_density(0)
        def set_pos_rot():
            def get_vec(rel,angle_delta):
                rotated = rotate_point(rel,radians(player1.angle+angle_delta))
                return player1.position[0] + rotated[0], player1.position[1] - rotated[1]
            if count > 0:
                emitter_turn1.set_position(get_vec([-3,-8],0))
                emitter_turn2.set_position(get_vec([ 7,6],0))
                emitter_turn1.set_particle_emit_angle(-player1.angle+180,15.0)
                emitter_turn2.set_particle_emit_angle(-player1.angle,15.0)
            else:
                emitter_turn1.set_position(get_vec([ 3,-8],0))
                emitter_turn2.set_position(get_vec([-7,6],0))
                emitter_turn1.set_particle_emit_angle(-player1.angle,15.0)
                emitter_turn2.set_particle_emit_angle(-player1.angle+180,15.0)
        def set_left():
            global count
            emitter_turn1.set_particle_emit_density(200)
            emitter_turn2.set_particle_emit_density(200)
            count =  5
        def set_right():
            global count
            emitter_turn1.set_particle_emit_density(200)
            emitter_turn2.set_particle_emit_density(200)
            count = -5
        if keys_pressed[K_LEFT]:
            player1.angle += 2.0
            if turning == None:
                set_left()
                turning = "left"
        if keys_pressed[K_RIGHT]:
            player1.angle -= 2.0
            if turning == None:
                set_right()
                turning = "right"
        if not keys_pressed[K_LEFT] and not keys_pressed[K_RIGHT]:
            if turning != None:
                if turning == "left":
                    set_right()
                else:
                    set_left()
                turning = None
        if count != 0:
            if count < 0: count += 1
            else:         count -= 1
            if count == 0: reset()
        set_pos_rot()

        if keys_pressed[K_UP]:
            player1.velocity[0] += dt*player.Player.thrust*sin(radians(player1.angle))
            player1.velocity[1] += dt*player.Player.thrust*cos(radians(player1.angle))
            emitter_rocket.set_particle_emit_density(100)
            emitter_rocket.set_particle_emit_angle(-player1.angle-90,5.0)
        if not keys_pressed[K_UP]:
            emitter_rocket.set_particle_emit_density(0)
        if keys_pressed[K_DOWN]:
            player1.velocity[0] *= 0.99
            player1.velocity[1] *= 0.99

        if keys_pressed[K_LCTRL] or keys_pressed[K_RCTRL] or keys_pressed[K_SPACE] or keys_pressed[K_RETURN] or keys_pressed[K_x] or keys_pressed[K_z]:
            player1.shoot()


    return True

# def game_end():
#     surf_level = font1.render("F2 Starts New Game", True, (0,0,0))
#     pos = [
#         (screen_size[0]/2.0)-(surf_level.get_width()/2.0),
#         (screen_size[1]/2.0)-(surf_level.get_height()/2.0)
#     ]
#     surface.blit(surf_level,pos)#,special_flags=BLEND_MAX)
#     pygame.display.update()
#     # clock.tick(15)

def update(dt):
    global level_text_brightness, hs

    if len(flowers) == 0:
        next_level()

    for flower in flowers:
        flower.update(dt, screen_size)

    for bee in bees:
        bee.update(screen_size)

    player1.update(dt, screen_size) #game_end)

    if player1.score > hs:
        hs = player1.score

    if len(clouds) != 0:
        for cloud in clouds:
            cloud.update(screen_size)

    if player1.alive:
        # player1.collide_bullets(asteroids, particle_system, dt)
        player1.collide_bees_bullet(bees, particle_system, dt)
        player1.collide_flowers(flowers, baske, particle_system)
        player1.collide_bees(bees, particle_system)
    emitter_rocket.set_position(player1.position)
##    particle_system.set_particle_occluders([asteroid.occluder for asteroid in asteroids])
    particle_system.update(dt)

    if level_text_brightness > 0.0:
        level_text_brightness -= dt

    return True

def draw():
    surface.fill(color)

    if len(clouds) != 0:
        for cloud in clouds:
            cloud.draw(surface)

    particle_system.draw(surface)

    player1.draw(surface)
    # surface.blit(player1.img, 100, 100)#player1.position[0], player1.position[1])

    for flower in flowers:
        flower.draw(surface)

    for bee in bees:
        bee.draw(surface)

    ba.draw(surface, baske)

    surf_level = font1.render("Level: "+str(level), True, (0,0,0))
    surface.blit(surf_level,(10,10))

    surf_lives = font1.render("Lives: "+str(max([player1.lives,0])), True, (0,0,0))
    surface.blit(surf_lives,(10,30))

    surf_score = font1.render("Score: "+str(player1.score), True, (0,0,0))
    surface.blit(surf_score,(screen_size[0]-surf_score.get_width()-10,10))

    surf_highscore = font1.render("High Score: "+str(hs), True, (0,0,0))
    surface.blit(surf_highscore,(screen_size[0]-surf_highscore.get_width()-10,30))

    surf_health = font1.render("Health: {}".format(player1.health), True, (0, 0, 0))
    surface.blit(surf_health,(10,50))

    surf_bee = font1.render("*you do not need to kill the bee(s) to win*", True, (0, 0, 0))
    surface.blit(surf_bee,(260,screen_size[1]-surf_bee.get_height()-10))

    if player1.lives >= 0:
        surf_remain = font1.render("Flowers Left: "+str(len(flowers)), True, (0,0,0))
        surface.blit(surf_remain,(10,screen_size[1]-surf_remain.get_height()-10))

        if level_text_brightness > 0.0:
            col = rndint(255.0*level_text_brightness)
            surf_level = font2.render("Level "+str(level), True, (col,col,col),(0,0,0))
            pos = [
                (screen_size[0]/2.0)-(surf_level.get_width()/2.0),
                (screen_size[1]/2.0)-(surf_level.get_height()/2.0)
            ]
            surface.blit(surf_level,pos,special_flags=BLEND_MAX)
    else:

        surf_level = font1.render("F2 Starts New Game", True, (0,0,0))
        pos = [
            (screen_size[0]/2.0)-(surf_level.get_width()/2.0),
            (screen_size[1]/2.0)-(surf_level.get_height()/2.0)
        ]
        surface.blit(surf_level,pos)

    surf_fps = font1.render("FPS: "+str(round(clock.get_fps(),1)), True, (0,0,0))
    surface.blit(surf_fps,(screen_size[0]-surf_fps.get_width()-10,screen_size[1]-surf_fps.get_height()-10))

    pygame.display.flip()

def main():
    global clock

    load_hs()

    target_fps = 60
    dt = 1.0/float(target_fps)

    reset_game()
    clock = pygame.time.Clock()
    while True:
        if not get_input(dt): break
        if not update(dt): break
        draw()
        clock.tick(target_fps)
    pygame.quit()

    write_hs()

# def intro():
#     global clock
#     while True:
#         surface.fill(color)
#         clock = pygame.time.Clock()
#         def button(msg,x,y,w,h,ic,ac,surface,action=None,):
#             mouse = pygame.mouse.get_pos()
#             click = pygame.mouse.get_pressed()
#             is_clicking = False
#
#             if x+w > mouse[0] > x and y+h > mouse[1] > y:
#                 pygame.draw.rect(surface, ac,(x,y,w,h))
#
#                 if not is_clicking and click[0] == 1 and action != None:
#                     is_clicking = True
#                     action()
#             else:
#                 pygame.draw.rect(surface, ic,(x,y,w,h))
#             # help with click control
#             if click[0] == 0:
#                 is_clicking = False
#
#             surf = font1.render(msg, True, (0,0,0))
#             surface.blit(surf,(x,y))
#
#         button(msg="Start Game", x=150,y=200,w=150,h=90,ic=(255,255,255),ac=(0,0,0),surface=surface,action=main)
#         button(msg="Exit", x=3000,y=200,w=150,h=90,ic=(255,255,255),ac=(0,0,0),surface=surface,action=exit)
#
#         surf_rules = font1.render("- destroy asteroids to win \n - you do not need to kill the bees \n - bees give health to the asteroids", True, (0,0,0))
#         surface.blit(surf_rules,(screen_size[0]/2-surf_rules.get_height(),screen_size[1]-surf_rules.get_height()-10))
#
#         pygame.display.update()
#         clock.tick(15)

if __name__ == "__main__":
    try:
        main()
    except:
        traceback.print_exc()
        pygame.quit()
        input()
