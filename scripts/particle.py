import random
from . import core_func

class Particle:
  def __init__(self, color=(255, 255, 255)):
    self.p = core_func.load_particle("static/p/p", 4)
    self.p = [core_func.change_color_palette(particle, (255, 255, 255), color) for particle in self.p ]
    self.frame = 0
    self.start_img = 0
    self.particles = []

  def add(self, origin, offset=[0, 0]):
    x, y = origin
    dir = [0, -1]
    self.particles.append([[x+random.randint(-5, 5)-offset[0], y-offset[1]], dir, self.p[self.start_img]])

  def update(self, display, dt):
    if self.frame < len(self.p)-1:
        self.frame += 0.5
    else:
      self.frame = 0
    for particle in self.particles:  
      particle[0][0] += particle[1][0]*dt
      particle[0][1] += particle[1][1]*dt
      #particle[1][1] += 0.2
      particle[2] = self.p[int(self.frame)]

      display.blit(particle[2], particle[0])
      
      if particle[2] == self.p[3]:
        self.particles.remove(particle)
        

class Fire:
  def __init__(self):
    self.first_layer = Particle((215, 56, 17))
    self.second_layer = Particle((215, 116, 17))

  def render(self, display, origin, dt):
    self.first_layer.add(origin)
    self.first_layer.update(display, dt)
    self.second_layer.add(origin)
    self.second_layer.update(display, dt)
  