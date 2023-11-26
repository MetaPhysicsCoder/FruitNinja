import pygame
import random

g = 0.2
block = 30
ScreenWidth = 1200 * 1.2
ScreenHeight = 800 * 1.2
pause = 80
meter = ScreenHeight // 10
plank = 0.01
pygame.init()
screen = pygame.display.set_mode((ScreenWidth, ScreenHeight))
pygame.display.set_caption('Tetris')
time = pygame.time.Clock()
images = [pygame.image.load('fruit1.png').convert_alpha(), pygame.image.load('fruit2.png').convert_alpha(), pygame.image.load('fruit3.png').convert_alpha(), pygame.image.load('fruit4.png').convert_alpha(), pygame.image.load('fruit5.png').convert_alpha(), pygame.image.load('fruit6.png').convert_alpha()]

for i in range(len(images)) :
    w, h = images[i].get_width(), images[i].get_height()
    p1 = w * h / ScreenWidth / ScreenHeight
    k = plank/p1
    k = k ** 0.5
    images[i] = pygame.transform.scale(images[i], (w * k, h * k))
on_screen = []
background_image = pygame.image.load('backgroung.jpg')
background_image = pygame.transform.scale(background_image, (ScreenWidth, ScreenHeight))


class Fruit:
    def __init__(self, num, x, y, vec_x, vec_y):
        self.num = num
        self.x = x
        self.y = y
        self.vec_x = vec_x
        self.vec_y = vec_y

    def update(self, t):
        self.x = self.x + self.vec_x * t * meter
        self.y = self.y + self.vec_y * t * meter + (g * (t ** 2) / 2) * meter
        self.vec_y = self.vec_y + g * t

    def draw(self):
        screen.blit(images[self.num],(self.x - images[self.num].get_width()//2, self.y -  images[self.num].get_height()//2))


def add_random_fruit():
    x1 = random.randint(ScreenWidth // 4, ScreenWidth // 4 * 3)
    otl = int(abs(x1 - ScreenWidth/2)/(ScreenWidth/2) * 100)
    nap = 1
    if x1 > ScreenWidth/2:
        nap = -1
    on_screen.append(
        Fruit(random.randint(0, len(images) - 1), x1, ScreenHeight,
             random.choice([nap])*random.randint(0, 10)/10 if otl > 10 else random.randint(-10, 10)/10, - random.randint(100, 130) / 100 * (g * ScreenHeight / (1 * meter)) ** 0.5))

add_random_fruit()
c = 0
fades = []
class Fade:
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.rad = 0.002
        self.life = 5
while True:
    if c > 60:
        c = 0
        add_random_fruit()
    screen.blit(background_image, (0, 0))
    new_on_screen = []
    for i in range(len(on_screen)):
        on_screen[i].update(pause/1000)
        on_screen[i].draw()
        if (on_screen[i].y > ScreenHeight and on_screen[i].vec_y > 0) or (on_screen[i].x > ScreenWidth or on_screen[i].x < 0):
            pass
        else:
            new_on_screen.append(on_screen[i])
    new_fades = []
    flag = False
    prev = None
    for i in fades:
        if i.life > 0:
            if flag:
                pygame.draw.line(screen, (255,255,255), (prev.x, prev.y), (i.x, i.y), int(i.rad * ScreenWidth) + 1)
            i.life-=1
            new_fades.append(i)
            flag = True
            prev = i

    fades = new_fades
    on_screen = new_on_screen

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            exit()
        elif event.type == pygame.MOUSEMOTION:
            evx, evy = pygame.mouse.get_pos()[0], pygame.mouse.get_pos()[1]
            fades.append(Fade(pygame.mouse.get_pos()[0], pygame.mouse.get_pos()[1]))
            for i in range(len(on_screen)):
                if (on_screen[i].x - evx)**2 + (on_screen[i].y - evy) ** 2 < (ScreenWidth/23)**2:
                    on_screen.pop(i)
                    break

    c += 1
    pygame.display.flip()
    time.tick(pause)
