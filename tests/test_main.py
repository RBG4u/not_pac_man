import pytest
from pac_man.main import calc_perimeter_walls, compose_context, is_captured_by_enemy

from pac_man.game_objects import Enemy, GigaEnemy, Player


def test__calc_perimeter_walls():
    screen_width = 50
    screen_height = 50
    wall_block_width = 10
    wall_block_height = 10

    expected = [(0, 0), (0, 40), (10, 0), (10, 40), (20, 0), (20, 40), (30, 0),
                (30, 40), (40, 0), (40, 40), (0, 10), (40, 10), (0, 20), (40, 20), (0, 30), (40, 30)]

    assert calc_perimeter_walls(screen_width, screen_height, wall_block_width, wall_block_height) == expected


def test__compose_context(screen, coord):
    result = compose_context(screen, in_field_walls_coords=[(40, 90)], player_coord=coord,
                             enemy_coord=coord, g_enemy_coord=coord, chest_coord=coord)

    assert result.player.rect.topleft == coord
    assert result.enemy.rect.topleft == coord
    assert result.giga_enemy.rect.topleft == coord
    assert result.chest.rect.topleft == coord


def test__is_collided_with_chest():
    pass


@pytest.mark.parametrize(
    'player_rect, enemy_rect, giga_enemy_rect, expected_result',
    [
        ((100, 100), (0, 0), (50, 50), False),
        ((5, 5), (0, 0), (50, 50), True),
        ((25, 25), (0, 0), (20, 20), True)
    ],
    ids=[
        'Player is not captured by enemies',
        'Player is captured by enemy',
        'Player is captured by giga enemy'
        ]
)
def test__is_captured_by_enemy(player_rect, enemy_rect, giga_enemy_rect, expected_result):
    player = Player(*player_rect)
    enemy = Enemy(*enemy_rect)
    giga_enemy = GigaEnemy(*giga_enemy_rect)

    result = is_captured_by_enemy(player, enemy, giga_enemy)

    assert result == expected_result
