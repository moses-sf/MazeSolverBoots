import random
from time import sleep

from utlities.cell import Cell, CellWall
from utlities.point import Point
from utlities.window import Window


class Maze:
    def __init__(
            self,
            origin: Point,
            cell_width: int,
            cell_height: int,
            rows: int,
            columns: int,
            window: Window | None = None,
            seed: int | None = None
    ):
        random.seed(seed)
        self.__win: Window | None = window
        self.__origin: int = origin
        self.__cell_width: int = cell_width
        self.__cell_height: int = cell_height
        self.__rows: int = rows
        self.__columns: int = columns
        self.__cells: list[list[Cell]] = self.__create_cells()
        self.path: list[tuple[int, int]] = []
        self.break_entrance_and_exit()
        self.animate()

    @property
    def get_cells(self) -> list[list[Cell]]:
        return self.__cells

    def __create_cells(self) -> list[list[Cell]]:
        cells = []
        for row in range(self.__rows):
            cells.append([])
            for column in range(self.__columns):
                cell = Cell(
                    Point(
                        self.__origin.x + self.__cell_width * column,
                        self.__origin.y + self.__cell_height * row
                    ),
                    Point(
                        self.__origin.x + self.__cell_width * (column + 1),
                        self.__origin.y + self.__cell_height * (row + 1)
                    ),
                    self.__win
                )
                cells[row].append(cell)
        return cells

    def break_walls_r(self, i, j):
        self.__cells[i][j].visit()
        neighbours = self.__get_neighbours(i, j)
        if len(neighbours) == 0 or (i == self.__rows - 1 and j == self.__columns - 1):
            return
        neighbour = random.choice(list(neighbours.keys()))
        self.__cells[i][j].toggle_wall(neighbour)
        if neighbour == CellWall.LEFT:
            self.__cells[i][j - 1].toggle_wall(CellWall.RIGHT)
            self.break_walls_r(i, j - 1)
        elif neighbour == CellWall.RIGHT:
            self.__cells[i][j + 1].toggle_wall(CellWall.LEFT)
            self.break_walls_r(i, j + 1)
        elif neighbour == CellWall.TOP:
            self.__cells[i - 1][j].toggle_wall(CellWall.BOTTOM)
            self.break_walls_r(i - 1, j)
        elif neighbour == CellWall.BOTTOM:
            self.__cells[i + 1][j].toggle_wall(CellWall.TOP)
            self.break_walls_r(i + 1, j)
        if not self.__cells[self.__rows - 1][self.__columns - 1].is_visited:
            random_visited_cell = random.choice(self.get_visited_cells())
            self.break_walls_r(random_visited_cell[0], random_visited_cell[1])

    def get_visited_cells(self) -> list[tuple[int, int]]:
        visited_cells = []
        for i in range(self.__rows):
            for j in range(self.__columns):
                if self.__cells[i][j].is_visited:
                    visited_cells.append((i, j))
        return visited_cells

    def solve_r(self, i, j):
        self.animate()
        if i == self.__rows - 1 and j == self.__columns - 1:
            return
        self.__cells[i][j].visit()
        neighbours = self.__cells[i][j].get_paths(i, j, self.__rows, self.__columns)
        possible_moves = []
        for neighbour in neighbours:
            if neighbour == CellWall.LEFT:
                if not self.__cells[i][j - 1].is_visited:
                    possible_moves.append(CellWall.LEFT)
            elif neighbour == CellWall.RIGHT:
                if not self.__cells[i][j + 1].is_visited:
                    possible_moves.append(CellWall.RIGHT)
            elif neighbour == CellWall.TOP:
                if not self.__cells[i - 1][j].is_visited:
                    possible_moves.append(CellWall.TOP)
            elif neighbour == CellWall.BOTTOM:
                if not self.__cells[i + 1][j].is_visited:
                    possible_moves.append(CellWall.BOTTOM)

        if len(possible_moves) == 0:
            last_move = self.path.pop()
            self.__cells[i][j].draw_move(self.__cells[last_move[0]][last_move[1]], undo=True)
            self.solve_r(last_move[0], last_move[1])
        self.path.append((i, j))
        if possible_moves:
            neighbour = random.choice(possible_moves)
            if neighbour == CellWall.LEFT:
                self.__cells[i][j].draw_move(self.__cells[i][j - 1])
                self.solve_r(i, j - 1)
            elif neighbour == CellWall.RIGHT:
                self.__cells[i][j].draw_move(self.__cells[i][j + 1])
                self.solve_r(i, j + 1)
            elif neighbour == CellWall.TOP:
                self.__cells[i][j].draw_move(self.__cells[i - 1][j])
                self.solve_r(i - 1, j)
            elif neighbour == CellWall.BOTTOM:
                self.__cells[i][j].draw_move(self.__cells[i + 1][j])
                self.solve_r(i + 1, j)

    def __get_neighbours(self, i, j) -> dict[CellWall, Cell]:
        neighbours = {}
        if j > 0 and not self.__cells[i][j - 1].is_visited:
            neighbours[CellWall.LEFT] = self.__cells[i][j - 1]
        if j < self.__columns - 1 and not self.__cells[i][j + 1].is_visited:
            neighbours[CellWall.RIGHT] = self.__cells[i][j + 1]
        if i > 0 and not self.__cells[i - 1][j].is_visited:
            neighbours[CellWall.TOP] = self.__cells[i - 1][j]
        if i < self.__rows - 1 and not self.__cells[i + 1][j].is_visited:
            neighbours[CellWall.BOTTOM] = self.__cells[i + 1][j]
        return neighbours

    def break_entrance_and_exit(self) -> None:
        self.__cells[0][0].toggle_wall(CellWall.TOP)
        self.__cells[0][0].draw()
        self.__cells[self.__rows - 1][self.__columns - 1].toggle_wall(CellWall.BOTTOM)
        self.__cells[self.__rows - 1][self.__columns - 1].draw()

    def animate(self):
        if self.__win:
            for row in self.__cells:
                for cell in row:
                    cell.draw()
            self.__win.redraw()
            # sleep(0.01)

    def reset_visited(self):
        for row in self.__cells:
            for cell in row:
                cell.reset_visited()
