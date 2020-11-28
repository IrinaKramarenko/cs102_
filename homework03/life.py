import pathlib
import random
import typing as tp
from copy import deepcopy

import pygame
from pygame.locals import *

Cell = tp.Tuple[int, int]
Cells = tp.List[int]
Grid = tp.List[Cells]


class GameOfLife:
    def __init__(
        self,
        size: tp.Tuple[int, int],
        randomize: bool = True,
        max_generations: tp.Optional[float] = float("inf"),
    ) -> None:
        # Размер клеточного поля
        self.rows, self.cols = size
        # Предыдущее поколение клеток
        self.prev_generation = self.create_grid()
        # Текущее поколение клеток
        self.curr_generation = self.create_grid(randomize=randomize)
        # Максимальное число поколений
        self.max_generations = max_generations
        # Текущее число поколений
        self.generations = 1

    def create_grid(self, randomize: bool = False) -> Grid:
        # Copy from previous assignment
        grid = [[0] * self.cols for i in range(self.rows)]
        if randomize:
            for i in range(self.rows):
                for j in range(self.cols):
                    grid[i][j] = random.randint(0, 1)
        self.curr_generation = grid
        return grid

    def get_neighbours(self, cell: Cell) -> Cells:
        # Copy from previous assignment
        Cells = []
        grid = deepcopy(self.curr_generation)
        for i in range(cell[0]-1, cell[0]+2):
            for j in range(cell[1]-1, cell[1]+2):
                if (i != cell[0] or j != cell[1]) and 0 <= i < len(grid) and 0 <= j < len(grid[i]):
                    Cells.append(grid[i][j])
        return Cells

    def get_next_generation(self) -> Grid:
        # Copy from previous assignment
        grid = deepcopy(self.curr_generation)
        for i in range(self.rows):
            for j in range(self.cols):
                num_neighbours = sum(self.get_neighbours((i, j)))
                if grid[i][j] == 0:
                    if num_neighbours == 3:
                        grid[i][j] = 1
                else:
                    if num_neighbours != 2 or num_neighbours != 3:
                        grid[i][j] = 0
        self.curr_generation = grid

    def step(self) -> None:
        """
        Выполнить один шаг игры.
        """
        if self.is_max_generations_exceeded:
            self.prev_generation = self.curr_generation
            self.curr_generation = self.get_next_generation()
            self.generations += 1

    @property
    def is_max_generations_exceeded(self) -> bool:
        """
        Не превысило ли текущее число поколений максимально допустимое.
        """
        return self.generations <= self.max_generations

    @property
    def is_changing(self) -> bool:
        """
        Изменилось ли состояние клеток с предыдущего шага.
        """
        return self.curr_generation != self.prev_generation

    @staticmethod
    def from_file(filename: pathlib.Path) -> "GameOfLife":
        """
        Прочитать состояние клеток из указанного файла.
        """
        pass

    def save(self, filename: pathlib.Path) -> None:
        """
        Сохранить текущее состояние клеток в указанный файл.
        """
        pass