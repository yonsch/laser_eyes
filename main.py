import Tkinter as tk
from tkFileDialog import *
from PIL import Image, ImageTk

from a import lens_flare
from cursor import Cursor

root = tk.Tk()

c, img, sprite = None, None, None
x, y = 0, 0


def save():
    global img
    fn = asksaveasfilename()
    if fn == '' or fn == (): return
    img.save(fn)


def open_image():
    global c, img, sprite, x, y, lazerbtn, savebtn
    fn = askopenfilename()
    if fn == '' or fn == (): return
    img = Image.open(fn)
    w, h = img.size
    if c is not None: c.destroy()
    c = tk.Canvas(root, width=w, height=h)
    c.pack()
    c.handle = ImageTk.PhotoImage(img)
    sprite = c.create_image(w / 2, h / 2, image=c.handle)
    Cursor.indices = [0, 1, 2, 3, 4]
    lazerbtn.config(state=tk.ACTIVE)
    savebtn.config(state=tk.DISABLED)


def lens(cursor):
    global c, img, sprite, lazerbtn, createbtn, removebtn, savebtn
    c.delete(sprite)
    lens_flare(img, cursor.x, cursor.y, cursor.get_angle())
    c.handle = ImageTk.PhotoImage(img)
    sprite = c.create_image(img.size[0] / 2, img.size[1] / 2, image=c.handle)
    c.lower(sprite)
    lazerbtn.config(state=tk.ACTIVE)
    createbtn.config(state=tk.DISABLED)
    removebtn.config(state=tk.DISABLED)
    savebtn.config(state=tk.ACTIVE)


def create_cursor():
    global c, lazerbtn
    Cursor(c, lens)
    if not Cursor.can_create(): lazerbtn.config(state=tk.DISABLED)


def on_select(cursor):
    global createbtn, removebtn
    if cursor is None: return

    def gen():
        lens(Cursor.selected)
        Cursor.selected.destroy()
    createbtn.config(state=tk.ACTIVE, command=gen)
    def rem():
        Cursor.selected.destroy()
        createbtn.config(state=tk.DISABLED)
        removebtn.config(state=tk.DISABLED)
    removebtn.config(state=tk.ACTIVE, command=rem)
Cursor.set_on_select(on_select)

top, mid, bottom = tk.Frame(root), tk.Frame(root), tk.Frame(root)
top.pack(fill=tk.X); mid.pack(fill=tk.X); bottom.pack(fill=tk.X)
tk.Button(top, text='open', command=open_image).pack(side=tk.LEFT)
savebtn = tk.Button(top, text='save', command=save, state=tk.DISABLED)
savebtn.pack(side=tk.LEFT)
lazerbtn = tk.Button(mid, text='add', command=create_cursor, state=tk.DISABLED)
lazerbtn.pack(side=tk.LEFT)
createbtn = tk.Button(mid, text='generate', state=tk.DISABLED)
createbtn.pack(side=tk.LEFT)
removebtn = tk.Button(mid, text='remove', state=tk.DISABLED)
removebtn.pack(side=tk.LEFT)

root.mainloop()
