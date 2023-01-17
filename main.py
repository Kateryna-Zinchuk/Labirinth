import pygame
import os
pygame.init()

def path_file(file_name):
    folder_path = os.path.abspath(__file__ + "/..")
    path = os.path.join(folder_path, file_name)
    return path


WIN_WIDTH = 800
WIN_HEIGHT = 600
FPS = 40
GREY = (100, 100, 100)
BLACK = (0, 0, 0)
BLUE = (13, 8, 112)
RED = (250, 2, 2)
LIGHT_RED = (255, 64, 64)
GREEN = (37, 140, 21)
LIGHT_GREEN = (91, 212, 72)

window = pygame.display.set_mode((WIN_WIDTH, WIN_HEIGHT))
clock = pygame.time.Clock()
fon = pygame.image.load(path_file("fon.jpg"))
fon = pygame.transform.scale(fon,(WIN_WIDTH, WIN_HEIGHT))

fon_hogwarts = pygame.image.load(path_file("hogwarts.jpg"))
fon_hogwarts = pygame.transform.scale(fon_hogwarts,(WIN_WIDTH, WIN_HEIGHT))

win_picture = pygame.image.load(path_file("win_image.png"))
win_picture = pygame.transform.scale(win_picture,(WIN_WIDTH, WIN_HEIGHT))

lose_picture = pygame.image.load(path_file("lose_image.jpg"))
lose_picture = pygame.transform.scale(lose_picture,(WIN_WIDTH, WIN_HEIGHT))

pygame.mixer.music.load(path_file("main.wav"))
pygame.mixer.music.set_volume(0.5)
pygame.mixer.music.play(-1)

win_music = pygame.mixer.Sound(path_file("win.wav"))
lose_music = pygame.mixer.Sound(path_file("lose.wav"))
lose_music.set_volume(0.5)

music_shoot = pygame.mixer.Sound(path_file("stupefy.wav"))
music_shoot.set_volume(0.3)

class GameSprite(pygame.sprite.Sprite):
    def __init__(self, x, y, width, height, img):
        super().__init__()
        self.rect = pygame.Rect(x, y, width, height)
        self.image = pygame.image.load(img)
        self.image = pygame.transform.scale(self.image, (width, height))
        

    def reset(self):
        window.blit(self.image, (self.rect.x, self.rect.y))


class Bullet(GameSprite):
    def __init__(self, x, y, width, height, img, speed):
        super().__init__(x, y, width, height, img)
        self.speed = speed

    def update(self):
        self.rect.x += self.speed
        if self.rect.left > WIN_WIDTH or self.rect.right < 0:
            self.kill()


class Enemy(GameSprite):
    def __init__(self, x, y, width, height, file_name, speed, direction, min_coord, max_coord):
        super().__init__(x, y, width, height, file_name)
        self.speed = speed
        self.direction = direction
        self.min_coord = min_coord
        self.max_coord = max_coord

    def update(self):
        if self.direction == "left" or self.direction == "right":
            if self.direction == "left":
                self.rect.x -= self.speed
            if self.direction == "right":
                self.rect.x += self.speed 

            if self.rect.right >= self.max_coord:
                self.direction = "left"
            if self.rect.left <= self.min_coord:
                self.direction = "right"

        elif self.direction == "up" or self.direction == "down":
            if self.direction == "down":
                self.rect.y += self.speed
            if self.direction == "up":
                self.rect.y -= self.speed

            if self.rect.top <= self.min_coord:
                self.direction = "down"
            if self.rect.bottom >= self.max_coord:
                self.direction = "up"

             



class Player(GameSprite):
    def __init__(self, x, y, width, height, img):
        super().__init__(x, y, width, height, img)
        self.speed_x = 0
        self.speed_y = 0
        self.direction = "left"
        self.image_l = self.image
        self.image_r = pygame.transform.flip(self.image, True, False)

        
    def update(self):
        if self.speed_x > 0 and self.rect.right < WIN_WIDTH or self.speed_x < 0 and self.rect.left > 0:
            self.rect.x += self.speed_x
        walls_touched = pygame.sprite.spritecollide(self, walls, False)
        if self.speed_x > 0:
            for wall in walls_touched:
                self.rect.right = min(self.rect.right, wall.rect.left)
        elif self.speed_x < 0:
            for wall in walls_touched:
                self.rect.left = max(self.rect.left, wall.rect.right)
        
        
        if self.speed_y < 0 and self.rect.top > 0 or self.speed_y > 0 and self.rect.bottom < WIN_HEIGHT:
            self.rect.y += self.speed_y
            walls_touched = pygame.sprite.spritecollide(self, walls, False)
        if self.speed_y > 0:
            for wall in walls_touched:
                self.rect.bottom = min(self.rect.bottom, wall.rect.top)
        elif self.speed_y < 0:
            for wall in walls_touched:
                self.rect.top = max(self.rect.top, wall.rect.bottom)

    def shoot(self):
        if self.direction == "right":
            bullet = Bullet(self.rect.right, self.rect.centery, 40, 40, path_file("thunder.jpg"), 5)
            bullets.add(bullet)
        if self.direction == "left":
            bullet = Bullet(self.rect.left -10, self.rect.centery, 40, 40, path_file("thunder.jpg"), -5)
            bullets.add(bullet)

class Button():
    def __init__(self, color, x, y, width, height, text):
        self.color = color
        self.rect = pygame.Rect(x, y, width, height)
        self.font30 = pygame.font.SysFont("arial", 30)
        self.text = self.font30.render(text, True, BLACK)

    def button_show(self, px_x, px_y):
        pygame.draw.rect(window, self.color, self.rect)
        window.blit(self.text, (self.rect.x + px_x, self.rect.y + px_y))


button_start = Button(GREEN, 150, 250, 100, 50, "START")
button_exit = Button(RED, 600, 250, 100, 50, "EXIT")

player = Player(50, 100, 50, 70, path_file("harry_potter.jpg"))

bullets = pygame.sprite.Group()


enemies = pygame.sprite.Group()
enemy1 = Enemy(400, 400, 70, 70, path_file("traps.jpg"), 4, "up", 200, 400)
enemies.add(enemy1)
enemy2 = Enemy(500, 300, 70, 70, path_file ("traps.jpg"), 2, "right", 500, 750)
enemies.add(enemy2)
enemy3 = Enemy(150, 0, 70, 70, path_file ("traps.jpg"), 2, "up", 100, 300)
enemies.add(enemy3)

goal = GameSprite(715, 380, 100, 70, path_file("price.jpg"))

walls = pygame.sprite.Group()
wall1 = GameSprite(150, 0, 30, 180, path_file("wall.jpg"))
walls.add(wall1)
wall2 = GameSprite(150, 300, 30, 180, path_file("wall.jpg"))
walls.add(wall2)
wall3 = GameSprite(150, 150, 180, 30, path_file("wall.jpg"))
walls.add(wall3)
wall4 = GameSprite(300, 40, 30, 130, path_file("wall.jpg"))
walls.add(wall4)
wall5 = GameSprite(300, 40, 120, 30, path_file("wall.jpg"))
walls.add(wall5)
wall6 = GameSprite(400, 40, 30, 130, path_file("wall.jpg"))
walls.add(wall6)
wall7 = GameSprite(400, 150, 130, 30, path_file("wall.jpg"))
walls.add(wall7)
wall8 = GameSprite(500, 180, 30, 130, path_file("wall.jpg"))
walls.add(wall8)
wall9 = GameSprite(500, 300, 30, 130, path_file("wall.jpg"))
walls.add(wall9)
wall_10 = GameSprite(500, 400, 120, 30, path_file("wall.jpg"))
walls.add(wall_10)
#wall_11 = GameSprite(590, 400, 120, 30, "wall.jpg")
#walls.add(wall_11)
wall_12 = GameSprite(700, 300, 30, 130, path_file("wall.jpg"))
walls.add(wall_12)
wall_13 = GameSprite(700, 80, 30, 350, path_file("wall.jpg"))
walls.add(wall_13)
#wall_14 = GameSprite(700, 60, 100, 30, "wall.jpg")
#walls.add(wall_14)
wall_15 = GameSprite(150, 300, 180, 30, path_file("wall.jpg"))
walls.add(wall_15)
wall_16 = GameSprite(300, 300, 30, 180, path_file("wall.jpg"))
walls.add(wall_16)
wall_17 = GameSprite(300, 420, 30, 130, path_file("wall.jpg"))
walls.add(wall_17)
wall_18 = GameSprite(300, 530, 400, 30, path_file("wall.jpg"))
walls.add(wall_18)
wall_19 = GameSprite(690, 500, 10, 15, path_file("wall.jpg"))
walls.add(wall_19)
wall_20 = GameSprite(690, 470, 10, 15, path_file("wall.jpg"))
walls.add(wall_20)


level = 0

game = True
play = True
while game:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            game = False
        if level == 0:
            if event.type == pygame.MOUSEMOTION:
                x, y = event.pos
                if button_start.rect.collidepoint(x, y):
                    button_start.color = LIGHT_GREEN
                    button_start.rect.width = 100
                    button_start.height = 100
                elif button_exit.rect.collidepoint(x, y):
                    button_exit.color = LIGHT_RED
                    button_exit.rect.width = 100
                    button_exit.rect.height = 100
                else:
                    button_start.color = GREEN
                    button_start.rect.width = 100
                    button_start.rect.width = 100

                    button_exit.color = RED
                    button_exit.rect.width = 100
                    button_exit.rect.width = 100
            if event.type == pygame.MOUSEBUTTONDOWN:
                x, y = event.pos
                if button_start.rect.collidepoint(x, y):
                    level = 1
                elif button_exit.rect.collidepoint(x, y):
                    game = False
        elif level == 1:
            

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_RIGHT or event.key == pygame.K_d:
                    player.speed_x = 5
                    player.direction = "right"
                    player.image = player.image_r
                if event.key == pygame.K_LEFT or event.key == pygame.K_a:
                    player.speed_x = -5
                    player.direction = "left"
                    player.image = player.image_l
                if event.key == pygame.K_UP or event.key == pygame.K_w:
                    player.speed_y = -5
                if event.key == pygame.K_DOWN or event.key == pygame.K_s:
                    player.speed_y = 5

                if event.key == pygame.K_SPACE:
                    player.shoot()
                    music_shoot.play()

            if event.type == pygame.KEYUP:
                if event.key == pygame.K_RIGHT or event.key == pygame.K_d:
                    player.speed_x = 0
                if event.key == pygame.K_LEFT or event.key == pygame.K_a:
                    player.speed_x = 0
                if event.key == pygame.K_UP or event.key == pygame.K_w:
                    player.speed_y = 0
                if event.key == pygame.K_DOWN or event.key == pygame.K_s:
                    player.speed_y = 0



    if level == 0:
        window.blit(fon_hogwarts, (0, 0))
        button_start.button_show(17, 17)
        button_exit.button_show(17, 17)
    elif level == 1:

        if play == True:
            window.blit(fon, (0, 0))
            player.reset()
            player.update()

            enemies.draw(window)
            enemies.update()

            goal.reset()

            walls.draw(window)

            bullets.draw(window)
            bullets.update()

            if pygame.sprite.collide_rect(player, goal):
                play = False
                window.blit(win_picture, (0, 0))
                pygame.mixer.music.stop()
                win_music.play()

            if pygame.sprite.spritecollide(player, enemies, False):
                play = False
                window.blit(lose_picture, (0, 0))
                pygame.mixer.music.stop()
                lose_music.play()

            pygame.sprite.groupcollide(bullets, walls, True, False)
            pygame.sprite.groupcollide(bullets, enemies, True, True)


    clock.tick(FPS)
    pygame.display.update()