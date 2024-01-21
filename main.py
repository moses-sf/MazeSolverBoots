from utlities.maze import Maze
from utlities.point import Point
from utlities.window import Window


def main():
    win = Window(800, 800)
    maze = Maze(Point(20, 20), 25, 25, 16, 16, win)
    maze.break_walls_r(0, 0)
    maze.animate()
    maze.reset_visited()
    maze.solve_r(0, 0)
    win.wait_for_close()


if __name__ == "__main__":
    main()
