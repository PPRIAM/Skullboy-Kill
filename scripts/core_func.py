import pygame, json, os, math

def change_color_palette(image, old_color, new_color):
    image = image
    for x in range(image.get_width()):
        for y in range(image.get_height()):
            if image.get_at((x, y)) == old_color:
                image.set_at((x, y), new_color)
    return image

def count_files_by_extension(path, extension):
    if not os.path.exists(path):
        return 0

    file_count = 0
    for files in os.listdir(path):
        if files.endswith(extension):
            file_count += 1
    return file_count

def generate_animation_data(path):
    animation_data = {}
    for folder in os.listdir(path):
        f = [file for file in os.listdir(path+'/'+folder)]
        animation_data[folder] = f
    return animation_data

def find_key_by_value(dictionary, value):
    for key, val in dictionary.items():
        if val == value:
            return key
    return None  # Retourne None si la valeur n'est pas trouvée dans le dictionnaire


def collision_test(rect, tiles):
    hit_list = []
    for tile in tiles:
        if rect.colliderect(tile):
            hit_list.append(tile)
    return hit_list

def read_json(filename):
	with open(filename+'.json') as f:
		content = json.loads(f.read())
	return content

def write_json(data, filename, tab=0):
	with open(filename+'.json', 'w') as f:
		f.write(json.dumps(data, indent=tab))

def debug(debug, screen, antialias = True, x=0, y=0, color=(255, 255, 255), background= None):
	font = pygame.font.SysFont('calibri', 16, True)
	screen.blit(font.render(str(debug[0])+':'+str(debug[1]), antialias, color, background), (x, y))

def create_grid(data):
	list = []
	for c in range(data['screen']['height']//data['screen']['tilescale']):
		list.append([])
		for l in range(data['screen']['width']//data['screen']['tilescale']):
			list[c].append('')
	return list

def load_img(loc, name):
  return pygame.image.load(loc+name+".png")

def load_particle(loc, len):
  imgs = []
  for i in range(len):
    img = pygame.image.load(loc+str(i)+'.png')
    imgs.append(img)
  return imgs

def load_imgs(loc, name, len):
  imgs = []
  for i in range(len):
    img = pygame.image.load(loc+"/"+name+str(i)+'.png')
    imgs.append(img)
  return imgs

def flip(image, left=False, right=False):
  image_copy = image.copy()
  image_copy = pygame.transform.flip(image_copy, left, right)
  return image_copy

def flips(image_list, lefts=False, rights=False):
  images = []
  for i in image_list:
    images.append(flip(i, lefts, rights))
  return images

def load_animation(sprite_name, anim_type):
  anim = {}
  for n in range(len(anim_type)):
    anim[anim_type[n][0]] = load_imgs("static/animations/"+sprite_name+"/"+anim_type[n][0], sprite_name+"-"+anim_type[n][0]+"-", anim_type[n][1])
    anim[anim_type[n][0]+"left"] = flips(load_imgs("static/animations/"+sprite_name+"/"+anim_type[n][0], sprite_name+"-"+anim_type[n][0]+"-", anim_type[n][1]), True)
  return anim

def create_tile_id(tilePath):
    tiles = os.listdir(tilePath)
    id_list = []
    id_dict = {}
    for i in tiles:
        if '_' in i:
            t = i.split('_')
            id_list.append(t[0][0] + t[1][0])
        else:
            id_list.append(i[0])
    for i, t in zip(id_list, tiles):
        id_dict[i] = t
    return id_dict

def mag(point1:list, point2:list) -> float:
  return math.sqrt((point1[0]-point2[0])**2+(point1[1]-point2[1])**2)

def normalize(vec:list , mag:float) -> list:
  return [vec[0]/mag, vec[1]/mag]
  
def clamp(value, min1, max1, min2, max2):
  return min2 + (max2-min2)*((value-min1)/(max1-min1))

