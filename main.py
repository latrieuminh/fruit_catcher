from pygame import *
from random import randint, uniform

S_WIDTH = 700
S_HEIGHT = 500



class GameSprite(sprite.Sprite):
    def __init__(self, player_image, player_x, player_y, size_x, size_y, player_speed):
        super().__init__()

        self.original_image = transform.scale(image.load(player_image), (size_x, size_y))
        self.image = self.original_image
        self.speed = player_speed
        self.rect = self.image.get_rect()
        self.rect.x = player_x
        self.rect.y = player_y
        self.direction = "right"

        self.size_x = size_x
        self.size_y = size_y
    def reset(self):
        main_win.blit(self.image, (self.rect.x, self.rect.y))

class Player(GameSprite):
    def update(self):
        keys = key.get_pressed()
        #left
        if (keys[K_LEFT] or keys[K_a]) and self.rect.x > 0:
            self.rect.x -= self.speed
            if self.direction != "left":
                self.image = transform.flip(self.original_image, True, False)
                self.direction = "left"

        #right
        if (keys[K_RIGHT] or keys[K_d]) and self.rect.x < S_WIDTH - self.size_x:
            self.rect.x += self.speed
            if self.direction != "right":
                self.image = self.original_image
                self.direction = "right"

player = Player('basket.png', 5, S_HEIGHT - 50, 50, 50, 10)

class Enemy(GameSprite):
    def update(self):
        global missed
        self.rect.y += self.speed
        if self.rect.y > S_HEIGHT:
            self.rect.x = randint(40, S_WIDTH - 40)
            self.rect.y = 0
            self.speed = randint(1, 6)
            missed = missed + 1

enemies1 = sprite.Group()


def create_enemies():
    for i in range(10):
        enemy = Enemy('fruit.png', randint(40, S_WIDTH - 40), -40, 60, 35, randint(1, 6))
        enemies1.add(enemy)

create_enemies()

score = 0
missed = 0
life = 3

max_missed = 50
max_score = 100
WHITE = (255, 255, 255)

main_win = display.set_mode((S_WIDTH, S_HEIGHT))
display.set_caption('fruit catcher')
background = transform.scale(image.load('bg.jpg'), (S_WIDTH, S_HEIGHT))


game = True
finish = False
clock = time.Clock()
FPS = 60
    
font.init()
font1 = font.Font(None, 36)
font2 = font.Font(None, 80)

win_text = font2.render("YOU WIN!", True, (255, 255, 255))
lose_text = font2.render("YOU LOSE!", True, (180, 0, 0))

while game:
    for e in event.get():
        if e.type == QUIT:
            game = False

    if not finish:
        main_win.blit(background, (0, 0))
        player.update()
        player.reset()
        enemies1.update()
        enemies1.draw(main_win)
        if missed >= max_missed or life == 0:
            finish = True
            main_win.blit(lose_text, (S_WIDTH // 2 - 150, S_HEIGHT // 2))

        if score >= max_score:
            finish = True
            main_win.blit(win_text, (S_WIDTH // 2 - 150, S_HEIGHT // 2))

        text_score = font1.render("Score: " + str(score), 1, WHITE)
        main_win.blit(text_score, (10, 20))

        text_miss = font1.render("Missed: " + str(missed), 1, WHITE)
        main_win.blit(text_miss, (10, 50))
    
    
    display.update()
    clock.tick (FPS)    