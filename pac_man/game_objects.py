import os
from dataclasses import dataclass
import pygame

from pygame import Surface
from pygame.image import load
from pygame.sprite import Sprite, Group, spritecollide
from pygame.transform import scale
from text import Text


class GameObject(Sprite):
    sprite_filename: str | None = None
    sprite_extension: str = "png"
    width: int = 40
    height: int = 40
    color_key: tuple[int, int, int] = (245, 245, 245)

    def __init__(self, topleft_x: int, topleft_y: int):
        super().__init__()
        sprite_image_full_path = os.path.join("resources", f"{self.sprite_filename}.{self.sprite_extension}")
        self.image = scale(load(sprite_image_full_path), (self.width, self.height))
        self.image.set_colorkey(self.color_key)
        self.rect = self.image.get_rect()
        self.rect.topleft = topleft_x, topleft_y

    def draw(self, surface: Surface) -> None:
        surface.blit(self.image, (self.rect.x, self.rect.y))

    def is_collided_with(self, another_object: "GameObject") -> bool:
        return self.rect.colliderect(another_object.rect)


class Player(GameObject):
    sprite_filename = "player"
    speed = 5
    visible = True

    def move(self, walls: Group) -> None:
        old_player_topleft = self.rect.topleft
        keys = pygame.key.get_pressed()
        if keys[pygame.K_w]:
            self.rect = self.rect.move(0, -1 * self.speed)
        if keys[pygame.K_s]:
            self.rect = self.rect.move(0, self.speed)
        if keys[pygame.K_a]:
            self.rect = self.rect.move(-1 * self.speed, 0)
        if keys[pygame.K_d]:
            self.rect = self.rect.move(self.speed, 0)

        if spritecollide(self, walls, dokill=False):
            self.rect.topleft = old_player_topleft


class Enemy(GameObject):
    sprite_filename = "slime_orig"
    speed = 2.5
    vector = (-1, 0)
    move_coord = []
    visible = True

    def move(self) -> None:
        if self.move_coord[0] * 40 > self.rect.topleft[0]:
            self.rect = self.rect.move(1 * self.speed, 0)
        if self.move_coord[0] * 40 < self.rect.topleft[0]:
            self.rect = self.rect.move(-1 * self.speed, 0)
        if self.move_coord[1] * 40 > self.rect.topleft[1]:
            self.rect = self.rect.move(0, 1 * self.speed)
        if self.move_coord[1] * 40 < self.rect.topleft[1]:
            self.rect = self.rect.move(0, -1 * self.speed)
        if self.move_coord[0] * 40 == self.rect.topleft[0] and self.move_coord[1] * 40 == self.rect.topleft[1]:
            self.move_coord = []


class GigaEnemy(GameObject):
    sprite_filename = "slime_giga"
    speed = 4
    vector = (1, 0)
    move_coord = []
    visible = True

    def move(self) -> None:
        if self.move_coord[0] * 40 > self.rect.topleft[0]:
            self.rect = self.rect.move(1 * self.speed, 0)
        if self.move_coord[0] * 40 < self.rect.topleft[0]:
            self.rect = self.rect.move(-1 * self.speed, 0)
        if self.move_coord[1] * 40 > self.rect.topleft[1]:
            self.rect = self.rect.move(0, 1 * self.speed)
        if self.move_coord[1] * 40 < self.rect.topleft[1]:
            self.rect = self.rect.move(0, -1 * self.speed)
        if self.move_coord[0] * 40 == self.rect.topleft[0] and self.move_coord[1] * 40 == self.rect.topleft[1]:
            self.move_coord = []


class Wall(GameObject):
    sprite_filename = "wall"


class Chest(GameObject):
    sprite_filename = "chest"


class End(GameObject):
    sprite_filename = "chest"


class New(GameObject):
    sprite_filename = "chest"


@dataclass
class Context:
    player: Player
    walls: Group
    enemy: Enemy
    giga_enemy: GigaEnemy
    score: int
    chest: Chest
    game_over: bool
    end: End
    new: New
    attributes_to_draw: list[str]


class Game:
    def __init__(self) -> None:
        pygame.init()

    def draw_whole_screen(self,
                          screen: pygame.surface.Surface,
                          context: Context,
                          ) -> None:
        screen.fill("black")
        context.walls.draw(screen)
        for attribute_name in context.attributes_to_draw:
            attribute_value = getattr(context, attribute_name)
            attribute_value.draw(screen)
        Text(str(context.score), (15, 15)).draw(screen)
        if context.game_over:
            Text(str('GAME OVER!'), (355, 300), 85).draw(screen)
            Text(str('RESTART?'), (425, 370), 65).draw(screen)
            Text(str('YES'), (990, 960), 40).draw(screen)
            Text(str('NO'), (40, 960), 40).draw(screen)
        pygame.display.flip()

    def quit(self) -> None:
        pygame.quit()
