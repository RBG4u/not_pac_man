import pytest


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
