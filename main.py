import pygame
import random

WIDTH, HEIGHT = 800, 600
FPS = 60
TILE_SIZE = 32
DIRECTS = [[0, -1], [1, 0], [0, 1], [-1, 0]]


class Tank:
    def __init__(self, color, px, py, direct, key_list, heal_points=5, armor=1):
        objects.append(self)
        self.type = 'tank'
        self.color = color
        self.rect = pygame.Rect(px, py, TILE_SIZE, TILE_SIZE)
        self.direct = direct
        self.moveSpeed = 1

        self.heal_points = heal_points
        self.armor = armor

        self.bullet_damage = 1
        self.bullet_speed = 5
        self.shoot_timer = 0
        self.shoot_delay = 60

        self.k_left = key_list[0]
        self.k_right = key_list[1]
        self.k_up = key_list[2]
        self.k_down = key_list[3]
        self.k_shoot = key_list[4]

    def update(self):
        oldX, oldY = self.rect.topleft
        if keys[self.k_left]:
            self.rect.x -= self.moveSpeed
            self.direct = 3
        if keys[self.k_right]:
            self.rect.x += self.moveSpeed
            self.direct = 1
        if keys[self.k_up]:
            self.rect.y -= self.moveSpeed
            self.direct = 0
        if keys[self.k_down]:
            self.rect.y += self.moveSpeed
            self.direct = 2

        for object in objects:
            if object != self and self.rect.colliderect(object.rect):
                self.rect.topleft = oldX, oldY

        if keys[self.k_shoot] and self.shoot_timer == 0:
            dx = DIRECTS[self.direct][0] * self.bullet_speed
            dy = DIRECTS[self.direct][1] * self.bullet_speed
            Bullet(self, self.rect.centerx, self.rect.centery, dx, dy, 1)
            self.shoot_timer = self.shoot_delay

        if self.shoot_timer > 0:
            self.shoot_timer -= 1

    def draw(self):
        pygame.draw.rect(window, self.color, self.rect)

        x = self.rect.centerx + DIRECTS[self.direct][0] * 30
        y = self.rect.centery + DIRECTS[self.direct][1] * 30

        pygame.draw.line(window, 'white', self.rect.center, (x, y), 4)

    def damage(self, value):
        self.heal_points -= abs(value)
        print(self.heal_points)
        if self.heal_points <= 0:
            objects.remove(self)


class Bullet:
    def __init__(self, parent, px, py, dx, dy, damage):
        bullets.append(self)
        self.px = px
        self.py = py
        self.dx = dx
        self.dy = dy
        self.damage = damage
        self.parent = parent

    def update(self):
        self.px += self.dx
        self.py += self.dy

        if self.px < 0 or self.px > WIDTH or self.py < 0 or self.py > HEIGHT:
            bullets.remove(self)
        else:
            for obj in objects:
                if obj != self.parent and obj.rect.collidepoint(self.px, self.py):
                    obj.damage(self.damage)
                    bullets.remove(self)
                    break

    def draw(self):
        pygame.draw.circle(window, 'yellow', (self.px, self.py), 2)


class Block:
    def __init__(self, px, py, size):
        objects.append(self)
        self.size = size
        self.py = py
        self.px = px
        self.type = 'block'

        self.rect = pygame.Rect(px, py, size, size)
        self.heal_points = 1

    def update(self):
        # for object in objects:
        #     if object.rect.collidepoint(self.px, self.py):
        #         obj.damage(1)
        #         break
        pass

    def draw(self):
        pygame.draw.rect(window, 'green', self.rect)
        pygame.draw.rect(window, 'grey20', self.rect)

    def damage(self, value):
        self.heal_points -= value
        if self.heal_points <= 0:
            objects.remove(self)


if __name__ == '__main__':
    window = pygame.display.set_mode((WIDTH, HEIGHT))
    clock = pygame.time.Clock()

    objects = []
    bullets = []
    blue_tank = Tank('white', 100, 275, 0, (pygame.K_a, pygame.K_d, pygame.K_w, pygame.K_s, pygame.K_z))
    red_tank = Tank('red', 650, 275, 0, (pygame.K_LEFT, pygame.K_RIGHT, pygame.K_UP, pygame.K_DOWN, pygame.K_SPACE))
    block = Block(100, 100, TILE_SIZE)
    run = True

    for i in range(0, 50):
        while True:
            x = random.randint(0, WIDTH // TILE_SIZE - 1) * TILE_SIZE
            y = random.randint(0, HEIGHT // TILE_SIZE - 1) * TILE_SIZE
            rect = pygame.Rect(x, y, TILE_SIZE, TILE_SIZE)
            fined = False

            for object in objects:
                if rect.colliderect(object.rect):
                    fined = True

            if not fined:
                break

        Block(x, y, TILE_SIZE)

    while run:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False

        keys = pygame.key.get_pressed()

        for obj in objects:
            obj.update()

        for bullet in bullets:
            bullet.update()

        window.fill('black')

        for bullet in bullets:
            bullet.draw()

        for obj in objects:
            obj.draw()

        pygame.display.update()
        clock.tick(FPS)

pygame.quit()
