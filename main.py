import pygame
import sys
import random
# Khởi tạo thư viện Pygame và hệ thống âm thanh
import asyncio
pygame.init()
pygame.mixer.init()

# Cài đặt kích thước và tiêu đề cửa sổ game
WIDTH = 800
HEIGHT = 400
screen = pygame.display.set_mode((WIDTH,HEIGHT))
pygame.display.set_caption("Dino Game")
clock = pygame.time.Clock()
try:
    # Tải các hình ảnh (background, khủng long, cây, chim) từ thư mục assets
    # [LƯU Ý QUAN TRỌNG]: Luôn dùng .convert() cho ảnh nền không trong suốt và .convert_alpha() cho ảnh có nền trong suốt 
    # Điều này giúp tăng tốc độ vẽ (render) lên rất nhiều lần!
    bg_img   = pygame.image.load('assets/background.jpg').convert()
    bg_img   = pygame.transform.scale(bg_img, (WIDTH, HEIGHT))
    dino_img = pygame.image.load('assets/dinosaur.png').convert_alpha()
    dino_duck_img = pygame.image.load('assets/dino_duck.png').convert_alpha()
    tree_img = pygame.image.load('assets/tree.png').convert_alpha()
    bird_img = pygame.image.load('assets/bird.png').convert_alpha()
    bird_img = pygame.transform.scale(bird_img, (60, 45))
    bird_img.set_colorkey((255, 255, 255))

    jump_sound  = pygame.mixer.Sound('sound/te.wav')
    score_sound = pygame.mixer.Sound('sound/tick.wav')

    try:
        game_font = pygame.font.Font('04B_19.TTF', 32)
    except:
        game_font = pygame.font.SysFont('Arial', 32, bold=True)

except Exception as e:
    print("Lỗi tải tài nguyên:", e)
    sys.exit()
dino_width, dino_height = dino_img.get_size()
tree_width, tree_height = tree_img.get_size()
bird_width, bird_height = bird_img.get_size()

mushroom_img = pygame.Surface((30, 30), pygame.SRCALPHA)
pygame.draw.ellipse(mushroom_img, (255, 50, 50), (0, 0, 30, 20))
pygame.draw.rect(mushroom_img, (220, 220, 220), (10, 15, 10, 15))
mushroom_width, mushroom_height = mushroom_img.get_size()

tumbleweed_img = pygame.Surface((30, 30), pygame.SRCALPHA)
pygame.draw.circle(tumbleweed_img, (184, 134, 11), (15, 15), 15, 2) # DarkGoldenrod
pygame.draw.circle(tumbleweed_img, (205, 133, 63), (15, 15), 10, 1) # Peru
pygame.draw.line(tumbleweed_img, (184, 134, 11), (5, 5), (25, 25), 2)
pygame.draw.line(tumbleweed_img, (184, 134, 11), (25, 5), (5, 25), 2)
pygame.draw.line(tumbleweed_img, (184, 134, 11), (15, 0), (15, 30), 2)
pygame.draw.line(tumbleweed_img, (184, 134, 11), (0, 15), (30, 15), 2)
tumbleweed_width, tumbleweed_height = tumbleweed_img.get_size()

dino_duck_img = pygame.transform.scale(dino_duck_img, (dino_width + 25, dino_height))
dino_duck_img.set_colorkey((255, 255, 255))

async def main():
    bg_x     = 0
    bg_speed = 5

    dino_x      = 50
    dino_y_base = 360 - dino_height
    dino_y      = dino_y_base
    dino_y_vel  = 0
    gravity     = 0.6
    is_jumping  = False
    jump_count  = 0
    is_ducking  = False

    tree_x = 800
    tree_y = 360 - tree_height

    bird_x = 800 + random.randint(500, 1000)
    bird_y = 360 - bird_height - random.randint(10, 60)

    score       = 0
    game_active = True
    has_mushroom = False
    mushroom_active = False
    mushroom_x = -100
    mushroom_y = 360 - 30
    mushroom_timer = random.randint(1200, 1800) # 20 đến 30 giây ở 60 FPS

    tumbleweed_active = False
    tumbleweed_x = -100
    tumbleweed_y = 360 - 30
    tumbleweed_spawn_timer = 900
    slow_timer = 0

    # Cài đặt màn đêm
    night_overlay = pygame.Surface((WIDTH, HEIGHT))
    night_overlay.set_alpha(150)
    night_overlay.fill((0, 0, 30))

    # VÒNG LẶP CHÍNH CỦA TRÒ CHƠI
    while True:
        # 1. Xử lý các sự kiện đầu vào từ người chơi (bấm phím, nhấp chuột, tắt game)
        # [LƯU Ý QUAN TRỌNG]: Bắt buộc phải gọi pygame.event.get() mỗi khung hình. 
        # Nếu không, máy tính sẽ tưởng game bị treo (Not Responding).
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

            if (event.type == pygame.KEYDOWN and event.key in [pygame.K_SPACE, pygame.K_UP]) or \
               (event.type == pygame.MOUSEBUTTONDOWN and event.button == 1):
                if game_active:
                    if not is_ducking:
                        if jump_count == 0 or (jump_count == 1 and has_mushroom):
                            if jump_count == 1:
                                has_mushroom = False # Tiêu hao nấm khi dùng nhảy kép
                            dino_y_vel = -12
                            is_jumping = True
                            jump_count += 1
                            jump_sound.play()
                else:
                    game_active = True
                    tree_x      = 800
                    bird_x      = 800 + random.randint(500, 1000)
                    score       = 0
                    bg_speed    = 5
                    dino_y      = dino_y_base
                    is_jumping  = False
                    jump_count  = 0
                    is_ducking  = False
                    has_mushroom = False
                    mushroom_active = False
                    mushroom_x = -100
                    mushroom_timer = random.randint(1200, 1800)
                    tumbleweed_active = False
                    tumbleweed_x = -100
                    tumbleweed_spawn_timer = 900
                    slow_timer = 0
                    
            if event.type == pygame.KEYDOWN and event.key == pygame.K_DOWN:
                if game_active and not is_jumping:
                    is_ducking = True
            if event.type == pygame.KEYUP and event.key == pygame.K_DOWN:
                is_ducking = False

        # 2. Cập nhật trạng thái và logic game (chỉ chạy khi nhân vật còn sống)
        if game_active:
            if slow_timer > 0:
                active_speed = bg_speed * 0.5
                slow_timer -= 1
            else:
                active_speed = bg_speed

            # --- Cuộn nền (tạo cảm giác nhân vật đang di chuyển) ---
            bg_x -= active_speed
            if bg_x <= -WIDTH:
                bg_x = 0

            # --- Vật lý nhảy ---
            dino_y_vel += gravity
            dino_y     += dino_y_vel
            if dino_y >= dino_y_base:
                dino_y    = dino_y_base
                is_jumping = False
                jump_count = 0

            # --- Di chuyển cây ---
            tree_x -= active_speed
            if tree_x < -tree_width:
                tree_x  = WIDTH + random.randint(100, 400)
                score  += 1
                if score % 5 == 0:
                    score_sound.play()
                    bg_speed += 0.5

            # --- Di chuyển chim ---
            bird_x -= (active_speed + 1.5)
            if bird_x < -bird_width:
                bird_x = WIDTH + random.randint(300, 800)
                bird_y = 360 - bird_height - random.randint(10, 60)
                score += 1
                score_sound.play() # Phát âm thanh khi vượt qua chim
                if score % 5 == 0:
                    bg_speed += 0.5
            # --- Di chuyển nấm ---
            if mushroom_active:
                mushroom_x -= active_speed
                if mushroom_x < -mushroom_width:
                    mushroom_active = False
                    mushroom_timer = random.randint(1200, 1800)
            else:
                mushroom_timer -= 1
                if mushroom_timer <= 0:
                    mushroom_active = True
                    mushroom_x = WIDTH + random.randint(100, 500)
                    
            # --- Di chuyển bụi cỏ khô (tumbleweed) ---
            if tumbleweed_active:
                tumbleweed_x -= active_speed * 1.2
                if tumbleweed_x < -tumbleweed_width:
                    tumbleweed_active = False
                    tumbleweed_spawn_timer = 900
            else:
                tumbleweed_spawn_timer -= 1
                if tumbleweed_spawn_timer <= 0:
                    tumbleweed_active = True
                    tumbleweed_x = WIDTH + random.randint(200, 600)

            # --- Kiểm tra va chạm (Collision Detection) ---
            # Tạo các khung chữ nhật ảo (Rect) bao quanh các đối tượng để xét xem chúng có đè lên nhau không
            # [LƯU Ý QUAN TRỌNG]: Hình ảnh thường có viền trống, nên ta phải thu nhỏ kích thước Rect (như +10, -20) 
            # để hitbox (vùng xét va chạm) ôm sát nhân vật hơn, giúp game công bằng không bị chết oan.
            if is_ducking:
                dino_rect = pygame.Rect(dino_x+10, dino_y+30, dino_width-20, dino_height-40)
            else:
                dino_rect = pygame.Rect(dino_x+10, dino_y+10, dino_width-10, dino_height-20)
            tree_rect = pygame.Rect(tree_x+5,  tree_y+10, tree_width-10,  tree_height-10)
            bird_rect = pygame.Rect(bird_x+5,  bird_y+5,  bird_width-10,  bird_height-10)
            mushroom_rect = pygame.Rect(mushroom_x+5, mushroom_y+5, mushroom_width-10, mushroom_height-10)
            tumbleweed_rect = pygame.Rect(tumbleweed_x+5, tumbleweed_y+5, tumbleweed_width-10, tumbleweed_height-10)

            if dino_rect.colliderect(tree_rect) or dino_rect.colliderect(bird_rect):
                game_active = False
            
            if mushroom_active and dino_rect.colliderect(mushroom_rect):
                has_mushroom = True
                mushroom_active = False
                mushroom_timer = random.randint(1200, 1800)
                score_sound.play() # Phát âm thanh khi ăn nấm
                
            if tumbleweed_active and dino_rect.colliderect(tumbleweed_rect):
                slow_timer = 600 # 10 giây ở 60 FPS
                tumbleweed_active = False
                tumbleweed_spawn_timer = 900
                
        # 3. Vẽ tất cả các đối tượng lên màn hình (Rendering)
        screen.blit(bg_img,   (bg_x,         0))
        screen.blit(bg_img,   (bg_x + WIDTH, 0))

        if is_ducking:
            screen.blit(dino_duck_img, (dino_x, dino_y + 5))
        else:
            screen.blit(dino_img, (dino_x, dino_y))
        screen.blit(tree_img, (tree_x, tree_y))
        screen.blit(bird_img, (bird_x, bird_y))
        if mushroom_active:
            screen.blit(mushroom_img, (mushroom_x, mushroom_y))
        if tumbleweed_active:
            screen.blit(tumbleweed_img, (tumbleweed_x, tumbleweed_y))

        # --- Chu kỳ Ngày & Đêm ---
        is_night = (int(score) // 10) % 2 != 0
        if is_night:
            screen.blit(night_overlay, (0, 0))
            text_color = (220, 220, 220)
        else:
            text_color = (50, 50, 50)

        score_surf = game_font.render(f'Score: {int(score)}', True, text_color)
        screen.blit(score_surf, (10, 10))
        
        if slow_timer > 0:
            slow_surf = game_font.render(f'Slowed: {slow_timer // 60}s', True, (255, 100, 100))
            screen.blit(slow_surf, (10, 90))
        
        if has_mushroom:
            # Hiển thị icon nấm góc trái để báo hiệu người chơi đang có nấm
            screen.blit(mushroom_img, (10, 50))
            
        if not game_active:
            go_surf = game_font.render('GAME OVER - Click de choi lai', True, (255, 0, 0))
            go_rect = go_surf.get_rect(center=(WIDTH/2, HEIGHT/2))
            screen.blit(go_surf, go_rect)

        # Bật đèn → đẩy bức tranh ra màn hình vật lý!
        pygame.display.update()
        
        # [LƯU Ý QUAN TRỌNG]: clock.tick(60) khóa tốc độ game ở 60 FPS (khung hình/giây).
        # Đảm bảo game chạy cùng một tốc độ trên mọi máy tính dù mạnh hay yếu.
        clock.tick(60)        await asyncio.sleep(0)

asyncio.run(main())
