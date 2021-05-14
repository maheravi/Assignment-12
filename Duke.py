import pygame
import random

pygame.init()


class Bird:
    speed = 5

    def __init__(self):
        self.direction = random.choice(['ltr', 'rtl'])
        if self.direction == 'ltr':
            self.x = -50
        elif self.direction == 'rtl':
            self.x = game.width + 50
        self.y = random.randint(0, game.height / 3)

    def show(self):
        if self.direction == 'ltr':
            game.display.blit(self.image, [self.x, self.y])
        elif self.direction == 'rtl':
            game.display.blit(pygame.transform.flip(self.image, True, False), [self.x, self.y])

    def fly(self):
        if self.direction == 'ltr':
            self.x += self.speed
        elif self.direction == 'rtl':
            self.x -= self.speed


class Duck(Bird):
    def __init__(self):
        super().__init__()
        self.image = pygame.transform.scale(pygame.image.load('duck.png'), (50, 50))
        self.rect = self.image.get_rect()


class Stork(Bird):
    def __init__(self):
        super().__init__()
        self.image = pygame.transform.scale(pygame.image.load('Stork.png'), (50, 50))
        self.rect = self.image.get_rect()


class Donkey:
    def __init__(self):
        self.game = game
        self.speed = 10
        self.image = pygame.transform.scale(pygame.image.load('donkey.png'), (50, 50))
        self.rect = self.image.get_rect()
        self.direction = random.choice(['ltr', 'rtl'])
        if self.direction == 'ltr':
            self.x = -50
        elif self.direction == 'rtl':
            self.x = game.width + 50
        self.y = random.randint(0, game.height / 2)

    def show(self):
        if self.direction == 'ltr':
            game.display.blit(pygame.transform.flip(self.image, True, False), [self.x, self.y])
            self.x += self.speed
        elif self.direction == 'rtl':
            game.display.blit(self.image, [self.x, self.y])
            self.x -= self.speed


class Cloud:
    def __init__(self):
        self.game = game
        self.x = 50
        self.y = random.randint(0, game.height / 2)
        self.speed = 5
        self.image = pygame.image.load("cloud.png")

    def show(self):
        self.game.display.blit(self.image, (self.x, self.y))
        self.x += self.speed


class Gun:
    def __init__(self):
        self.x = game.width / 2
        self.y = game.height / 2
        self.image = pygame.image.load('shooter.png')
        self.score = 0
        self.sound = pygame.mixer.Sound('shotgun.wav')
        self.sound2 = pygame.mixer.Sound('Reload.mp3')
        self.sound3 = pygame.mixer.Sound('Empty.mp3')
        self.gu = pygame.transform.scale(self.image, (50, 50))
        self.rect = self.gu.get_rect()
        self.ammo = 10

    def show(self):
        game.display.blit(self.image, (self.x, self.y))

    def fire(self):
        self.sound.play()
        self.sound2.play()
        self.ammo -= 1

    def no_ammo(self):
        self.sound3.play()


class Game:
    def __init__(self):
        self.width = 852
        self.height = 480
        self.display = pygame.display.set_mode((self.width, self.height))
        self.clock = pygame.time.Clock()
        self.background = pygame.image.load('background.jpg')
        self.fps = 30

    def play(self):
        pygame.mouse.set_visible(False)

        my_gun = Gun()
        ducks = []
        clouds = []
        storks = []
        donkeys = []

        while True:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    exit()

                if event.type == pygame.MOUSEMOTION:
                    my_gun.x = pygame.mouse.get_pos()[0]
                    my_gun.y = pygame.mouse.get_pos()[1]

                if event.type == pygame.MOUSEBUTTONDOWN:
                    if my_gun.ammo > 0:
                        my_gun.fire()
                        for duck in ducks:
                            if pygame.Rect(
                                    my_gun.x, my_gun.y, 50, 50).colliderect(pygame.Rect(duck.x, duck.y, 50, 50)):
                                my_gun.score += 1
                                my_gun.ammo += 2
                                ducks.remove(duck)
                        for stork in storks:
                            if pygame.Rect(
                                    my_gun.x, my_gun.y, 50, 50).colliderect(pygame.Rect(stork.x, stork.y, 50, 50)):
                                my_gun.score += 1
                                my_gun.ammo += 2
                                storks.remove(stork)

                        for donkey in donkeys:
                            if pygame.Rect(
                                    my_gun.x, my_gun.y, 50, 50).colliderect(pygame.Rect(donkey.x, donkey.y, 50, 50)):
                                my_gun.ammo += 10
                                donkeys.remove(donkey)

                    elif my_gun.ammo == 0 or my_gun.ammo < 0:
                        my_gun.no_ammo()

            self.display.blit(self.background, (0, 0))
            my_gun.show()

            if random.random() < 0.04:
                ducks.append(Duck())

            if random.random() < 0.003:
                clouds.append(Cloud())

            if random.random() < 0.02:
                storks.append(Stork())

            if random.random() < 0.001:
                donkeys.append(Donkey())

            for duck in ducks:
                duck.show()
                duck.fly()

            for stork in storks:
                stork.show()
                stork.fly()

            for cloud in clouds:
                cloud.show()
                if cloud.y == game.width:
                    clouds.remove(cloud)

            for donkey in donkeys:
                donkey.show()

            font = pygame.font.SysFont('comicsansms', 20)
            score_font = font.render("Score: " + str(my_gun.score), True, (255, 0, 0))
            font_pos = score_font.get_rect(center=(50, self.height - 50))
            self.display.blit(score_font, font_pos)
            score_font = font.render("Ammo: " + str(my_gun.ammo), True, (255, 0, 0))
            font_pos = score_font.get_rect(center=(50, self.height - 30))
            self.display.blit(score_font, font_pos)

            pygame.display.update()
            self.clock.tick(self.fps)


if __name__ == "__main__":
    game = Game()
    game.play()
