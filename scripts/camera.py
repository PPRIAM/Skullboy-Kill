
class Camera:
  def __init__(self, target):
    self.target = target
    self.offset = [0, 0]

  def update(self, screen):
    self.offset[0] += (self.target.x-self.offset[0]-(screen.get_width()//2-self.target.width//2))/5
    self.offset[1] += (self.target.y-self.offset[1]-(screen.get_height()//2-self.target.height//2))/5

