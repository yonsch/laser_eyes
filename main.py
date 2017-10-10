import Tkinter as tk
from tkFileDialog import *
from PIL import Image, ImageTk

from a import lens_flare
from cursor import Cursor

root = tk.Tk()

c, img, sprite = None, None, None
x, y = 0, 0


def poo():
    global c, img, sprite, x, y, lazerbtn
    fn = askopenfilename()
    if fn == '': return
    img = Image.open(fn)
    w, h = img.size
    if c is not None: c.destroy()
    c = tk.Canvas(root, width=w, height=h)
    c.pack()
    c.handle = ImageTk.PhotoImage(img)
    sprite = c.create_image(w / 2, h / 2, image=c.handle)
    Cursor.indices = [0, 1, 2, 3, 4]
    lazerbtn.config(state=tk.ACTIVE)


def lens(cursor):
    global c, img, sprite, lazerbtn, createbtn
    c.delete(sprite)
    lens_flare(img, cursor.x, cursor.y, cursor.get_angle())
    c.handle = ImageTk.PhotoImage(img)
    sprite = c.create_image(img.size[0] / 2, img.size[1] / 2, image=c.handle)
    c.lower(sprite)
    lazerbtn.config(state=tk.ACTIVE)
    createbtn.config(state=tk.DISABLED)


def create_cursor():
    global c, lazerbtn
    Cursor(c, lens)
    if not Cursor.can_create(): lazerbtn.config(state=tk.DISABLED)


def on_select(cursor):
    global createbtn
    if cursor is None: return

    def gen():
        lens(Cursor.selected)
        Cursor.selected.destroy()
    createbtn.config(state=tk.ACTIVE, command=gen)
Cursor.set_on_select(on_select)

tk.Button(root, text='open', command=poo).pack()
lazerbtn = tk.Button(root, text='add', command=create_cursor, state=tk.DISABLED)
lazerbtn.pack()
createbtn = tk.Button(root, text='generate', state=tk.DISABLED)
createbtn.pack()

root.mainloop()
