import pygame
import random
import time

pygame.init()
clock = pygame.time.Clock()

WIDTH, HEIGHT = 700, 800
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("PiyasaSim2025")

road = pygame.image.load("Images/road.png")
road = pygame.transform.scale(road, (700, 800))
road_posFirst = [-60.5, 0]
road_posSecond = [-60.5, -800]

civic_img_original = pygame.image.load("Images/civic3.png")
civic_img = civic_img_original.copy()
civic = civic_img.get_rect(center=(WIDTH / 3.2, HEIGHT / 1.2))
civic_velX = 0
civic_velY = 0

npc_imgs = [
    pygame.image.load("Images/npcArac3.png"),
    pygame.image.load("Images/npcKamyon2.png"),
    pygame.image.load("Images/npcArac2.png")
]

exhaust_start = pygame.mixer.Sound("Sounds/exhauststart.wav")
engine_loop = pygame.mixer.Sound("Sounds/ilerleme.wav")
engine_stop = pygame.mixer.Sound("Sounds/yavaslama.wav")
break_sound = pygame.mixer.Sound("Sounds/fren.wav")

break_sound.set_volume(0.1)
engine_loop.set_volume(50)
engine_stop.set_volume(0.1)
exhaust_start.set_volume(0.5)

exhaust_particles = []
npc_exhaust_particles = []
npcs = []
lane_width = 120
lane_count = 4
left_margin = 50
right_margin = 60

w_pressed = False

font = pygame.font.SysFont(None, 80)
score = 0

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

def mainMenu():
    menu_font = pygame.font.SysFont(None, 70)
    selected_option = None
    while selected_option is None:
        screen.fill((10, 10, 30))
        play_text = menu_font.render("Oyna", True, (255, 255, 255))
        credits_text = menu_font.render("Credits", True, (255, 255, 255))
        exit_text = menu_font.render("Çıkış", True, (255, 255, 255))
        play_rect = play_text.get_rect(center=(WIDTH // 2, HEIGHT // 2 - 100))
        credits_rect = credits_text.get_rect(center=(WIDTH // 2, HEIGHT // 2))
        exit_rect = exit_text.get_rect(center=(WIDTH // 2, HEIGHT // 2 + 100))
        screen.blit(play_text, play_rect)
        screen.blit(credits_text, credits_rect)
        screen.blit(exit_text, exit_rect)
        pygame.display.flip()
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                exit()
            elif event.type == pygame.MOUSEBUTTONDOWN:
                if play_rect.collidepoint(event.pos):
                    selected_option = "play"
                elif credits_rect.collidepoint(event.pos):
                    showCredits()
                elif exit_rect.collidepoint(event.pos):
                    pygame.quit()
                    exit()
        clock.tick(60)
    gameLoop()

def scoreBoard(score):
    digit_font = pygame.font.SysFont(None, 40)
    score_str = str(int(score))
    clear_rect = pygame.Rect(WIDTH - 50, 10, 40, len(score_str) * 45)
    pygame.draw.rect(screen, (30, 30, 30), clear_rect)
    x_pos = WIDTH - 30
    y_pos = 10
    for digit in score_str:
        digit_surface = digit_font.render(digit, True, (255, 255, 255))
        digit_rect = digit_surface.get_rect(center=(x_pos, y_pos + 20))
        screen.blit(digit_surface, digit_rect)
        y_pos += 45

def showCredits():
    font = pygame.font.SysFont(None, 50)
    running = True
    while running:
        screen.fill((10, 10, 30))
        credits_text = font.render("YAPIMCILAR", True, (0, 255, 255))
        credits_text2 = font.render("BAHADIR BOSTAN", True, (255, 255, 255))
        credits_text3 = font.render("ASİL MUHAMMET ÜNAL", True, (255, 255, 255))
        credits_text4 = font.render("AHMET HAKAN ATAŞ", True, (255, 255, 255))
        back_text = font.render("Geri dönmek için herhangi bir tuşa bas", True, (180, 180, 180))
        screen.blit(credits_text, (WIDTH // 2 - credits_text.get_width() // 2, HEIGHT // 2 - 150))
        screen.blit(credits_text2, (WIDTH // 2 - credits_text2.get_width() // 2, HEIGHT // 2 - 50))
        screen.blit(credits_text3, (WIDTH // 2 - credits_text3.get_width() // 2, HEIGHT // 2 + 50))
        screen.blit(credits_text4, (WIDTH // 2 - credits_text4.get_width() // 2, HEIGHT // 2 + 150))
        screen.blit(back_text, (WIDTH // 2 - back_text.get_width() // 2, HEIGHT // 2 + 300))
        pygame.display.flip()
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                exit()
            elif event.type == pygame.KEYDOWN:
                running = False

def gameOverMenu(score):
    font = pygame.font.SysFont(None, 60)
    small_font = pygame.font.SysFont(None, 45)
    selected = False
    while not selected:
        screen.fill((20, 20, 20))
        score_text = font.render(f"Skorun: {int(score)}", True, (255, 255, 0))
        screen.blit(score_text, (WIDTH // 2 - score_text.get_width() // 2, HEIGHT // 2 - 150))
        menu_text = small_font.render("Ana Menüye Dön", True, (255, 255, 255))
        quit_text = small_font.render("Çıkış", True, (255, 255, 255))
        menu_rect = menu_text.get_rect(center=(WIDTH // 2, HEIGHT // 2))
        quit_rect = quit_text.get_rect(center=(WIDTH // 2, HEIGHT // 2 + 80))
        pygame.draw.rect(screen, (70, 70, 70), menu_rect.inflate(30, 15))
        pygame.draw.rect(screen, (70, 70, 70), quit_rect.inflate(30, 15))
        screen.blit(menu_text, menu_rect)
        screen.blit(quit_text, quit_rect)
        pygame.display.flip()
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                exit()
            elif event.type == pygame.MOUSEBUTTONDOWN:
                if menu_rect.collidepoint(event.pos):
                    selected = True
                    mainMenu()
                elif quit_rect.collidepoint(event.pos):
                    pygame.quit()
                    exit()
        clock.tick(60)

def gameLoop():
    global civic_img, civic, civic_velX, civic_velY, w_pressed, score, npcs
    civic_img = civic_img_original.copy()
    civic = civic_img.get_rect(center=(WIDTH / 3.2, HEIGHT / 1.2))
    civic_velX = 0
    civic_velY = 0
    w_pressed = False
    score = 0
    npcs = []
    engine_loop.stop()
    engine_loop.play(-1)

    game_over = False
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
                    civic_velY = -3.6
                if event.key == pygame.K_s:
                    civic_velY = 3.6
                    break_sound.play()
                if event.key == pygame.K_a:
                    civic_velX = -3.3
                    civic_img = pygame.transform.rotate(civic_img_original, 10)
                if event.key == pygame.K_d:
                    civic_velX = 3.3
                    civic_img = pygame.transform.rotate(civic_img_original, -10)
            if event.type == pygame.KEYUP:
                if event.key == pygame.K_w:
                    w_pressed = False
                    engine_stop.play()
                    civic_velY = 0
                if event.key == pygame.K_s:
                    civic_velY = 0
                if event.key in [pygame.K_a, pygame.K_d]:
                    civic_velX = 0
                    civic_img = civic_img_original.copy()

        civic.x += civic_velX
        civic.y += civic_velY

        if civic.left <= 10:
            civic.left = 10
        if civic.right >= WIDTH - 145:
            civic.right = WIDTH - 145
        if civic.top >= HEIGHT - 40:
            civic.top = HEIGHT - 40
        if civic.top <= 40:
            civic.top = 40

        road_speed = 5.4 + abs(civic_velY) * 0.5
        road_speed = max(4.3, min(road_speed, 6.5))
        road_posFirst[1] += road_speed
        road_posSecond[1] += road_speed
        if road_posFirst[1] >= HEIGHT:
            road_posFirst[1] = -HEIGHT
        if road_posSecond[1] >= HEIGHT:
            road_posSecond[1] = -HEIGHT

        score += road_speed * 0.2
        scoreBoard(score)

        if w_pressed:
            create_exhaust(civic.centerx - 15, civic.bottom - 5)

        adjust_speed_based_on_proximity()
        check_npc_collisions()
        for npc in npcs:
            npc['rect'].y += npc['speed']
            if npc['rect'].top >= HEIGHT or npc['rect'].bottom <= -100:
                npcs.remove(npc)
                npcs.append(create_npc())
            if random.random() < 0.02:
                create_exhaust(npc['rect'].centerx - 10, npc['rect'].bottom - 5, is_npc=True)

        for npc in npcs:
            if civic.colliderect(npc['rect']):
                engine_loop.stop()
                w_pressed = False
                screen.fill((0, 0, 0))
                text = font.render("KAZA YAPTIN!", True, (255, 0, 0))
                screen.blit(text, (WIDTH // 2 - 200, HEIGHT // 2 - 50))
                pygame.display.update()
                pygame.time.wait(1500)
                gameOverMenu(score)
                game_over = True

        screen.blit(road, road_posFirst)
        screen.blit(road, road_posSecond)
        screen.blit(civic_img, civic)
        for npc in npcs:
            screen.blit(npc['img'], npc['rect'])

        update_and_draw_particles()
        generate_npcs()
        pygame.display.update()
        clock.tick(60)

mainMenu()
pygame.quit()
