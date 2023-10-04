import random
import pygame
from pygame.sprite import Group, spritecollide

from game_objects import Player, Enemy, GigaEnemy, Wall, Chest, Context, Game, End, New

from genetic_objects import find_objects
from a_star import manhattan_distance, ai_move


def calc_perimeter_walls(screen_width: int,
                         screen_height: int,
                         wall_block_width: int,
                         wall_block_height: int,
                         ) -> list[tuple[int, int]]:
    horizontal_wall_blocks_amount = screen_width // wall_block_width
    vertical_wall_blocks_amount = screen_height // wall_block_height - 2

    walls_coordinates = []
    for block_num in range(horizontal_wall_blocks_amount):
        walls_coordinates.extend([
            (block_num * wall_block_width, 0),
            (block_num * wall_block_width, screen_height - wall_block_height)
        ])
    for block_num in range(1, vertical_wall_blocks_amount + 1):
        walls_coordinates.extend([
            (0, block_num * wall_block_height),
            (screen_width - wall_block_width, block_num * wall_block_height)
        ])

    return walls_coordinates


def compose_context(screen: pygame.surface.Surface,
                    in_field_walls_coords: list[tuple[int, int]],
                    player_coord: tuple[int, int],
                    enemy_coord: tuple[int, int],
                    g_enemy_coord: tuple[int, int],
                    chest_coord: tuple[int, int],
                    ) -> Context:
    walls_coordinates = calc_perimeter_walls(screen.get_width(),
                                             screen.get_height(),
                                             Wall.width,
                                             Wall.height)
    walls_coordinates.extend(in_field_walls_coords)
    return Context(player=Player(*player_coord),
                   walls=Group(*[Wall(x, y) for (x, y) in walls_coordinates]),
                   enemy=Enemy(*enemy_coord),
                   giga_enemy=GigaEnemy(*g_enemy_coord),
                   score=0,
                   chest=Chest(*chest_coord),
                   game_over=False,
                   end=End(topleft_x=40, topleft_y=1000),
                   new=New(topleft_x=1000, topleft_y=1000),
                   attributes_to_draw=['player', 'enemy', 'giga_enemy',
                                       'chest'])


def move_enemy(enemy: Enemy | GigaEnemy, walls_group: Group,
               player: Player, walls_coord: list[tuple[int, int]],
               chest_coord: tuple[int, int]
               ) -> None:
    static_objects = walls_coord + [chest_coord]
    old_enemy_topleft = enemy.rect.topleft

    distance = manhattan_distance(enemy.rect.topleft, player.rect.topleft)

    if distance < 600 and enemy.move_coord == []:
        enemy.move_coord = ai_move(static_objects, player, enemy)
    elif enemy.move_coord != []:
        enemy.move()
    else:
        enemy.rect = enemy.rect.move(enemy.vector[0] * enemy.speed,
                                     enemy.vector[1] * enemy.speed)

    if spritecollide(enemy, walls_group, dokill=False):
        enemy.rect.topleft = old_enemy_topleft
        enemy.vector = (random.choice([-1, 1]), random.choice([-1, 1]))


def is_collided_with_chest(context: Context, coins: int,
                           new_chest: tuple[int, int]) -> int:
    if context.player.is_collided_with(context.chest):
        context.score += 1
        coins = context.score
        context.chest.rect.topleft = new_chest
    return coins


def is_captured_by_enemy(player: Player,
                         enemy: Enemy,
                         giga_enemy: GigaEnemy) -> bool:
    if player.is_collided_with(enemy) or player.is_collided_with(giga_enemy):
        return True
    return False


def end_game(context: Context, next_level: int) -> tuple[bool, int, int]:
    del context.attributes_to_draw[1:5]
    context.attributes_to_draw.extend(['end', 'new'])
    if context.player.is_collided_with(context.new):
        context.game_over = False
        return True, 0, 0
    if context.player.is_collided_with(context.end):
        return False, 0, 0
    return True, context.score, next_level


def main() -> None:
    game = Game()
    screen = pygame.display.set_mode((1080, 1080))
    clock = pygame.time.Clock()
    running = True
    coins = 0
    next_level = 0

    while running:
        if coins == next_level:
            objects = find_objects()
            walls_coords = objects[:-5]
            player_coord = objects[-1]
            enemy_coord = objects[-2]
            g_enemy_coord = objects[-3]
            chest_coord = objects[-4]
            context = compose_context(screen, walls_coords, player_coord,
                                      enemy_coord, g_enemy_coord, chest_coord)
            next_level += 2
            context.score = coins
            coins = 0

        game.draw_whole_screen(screen, context)

        context.player.move(context.walls)
        if context.game_over is False:
            move_enemy(context.enemy,
                       context.walls,
                       context.player,
                       walls_coords,
                       chest_coord)

            move_enemy(context.giga_enemy,
                       context.walls,
                       context.player,
                       walls_coords,
                       chest_coord)

        if context.game_over is False:
            coins = is_collided_with_chest(context,
                                           coins,
                                           new_chest=objects[-5])
            context.game_over = is_captured_by_enemy(context.player,
                                                     context.enemy,
                                                     context.giga_enemy)
        else:
            running, coins, next_level = end_game(context,
                                                  next_level)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

        clock.tick(60) / 1000

    game.quit()


if __name__ == "__main__":
    main()
