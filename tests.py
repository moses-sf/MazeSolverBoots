import unittest

from utlities.cell import CellWall
from utlities.maze import Maze
from utlities.point import Point


class Tests(unittest.TestCase):
    def test_maze_create_cells(self):
        num_cols = 12
        num_rows = 10
        m1 = Maze(Point(0, 0), 10, 10, num_rows, num_cols)
        self.assertEqual(
            len(m1.get_cells),
            num_rows,
        )
        self.assertEqual(
            len(m1.get_cells[0]),
            num_cols,
        )

    def test_maze_break_entrance_and_exit(self):
        num_cols = 12
        num_rows = 10
        m1 = Maze(Point(0, 0), 10, 10, num_rows, num_cols)
        self.assertFalse(m1.get_cells[0][0].get_walls()[CellWall.TOP])
        self.assertTrue(m1.get_cells[0][0].get_walls()[CellWall.LEFT])
        self.assertTrue(m1.get_cells[0][0].get_walls()[CellWall.RIGHT])
        self.assertTrue(m1.get_cells[0][0].get_walls()[CellWall.BOTTOM])
        self.assertTrue(m1.get_cells[num_rows - 1][num_cols - 1].get_walls()[CellWall.TOP])
        self.assertTrue(m1.get_cells[num_rows - 1][num_cols - 1].get_walls()[CellWall.LEFT])
        self.assertTrue(m1.get_cells[num_rows - 1][num_cols - 1].get_walls()[CellWall.RIGHT])
        self.assertFalse(m1.get_cells[num_rows - 1][num_cols - 1].get_walls()[CellWall.BOTTOM])

    def test_maze_break_reset(self):
        num_cols = 12
        num_rows = 10
        m1 = Maze(Point(0, 0), 10, 10, num_rows, num_cols)
        m1.break_walls_r(0, 0)
        m1.reset_visited()
        self.assertEqual(
            len(m1.get_visited_cells()),
            0,
        )


if __name__ == "__main__":
    unittest.main()
