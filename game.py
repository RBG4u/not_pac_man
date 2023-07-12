import random
from typing import List, Tuple, Dict, Any

import pygame
from pygame.sprite import Group, spritecollide

from game_object import GameObject
from text import Text

from genetic_objects import find_objects
from a_star import manhattan_distance, ai_move


class Player(GameObject):
    sprite_filename = "player"

class Enemy(GameObject):
    sprite_filename = "slime_orig"

class GigaEnemy(GameObject):
    sprite_filename = "slime_giga"

class Wall(GameObject):
    sprite_filename = "wall"

class Chest(GameObject):
    sprite_filename = "chest"


def calculate_walls_coordinates(screen_width: int, screen_height: int, wall_block_width: int, 
                                wall_block_height: int, in_field_walls: List[List[int]]) -> List[Tuple[int, int] | List[int]]:
    
    horizontal_wall_blocks_amount = screen_width // wall_block_width
    vertical_wall_blocks_amount = screen_height // wall_block_height - 2

    walls_coordinates = []
    for block_num in range(horizontal_wall_blocks_amount):
        walls_coordinates.extend([
            (block_num * wall_block_width, 0),
            (block_num * wall_block_width, screen_height - wall_block_height),
        ])
    for block_num in range(1, vertical_wall_blocks_amount + 1):
        walls_coordinates.extend([
            (0, block_num * wall_block_height),
            (screen_width - wall_block_width, block_num * wall_block_height),
        ])

    walls_coordinates.extend(in_field_walls)

    return walls_coordinates


def compose_context(screen: pygame.surface.Surface, objects: List[List[int]]) -> Dict[str, Any]:
    walls_coordinates = calculate_walls_coordinates(screen.get_width(), screen.get_height(), Wall.width, Wall.height, objects[:-5])
    return {
        "player": Player(*objects[-1]),
        "walls": Group(*[Wall(x, y) for (x, y) in walls_coordinates]),
        "enemy": Enemy(*objects[-2]),
        "giga_enemy": GigaEnemy(*objects[-3]),
        "score": 0,
        "chest": Chest(*objects[-4])
    }


def draw_whole_screen(screen: pygame.surface.Surface, context: Dict[str, Any]) -> None:
    screen.fill("black")
    context["player"].draw(screen)
    context["walls"].draw(screen)
    context["chest"].draw(screen)
    context["enemy"].draw(screen)
    context["giga_enemy"].draw(screen)
    Text(str(context["score"]), (15, 15)).draw(screen)


def move_player(player: Player, walls: List[List[int]], player_speed: int) -> None:
    old_player_topleft = player.rect.topleft
    keys = pygame.key.get_pressed()
    if keys[pygame.K_w]:
        player.rect = player.rect.move(0, -1 * player_speed)
    if keys[pygame.K_s]:
        player.rect = player.rect.move(0, player_speed)
    if keys[pygame.K_a]:
        player.rect = player.rect.move(-1 * player_speed, 0)
    if keys[pygame.K_d]:
        player.rect = player.rect.move(player_speed, 0)
    
    if spritecollide(player, walls, dokill=False):
        player.rect.topleft = old_player_topleft


def move_enemy(enemy: Enemy | GigaEnemy, walls_group: Group, 
               vector: Tuple[int, int], enemy_speed: int, player: Player, 
               walls_coord: List[List[int]], move_coord: List) -> Tuple[Tuple[int, int], List, Enemy | GigaEnemy]:
    
    old_enemy_topleft = enemy.rect.topleft
    distance = manhattan_distance(enemy.rect.topleft, player.rect.topleft)

    if distance < 600 and move_coord == []:
        move_coord = ai_move(walls_coord, player, enemy)
    elif move_coord != []:
        if move_coord[0] * 40 > enemy.rect.topleft[0]:
            enemy.rect = enemy.rect.move(1 * enemy_speed, 0)
        if move_coord[0] * 40 < enemy.rect.topleft[0]:
            enemy.rect = enemy.rect.move(-1 * enemy_speed,0)
        if move_coord[1] * 40 > enemy.rect.topleft[1]:
            enemy.rect = enemy.rect.move(0, 1 * enemy_speed)
        if move_coord[1] * 40 < enemy.rect.topleft[1]:
            enemy.rect = enemy.rect.move(0, -1 * enemy_speed)
        if move_coord[0] * 40 == enemy.rect.topleft[0] and move_coord[1] * 40 == enemy.rect.topleft[1]:
            move_coord = []
    else:
        enemy.rect = enemy.rect.move(vector[0] * enemy_speed, vector[1] * enemy_speed)
            

    if spritecollide(enemy, walls_group, dokill=False):
        enemy.rect.topleft = old_enemy_topleft
        vector = (random.choice([-1, 1]), random.choice([-1, 1]))

    return vector, move_coord, enemy


def main() -> None:
    pygame.init()
    screen = pygame.display.set_mode((1080, 1080))
    clock = pygame.time.Clock()
    running = True
    player_speed = 5
    enemy_speed = 4
    coins = 0
    next_level = 0
    vector_enemy = [(1, 0), (-1, 0)]
    move_coords = [[], []]

    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

        if coins == next_level:
            objects = find_objects()
            context = compose_context(screen, objects)
            next_level += 2
            context["score"] = coins
            coins = 0
            move_coords = [[], []]

        draw_whole_screen(screen, context)
        pygame.display.flip()

        move_player(context["player"], context["walls"], player_speed)

        vector_enemy[0], move_coords[0], context["enemy"] = move_enemy(context["enemy"], context["walls"], 
                                                                       vector_enemy[0], enemy_speed, 
                                                                       context["player"], objects[:-3], move_coords[0])
        vector_enemy[1], move_coords[1], context["giga_enemy"] = move_enemy(context["giga_enemy"], context["walls"], 
                                                                            vector_enemy[1], enemy_speed, 
                                                                            context["player"], objects[:-3], move_coords[1])

        if context["player"].is_collided_with(context["chest"]):
            context["score"] += 1
            coins = context["score"]
            context["chest"].rect.topleft = objects[-5]

        if context["player"].is_collided_with(context["enemy"]) or context["player"].is_collided_with(context["giga_enemy"]):
            break

        clock.tick(60) / 1000

    pygame.quit()


if __name__ == "__main__":
    main()
    