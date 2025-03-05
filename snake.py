import pygame
import random

pygame.init()

size = width, height = 600, 400
screen = pygame.display.set_mode(size)
pygame.display.set_caption("Snake Game")
clock = pygame.time.Clock()

pygame.mixer.init()
eat_sound = pygame.mixer.Sound("eat.wav") 
speed_sound = pygame.mixer.Sound("speed.wav")
slow_sound = pygame.mixer.Sound("slow.wav")
gameover_sound = pygame.mixer.Sound("gameover.wav")
pygame.mixer.music.load("background_music.mp3")
pygame.mixer.music.play(-1)

# start position
x0 = width // 2
y0 = height // 2
speed = 20  
move_speed = 15 
points = 0
base_move_speed = move_speed
f1 = pygame.font.Font(None, 36)
f2 = pygame.font.Font(None, 50)

def random_pos(exclude=[]):
    while True:
        rand_x = random.randint(0, width//speed-1) * speed
        rand_y = random.randint(0, height//speed-1) * speed
        if (rand_x, rand_y) not in exclude:
            return rand_x, rand_y

def draw_background():
    screen.fill((20, 40, 20))
    for x in range(0, width, speed):
        pygame.draw.line(screen, (40, 60, 40), (x, 0), (x, height))
    for y in range(0, height, speed):
        pygame.draw.line(screen, (40, 60, 40), (0, y), (width, y))

food_types = {
    "normal": {"color": (255, 0, 0), "effect": lambda: None, "duration": 0, "points": 1, "shape": "circle"},
    "speed": {"color": (255, 255, 0), "effect": lambda: globals().update({"move_speed": base_move_speed * 2}), "duration": 300, "points": 2, "shape": "triangle"},
    "slow": {"color": (0, 0, 255), "effect": lambda: globals().update({"move_speed": base_move_speed // 2}), "duration": 300, "points": 2, "shape": "square"},
    "bonus": {"color": (255, 215, 0), "effect": lambda: None, "duration": 0, "points": 5, "shape": "diamond"},
    "invincible": {"color": (255, 105, 180), "effect": lambda: globals().update({"invincible": True}), "duration": 600, "points": 3, "shape": "hexagon"}
}

#start food pos 
food_x, food_y = random_pos(exclude=[(x0, y0)])
current_food = random.choice(list(food_types.keys()))


portal1 = random_pos(exclude=[(x0, y0)])
portal2 = random_pos(exclude=[(x0, y0), portal1])
portal_size = 30

enemies = [{"x": random_pos()[0], "y": random_pos()[1], "dx": random.choice([-2, 2]), "dy": random.choice([-2, 2])} for _ in range(3)]

#snake movement
snake_body = [(x0, y0)]
direction = "RIGHT"
last_direction = direction
velocity_x, velocity_y = move_speed, 0
effect_timer = 0
invincible = False
running = True
frame_count = 0
pulse_timer = 0
particles = []

def game_over_screen():
    gameover_sound.play()
    screen.fill((20, 20, 20))
    game_over_text = f2.render("Game Over", True, (255, 0, 0))
    score_text = f1.render(f"Score: {points}", True, (255, 255, 255))
    restart_text = f1.render("Press R to Restart", True, (255, 255, 255))
    screen.blit(game_over_text, (width//2 - 100, height//2 - 50))
    screen.blit(score_text, (width//2 - 50, height//2))
    screen.blit(restart_text, (width//2 - 100, height//2 + 50))
    pygame.display.flip()
    
    waiting = True
    while waiting:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return False
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_r:
                    return True
    return False

def play_sound(effect):
    if effect == "normal":
        eat_sound.play()
    elif effect == "speed":
        speed_sound.play()
    elif effect == "slow":
        slow_sound.play()
    elif effect == "bonus" or effect == "invincible":
        eat_sound.play()

def spawn_particles(x, y, color):
    for _ in range(5):
        particles.append([x + speed//2, y + speed//2, random.uniform(-2, 2), random.uniform(-2, 2), color, 20])

def draw_food(x, y, food_type):
    color = food_types[food_type]["color"]
    shape = food_types[food_type]["shape"]
    scale = speed//2 + (1 if frame_count % 10 < 5 else 0)
    
    if shape == "circle":
        pygame.draw.circle(screen, color, (x + speed//2, y + speed//2), scale)
    elif shape == "triangle":
        pygame.draw.polygon(screen, color, [(x + speed//2, y + scale), (x + scale, y + speed - scale), (x + speed - scale, y + speed - scale)])
    elif shape == "square":
        pygame.draw.rect(screen, color, (x + speed//4, y + speed//4, scale, scale))
    elif shape == "diamond":
        pygame.draw.polygon(screen, color, [(x + speed//2, y), (x + speed, y + speed//2), (x + speed//2, y + speed), (x, y + speed//2)])
    elif shape == "hexagon":
        pygame.draw.polygon(screen, color, [
            (x + speed//2, y), (x + speed, y + speed//4), (x + speed, y + 3*speed//4),
            (x + speed//2, y + speed), (x, y + 3*speed//4), (x, y + speed//4)
        ])

while running:
    draw_background()
    
    pygame.draw.rect(screen, (0, 191, 255), (portal1[0], portal1[1], portal_size, portal_size))  # Голубой
    pygame.draw.rect(screen, (255, 165, 0), (portal2[0], portal2[1], portal_size, portal_size))  # Оранжевый
    
    # enemy movement
    for enemy in enemies:
        enemy["x"] += enemy["dx"]
        enemy["y"] += enemy["dy"]
        if enemy["x"] <= 0 or enemy["x"] >= width - speed:
            enemy["dx"] = -enemy["dx"]
        if enemy["y"] <= 0 or enemy["y"] >= height - speed:
            enemy["dy"] = -enemy["dy"]
        pygame.draw.rect(screen, (139, 0, 139), (enemy["x"], enemy["y"], speed, speed))
    
    text1 = f1.render(f'Score: {points}', True, (255, 255, 255))
    
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_RIGHT and last_direction != "LEFT":
                direction = "RIGHT"
            elif event.key == pygame.K_LEFT and last_direction != "RIGHT":
                direction = "LEFT"
            elif event.key == pygame.K_UP and last_direction != "DOWN":
                direction = "UP"
            elif event.key == pygame.K_DOWN and last_direction != "UP":
                direction = "DOWN"
    
    frame_count += 1
    if frame_count >= 5:
        frame_count = 0
        
        if direction == "RIGHT":
            velocity_x = move_speed
            velocity_y = 0
        elif direction == "LEFT":
            velocity_x = -move_speed
            velocity_y = 0
        elif direction == "UP":
            velocity_x = 0
            velocity_y = -move_speed
        elif direction == "DOWN":
            velocity_x = 0
            velocity_y = move_speed
        
        #portal ols pos to teleport
        old_x, old_y = x0, y0  
        x0 += velocity_x
        y0 += velocity_y
        
        head_rect = pygame.Rect(x0, y0, speed, speed)
        portal1_rect = pygame.Rect(portal1[0], portal1[1], portal_size, portal_size)
        portal2_rect = pygame.Rect(portal2[0], portal2[1], portal_size, portal_size)
        
        if head_rect.colliderect(portal1_rect):
            x0, y0 = portal2[0] + (x0 - old_x), portal2[1] + (y0 - old_y) 
        elif head_rect.colliderect(portal2_rect):
            x0, y0 = portal1[0] + (x0 - old_x), portal1[1] + (y0 - old_y)
        
        if x0 >= width:
            x0 = 0
        elif x0 < 0:
            x0 = width - speed
        if y0 >= height:
            y0 = 0
        elif y0 < 0:
            y0 = height - speed
        
        snake_body.insert(0, (x0, y0))
        
        head_rect = pygame.Rect(x0, y0, speed, speed)
        food_rect = pygame.Rect(food_x, food_y, speed, speed)
        if head_rect.colliderect(food_rect):
            points += food_types[current_food]["points"]
            food_types[current_food]["effect"]()
            effect_timer = food_types[current_food]["duration"]
            play_sound(current_food)
            spawn_particles(food_x, food_y, food_types[current_food]["color"])
            food_x, food_y = random_pos(exclude=snake_body + [portal1, portal2])
            current_food = random.choices(list(food_types.keys()), weights=[50, 20, 20, 10, 5])[0]
        else:
            snake_body.pop()
        
        for enemy in enemies:
            if not invincible and head_rect.colliderect(pygame.Rect(enemy["x"], enemy["y"], speed, speed)):
                running = False
    
    if effect_timer > 0:
        effect_timer -= 1
        if effect_timer == 0:
            move_speed = base_move_speed
            invincible = False
    
    if points > 0 and points % 10 == 0:
        base_move_speed = move_speed + 1
    
    draw_food(food_x, food_y, current_food)
    
    for particle in particles[:]:
        particle[0] += particle[2]
        particle[1] += particle[3]
        particle[5] -= 1
        if particle[5] <= 0:
            particles.remove(particle)
        else:
            pygame.draw.circle(screen, particle[4], (int(particle[0]), int(particle[1])), 2)
    
    pulse_timer += 1
    pulse_size = speed + (3 if pulse_timer % 20 < 10 else 0)
    glow_alpha = 128 + int(127 * (pulse_timer % 30 / 30))
    
    head_drawn = False
    for segment in snake_body:
        if not head_drawn:
            pygame.draw.rect(screen, (0, 255, 0) if not invincible else (255, 105, 180), 
                           (segment[0], segment[1], pulse_size, pulse_size))
            pygame.draw.circle(screen, (255, 255, 255), (segment[0] + speed//4, segment[1] + speed//4), 2)
            head_drawn = True
        else:
            glow_surface = pygame.Surface((speed, speed), pygame.SRCALPHA)
            glow_surface.fill((0, 150, 0, glow_alpha))
            screen.blit(glow_surface, (segment[0], segment[1]))
            pygame.draw.rect(screen, (0, 150, 0), (segment[0], segment[1], speed, speed))
    
    for segment in snake_body[1:]:
        if not invincible and segment[0] == x0 and segment[1] == y0:
            running = False
    
    screen.blit(text1, (10, 10))
    
    last_direction = direction
    clock.tick(60)
    pygame.display.flip()

    if not running:
        if game_over_screen():
            x0, y0 = width // 2, height // 2
            snake_body = [(x0, y0)]
            direction = "RIGHT"
            last_direction = direction
            velocity_x, velocity_y = move_speed, 0
            points = 0
            move_speed = base_move_speed
            food_x, food_y = random_pos()
            current_food = random.choice(list(food_types.keys()))
            effect_timer = 0
            invincible = False
            portal1 = random_pos(exclude=[(x0, y0)])
            portal2 = random_pos(exclude=[(x0, y0), portal1])
            enemies = [{"x": random_pos()[0], "y": random_pos()[1], "dx": random.choice([-2, 2]), "dy": random.choice([-2, 2])} for _ in range(3)]
            particles.clear()
            running = True

pygame.quit()