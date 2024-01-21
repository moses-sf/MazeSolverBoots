from tkinter import Tk, BOTH, Canvas

from utlities.line import Line


class Window:
    def __init__(self, width: int, height: int):
        self.__root: Tk = Tk()
        self.__title: str = "Maze Solver"
        self.__canvas: Canvas = Canvas(self.__root, width=width, height=height, background="white")
        self.__canvas.pack()
        self.__running: bool = False
        self.__root.protocol("WM_DELETE_WINDOW", self.close)

    def draw_line(self, line: Line, fill_colour: str = "black"):
        line.draw(self.__canvas, fill_colour)

    def redraw(self):
        self.__root.update_idletasks()
        self.__root.update()

    def wait_for_close(self):
        self.__running = True
        while self.__running:
            self.redraw()

    def close(self):
        self.__running = False
