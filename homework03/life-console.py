import curses
import time
from life import GameOfLife
from ui import UI


class Console(UI):

    def __init__(self, life: GameOfLife) -> None:
        super().__init__(life)
        
    def draw_borders(self, screen) -> None:
        """ Отобразить рамку. """
        screen.border()
        #for x in range(1, self.life.cols+1):
        #    screen.addstr(x, 0, "|")
        #    screen.addstr(x, self.life.rows+1, "|") 
        #for y in range(1, self.life.rows+1):
        #    screen.addstr(0, y, "-")
        #    screen.addstr(self.life.cols+1, y, "-")
        #screen.addstr(0,0, "+")
        #screen.addstr(0, self.life.cols+1, "+")
        #screen.addstr(self.life.rows+1, 0, "+")
        #screen.addstr(self.life.rows+1, self.life.cols+1, "+")   

    def draw_grid(self, screen) -> None:
        """ Отобразить состояние клеток. """
        for i in range(1, len(self.life.curr_generation)-1):
            for j in range(1, len(self.life.curr_generation[i])-1):
                if self.life.curr_generation[i][j]:
                    screen.addstr(i, j, "*")
                else:
                    screen.addstr(i, j, " ")

    def run(self) -> None:
        screen = curses.initscr().derwin(len(self.life.curr_generation), len(self.life.curr_generation[0]), 0, 0)
        # PUT YOUR CODE HERE
        while self.life.is_changing and not self.life.is_max_generations_exceeded:
            self.draw_borders(screen)
            self.draw_grid(screen)
            screen.refresh()
            self.life.step()
            time.sleep(1)
        curses.endwin()

if __name__ == "__main__":
    game = GameOfLife((20, 20))
    cons = Console(game)
    cons.run()