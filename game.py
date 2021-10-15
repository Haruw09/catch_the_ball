import pygame
import pygame.draw
from random import randint
pygame.init()
font = pygame.font.SysFont('arial', 50)
FPS = 50
width = 1000
length = 500
min_ball_size = 50
max_ball_size = 150

# создание дисплея
screen = pygame.display.set_mode((width, length))
name = input('Your name: ')

# цвета текста и фона соответственно
BLUE = (0, 0, 255)
WHITE = (255, 255, 255)

# класс из функций, создающих шарики
class Balls(pygame.sprite.Sprite):
  # импортит спрайты шаров из файлов
    def __init__(self):
        pygame.sprite.Sprite.__init__(self)
        if randint(0, 1) == 0:
            self.image = pygame.image.load('ball1.png')
            self.coefficient = 2
        else:
            self.image = pygame.image.load('ball2.png')
            self.coefficient = 1
        # задает начальные координаты шаров и их скорости, а также сжимает спрайты до нужных размеров
        self.rect = self.image.get_rect()
        self.rect.x = randint(max_ball_size, width - max_ball_size)
        self.rect.y = randint(max_ball_size, length - max_ball_size)
        self.scal = randint(min_ball_size, max_ball_size)
        self.image = pygame.transform.scale(self.image, (self.scal, self.scal))
        self.v_x = randint(-3, 3)
        self.v_y = randint(-3, 3)
    
    # движение с отраженим от стен, стирание шаров (на которые не кликает пользователь)
    def update(self):
        if self.rect.x + self.v_x <= 0 or self.rect.x + self.v_x >= width - self.scal:
            self.v_x = -self.v_x
        if self.rect.y + self.v_y <= 0 or self.rect.y + self.v_y >= length - self.scal:
            self.v_y = -self.v_y
        self.rect.x += self.v_x
        self.rect.y += self.v_y
        if(randint(1, 40) == 1):
            self.kill
    
    # определяет, попал ли пользователь по шару
    def condition_of_being_cought(self, coords):
        x_m = coords[0]
        y_m = coords[1] 
        if x_m >= self.rect.x and x_m <= self.rect.x + self.scal:
            condition_x = True
        else:
            condition_x = False
        if self.rect.y <= y_m and self.rect.y + self.scal >= y_m:
            condition_y = True
        else:
            condition_y = False
        if  condition_x and condition_y:
            return True
        else:
            return False
    
# выводит очки пользователя на экран
def score(Score):
    text = font.render("Score: " + str(Score), True, BLUE)
    screen.blit(text, (100, 100))

    
clock = pygame.time.Clock()
finished = False
Score = 0 
ball_class = Balls() 
ball = pygame.sprite.Group()
ball.add(ball_class)
ball.update()
pygame.display.flip()


while not finished:
    # обновление экрана, изменение движения шаров и их удаление (если нужно)
    clock.tick(FPS)
    screen.fill(WHITE)
    score(Score)
    ball.update()
    ball.draw(screen)
    pygame.display.flip()
    # добавление шаров
    if randint(1, 60) == 1:
        ball_class = Balls()
        ball.add(ball_class)
    # проверка, попал ли пользователь по шару, начисление очков и удаление "кликнутых" шариков
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            finished = True
        elif event.type == pygame.MOUSEBUTTONDOWN:
            for i in ball:
                if i.condition_of_being_cought(event.pos):
                    if i.coefficient == 2:
                        Score += 1
                    elif i.coefficient == 1: 
                        Score += 5
                    i.kill()

# выведем счет игрока в файл                
output = open('out.txt', 'w')
print('Name:' + name + ': ' + str(Score) + '\n', file = output)
    
pygame.quit()
