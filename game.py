from main.games.PlataformGame.loadSprites import sprite_list, l_sprite_list
import pygame

class World:
    def __init__(self, data):
        self.data = data
        self.tiles = []

        ycor = 0
        for line in data:
            # Iterates through rows in map file
            xcor = 0
            for n in line:
                # Iterates through blocks in each row
                if n == '1':
                    tile = DIRT
                    self.tiles.append((tile, (xcor, ycor), pygame.rect.Rect(xcor, ycor, TILESIZE , TILESIZE)))
                elif n == '2':
                    tile = GRASS
                    self.tiles.append((tile, (xcor, ycor), pygame.rect.Rect(xcor, ycor, TILESIZE , TILESIZE)))
                xcor += TILESIZE
            ycor += TILESIZE

    def render(self):
        for tile in self.tiles:
            SCREEN.blit(tile[0], (tile[1][0], tile[1][1]))

    def collision(self):
        walls = [i for i in self.tiles if i[1][1] < p.y + p.rect.height]
        for i in walls:
            if i[2].colliderect(p.rect):
                if p.right:
                    p.x -= 10
                    p.rect[0] -= 10
                else:
                    p.x += 10
                    p.rect[0] += 10
            pygame.draw.rect(SCREEN, (200, 0, 0), pygame.Rect(i[1][0], i[1][1], TILESIZE, TILESIZE), 5)

    def gravity(self):
        # Pygame Rect -> (left, top, width, height)
        # i -> (Surface, (xcor, ycor), pygame.rect.Rect(xcor, ycor, TILESIZE , TILESIZE))
        # i[1][1] -> ycor of Surface
        below = [i for i in self.tiles if i[1][1] > p.rect.bottom]
        y_below = [i[1][1] for i in self.tiles if i[1][1] > p.rect.bottom]

        for i in below:
            pygame.draw.rect(SCREEN, (0, 0, 255), i[2], 1)

        if y_below:
            print(min(y_below), p.rect.bottom)
            for i in below:
                if i[2].top == p.rect.bottom:
                    print('equals')

            if any(p.rect.bottom == y_below[y_below.index(i)] for i in y_below):
                print('collision')

            elif p.rect.bottom + GRAVITY > min(y_below):
                p.rect.bottom = min(y_below)
                p.y = p.rect.y

            else:
                p.rect.bottom += GRAVITY
                p.y += GRAVITY

        else:
            p.rect.y += GRAVITY
            p.y += GRAVITY

class Player:
    def __init__(self):
        self.x = 10
        self.rect = pygame.rect.Rect(self.x + 80, set_height(self.x + 80), 45, 100)
        self.y = self.rect.y
        self.moving, self.attacking, self.on_air = (False, False, False)
        self.sprite = sprite_list['idle'][0]
        self.sprite_index = 0
        self.jumping = 0
        self.right = True

    def render(self):
        if self.jumping and self.right:
            self.sprite = 'KNIGHT/' + sprite_list['jump'][self.sprite_index]
        elif self.jumping and not self.right:
            self.sprite = 'KNIGHT_LEFT/' + l_sprite_list['jump'][self.sprite_index]
        elif self.right and self.moving:
            self.sprite = 'KNIGHT/' + sprite_list['run'][self.sprite_index]
        elif not self.right and self.moving:
            self.sprite = 'KNIGHT_LEFT/' + l_sprite_list['run'][self.sprite_index]
        elif not self.right and not self.moving:
            self.sprite = 'KNIGHT_LEFT/' + l_sprite_list['idle'][0]
        else:
            self.sprite = 'KNIGHT/' + sprite_list['idle'][0]

        load = pygame.transform.scale(pygame.image.load('Images/' + self.sprite), (200, 200))
        SCREEN.blit(load, (self.x, self.y - 35))
        pygame.draw.rect(SCREEN, (255, 0, 0), self.rect, 1)
        pygame.draw.line(SCREEN, (255, 255, 255), (0, self.y), (1500, self.y), 3)
        pygame.draw.line(SCREEN, (255, 255, 255), (0, self.y + self.rect[3]), (1500, self.y + self.rect[3]), 3)
        self.sprite_index += 1
        if self.sprite_index > 8:
            self.sprite_index = 0

    def jump(self):
        self.y -= GRAVITY * 1.5
        self.rect[1] -= GRAVITY * 1.5
        self.jumping -= 1

def set_height(char_x):
    same_col = [i[1][1] for i in w1.tiles if char_x in range(i[2].x, i[2].x + i[2].width)]
    return min(same_col) - 5

def main():
    global run
    while run:
        CLOCK.tick(FPS)
        pygame.time.delay(10)
        for e in pygame.event.get():
            if e.type == pygame.QUIT:
                run = False

        keys = pygame.key.get_pressed()
        if keys[pygame.K_a]:
            p.x -= 10
            p.rect[0] -= 10
            p.right = False
            p.moving = True

        elif keys[pygame.K_d]:
            p.x += 10
            p.rect[0] += 10
            p.right = True
            p.moving = True

        else:
            p.moving = False

        if keys[pygame.K_SPACE] and not p.on_air:
            p.jumping = 15

        if keys[pygame.K_u]:
            p.y -= GRAVITY
            p.rect.y -= GRAVITY

        SCREEN.blit(SKY, (0, 0))
        w1.render()
        # w1.collision()
        if p.jumping:
            p.jump()
        w1.gravity()

        p.render()
        pygame.display.update()

W, H = 1365, 715
TILESIZE = 65

run = True

FPS = 60
GRAVITY = 20
ICON = pygame.image.load('Images/icon.png')
SKY = pygame.image.load('Images/sky.jpg')
DIRT = pygame.transform.scale(pygame.image.load('Images./dirt.jpg'), (TILESIZE, TILESIZE))
GRASS = pygame.transform.scale(pygame.image.load('Images./grass.jpg'), (TILESIZE, TILESIZE))
CLOCK = pygame.time.Clock()
MAP = open('map.txt', 'r').readlines()

w1 = World(MAP)
p = Player()

if __name__ == '__main__':
    pygame.init()
    SCREEN = pygame.display.set_mode((W, H), pygame.RESIZABLE)
    pygame.display.set_caption('Plataformer')
    pygame.display.set_icon(ICON)

    main()
