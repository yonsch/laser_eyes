import Tkinter as tk
import math


class Cursor(object):
    instances = []
    selected = None
    _on_select = None

    def __init__(self, canvas, cmd=None, x=100, y=100):
        if not Cursor.can_create():
            print 'cannot create more than 5 lasers'
            return

        self.x, self.y = x, y
        self.r, self.hr = 15, 4
        self.hx, self.hy = x - self.r + self.hr / 2, y - self.r + self.hr / 2
        index = len(Cursor.instances)
        self.id, self.hid, self.rid = 'ring%i' % index, 'handle%i' % index, "resize%i" % index
        Cursor.instances.append(self)

        self.canvas = canvas
        assert isinstance(self.canvas, tk.Canvas)
        self.center = self.canvas.create_oval(self.x-4, self.y-4, self.x+4, self.y+4, fill='black', tags=self.id)
        self.ring = self.canvas.create_oval(self.x-self.r, self.y-self.r, self.x+self.r, self.y+self.r,
                                            width=3, outline='#000000')
        self.handle = self.canvas.create_oval(self.hx-self.hr, self.hy-self.hr, self.hx+self.hr, self.hy+self.hr,
                                              fill='#FFFFFF', tags=self.hid)
        self.resizer = self.canvas.create_oval(self.x+self.r+2, self.y+self.r+2, self.x+self.r-2, self.y+self.r-2,
                                              fill='#FFFFFF', tags=self.rid)

        self.canvas.tag_bind(self.id, '<Button-1>', self.select)
        self.canvas.tag_bind(self.id, '<B1-Motion>', self.render)
        self.canvas.tag_bind(self.hid, '<B1-Motion>', self.rotate)
        self.canvas.tag_bind(self.rid, '<B1-Motion>', self.resize)

        def c(_):
            if cmd is not None: cmd(self)
            self.destroy()
        self.canvas.tag_bind(self.id, '<Double-Button-1>', c)
        self.select()

    def resize(self, e):


    def select(self, _=None):
        for c in Cursor.instances:
            self.canvas.itemconfig(c.center, outline='#000000')
        self.canvas.itemconfig(self.center, outline='#FFFFFF')
        Cursor.selected = self
        if Cursor._on_select is not None: Cursor._on_select(self)

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
        Cursor.instances.remove(self)
        if Cursor.selected is self:
            Cursor.selected = None
            if Cursor._on_select is not None: Cursor._on_select(None)

    @staticmethod
    def can_create(): return len(Cursor.instances) < 5

    @staticmethod
    def set_on_select(f): Cursor._on_select = staticmethod(f)
