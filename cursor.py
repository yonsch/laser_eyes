import Tkinter as tk
import math

from a import lens_flare


class Cursor(object):
    def __init__(self, canvas, x=100, y=100):
        self.x, self.y = x, y
        self.r, self.hr = 15, 4
        self.hx, self.hy = x - self.r + self.hr / 2, y - self.r + self.hr / 2

        self.canvas = canvas
        assert isinstance(self.canvas, tk.Canvas)
        self.center = self.canvas.create_oval(self.x-4, self.y-4, self.x+4, self.y+4, fill='black', tags='ring')
        self.ring = self.canvas.create_oval(self.x-self.r, self.y-self.r, self.x+self.r, self.y+self.r,
                                            width=3, outline='#000000')
        self.handle = self.canvas.create_oval(self.hx-self.hr, self.hy-self.hr, self.hx+self.hr, self.hy+self.hr,
                                              fill='white', tags='handle')

        self.canvas.tag_bind('ring', '<B1-Motion>', self.render)
        self.canvas.tag_bind('handle', '<B1-Motion>', self.rotate)

    def rotate(self, e):
        dx, dy = e.x - self.x, e.y - self.y
        l = self.r / (math.hypot(dx, dy) + 0.000001)
        dx, dy = dx * l + self.x - self.hx, dy * l + self.y - self.hy
        self.canvas.move(self.handle, dx, dy)
        self.hx, self.hy = self.hx + dx, self.hy + dy

    def render(self, e):
        dx, dy = e.x - self.x, e.y - self.y
        self.canvas.move(self.center, dx, dy)
        self.canvas.move(self.ring, dx, dy)
        self.canvas.move(self.handle, dx, dy)
        self.x, self.y = e.x, e.y
        self.hx, self.hy = self.hx + dx, self.hy + dy

    def get_angle(self):
        return math.atan((self.y - self.hy) / (self.x - self.hx + 0.000001))
