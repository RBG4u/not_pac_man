import pytest
import pygame


@pytest.fixture
def graph():
    return {(1, 1): [[2, 1], [1, 2]], (1, 2): [[1, 1]], (2, 1): [[1, 1]]}


@pytest.fixture
def field():
    return [[1, 1, 1, 1], [1, 0, 0, 1], [1, 0, 1, 1], [1, 1, 1, 1]]


@pytest.fixture
def start():
    return (1, 2)


@pytest.fixture
def goal():
    return (2, 1)


@pytest.fixture
def screen():
    return pygame.Surface((1080, 1080))


@pytest.fixture
def coord():
    return (20, 10)
