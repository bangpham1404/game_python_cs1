import pygame,sys,random,copy
from models.Hero import Hero
from models.Soldier import Soldier
from setting import Direction,Status_Hero

pygame.init()
#Chiều dài chiều rộng 
SCREEN_WIDTH = 1280
SCREEN_HEIGHT = 720
#Khởi tạo màn hình game
screen = pygame.display.set_mode((SCREEN_WIDTH,SCREEN_HEIGHT))

#Khai báo nhân vật hero
hero:Hero = Hero()
hero.load_game
#Khai báo list soldier
lst_soldier:list[Soldier] = []
# soldier = Soldier()
# soldier.rect.x = 1000
# soldier.direction = Direction.LEFT

#Setup thời gian tạo lính và hero
time_create_soldier = 0

#Thiết lập âm thanh
bg_sound = pygame.mixer.Sound('./sounds/music.mp3') #Nhạc nền
hero_attack_sound = pygame.mixer.Sound('./sounds/mg.wav') #Âm thanh súng hero
hero_die_sound = pygame.mixer.Sound('./sounds/enemy.wav') #Âm thanh khi hero chết
soldier_die_sound = pygame.mixer.Sound('./sounds/soldier1.wav') #Âm thanh khi soldier chết
hero_move_sound = pygame.mixer.Sound('./sounds/footstep.wav')
bg_sound.play(-1) #Phát nhạc nền liên tục


#Background game
bg_game = pygame.image.load('./images/bkgd.png')
bg_game_rect = bg_game.get_rect()
bg_game = pygame.transform.scale(bg_game,(bg_game_rect.width,SCREEN_HEIGHT))

scroll_bg = bg_game_rect.x
x_hero_start = hero.rect.x
running = True

#Đồng hồ xử lý chết
time_die_soldier = 0
time_die_hero = 0

while running:
    x_current_hero = hero.rect.x
    
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            hero.save_game()
            running = False
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_j:
                hero.attack()
                #Phát âm thanh súng hero
                hero_attack_sound.play()
            if event.key == pygame.K_k:
                hero.jump() 
                                        
    #Xử lý di chuyển
    key = pygame.key.get_pressed()
    #w: đi lên, s: xuống, a:left, d:right j:attack, k:jump
    if key[pygame.K_a]:
        hero.move(Direction.LEFT)
        #Phát âm thanh di chuyển của hero
        hero_move_sound.play()
    elif key[pygame.K_d]:
        hero.move(Direction.RIGHT)
        #Phát âm thanh di chuyển của hero
        hero_move_sound.play()
    else: 
        #Nếu người dùng không đè phím nào thì trả về trạng thái đứng yên
        hero.status = Status_Hero.FREEZE
    #Xử lý bắn đạn
    # if key[pygame.K_j]:
    #     hero.attack()
    #Background
    if hero.direction == Direction.RIGHT and x_hero_start != x_current_hero:
        scroll_bg -= hero.speed
        x_hero_start = x_current_hero
    elif hero.direction == Direction.LEFT and x_hero_start != x_current_hero:
        scroll_bg += hero.speed
        x_hero_start = x_current_hero
    screen.blit(bg_game,(scroll_bg,bg_game_rect.y))
      
    current_time_soldier = pygame.time.get_ticks()
    #Tạo ra 1 lính sau mỗi 5s
    if hero.live > 0 and current_time_soldier - time_create_soldier >= 5000:
        new_soldier = Soldier()
        new_soldier.rect.x = random.randint(500,1000)
        new_soldier.direction = Direction.LEFT
        lst_soldier.append(new_soldier)
        time_create_soldier = current_time_soldier

    #Xử lý bắn
    for bullet in hero.lst_bullet:
        for soldier_item in lst_soldier:
            if bullet.rect.colliderect(soldier_item.rect) and soldier_item.status != Status_Hero.DIE:
                soldier_item.status = Status_Hero.DIE
                hero.lst_bullet.remove(bullet)
                #Phát âm thanh khi soldier chết
                soldier_die_sound.play()
                hero.score += 100
                break
    
    for soldier_item in lst_soldier:
        #Vẽ soldier
        soldier_item.draw(screen,hero)
   
    #xử lý chết cho tất cả lst_soldier
    current_time_die_soldier = pygame.time.get_ticks()
    if current_time_die_soldier - time_die_soldier > 3000:
        for soldier_item in lst_soldier:
            if soldier_item.status == Status_Hero.DIE:
                 lst_soldier.remove(soldier_item)

        time_die_soldier = current_time_die_soldier

    # Vẽ hero
    hero.draw(screen)

    #Cập nhật màn hình game 
    pygame.display.flip()
pygame.quit()
sys.exit()




