from games.PlataformGame.loadSprites import sprite_list, l_sprite_list, e_sprite_list, e_sprite_list_l
from pygame.math import Vector2
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
                    self.tiles.append((tile, Vector2(xcor, ycor), pygame.rect.Rect(xcor, ycor, TILESIZE , TILESIZE)))
                elif n == '2':
                    tile = GRASS
                    self.tiles.append((tile, Vector2(xcor, ycor), pygame.rect.Rect(xcor, ycor, TILESIZE , TILESIZE)))
                elif n == 'E':
                    Enemy(xcor, ycor - 81)
                elif n == 'C':
                    Coin(xcor, ycor + 20)
                elif n == 'D':
                    Door(xcor, ycor - 20)

                xcor += TILESIZE
            ycor += TILESIZE

    def render(self):
        for tile in self.tiles:
            SCREEN.blit(tile[0], (tile[1].x - camera.offset.x , tile[1].y - camera.offset.y + 30))

    def collision(self):
        for entity in ENTITIES:
            walls = [i for i in self.tiles if i[1].y < entity.y + entity.rect.height]
            if type(entity) == Enemy:
                # Checks for collision between player and enemy
                if player.rect.colliderect(entity.rect) and not player.immunity:
                    player.immunity = 20
                    player.hp -= 1
                    if player.right:
                        player.x += 200
                        player.rect.x += 200
                    else:
                        player.x -= 200
                        player.rect.x -= 200

            for i in walls:
                # wall collisions
                if i[2].colliderect(entity.rect):
                    if type(entity) == Enemy and not entity.on_air:
                        entity.jumping = 15

                    if entity.right:
                        entity.x -= entity.speed
                        entity.rect.x -= entity.speed
                    else:
                        entity.x += entity.speed
                        entity.rect.x += entity.speed

                if entity.rect.top < i[1].y + TILESIZE and entity.rect.x in range(int(i[1].x), int(i[1].x) + TILESIZE):
                    entity.rect.y += GRAVITY * 1.5
                    entity.y = entity.rect.y
                    entity.jumping = 0

        for coin in Coin.coin_list:
            if player.rect.colliderect(coin.rect):
                COIN_SOUND.play()
                Coin.coin_list.remove(coin)
                player.coins += 1
                break

    def gravity(self):
        # Pygame Rect -> (left, top, width, height)
        # i -> (Surface, (xcor, ycor), pygame.rect.Rect(xcor, ycor, TILESIZE , TILESIZE))

        global y_below
        for entity in ENTITIES:
            # below = [i for i in self.tiles if i[1][1] > p.rect.bottom]
            # for i in below:
            #    pygame.draw.rect(SCREEN, (0, 0, 255), i[2], 1)

            y_below = [i[1].y for i in self.tiles if i[1].y > entity.rect.bottom and entity.rect.left in range(i[2].left, i[2].right)
                       or i[1].y > entity.rect.bottom and entity.rect.right in range(i[2].left, i[2].right)]

            if y_below:
                if entity.rect.bottom + 1 == min(y_below):
                    entity.on_air = False

                elif entity.rect.bottom + GRAVITY > min(y_below):
                    entity.rect.bottom = min(y_below) - 1
                else:
                    entity.rect.bottom += GRAVITY
                    entity.on_air = True

            else:
                entity.rect.bottom += GRAVITY
                entity.on_air = True

            entity.y = entity.rect.y


class Camera:
    def __init__(self, target, camera_type):
        self.target = target
        self.camera_type = camera_type
        self.offset = Vector2(0, 0)
        self.offset_float = Vector2(0, 0)
        self.CONST = Vector2(-W / 2 + player.rect.w / 2, -target.rect.bottom + 300)

    def follow(self):
        self.offset_float.x += (self.target.x - self.offset_float.x + self.CONST.x)
        self.offset_float.y += (self.target.y - self.offset_float.y + self.CONST.y)
        self.offset.x, self.offset.y = int(self.offset_float.x), int(self.offset_float.y)

class Player:
    def __init__(self):
        self.x = 10
        self.rect = pygame.rect.Rect(self.x + 80, set_height(self.x + 80), 45, 95)
        self.y = self.rect.y
        self.moving, self.on_air = False, False
        self.sprite = sprite_list['idle'][0]
        self.sprite_index = 0
        self.jumping = 0
        self.right = True
        self.speed = 10
        self.attacking = 0
        self.atk_cooldown = 0
        self.immunity = 0
        self.hp = 100
        self.hit_enemy = False
        self.coins = 0
        ENTITIES.append(self)

    def render(self):
        if self.immunity and self.right:
            self.sprite = 'KNIGHT/' + sprite_list['hurt'][self.sprite_index]
        elif self.immunity and not self.right:
            self.sprite = 'KNIGHT_LEFT/' + l_sprite_list['hurt'][self.sprite_index]
        elif self.attacking and self.right:
            self.sprite = 'KNIGHT/' + sprite_list['attack'][self.sprite_index]
        elif self.attacking and not self.right:
            self.sprite = 'KNIGHT_LEFT/' + l_sprite_list['attack'][self.sprite_index]
        elif self.jumping and self.right:
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

        load = pygame.transform.scale(pygame.image.load('Images/' + self.sprite), (200, 200)).convert_alpha(SCREEN)
        SCREEN.blit(load, (self.x - camera.offset.x, self.y - camera.offset.y))
        # pygame.draw.rect(SCREEN, (255, 0, 0), (self.rect.x - camera.offset.x, self.rect.y - camera.offset.y + 35, self.rect.width, self.rect.height), 1)
        self.sprite_index += 1
        if self.sprite_index > 8:
            self.sprite_index = 0

    def jump(self):
        self.y -= GRAVITY * 1.5
        self.rect.y -= GRAVITY * 1.5
        self.jumping -= 1

    def attack(self):
        self.attacking -= 1
        if self.right:
            atk_rect = pygame.rect.Rect(self.rect.right + 5, self.rect.y + self.rect.height / 1.2, 70, 20)
        else:
            atk_rect = pygame.rect.Rect(self.rect.left - 70 - 5, self.rect.y + self.rect.height / 1.2, 70, 20)

        if not player.hit_enemy:
            for e in ENTITIES:
                if atk_rect.colliderect(e.rect) and not e.immunity:
                    ENEMY_HURT.play()
                    e.immunity = 20
                    e.hp -= 1
                    player.hit_enemy = True
                    if self.right:
                        e.x += 200
                        e.rect.x += 200
                    else:
                        e.x -= 200
                        e.rect.x -= 200
                    SWORD_HIT.play()

        # pygame.draw.rect(SCREEN, (0, 255, 0), [atk_rect.x - camera.offset.x, atk_rect.y - camera.offset.y, atk_rect.width, atk_rect.height], 5)

class Enemy:
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.rect = pygame.rect.Rect(self.x + 30, self.y, 45, 80)
        self.moving, self.attacking, self.on_air = (False, False, False)
        self.sprite = e_sprite_list['idle'][0]
        self.sprite_index = 0
        self.jumping = 0
        self.right = True
        self.speed = 9
        self.immunity = 0
        self.hp = 3
        self.hit_enemy = False
        self.behaviour = dict()
        ENTITIES.append(self)

    def set_behaviour(self):
        if player.x in range(self.x - self.rect.width - 400, self.x) and not self.behaviour:
            self.behaviour.setdefault('go_left', 5)
        elif player.x in range(self.x, self.x + 400) and not self.behaviour:
            self.behaviour.setdefault('go_right', 5)

        if player.x in range(self.x, self.x + 50) and not self.attacking or player.x in range(self.x - 175, self.x) and not self.attacking:
            if not self.immunity:
                self.attacking = 10
                ENEMY_ATTACK.play()

    def behave(self):
        self.moving = False
        below = [i[1].y for i in world.tiles if i[1].y > self.rect.bottom and self.rect.left + self.speed in range(i[2].left, i[2].right)
                 or i[1].y > self.rect.bottom and self.rect.right - self.speed in range(i[2].left, i[2].right)]

        if 'go_left' in self.behaviour.keys() and below and not self.immunity:
            self.behaviour['go_left'] -= 1
            self.right = False
            self.moving = True
            self.x -= self.speed
            self.rect.x -= self.speed
            self.sprite = e_sprite_list_l['run'][(self.sprite_index + 1) % len(self.sprite)]

            if self.behaviour['go_left'] <= 0:
                self.behaviour.pop('go_left')

        elif 'go_right' in self.behaviour.keys() and below and not self.immunity:
            self.behaviour['go_right'] -= 1
            self.right = True
            self.moving = True
            self.x += self.speed
            self.rect.x += self.speed
            self.sprite = e_sprite_list['run'][(self.sprite_index + 1) % len(self.sprite)]

            if self.behaviour['go_right'] <= 0:
                self.behaviour.pop('go_right')

    def jump(self):
        self.y -= GRAVITY * 1.5
        self.rect.y -= GRAVITY * 1.5
        self.jumping -= 1

    def render(self):
        if self.immunity and self.right:
            self.sprite = 'MINOTAUR/PNGSequences/' + e_sprite_list['hurt'][self.sprite_index]
        elif self.immunity and not self.right:
            self.sprite = 'MINOTAUR_LEFT/PNGSequences/' + e_sprite_list_l['hurt'][self.sprite_index]
        elif self.attacking and self.right:
            self.sprite = 'MINOTAUR/PNGSequences/' + e_sprite_list['attack'][self.sprite_index]
        elif self.attacking and not self.right:
            self.sprite = 'MINOTAUR_LEFT/PNGSequences/' + e_sprite_list_l['attack'][self.sprite_index]
        elif self.jumping and self.right:
            self.sprite = 'MINOTAUR/PNGSequences/' + e_sprite_list['jump'][(self.sprite_index + 1) % len(e_sprite_list['jump'])]
        elif self.jumping and not self.right:
            self.sprite = 'MINOTAUR_LEFT/PNGSequences/' + e_sprite_list_l['jump'][(self.sprite_index + 1) % len(e_sprite_list_l['jump'])]
        elif self.right and self.moving:
            self.sprite = 'MINOTAUR/PNGSequences/' + e_sprite_list['run'][(self.sprite_index + 1) % len(e_sprite_list['run'])]
        elif not self.right and self.moving:
            self.sprite = 'MINOTAUR_LEFT/PNGSequences/' + e_sprite_list_l['run'][(self.sprite_index + 1) % len(e_sprite_list_l['run'])]
        elif not self.right and not self.moving:
            self.sprite = 'MINOTAUR_LEFT/PNGSequences/' + e_sprite_list_l['idle'][0]
        else:
            self.sprite = 'MINOTAUR/PNGSequences/' + e_sprite_list['idle'][0]

        load = pygame.transform.scale(pygame.image.load('Images/' + self.sprite), (100, 100)).convert_alpha(SCREEN)
        SCREEN.blit(load, (self.x - camera.offset.x, self.y - camera.offset.y))
        # pygame.draw.rect(SCREEN, (255, 0, 0), (self.rect.x - camera.offset.x, self.rect.y - camera.offset.y, self.rect.width, self.rect.height), 1)
        self.sprite_index += 1
        if self.sprite_index > 8:
            self.sprite_index = 0

    def attack(self):
        self.attacking -= 1
        if self.right:
            atk_rect = pygame.rect.Rect(self.rect.right + 5, self.rect.y + self.rect.height / 2, 40, 20)
        else:
            atk_rect = pygame.rect.Rect(self.rect.left - 40 - 5, self.rect.y + self.rect.height / 2, 40, 20)

        if atk_rect.colliderect(player.rect) and not player.immunity and not self.hit_enemy:
            player.hp -= 1
            player.immunity = 20
            self.hit_enemy = True
            if self.right:
                player.x += 100
                player.rect.x += 100
            else:
                player.x -= 100
                player.rect.x -= 100

        # pygame.draw.rect(SCREEN, (0, 0, 255), [atk_rect.x - camera.offset.x, atk_rect.y - camera.offset.y, atk_rect.width, atk_rect.height], 5)

class Coin:
    sprite_index = 30
    coin_list = []
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.rect = pygame.rect.Rect(x, y, 30, 30)
        self.coin_list.append(self)

    def get_sprite(self, width, height):
        surface = pygame.Surface((width, height),pygame.SRCALPHA, 32) #
        surface.blit(COIN, (0, 0), (0, 0, self.sprite_index, height))
        return surface

    @classmethod
    def render(cls):
        sprite = cls.get_sprite(cls, 30, 30).convert_alpha(SCREEN)
        for coin in cls.coin_list:
            SCREEN.blit(sprite, (coin.x - camera.offset.x, coin.y - camera.offset.y))
            # pygame.draw.rect(SCREEN, (0, 255, 0), (coin.x - c.offset.x, coin.y - c.offset.y , 30, 30), 3)

class Door:
    doors = []
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.rect = pygame.rect.Rect(x, y, 100, 100)
        self.doors.append(self)

    def display(self):
        SCREEN.blit(DOOR, (self.x - camera.offset.x, self.y - camera.offset.y))
        # pygame.draw.rect(SCREEN, (0, 255, 0), (self.rect.x - camera.offset.x, self.rect.y - camera.offset.y, self.rect.width, self.rect.height), 1)

    def collision(self):
        if self.rect.colliderect(player.rect):
            next_map()

def set_height(char_x):
    # 101 is the height of the player's rect + 1
    same_col = [i[1][1] for i in world.tiles if char_x in range(i[2].x, i[2].x + i[2].width)]
    return min(same_col) - 101

def coin_display():
    text_display = FONT.render(str(player.coins), 1, (0, 0, 0))
    surface = pygame.Surface((30, 75),pygame.SRCALPHA, 32)
    surface.blit(COIN, (0, 0), (0, 0, 30, 75))
    SCREEN.blit(text_display, (30, 30))
    SCREEN.blit(surface, (80, 35))

def next_map():
    global map_index, world, player, camera
    map_index = map_index + 1 if map_index + 1 < len(MAP_LIST) else map_index
    ENTITIES.clear()
    Coin.coin_list.clear()
    Door.doors.clear()
    world = World(MAP_LIST[map_index])
    player = Player()
    camera = Camera(player, Camera.follow)

def main():
    global run
    pygame.mixer.music.play(-1)
    while run:
        CLOCK.tick(FPS)

        for e in pygame.event.get():
            if e.type == pygame.QUIT:
                run = False
            elif e.type == pygame.MOUSEBUTTONDOWN and e.button == 1 and not player.attacking and not player.immunity:
                player.attacking = 15
                SWORD_SLASH.play()
                break

        keys = pygame.key.get_pressed()
        if keys[pygame.K_a]:
            player.x -= player.speed
            player.rect.x -= player.speed
            player.right = False
            player.moving = True

        elif keys[pygame.K_d]:
            player.x += player.speed
            player.rect.x += player.speed
            player.right = True
            player.moving = True

        else:
            player.moving = False

        if keys[pygame.K_SPACE] and not player.on_air:
            player.jumping = 15
            for e in ENTITIES:
                if type(e) == Enemy:
                    if e.behaviour and not e.on_air:
                        e.jumping = 15

        if keys[pygame.K_u]:
            player.y -= GRAVITY
            player.rect.y -= GRAVITY

        SCREEN.blit(SKY, (0, 0))
        world.collision()
        world.gravity()
        camera.camera_type(camera)
        world.render()
        Coin.render()
        Coin.render()
        coin_display()
        Door.doors[0].display()
        Door.doors[0].collision()

        for e in ENTITIES:
            if not e.attacking:
                e.hit_enemy = False

            if e.immunity:
                e.immunity -= 1

            if e.hp < 1:
                ENTITIES.remove(e)

            if e.jumping:
                e.jump()

            if e.attacking:
                e.attack()

            if type(e) == Enemy:
                e.set_behaviour()
                e.behave()
            e.render()

        pygame.display.update()

W, H = 1350, 700
TILESIZE = 50

run = True

FPS = 60
GRAVITY = 20
ICON = pygame.image.load('Images/icon.png')

CLOCK = pygame.time.Clock()
MAP = open('map.txt', 'r').readlines()
MAP2 = open('map2.txt', 'r').readlines()
MAP_LIST = [MAP, MAP2]
map_index = 0
ENTITIES = []

if __name__ == '__main__':
    pygame.init()
    SCREEN = pygame.display.set_mode((W, H), pygame.RESIZABLE)

    FONT = pygame.font.SysFont("Times New Roman", 40)
    SKY = pygame.image.load('Images/sky.jpg').convert_alpha(SCREEN)
    DIRT = pygame.transform.scale(pygame.image.load('Images/dirt.jpg'), (TILESIZE, TILESIZE)).convert_alpha(SCREEN)
    GRASS = pygame.transform.scale(pygame.image.load('Images/grass.jpg'), (TILESIZE, TILESIZE)).convert_alpha(SCREEN)
    COIN = pygame.image.load('C:\\Users\Miguel\PycharmProjects\MyProjects\main\games\PlataformGame\Images\Coin4.png').convert_alpha(SCREEN)
    DOOR = pygame.transform.scale(pygame.image.load('C:\\Users\Miguel\PycharmProjects\MyProjects\main\games\PlataformGame\Images\door.png'), (100, 100)).convert_alpha(SCREEN)

    pygame.mixer.music.load('C:\\Users\Miguel\PycharmProjects\MyProjects\main\games\PlataformGame\Sounds\\background.mp3')
    SWORD_SLASH = pygame.mixer.Sound('C:\\Users\Miguel\PycharmProjects\MyProjects\main\games\PlataformGame\Sounds\sword.mp3')
    SWORD_HIT = pygame.mixer.Sound('C:\\Users\Miguel\PycharmProjects\MyProjects\main\games\PlataformGame\Sounds\sword_impact.wav')
    ENEMY_ATTACK = pygame.mixer.Sound('C:\\Users\Miguel\PycharmProjects\MyProjects\main\games\PlataformGame\Sounds\enemy.wav')
    ENEMY_HURT = pygame.mixer.Sound('C:\\Users\Miguel\PycharmProjects\MyProjects\main\games\PlataformGame\Sounds\enemy_hurt.wav')
    COIN_SOUND = pygame.mixer.Sound('C:\\Users\Miguel\PycharmProjects\MyProjects\main\games\PlataformGame\Sounds\coin.wav')

    pygame.display.set_caption('Plataformer')
    pygame.display.set_icon(ICON)
    world = World(MAP_LIST[map_index])
    player = Player()
    camera = Camera(player, Camera.follow)

    main()
