from tkinter import *
import time
import puzzle1
from random import *
class Puzzle_visualization():
    def __init__(self):

        self.a = 0
        self.b = 0

        self.boards = puzzle1.get_path_from_user()
        self.root = Tk()
        self.w = Canvas(self.root, width=1000, height=1000)
        self.w.pack()
        self.rec()
        self.root.mainloop()

    def rec(self):
        a, b, c, d, = 0, 0, 0, 0
        total = len(self.boards)
        for i in range(total):
            delay = 1000 * (i+1)
            b += 100
            d += 100
            self.root.after(delay, self.draw, self.boards[i])


    def draw(self, board):

        x1 = 0
        y1 = 0
        x2 = 100
        y2 = 100
        c = 1
        self.a+=1
        for k, v in board.items() :
            self.w.create_rectangle(0, 400, 100, 500,fill = 'cyan')
            self.w.create_text((50), (450), text = self.a)
            self.w.create_rectangle(x1, y1, x2, y2,fill = 'cyan')
            self.w.create_text(((x1+x2)//2, (y1+y2)//2), text = v)
            x1+=100
            x2 += 100
            if c%3 == 0:
                y1 += 100
                y2 += 100
                x1 = 0
                x2 = 100
            c+=1

visualize=Puzzle_visualization()
