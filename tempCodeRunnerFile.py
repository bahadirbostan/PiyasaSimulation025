import pygame
import random
import time

pygame.init()
clock = pygame.time.Clock()

WIDTH, HEIGHT = 700, 800
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("PiyasaSim2025")

# Görseller
road = pygame.image.load("road.png")
road = pygame.transform.scale(road, (700, 800))
road_posFirst = [-60.5, 0]
road_posSecond = [-60.5, -800]

civic_img = pygame.image.load("civic3.png")
civic = civic_img.get_rect(center=(WIDTH / 3.2, HEIGHT / 1.2))
civic_velX = 0
civic_velY = 0

npc_imgs = [
    pygame.image.load("npcArac3.png"),
    pygame.image.load("npcKamyon2.png"),
    pygame.image.load("npcArac2.png")
]

# Sesler
exhaust_start = pygame.mixer.Sound("exhauststart.wav")
engine_loop = pygame.mixer.Sound("ilerleme.wav")
engine_stop = pygame.mixer.Sound("yavaslama.wav")
break_sound = pygame.mixer.Sound("fren.wav")

break_sound.set_volume(0.1)
engine_loop.set_volume(50)
engine_stop.set_volume(0.1)
exhaust_start.set_volume(0.5)
# Egzoz partikülleri
exhaust_particles = []
npc_exhaust_particles = []

# Yol ayarları
npcs = []
lane_width = 120
lane_count = 4
left_margin = 50
right_margin = 60

# W basılı mı kontrolü
w_pressed = False

# Fonksiyonlar
def create_npc():
    npc_img = random.choice(npc_imgs)
    lane = random.randint(0, lane_count - 1)
    npc_x = left_margin + lane * lane_width + lane_width // 2
    npc_y = random.randint(-1000, -100)
    npc_rect = npc_img.get_rect(center=(npc_x, npc_y))
    speed = random.uniform(1.2, 3)
    return {"rect": npc_rect, "img": npc_img, "speed": speed}

def generate_npcs():
    if len(npcs) < 4:
        new_npc = create_npc()
        npcs.append(new_npc)
        time.sleep(1.6)

def adjust_speed_based_on_proximity():
    for i in range(len(npcs) - 1):
        npc1 = npcs[i]
        npc2 = npcs[i + 1]
        distance_x = npc1['rect'].centerx - npc2['rect'].centerx
        distance_y = npc1['rect'].centery - npc2['rect'].centery
        distance = (distance_x ** 2 + distance_y ** 2) ** 0.5
        if distance < 150:
            npc2['speed'] = max(npc1['speed'] - 0.5, 0.5)
        else:
            npc2['speed'] = random.uniform(1, 2)

def create_exhaust(x, y, is_npc=False):
    particle = {
        "x": x,
        "y": y,
        "radius": random.randint(3, 6),
        "alpha": 255,
        "is_npc": is_npc
    }
    if is_npc:
        npc_exhaust_particles.append(particle)
    else:
        exhaust_particles.append(particle)

def update_and_draw_particles():
    for particle_list in [exhaust_particles, npc_exhaust_particles]:
        for particle in particle_list[:]:
            particle["y"] -= 1
            particle["radius"] -= 0.1
            particle["alpha"] -= 5
            if particle["alpha"] <= 0 or particle["radius"] <= 0:
                particle_list.remove(particle)
                continue
            surface = pygame.Surface((10, 10), pygame.SRCALPHA)
            pygame.draw.circle(surface, (100, 100, 100, particle["alpha"]), (5, 5), int(particle["radius"]))
            screen.blit(surface, (particle["x"], particle["y"]))
def check_collision_with_existing(npc_rect):
    for npc in npcs:
        if npc['rect'].colliderect(npc_rect):
            
            npcs.remove(npc)
            return True 
    return False

def check_npc_collisions():
    min_distance = 140  

    for i in range(len(npcs)):
        for j in range(i + 1, len(npcs)):
            npc1 = npcs[i]
            npc2 = npcs[j]

            distance_x = npc1['rect'].centerx - npc2['rect'].centerx
            distance_y = npc1['rect'].centery - npc2['rect'].centery
            distance = (distance_x ** 2 + distance_y ** 2) ** 0.5

            if distance < min_distance:
                if random.choice([True, False]):
                    npc1['speed'] = 2.3
                else:
                    npc2['speed'] = 1.1

                return


# Ana oyun döngüsü
game_over = False
font = pygame.font.SysFont(None, 80)

while not game_over:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            game_over = True

        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE:
                game_over = True
            if event.key == pygame.K_w:
                if not w_pressed:
                    w_pressed = True
                    exhaust_start.play()
                    engine_loop.play(-1)
                civic_velY = -3.6
            if event.key == pygame.K_s:
                civic_velY = 3.6
                break_sound.play()
            if event.key == pygame.K_a:
                civic_velX = -3.3
            if event.key == pygame.K_d:
                civic_velX = 3.3

        if event.type == pygame.KEYUP:
            if event.key == pygame.K_w:
                w_pressed = False
        
                engine_stop.play()
                civic_velY = 0
            if event.key in [pygame.K_s, pygame.K_a, pygame.K_d]:
                civic_velX = 0
                civic_velY = 0

    # Civic pozisyon güncelle
    civic.x += civic_velX
    civic.y += civic_velY

    # Sınırlama
    if civic.left <= 10:
        civic.left = 10
    if civic.right >= WIDTH - 145:
        civic.right = WIDTH - 145
    if civic.top >= HEIGHT - 40:
        civic.top = HEIGHT - 40
    if civic.top <= 40:
        civic.top = 40

    # Arka plan hareketi
    road_speed = 5.4 + abs(civic_velY) * 0.5
    road_speed = max(4.3, min(road_speed, 6.5))
    road_posFirst[1] += road_speed
    road_posSecond[1] += road_speed
    if road_posFirst[1] >= HEIGHT:
        road_posFirst[1] = -HEIGHT
    if road_posSecond[1] >= HEIGHT:
        road_posSecond[1] = -HEIGHT

    # Egzoz partikülü oluştur (civic)
    if w_pressed:
        create_exhaust(civic.centerx - 15, civic.bottom - 5)

    # NPC güncellemeleri
    adjust_speed_based_on_proximity()
    check_npc_collisions()
    for npc in npcs:
        npc['rect'].y += npc['speed']
        if npc['rect'].top >= HEIGHT or npc['rect'].bottom <= -100:
            npcs.remove(npc)
            npcs.append(create_npc())
        if random.random() < 0.02:
            create_exhaust(npc['rect'].centerx - 10, npc['rect'].bottom - 5, is_npc=True)

    # Çarpışma kontrolü
    for npc in npcs:
        if civic.colliderect(npc['rect']):
            screen.fill((0, 0, 0))
            text = font.render("KAZA YAPTIN!", True, (255, 0, 0))
            screen.blit(text, (WIDTH // 2 - 200, HEIGHT // 2 - 50))
            pygame.display.update()
            pygame.time.wait(2000)
            game_over = True

    # Çizimler
    screen.blit(road, road_posFirst)
    screen.blit(road, road_posSecond)
    screen.blit(civic_img, civic)

    for npc in npcs:
        screen.blit(npc['img'], npc['rect'])

    update_and_draw_particles()
    generate_npcs()
    clock.tick(60)
    pygame.display.update()

pygame.quit()
