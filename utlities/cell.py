from enum import Enum
from typing import Self, List

from multimethod import multimethod

from utlities.line import Line
from utlities.point import Point
from utlities.window import Window


class CellWall(Enum):
    LEFT = "left"
    RIGHT = "right"
    TOP = "top"
    BOTTOM = "bottom"


class Cell:
    cell_wall_opposite = {
        CellWall.LEFT: CellWall.RIGHT,
        CellWall.RIGHT: CellWall.LEFT,
        CellWall.TOP: CellWall.BOTTOM,
        CellWall.BOTTOM: CellWall.TOP
    }

    def __init__(self, point_1: Point, point_2: Point, window: Window | None = None):
        self.has_left_wall: bool = True
        self.has_right_wall: bool = True
        self.has_top_wall: bool = True
        self.has_bottom_wall: bool = True
        self.top_left = point_1
        self.bottom_right = point_2
        self._window: Window | None = window
        self.__visited = False

    def visit(self) -> None:
        self.__visited = True

    def get_paths(self, i, j, rows, columns) -> List[CellWall]:
        paths = []
        for wall in self.get_walls():
            if not self.get_walls()[wall]:
                if not (wall == CellWall.LEFT and j == 0) and not (wall == CellWall.RIGHT and j == columns - 1) \
                        and not (wall == CellWall.TOP and i == 0) and not (wall == CellWall.BOTTOM and i == rows - 1):
                    paths.append(wall)
        return paths

    @property
    def is_visited(self) -> bool:
        return self.__visited

    @property
    def centre(self) -> Point:
        return Point((self.top_left.x + self.bottom_right.x) / 2, (self.top_left.y + self.bottom_right.y) / 2)

    def line_to(self, to_cell: Self) -> Line:
        return Line(self.centre, to_cell.centre)

    def draw_move(self, to_cell: Self, undo=False) -> None:
        self._window.draw_line(self.line_to(to_cell), fill_colour="red" if undo else "gray")

    def get_walls(self) -> dict[CellWall, bool]:
        return {
            CellWall.LEFT: self.has_left_wall,
            CellWall.RIGHT: self.has_right_wall,
            CellWall.TOP: self.has_top_wall,
            CellWall.BOTTOM: self.has_bottom_wall
        }

    @multimethod
    def toggle_wall(self, wall: CellWall) -> None:
        if wall == CellWall.LEFT:
            self.has_left_wall = not self.has_left_wall
        elif wall == CellWall.RIGHT:
            self.has_right_wall = not self.has_right_wall
        elif wall == CellWall.TOP:
            self.has_top_wall = not self.has_top_wall
        elif wall == CellWall.BOTTOM:
            self.has_bottom_wall = not self.has_bottom_wall

    @multimethod
    def toggle_wall(self, walls: List[CellWall]) -> None:
        for wall in walls:
            self.toggle_wall(wall)

    def reset_visited(self) -> None:
        self.__visited = False

    def wall_line(self, wall: CellWall) -> Line:
        if wall == CellWall.LEFT:
            return Line(self.top_left, Point(self.top_left.x, self.bottom_right.y))
        elif wall == CellWall.RIGHT:
            return Line(Point(self.bottom_right.x, self.top_left.y), self.bottom_right)
        elif wall == CellWall.TOP:
            return Line(self.top_left, Point(self.bottom_right.x, self.top_left.y))
        elif wall == CellWall.BOTTOM:
            return Line(Point(self.top_left.x, self.bottom_right.y), self.bottom_right)

    def draw(self) -> None:
        if self._window:
            walls = self.get_walls()
            for wall in walls:
                if walls[wall]:
                    self._window.draw_line(self.wall_line(wall))
                else:
                    self._window.draw_line(self.wall_line(wall), fill_colour="white")
