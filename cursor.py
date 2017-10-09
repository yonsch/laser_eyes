import Tkinter as tk
import math


class Cursor(object):
    indices = [0, 1, 2, 3, 4]

    def __init__(self, canvas, cmd=None, x=100, y=100):
        if not Cursor.indices:
            print 'cannot create more than 5 lasers'
            return

        self.x, self.y = x, y
        self.r, self.hr = 15, 4
        self.hx, self.hy = x - self.r + self.hr / 2, y - self.r + self.hr / 2
        self.index = Cursor.indices.pop()
        self.id, self.hid = 'ring%i' % self.index, 'handle%i' % self.index

        self.canvas = canvas
        assert isinstance(self.canvas, tk.Canvas)
        self.center = self.canvas.create_oval(self.x-4, self.y-4, self.x+4, self.y+4, fill='black', tags=self.id)
        self.ring = self.canvas.create_oval(self.x-self.r, self.y-self.r, self.x+self.r, self.y+self.r,
                                            width=3, outline='#000000')
        self.handle = self.canvas.create_oval(self.hx-self.hr, self.hy-self.hr, self.hx+self.hr, self.hy+self.hr,
                                              fill='#FFFFFF', tags=self.hid)

        self.canvas.tag_bind(self.id, '<B1-Motion>', self.render)
        self.canvas.tag_bind(self.hid, '<B1-Motion>', self.rotate)

        def c(_):
            if cmd is not None: cmd(self)
            self.destroy()
        self.canvas.tag_bind(self.id, '<Double-Button-1>', c)

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

    def destroy(self):
        self.canvas.delete(self.ring)
        self.canvas.delete(self.center)
        self.canvas.delete(self.handle)
        Cursor.indices.append(self.index)

    @staticmethod
    def can_create(): return len(Cursor.indices) != 0
