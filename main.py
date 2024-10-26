import pygame
from pygame.math import Vector2
import math
from math import sin, radians, degrees, copysign
import os
from os import walk
 
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (255, 0, 0)
BLUE = (0, 0, 255)
GREEN = (0, 255, 0)
FUSCIA = (0, 255, 255)
SKY = (137, 217, 239)
BROWN = (69, 30, 10)
#PLAYER_HEIGHT = 10
 
# initialize pygame
pygame.init()

screen_size = (640, 480)

# variables
world_offset = Vector2(0,0)
 
# create a window
scale = 2
screen_scale = pygame.display.set_mode((screen_size[0] * scale, screen_size[1] * scale), 0, 32)
screen = pygame.Surface(screen_size)
#screen = pygame.display.set_mode(screen_size)
pygame.display.set_caption("pygame Test")
 
# clock is used to set a max fps
clock = pygame.time.Clock()
 
# create a demo surface, and draw a red line diagonally across it
surface_size = (25, 45)
test_surface = pygame.Surface(surface_size)
test_surface.fill(WHITE)
#pygame.draw.aaline(test_surface, RED, (0, surface_size[1]), (surface_size[0], 0))

# import sprites
path = 'sprites/dog/'
filenames = [f for f in os.listdir(path) if f.endswith('.png')]
images = {}
for name in filenames:
    imagename = os.path.splitext(name)[0] 
    images[imagename] = pygame.image.load(os.path.join(path, name)).convert_alpha()

path = 'sprites'
filenames = [f for f in os.listdir(path) if f.endswith('.png')]
bg_images = {}
for name in filenames:
    imagename = os.path.splitext(name)[0]
    bg_images[imagename] = pygame.image.load(os.path.join(path, name)).convert_alpha()




class Level:
    def __init__(self, x, y, width, height, img):
        self.position = Vector2(x, y)
        self.worldposition = Vector2(0, 0)
        self.w = width
        self.h = height
        self.rect = pygame.Rect(self.position.x, self.position.y, self.w, self.h)
        self.img = img

    def update(self):
        self.worldposition.x = world_offset.x + self.position.x
        self.worldposition.y = world_offset.y + self.position.y
        self.rect = pygame.Rect(self.worldposition.x, self.worldposition.y, self.w, self.h)
        screen.blit(self.img, (self.worldposition.x, self.worldposition.y))
        '''
        if self.position.x <= p1.position.x <= self.position.x + self.w and self.position.y <= p1.position.y <= self.position.y + self.h:
            print("on platform")
            p1.position.y = self.position.y - PLAYER_HEIGHT
            p1.jumping = False
        '''

levels = []


l = Level(0, 300, 32, 32, bg_images['edgeleft'])
levels.append(l)
for i in range(30):
    l = Level(32 * i, 300, 32, 32, bg_images['ground'])
    levels.append(l)

l = Level(250, 268, 32, 32, bg_images['ground'])
levels.append(l)
l = Level(550, 268, 32, 32, bg_images['ground'])
levels.append(l)


def timer(countdown, amount, dt):
    countdown -= amount * dt
    return countdown


class Player:
    def __init__(self, x, y, colour, up, down, left, right, angle=0.0, length=4, max_steering=180, max_acceleration=20):
        self.position = Vector2(x, y)
        self.velocity = Vector2(0.0, 0.0)
        self.angle = angle
        self.length = length
        self.max_acceleration = max_acceleration
        self.max_steering = max_steering
        self.max_velocity = 80
        self.brake_deceleration = 20
        self.free_deceleration = 40
        self.acceleration = 0.0
        self.steering = 0.0
        self.colour = colour
        self.up = up
        self.down = down
        self.left = left
        self.right = right
        self.acceleration_rate = 25
        self.jumping = False
        #self.rect = None
        self.delay = 0.0
        self.w = 64
        self.h = 64
        self.sprite = "stand_right"
        self.frame = 0
        self.animation_speed = 4
        self.direction = True #True == right, False == left
        self.double_jump = 1
    def animate(self, img):
        self.frame += self.animation_speed * dt
        current_frame = img[int(self.frame) % len(img)]
        self.sprite = current_frame
        

    def update(self, dt, pressed):
        self.velocity += (self.acceleration * dt * 1, 0)

        self.velocity.x = pygame.math.clamp(self.velocity.x, -self.max_velocity, self.max_velocity)
        #self.rect = pygame.draw.rect(screen, BLUE, pygame.Rect(self.position.x, self.position.y + self.h, self.w, 1), 0)
        left_offset = 21
        top_offset = 22
        right_offset = 23
        rect =  pygame.Rect(self.position.x + left_offset + 1, self.position.y + top_offset, self.w - right_offset - 1, self.h - top_offset + 2)
        xrect = pygame.Rect(self.position.x + left_offset - 1, self.position.y + top_offset, self.w - right_offset + 2, self.h - top_offset - 2)
        #pygame.draw.rect(screen, BLUE, rect, 0)
        #pygame.draw.rect(screen, FUSCIA, xrect, 0) 
        #print(self.rect)



        if self.delay > 0:
            self.delay = timer(self.delay, 1, dt)
        else:
            self.delay = 0

        if pressed[self.up]:
            if not self.jumping:
                self.velocity.y = -1000
                self.jumping = True
                self.delay = .5
            else:
                if self.double_jump > 0 and self.delay <= 0:
                    self.velocity.y = -1000
                    self.double_jump -= 1
                
        if self.jumping:
            if self.velocity.y < 0:
                self.velocity.y += self.acceleration_rate * 7 * dt
            else:
                self.velocity.y += self.acceleration_rate * 10 * dt
            
        
            #print(self.velocity.y)
        colliding = False
        xcollide = False
        for level_segment in levels:
            if xrect.colliderect(level_segment.rect):
                if abs(self.velocity.x) > 0:
                    xcollide = True
                    print(f' 1 {xcollide} {self.direction}')

                '''   
                if self.velocity.x > 0:
                    self.position.x = level_segment.worldposition.x - self.w
                elif self.velocity.x < 0:
                    self.position.x = level_segment.worldposition.x
                '''

            if rect.colliderect(level_segment.rect):
                if self.velocity.y > 0:
                    self.position.y = level_segment.worldposition.y - self.h
                    #print(f' collide pos {level_segment.worldposition.y}')
                    #print('collide')
                    
                    colliding = True
                    self.double_jump = 1

                    if self.delay <= 0:
                        self.jumping = False
                #if self.velocity.x > 0:
                #    self.position.x = level_segment.position.x + self.w
            

        if not colliding:
            #print(colliding)
            self.jumping = True

        '''
        elif pressed[self.down]:
            pass
            #self.velocity.y = speed
        else:
            self.velocity.y = 0
        '''
        if xcollide:
            self.acceleration = 0

            if self.velocity.x > 0:
                self.velocity.x = pygame.math.clamp(self.velocity.x, 0, -self.max_velocity)
            elif self.velocity.x < 0:
                self.velocity.x = pygame.math.clamp(self.velocity.x, 0, self.max_velocity)
            else:
                self.velocity.x = 0

        else:
            if pressed[self.left]:
                if not xcollide:
                    if self.velocity.x > 0:
                        self.acceleration = 0
                    self.acceleration += self.acceleration_rate * dt
                    self.acceleration = pygame.math.clamp(self.acceleration, 0, self.max_acceleration)
                    self.velocity.x = -pygame.math.lerp(0, self.max_velocity, self.acceleration / self.max_acceleration)
                    self.direction = False
            elif pressed[self.right]:
                if not xcollide:
                    if self.velocity.x < 0:
                        self.acceleration = 0
                    self.acceleration += self.acceleration_rate * dt
                    self.acceleration = pygame.math.clamp(self.acceleration, 0, self.max_acceleration)
                    self.velocity.x = pygame.math.lerp(0, self.max_velocity, self.acceleration / self.max_acceleration)
                    self.direction = True
            else:
                #if not self.jumping:
                #    if self.velocity.x > 0:
                #        self.sprite = "stand_right"
                #    elif self.velocity.x < 0:
                #        self.sprite = "stand_left"
                self.velocity.x = 0
                self.acceleration = 0
                
        self.velocity.x = pygame.math.clamp(self.velocity.x, -self.max_velocity, self.max_velocity)
        self.velocity.y = pygame.math.clamp(self.velocity.y, -self.max_velocity, self.max_velocity)


        if self.steering:
            turning_radius = self.length / sin(radians(self.steering))
            angular_velocity = self.velocity.x / turning_radius
        else:
            angular_velocity = 0

        self.position += self.velocity.rotate(-self.angle) * dt

        self.angle += degrees(angular_velocity) * dt

        
        if self.jumping:
            if self.direction:
                self.sprite = "jump_right"
            else:
                self.sprite = "jump_left"
        else:    
            if self.velocity.x > 1:
                self.animate(["walk_right1", "walk_right2"])
            elif self.velocity.x < -1:
                self.animate(["walk_left1", "walk_left2"])
            else:
                if self.direction:
                    self.sprite = "stand_right"
                else:
                    self.sprite = "stand_left"

        #print(f' 2 {xcollide} {self.direction}')
        #pygame.draw.rect(screen, self.colour, pygame.Rect(self.position.x, self.position.y, self.w, self.h), 0)
        screen.blit(images[self.sprite], (self.position.x, self.position.y))


p1 = Player(360,100, RED, pygame.K_UP, pygame.K_DOWN, pygame.K_LEFT, pygame.K_RIGHT)
#p2 = Player(240, 240, BLUE, pygame.K_w, pygame.K_s, pygame.K_a, pygame.K_d)


bg = pygame.transform.scale(bg_images['clouds'], (320, 240))

scroll = 0
scroll_speed = 2
tiles = math.ceil(screen_size[0]/bg.get_width()) + 1
running = True
while running:
    dt = clock.get_time() / 1000
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False


    
     
    #clear the screen
    screen.fill(SKY)

    i = 0
    while (i < tiles):
        screen.blit(bg, (bg.get_width() * i + scroll, 0))
        i += 1
    # FRAME FOR SCROLLING
    scroll -= 2

    # RESET THE SCROLL FRAME
    if abs(scroll) > bg.get_width():
        scroll = 0

    screen_rect_x = screen_size[0] / 4
    screen_rect_y = screen_size[1] / 4
    screen_rect_width = screen_size[0] / 3
    screen_rect_height = screen_size[1] / 2
    #pygame.draw.rect(screen, RED, pygame.Rect(screen_rect_x, screen_rect_y, screen_rect_width, screen_rect_height), 1)
    pygame.draw.rect(screen, BROWN, pygame.Rect(0, 332, screen_size[0], 300), 0)
     
    # draw to the screen
    # YOUR CODE HERE
    x = (screen_size[0]/2) - (surface_size[0]/2)
    y = (screen_size[1]/2) - (surface_size[1]/2)
    #screen.blit(test_surface, (x, y))

    turn_rate = 50  # pygame.math.lerp(0, 125, abs(p1.velocity.x) / 10)
    acceleration_rate = 5
    pressed = pygame.key.get_pressed()


    p1.update(dt, pressed)
    #p2.update(dt, pressed)
    #middle_point = (p1.position + p2.position) / 2

    #pygame.draw.circle(screen, WHITE, middle_point, 5)

    for level_segment in levels:
        level_segment.update()


    scroll_speed = pygame.math.lerp(1, 3, p1.position.x / screen_size[0] / 4)
    print(f' ss {scroll_speed}, pos {p1.position.x}, max {screen_size[0] / 4}, / {p1.position.x / screen_size[0] / 4}')
    if p1.position.x <= screen_rect_x:
        #print("outside of rect left")
        world_offset.x += scroll_speed
        p1.position.x += scroll_speed
        scroll += 1
        #p2.position.x += 1
    elif p1.position.x + 64 >= screen_rect_x + screen_rect_width:
        #print("outside of rect right")
        world_offset.x -= scroll_speed
        p1.position.x -= scroll_speed
        scroll -= 1
        #p2.position.x -= 1
    elif p1.position.y <= screen_rect_y:
        #print("outside of rect up")
        world_offset.y += scroll_speed
        p1.position.y += scroll_speed
        #p2.position.y += 1
    elif p1.position.y >= screen_rect_y + screen_rect_height:
        #print("outside of rect down")
        world_offset.y -= scroll_speed
        #p2.position.y -= 1
        p1.position.y -= scroll_speed
    #print(f'x = {p1.position.x} - {screen_rect_x}, y = {p1.position.y} - {screen_rect_y}')

    '''
    if pressed[pygame.K_UP]:
        p1.angle = 90
        if p1.acceleration < 0:
            p1.acceleration = 0
        if p1.velocity.x < 0:
            p1.acceleration = p1.brake_deceleration
        else:
            p1.acceleration += acceleration_rate * dt
    elif pressed[pygame.K_DOWN]:
        p1.angle = 270
        if p1.acceleration < 0:
            p1.acceleration = 0
        if p1.velocity.x < 0:
            p1.acceleration = p1.brake_deceleration
        else:
            p1.acceleration += acceleration_rate * dt
    elif pressed[pygame.K_LEFT]:
        p1.angle = 180
        if p1.acceleration < 0:
            p1.acceleration = 0
        if p1.velocity.x < 0:
            p1.acceleration = p1.brake_deceleration
        else:
            p1.acceleration += acceleration_rate * dt
    elif pressed[pygame.K_RIGHT]:
        p1.angle = 0
        if p1.acceleration < 0:
            p1.acceleration = 0
        if p1.velocity.x < 0:
            p1.acceleration = p1.brake_deceleration
        else:
            p1.acceleration += acceleration_rate * dt
    print(pressed[pygame.KEYDOWN])
    if p1.velocity.x > 0:
        p1.velocity.x -= p1.brake_deceleration * dt
    else:
        p1.velocity.x = 0
    #print(p1.velocity.x)
    '''
    '''
    elif pressed[pygame.K_DOWN]:
        if p1.acceleration > 0:
            p1.acceleration = 0
        if p1.velocity.x > 0:
            p1.acceleration = -p1.brake_deceleration
        else:
            p1.acceleration -= 2 * dt
    else:
        if abs(p1.velocity.x) > dt * p1.free_deceleration:
            p1.acceleration = -copysign(p1.free_deceleration, p1.velocity.x)
        else:
            if dt != 0:
                p1.acceleration = 0
    if pressed[pygame.K_RIGHT]:
        if p1.velocity.x > 0:
            #frame -= 1
            p1.angle -= turn_rate * dt
        else:
            p1.angle += turn_rate * dt
    elif pressed[pygame.K_LEFT]:
        if p1.velocity.x > 0:
            p1.angle += turn_rate * dt
        else:
            p1.angle -= turn_rate * dt
    

    if pressed[pygame.K_w]:
        if p2.acceleration < 0:
            p2.acceleration = 0
        if p2.velocity.y < 0:
            p2.acceleration = p2.brake_deceleration
        else:
            p2.acceleration += acceleration_rate * dt
        p2.velocity.y -= p2.acceleration * dt * 1
        p2dir = 'up'
    elif pressed[pygame.K_s]:
        if p2.acceleration < 0:
            p2.acceleration = 0
        if p2.velocity.y > 0:
            p2.acceleration = p2.brake_deceleration
        else:
            p2.acceleration += acceleration_rate * dt
        p2.velocity.y += p2.acceleration * dt * 1
        p2dir = 'down'
    elif pressed[pygame.K_d]:
        if p2.acceleration < 0:
            p2.acceleration = 0
        if p2.velocity.x < 0:
            p2.acceleration = p2.brake_deceleration
        else:
            p2.acceleration += acceleration_rate * dt
        p2.velocity.x += p2.acceleration * dt * 1
        p2dir = 'right'
    elif pressed[pygame.K_a]:
        if p2.acceleration < 0:
            p2.acceleration = 0
        if p2.velocity.y > 0:
            p2.acceleration = p2.brake_deceleration
        else:
            p2.acceleration += acceleration_rate * dt
        p2.velocity.x -= p2.acceleration * dt * 1
        p2dir = 'left'
    '''
    #print(f'velx {p2.velocity.x}, vely {p2.velocity.y}, accel {p2.acceleration}, dir {p2dir}')


    

    # flip() updates the screen to make our changes visible
    screen_scale.blit(pygame.transform.scale(screen, screen_scale.get_size()), (0, 0))
    pygame.display.update()
    #pygame.display.flip()
     
    # how many updates per second
    clock.tick(60)
 
pygame.quit()
