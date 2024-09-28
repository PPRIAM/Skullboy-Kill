import pygame, sys, time,math, random
from scripts import core_func, entities, camera

pygame.init()
clock = pygame.time.Clock()
FPS = 60
start_time = time.time()

s_tick = pygame.time.get_ticks()
last_spawn = pygame.time.get_ticks()
controls_tick = pygame.time.get_ticks()

screen = pygame.display.set_mode((640, 480))
display = pygame.Surface([320, 240])
pygame.display.set_caption("SkullBoy Kill")
pygame.mouse.set_visible(False)

font = pygame.font.Font("static/fonts/Essentle4.otf")

display_overlay = pygame.Surface(screen.get_size())

game_data = core_func.read_json("game")

player = entities.Player([screen.get_width()//2, screen.get_height()//2], 10, core_func.generate_animation_data("static/animations/player"), game_data, velocity=[3, 3], dash_speed=200, dash_reload_tick=10000)

gun = entities.Gun(core_func.load_img("static/", "gun"), 99999, [player.rect.centerx, player.rect.centery])

bullet = entities.Bullet(core_func.load_img("static/", "bullet"), 10, 2)

#enemy = entities.Enemy([random.randint(150, 150), random.randint(150, 150)], 1, 10, core_func.generate_animation_data(game_data["animation_path"]["enemy"]), game_data)

enemy_spawn_point = [[0, 0], [screen.get_width(), 0], [0, screen.get_height()], [screen.get_width(), screen.get_height()]]
enemies = []
enemies.append(entities.Enemy(random.choice(enemy_spawn_point), 1.5, 10, core_func.generate_animation_data(game_data["animation_path"]["enemy"]), game_data, 0.01))

camera = camera.Camera(player.rect)

spawn_wait_time = 5000

trail_length = 2
trail_life = 0.5
trail_list = []

dash_ui = core_func.load_img("static/", "dash_ui")

controls = core_func.load_img("static/", "controls")

skullhead = core_func.load_img("static/", "skullhead")

shoot = pygame.mixer.Sound("static/sounds/player_shoot.wav")
shoot.set_volume(0.2)
enemy_hurt = pygame.mixer.Sound("static/sounds/enemy_hurt.wav")
enemy_hurt.set_volume(0.1)
dash = pygame.mixer.Sound("static/sounds/dash.wav")
dash.set_volume(0.3)

pygame.mixer.music.load("static/sounds/music.wav")
pygame.mixer.music.set_volume(0.5)
pygame.mixer.music.play(-1)

death_screen = pygame.Surface(screen.get_size())

while True:
	
	clock.tick(FPS)
	screen.fill((255, 255, 255))
	screen.fill((0, 0, 0))
	death_screen.fill((0, 0, 0))
	dt = time.time()-start_time
	dt *= 60
	start_time = time.time()

	current_tick = pygame.time.get_ticks()-s_tick
	shooting_tick = current_tick

	#camera.update(screen)
	
	player.render(screen, camera.offset)
	player.update(dt, game_data)
	if player.rect.x < 0:
		player.rect.x += screen.get_width()-player.rect.width
	elif player.rect.x + player.rect.width > screen.get_width():
		player.rect.x -= screen.get_width()-player.rect.width
	if player.rect.y < 0:
		player.rect.y += screen.get_height()-player.rect.height
	elif player.rect.y+player.rect.height > screen.get_height():
		player.rect.y -= screen.get_height()-player.rect.height
	

	for i in range(trail_length):
		img = player.image.convert()
		img.set_alpha(core_func.clamp(i, 0, trail_length, 0, 255))
		trail_list.append([img, trail_life, player.rect.topleft])

	#pygame.draw.rect(screen, (255, 0, 0), pygame.Rect(player.rect.x-camera.offset[0], player.rect.y-camera.offset[1], player.image.get_width(), player.image.get_height()), 1)
	for enemy in enemies:
		for b in bullet.bullets:
			if pygame.Rect(b[0][0], b[0][1], bullet.image.get_width(), bullet.image.get_height()).colliderect(enemy.rect):
				enemy.on_damage(bullet.damage)
				enemy_hurt.play()
				bullet.bullets.remove(b)
		enemy.render(screen, camera.offset)
		enemy.update(player, dt, game_data, camera.offset)
		pygame.draw.rect(screen, (255, 255, 255), (enemy.rect.x, enemy.rect.y-10, core_func.clamp(enemy.health, 0, enemy.max_health, 0, enemy.rect.height), 2))
		#pygame.draw.rect(screen, (255, 0, 0), pygame.Rect(enemy.rect.x-camera.offset[0], enemy.rect.y-camera.offset[1], enemy.image.get_width(), enemy.image.get_height()), 1)
		if enemy.rect.colliderect(player.rect):
			player.set_damage(enemy.damage)
		if enemy.health < 1:
			player.kill += 1
			enemies.remove(enemy)

	if player.health > 0:
		dash_ui_copy = dash_ui.copy()
		dash_ui_copy.set_alpha(core_func.clamp(pygame.time.get_ticks()-player.dash_start_tick, 0, player.max_dash_reload_tick, 50, 255))
		#for t in trail_list:
		#	screen.blit(t[0], t[2])
		#	t[1] -= 0.1
		#	if t[1] <= 0:
		#		trail_list.remove(t)
		if pygame.time.get_ticks()-last_spawn > spawn_wait_time:
			if spawn_wait_time > 1000:
				spawn_wait_time -= 250
			if len(enemies) < 25:
				enemies.append(entities.Enemy(random.choice(enemy_spawn_point), random.randrange(2, 4), 10, core_func.generate_animation_data(game_data["animation_path"]["enemy"]), game_data, 0.01))
			last_spawn = pygame.time.get_ticks()
		gun.render(screen, camera.offset)
		gun.update([pygame.mouse.get_pos()[0], pygame.mouse.get_pos()[1]], player.rect.center, camera.offset)
	
	bullet.update(dt, screen)

	screen.blit(pygame.transform.scale2x(pygame.image.load("static/crosshair.png").convert()), (pygame.mouse.get_pos()[0], pygame.mouse.get_pos()[1]))
	
	#screen.blit(pygame.transform.scale(screen, screen.get_size()), (0, 0))

	pygame.draw.rect(screen, pygame.Color(255, 255, 255, 64), (32, 32, core_func.clamp(player.health,0, player.max_health, 0, 200), 15))
	pygame.draw.rect(screen, (255, 255, 255), (32-4, 32-4, 208, 23), 2)

	pygame.draw.rect(display_overlay, (255, 255, 255), (16, 16, screen.get_width()-32, screen.get_height()-32),5,  border_radius=10)

	screen.blit(pygame.transform.scale2x(dash_ui_copy), (32, 40+dash_ui_copy.get_height()))

	screen.blit(display_overlay, (0, 0), special_flags=pygame.BLEND_RGBA_ADD)
	
	if pygame.time.get_ticks()-controls_tick < 7000:
		controls.set_alpha(core_func.clamp(pygame.time.get_ticks()-controls_tick, 0, 7000, 255, 0))
		screen.blit(controls, (240, 133))

	if player.health > 0:
		kill = font.render("KILL :"+str(player.kill), False, (255, 255, 255))
		screen.blit(kill, (screen.get_width() - kill.get_width()-32, 32))
	#screen.blit(skullhead, (screen.get_width() - kill.get_width()-32-skullhead.get_width(), 32))

	if player.health <= 0:
		dead_text = font.render("You're DEAD", False, (255, 255, 255))
		kill_text = font.render("Kill :"+str(player.kill), False, (255, 255, 255))
		restart_text = font.render('Press "r" to restart', False, (255, 255, 255))
		screen.blit(dead_text, (screen.get_width()//2 - dead_text.get_width()//2, 150))
		screen.blit(kill_text, (screen.get_width()//2 - kill_text.get_width()//2, 180))
		screen.blit(restart_text, (screen.get_width()//2 - restart_text.get_width()//2, 210))
		#screen.blit(death_screen, (0, 0))

	

	pygame.display.flip()
	for event in pygame.event.get():
		if event.type == pygame.QUIT:
			pygame.quit()
			sys.exit()
		if event.type == pygame.KEYDOWN:
			if event.key == pygame.K_w : player.movement[1] -= 1
			if event.key == pygame.K_s : player.movement[1] += 1
			if event.key == pygame.K_a: player.movement[0] -= 1
			if event.key == pygame.K_d: player.movement[0] += 1
			if event.key == pygame.K_r:
				if player.health <= 0:
					player.health = player.max_health
					enemies = []
					player.rect.center = [screen.get_width() / 2, screen.get_height() / 2]
					player.kill = 0
					spawn_wait_time = 5000
		if event.type == pygame.KEYUP:
			if event.key == pygame.K_w : player.movement[1] += 1
			if event.key == pygame.K_s : player.movement[1] -= 1
			if event.key == pygame.K_a: player.movement[0] += 1
			if event.key == pygame.K_d: player.movement[0] -= 1
		if event.type == pygame.MOUSEBUTTONDOWN:
			if event.button == 1:
				if player.health > 0:
					if shooting_tick > 260:
						s_tick = pygame.time.get_ticks()
						shoot.play()
						gun.shoot(bullet, [player.rect.centerx, player.rect.centery], gun.get_angle([pygame.mouse.get_pos()[0], pygame.mouse.get_pos()[1]]), camera.offset)

			if event.button == 3:
				if player.health > 0:
					player.dash(pygame.time.get_ticks(), pygame.mouse.get_pos())
