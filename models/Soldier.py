import pygame,random
from setting import Direction,Status_Hero
from models.Hero import Hero
from models.Bullet import Bullet
class Soldier:
    def __init__(self):
        self.image = pygame.image.load('./images/right/soldier/freeze/0.png')
        self.rect = self.image.get_rect()
        self.rect.y = 500
        self.frame = 0
        self.status = Status_Hero.FREEZE
        self.direction = Direction.RIGHT
        self.lst_bullet = []
        self.time_status_start = 0
        self.speed = 10
        self.time_random_status_start = 0
        self.time_move_start = 0
        self.time_attack_start = 0
        self.soldier_attack_sound = pygame.mixer.Sound('./sounds/enemy.wav')
        self.hero_die_sound = pygame.mixer.Sound('./sounds/marco.wav') #Âm thanh khi hero chết
    def move(self,rect_hero):
        if rect_hero.x < self.rect.x:
            self.direction = Direction.LEFT
        else:
            self.direction = Direction.RIGHT
        self.status = Status_Hero.MOVE
        if self.direction == Direction.LEFT:
            self.rect.x -= self.speed
        else:
            self.rect.x += self.speed
    def update_status(self):
        #Xử lý folder hướng
        folder_name_direct = ''
        if self.direction == Direction.LEFT:
            folder_name_direct = 'left'
        else:
            folder_name_direct = 'right'
        #Xử lý folder status
        folder_status_name = ''
        #Frame theo status
        frame_count = 0
        if self.status == Status_Hero.MOVE:
            folder_status_name = 'move'
            frame_count = 7
        elif self.status == Status_Hero.ATTACK:
            folder_status_name = 'attack'
            frame_count = 5
        elif self.status == Status_Hero.DIE: 
            folder_status_name = 'die'
            frame_count = 15
        else:
            folder_status_name = 'freeze'
            frame_count = 4
        

        image_src =  f'./images/{folder_name_direct}/soldier/{folder_status_name}/{self.frame % frame_count}.png'
        
        self.image = pygame.image.load(image_src)
    def attack(self):
        self.status = Status_Hero.ATTACK
        #Tạo ra 1 viên đạn mới nạp vào self.list_bullet
        if self.direction == Direction.RIGHT:
            x_bullet = self.rect.x + self.rect.width 
            y_bullet = self.rect.y + self.rect.height // 2
            new_bullet = Bullet(x_bullet,y_bullet,Direction.RIGHT,'./images/bullet/1.png')
            self.lst_bullet.append(new_bullet)
        else:
            x_bullet = self.rect.x
            y_bullet = self.rect.y + self.rect.height // 2
            new_bullet = Bullet(x_bullet,y_bullet,Direction.LEFT,'./images/bullet/1.png')
            self.lst_bullet.append(new_bullet)
        #Phát âm thanh súng soldier
        self.soldier_attack_sound.play()
        
    def draw(self,screen,hero:Hero):
        screen.blit(self.image,self.rect)
        #Update status cập nhật frame
        current_status_time = pygame.time.get_ticks()
        if current_status_time - self.time_status_start >= 300:
            self.frame += 1
            self.time_status_start = current_status_time
            
        # Chuyển đổi trạng thái
        current_change_status = pygame.time.get_ticks()
        if current_change_status - self.time_random_status_start > 5000:
            #Chuyển enum -> list
            lst_enum = list(Status_Hero)
            #Tiến hành random enum
            status_random = random.choice(lst_enum)
            while status_random == Status_Hero.DIE:
                status_random = random.choice(lst_enum)     
            self.status = status_random
            self.time_random_status_start = current_change_status
        #Xử lý từng trạng thái sau khi random
        if self.status == Status_Hero.MOVE:
            current_move = pygame.time.get_ticks()
            if current_move - self.time_move_start >= 300:
                self.move(hero.rect)
                self.time_move_start = current_move
        elif self.status == Status_Hero.ATTACK:
            current_attack = pygame.time.get_ticks()
            if current_attack - self.time_attack_start >2500:
                self.attack()
                self.time_attack_start = current_attack
  
        #Vẽ lại đạn
        for bullet in self.lst_bullet:
            bullet.move()
            bullet.draw(screen)
            #Xử lý remove đạn soldier bay ra khỏi màn hình
            if bullet.rect.x > screen.get_width() or bullet.rect.x < 0:
                self.lst_bullet.remove(bullet)
            #Xử lý đạn của soldier bắn trúng hero
            if bullet.rect.colliderect(hero.rect) and hero.status != Status_Hero.DIE:
                self.lst_bullet.remove(bullet)
                hero.live -= 1
                #Phát âm thanh
                self.hero_die_sound.play()
                if hero.live <= 0:
                    hero.live = 0
                    hero.speed = 0
                    self.status = Status_Hero.FREEZE

        self.update_status()
        
        
        