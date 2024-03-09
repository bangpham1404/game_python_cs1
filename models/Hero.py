import pygame
from setting import Status_Hero,Direction
from models.Bullet import Bullet
class Hero:
    def __init__(self):
        self.image = pygame.image.load('./images/right/hero/freeze/0.png')
        self.rect = self.image.get_rect()
        self.rect.y = 500
        self.frame = 0
        self.status = Status_Hero.FREEZE
        self.direction = Direction.RIGHT
        self.lst_bullet:list[Bullet] = []
        self.time_status_start = 0
        self.speed = 10
        self.live = 3
        self.score = 0
        # Setup sự kiện nhảy (jump)
        self.speed_jump = -50 #Tốc độ nhảy
        self.gravity = 5 #Trọng lực
        self.jump_velocity = 0 #Vận tốc nhảy ban đầu
        self.jumping = False
        
    def jump(self):
        if not self.jumping:
            self.jumping = True
            self.jump_velocity = self.speed_jump 
    def move(self,direction):
        self.direction = direction
        self.status = Status_Hero.MOVE
        if self.direction == Direction.LEFT:
            self.rect.x -= self.speed
        else:
            self.rect.x += self.speed
    def attack(self):
        self.status = Status_Hero.ATTACK
        #Tạo ra 1 viên đạn mới nạp vào self.list_bullet
        if self.direction == Direction.RIGHT:
            x_bullet = self.rect.x + self.rect.width 
            y_bullet = self.rect.y + self.rect.height // 2
            new_bullet = Bullet(x_bullet,y_bullet,Direction.RIGHT)
            self.lst_bullet.append(new_bullet)
        else:
            x_bullet = self.rect.x
            y_bullet = self.rect.y + self.rect.height // 2
            new_bullet = Bullet(x_bullet,y_bullet,Direction.LEFT)
            self.lst_bullet.append(new_bullet)


    
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
            frame_count = 4
        elif self.status == Status_Hero.ATTACK:
            folder_status_name = 'attack'
            frame_count = 4
        elif self.status == Status_Hero.DIE: 
            folder_status_name = 'die'
            frame_count = 19
        else:
            folder_status_name = 'freeze'
            frame_count = 3
        

        image_src =  f'./images/{folder_name_direct}/hero/{folder_status_name}/{self.frame % frame_count}.png'
        
        self.image = pygame.image.load(image_src)

    def draw(self,screen):
        if self.jumping:
            print(self.jumping)
            #Xử lý nhảy
            self.jump_velocity += self.gravity
            self.rect.y += self.jump_velocity
            #Xử lý chạm đất
            if self.rect.y > 500:
                self.jumping = False
                self.jump_velocity = 0

        #Vẽ đạn
        for bullet in self.lst_bullet:
            bullet.move()
            bullet.draw(screen)
            if bullet.rect.x > screen.get_width() and bullet.direction == Direction.RIGHT:
                self.lst_bullet.remove(bullet)
            elif bullet.rect.x < 0 and bullet.direction == Direction.LEFT:
                self.lst_bullet.remove(bullet)
                
            print(self.lst_bullet)
        screen.blit(self.image,self.rect)

        #Xử lý hero chết
        if self.live == 0:
            self.status = Status_Hero.DIE

        #Update status cập nhật frame
        current_status_time = pygame.time.get_ticks()
        if current_status_time - self.time_status_start >= 300:
            self.frame += 1
            self.time_status_start = current_status_time

        self.update_status()

        #Vẽ mạng và điểm lên màn hình
        f_game = pygame.font.Font('./fonts/font.otf',32)
        title_live = f_game.render(f'Live: {self.live}',True,'Yellow')
        f_game = pygame.font.Font('./fonts/font.otf',32)
        title_score = f_game.render(f'Score: {self.score}',True,'Yellow')
        screen.blit(title_live,(0,0))
        screen.blit(title_score,(screen.get_height() - title_score.get_width(),0))
        #Game Over
        f_game_over = pygame.font.Font('./fonts/font.otf',64)
        title_game_over = f_game_over.render('GAME OVER',True,'Red')
        x_title_game_over = screen.get_width()/2 - title_game_over.get_width()//2
        y_title_game_over = screen.get_height()/2 - title_game_over.get_height()
        if self.live == 0:
            screen.blit(title_game_over,(x_title_game_over,y_title_game_over))
        screen.blit(self.image,self.rect)