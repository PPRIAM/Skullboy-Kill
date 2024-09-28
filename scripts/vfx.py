import pygame
from . import core_func

class Trail:
    def __init__(self, type, length, lifetime, source, r=255, g=255, b=255):
        self.type = type
        self.length = length
        self.lifetime = lifetime
        self.source = source
        self.trails = []
        self.r = r
        self.g = g
        self.b = b

    def add(self, pos):
        if len(self.trails) <= self.length:
            if self.type == "circle":
                radius = 2
                self.trails.append([pos, radius, radius])

    def update(self, display, dt):
        for trail in self.trails:
            color = (self.r, self.g, self.b, core_func.clamp(trail[1], 0, trail[2], 0, 255))
            #print(color, trail[1], trail[2])
            pygame.draw.circle(display, color, trail[0], trail[1])
            if trail[1] > 1:
                trail[1] -= self.lifetime

