import pygame, math
from . import core_func

class Entity:
  def __init__(self, origin, speed, image, isMovable=False, outline=False, colorkey = (0, 0, 0)):
    self.image = image.convert()
    self.image.set_colorkey(colorkey)
    self.rect = self.image.get_rect(center=origin)
    self.isMovable = isMovable
    self.movement = [0, 0]
    self.speed = speed
    self.outline = outline
    self.mask = pygame.mask.from_surface(self.image)
    

  def render(self, display, offset=[0, 0]):
    display.blit(self.image, (self.rect.x-offset[0], self.rect.y-offset[1]))
  def update(self, sprite):
    if self.isMovable:
      if self.rect.colliderect(sprite.rect):
        self.movement = sprite.movement

class Player(Entity):
    def __init__(self, origin, speed,  animation_data, game_data, health=10, velocity=[2, 2], dash_speed=100, dash_reload_tick=5000, dash_amount=1):
        Entity.__init__(self, origin, speed, pygame.Surface([1,1]))
        self.origin = origin
        self.states = [k for k in list(animation_data.keys())]
        self.state = "idle"
        self.animation_data = animation_data 
        self.frames = self.animation_data[self.state]
        self.animation_speed = 0.21
        self.frame_index = 0
        self.direction = "left"
        self.image = pygame.transform.scale2x(pygame.image.load(game_data['animation_path']['player']+'/'+self.state+'/'+self.frames[self.frame_index]))
        self.rect = self.image.get_rect(center = self.origin)
        self.health = health
        self.max_health = health
        self.velocity = velocity
        self.is_dashing = False
        self.dash_reload_tick = dash_reload_tick
        self.dash_speed = dash_speed
        self.dash_direction = [0, 0]
        self.dash_amount = dash_amount
        self.max_dash_reload_tick = dash_reload_tick
        self.dash_start_tick = 0
        self.kill = 0

    def set_action(self, action):
        if action in self.animation_data:
            self.state = action
            self.frames = self.animation_data[self.state]
    
    def update(self, dt, game_data):
        if self.movement[0]<0:
            self.direction = "left"
        elif self.movement[0]>0:
            self.direction = "right"

        self.animate(dt, game_data)
        self.set_action("idle")
 
        if self.movement[0] != 0 or self.movement[1] != 0:
            self.set_action("run")

        if self.health <= 0:
            self.movement[0], self.movement[1] = 0, 0
            self.set_action("die")

        self.move(dt)

        if pygame.time.get_ticks()-self.dash_start_tick > self.max_dash_reload_tick and self.dash_amount < 1:
            self.dash_amount += 1
            self.dash_start_tick = pygame.time.get_ticks()
      
    def move(self, dt):
        self.rect.x += self.velocity[0]*self.movement[0] * dt
        self.rect.y += self.velocity[1]* self.movement[1] * dt

    def dash(self, current_tick, point):
        if not self.is_dashing and self.dash_amount > 0:
            self.is_dashing = True
            self.dash_direction = core_func.normalize([point[0]-self.rect.centerx, point[1]-self.rect.centery], core_func.mag(self.rect.center, point))

        if self.is_dashing:
            self.rect.x += self.dash_speed*self.dash_direction[0]
            self.rect.y += self.dash_speed*self.dash_direction[1]
            if self.dash_amount > 0:
                self.dash_amount -= 1
        
        self.is_dashing  = False


    def set_damage(self, damage):
        if self.health > 0:
            self.health -= damage

    def animate(self, dt, game_data):
        if self.state in ["idle", "run"]:
            self.frame_index += self.animation_speed * dt

        if self.state == "die":
            if self.frame_index <= len(self.frames)-1:
                self.frame_index += self.animation_speed * dt 

        if self.frame_index >= len(self.frames) and self.state in ["idle", "run"]:
            self.frame_index = 0

        if self.direction == "left":
            self.image = pygame.transform.scale2x(pygame.transform.flip(pygame.image.load(game_data['animation_path']['player']+'/'+self.state+'/'+self.frames[int(self.frame_index)]), True, False))
        else:
            self.image = pygame.transform.scale2x(pygame.image.load(game_data['animation_path']['player']+'/'+self.state+'/'+self.frames[int(self.frame_index)]))
    
class Gun:
    def __init__(self, image, max_magazine, pos=[0, 0]):
        self.image = core_func.change_color_palette(image, (0, 0,0), (1, 1,1))
        self.image.set_colorkey((0, 0, 0))
        self.img_copy = self.image.copy()
        self.pos = pos
        self.flip = False
        self.magazine = max_magazine
        self.max_magazine = max_magazine
        self.rect = self.img_copy.get_rect(center=self.pos)

    def update(self, point, pos, offset=[0, 0]):
        self.rect = self.img_copy.get_rect(center=pos)
        angle = math.degrees(-self.get_angle(point))
        if angle > 90 or angle <-90:
            self.img_copy = pygame.transform.scale2x(pygame.transform.flip(pygame.transform.rotate(self.image, math.degrees(self.get_angle(point))), False, True))
        else:
            self.img_copy = pygame.transform.scale2x(pygame.transform.flip(pygame.transform.rotate(self.image, math.degrees(-self.get_angle(point))), False, False))
        self.img_copy.set_colorkey((0, 0, 0))

    def get_angle(self, point, offset=[0, 0]):
        return math.atan2(point[1]-(self.rect.centery), point[0]-(self.rect.centerx))

    def render(self, display, offset=[0, 0]):
        display.blit(self.img_copy, [self.rect.x-offset[0], self.rect.y-offset[1]])

    def shoot(self, bullet, pos,angle, offset=[0, 0]):
        if self.magazine > 0:
            self.magazine -= 1
            bullet.add_bullet(pos, angle, offset)

    def reload(self):
        if self.magazine != self.max_magazine:
            self.magazine = self.max_magazine


class Bullet:
    def __init__(self, image, velocity, damage):
        self.image = image.convert()
        self.bullets = []
        self.velocity = velocity
        self.damage = damage

    def add_bullet(self, pos, angle, offset=[0, 0]):
        self.bullets.append([[pos[0]-offset[0], pos[1]-offset[1]], angle, self.velocity])

    def update(self, dt, display, offset=[0, 0]):
        for bullet in self.bullets:
            bullet[0][0] += bullet[2]*math.cos(bullet[1])*dt
            bullet[0][1] += bullet[2]*math.sin(bullet[1])*dt
            display.blit(pygame.transform.scale2x(pygame.transform.rotate(self.image, math.degrees(-bullet[1]))), [bullet[0][0]-offset[0], bullet[0][1]-offset[1]])

            if bullet[0][0] < 0 or bullet[0][0] > display.get_width() or bullet[0][1] < 0 or bullet[0][1] > display.get_height():
                self.bullets.remove(bullet)

    def set_damage(self, entity_health, damage):
        entity_health -= damage

class Enemy(Entity):
    def __init__(self, origin, speed, health, animation_data, game_data, damage=1):
        Entity.__init__(self, origin, speed, pygame.Surface([1, 1]))
        self.pos = origin
        self.animation_data = animation_data
        self.state = "run"
        self.frame_index = 0
        self.frames = self.animation_data[self.state]
        self.image = pygame.transform.scale2x(pygame.image.load(game_data['animation_path']['enemy']+'/'+self.state+'/'+self.frames[self.frame_index]))
        self.rect = self.image.get_rect(center=self.pos)
        self.animation_speed= 0.25
        self.velocity = [speed, speed]
        self.health = health
        self.max_health = health
        self.damage = damage

    def set_action(self, action):
        if action in self.animation_data:
            self.state = action
            self.frames = self.animation_data[self.state]

    def update(self, target, dt, game_data, offset=[0, 0]):
        self.set_action("idle")
        mag = core_func.mag(self.rect.center, target.rect.center)
        n = core_func.normalize([self.rect.centerx-target.rect.center[0], self.rect.centery-target.rect.center[1]], mag)

        if target.health > 0 and not self.rect.colliderect(target.rect):
            self.set_action("run")
            self.rect.centerx -= self.velocity[0]*n[0]*dt
            self.rect.centery -= self.velocity[1]*n[1]*dt
        self.animate(dt, game_data)

    def on_damage(self, damage):
        self.health -= damage

    def animate(self, dt, game_data):
        if self.state == "idle":
            self.frame_index = 0
        if self.state == "run":
            self.frame_index += self.animation_speed*dt

        if self.frame_index > len(self.frames):
            self.frame_index = 0

        self.image = pygame.transform.scale2x(pygame.image.load(game_data['animation_path']['enemy']+'/'+self.state+'/'+self.frames[int(self.frame_index)]))
