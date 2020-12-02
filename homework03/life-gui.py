import pygame
from pygame.locals import *

from life import GameOfLife
from ui import UI


class GUI(UI):
    """GUI"""

    def __init__(self, life: GameOfLife, cell_size: int = 10, speed: int = 10) -> None:
        super().__init__(life)
        self.cell_size = cell_size
        self.speed = speed
        self.screen = pygame.display.set_mode(
            (self.cell_size * self.life.cols, self.cell_size * self.life.rows)
        )

    def draw_lines(self) -> None:
        """Drawing web"""
        # Copy from previous assignment
        for width in range(0, self.life.rows * self.cell_size, self.cell_size):
            pygame.draw.line(
                self.screen,
                pygame.Color("black"),
                (width, 0),
                (width, self.life.cols * self.cell_size),
            )
        for height in range(0, self.life.cols * self.cell_size, self.cell_size):
            pygame.draw.line(
                self.screen,
                pygame.Color("black"),
                (0, height),
                (self.life.rows * self.cell_size, height),
            )

    def draw_grid(self) -> None:
        """Drawing cells"""
        # Copy from previous assignment
        for i in range(self.life.cols):
            for j in range(self.life.rows):
                if not self.life.curr_generation[i][j]:
                    color = pygame.Color("white")
                else:
                    color = pygame.Color("green")
                pygame.draw.rect(
                    self.screen,
                    color,
                    (
                        j * self.cell_size,
                        i * self.cell_size,
                        self.cell_size,
                        self.cell_size,
                    ),
                )

    def run(self) -> None:
        # Copy from previous assignment
        pygame.init()
        clock = pygame.time.Clock()
        pygame.display.set_caption("Game of Life")
        self.screen.fill(pygame.Color("white"))
        self.life.create_grid(True)
        running = True
        pause = False
        while running and not self.life.is_max_generations_exceeded:
            for event in pygame.event.get():
                if event.type == QUIT:
                    running = False
                elif event.type == KEYUP and event.key == K_SPACE:
                    pause = not pause
                elif event.type == MOUSEBUTTONDOWN and pause:
                    row, col = pygame.mouse.get_pos()
                    self.life.curr_generation[row // self.cell_size][
                        col // self.cell_size
                    ] = (
                        (
                            self.life.curr_generation[row // self.cell_size][
                                col // self.cell_size
                            ]
                            + 1
                        )
                        % 2
                    )
            self.draw_grid()
            self.draw_lines()
            if not pause:
                self.life.step()
            pygame.display.flip()
            clock.tick(self.speed)
        pygame.quit()


if __name__ == "__main__":
    life = GameOfLife((24, 24), max_generations=20)
    gui = GUI(life)
    gui.run()
