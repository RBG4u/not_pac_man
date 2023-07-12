import pytest
from game import calculate_walls_coordinates, compose_context

import pygame


def test_calculate_walls_coordinates():
    screen_width = 100 
    screen_height = 100
    wall_block_width = 10 
    wall_block_height = 10
    in_field_walls = [[10, 20], [10, 30]]

    expected = [(0, 0), (0, 90), (10, 0), (10, 90), (20, 0), (20, 90), (30, 0), (30, 90), (40, 0), (40, 90), 
                (50, 0), (50, 90), (60, 0), (60, 90), (70, 0), (70, 90), (80, 0), (80, 90), (90, 0), (90, 90), 
                (0, 10), (90, 10), (0, 20), (90, 20), (0, 30), (90, 30), (0, 40), (90, 40), (0, 50), (90, 50), 
                (0, 60), (90, 60), (0, 70), (90, 70), (0, 80), (90, 80), [10, 20], [10, 30]]

    assert calculate_walls_coordinates(screen_width, screen_height, wall_block_width, wall_block_height, in_field_walls) == expected


def test_compose_context():
    screen = pygame.display.set_mode((1080, 1080))
    objects = [[10, 20], [10, 30], [10, 40], [10, 50], [10, 60], [10, 70]]

    result = compose_context(screen, objects)

    assert result['player'].rect.topleft == (10, 70)
    assert result['enemy'].rect.topleft == (10, 60)
    assert result['giga_enemy'].rect.topleft == (10, 50)
    assert result['chest'].rect.topleft == (10, 40)
