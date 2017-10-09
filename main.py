import Tkinter as tk
from tkFileDialog import *
from PIL import Image, ImageTk

from a import lens_flare
from cursor import Cursor

root = tk.Tk()

c, img, sprite = None, None, None
x, y = 0, 0
def poo():
    global c, img, sprite, x, y
    #fn = askopenfilename()
    fn = '/Users/michael/Desktop/bear.jpg'
    if fn == '': return
    img = Image.open(fn)
    w, h = img.size
    if c is not None: c.destroy()
    c = tk.Canvas(root, width=w, height=h)
    c.pack()
    c.handle = ImageTk.PhotoImage(img)
    sprite = c.create_image(w / 2, h / 2, image=c.handle)
    #c.bind('<Button-1>', lambda e: lens(e.x, e.y))

def lens(x=0, y=0, a=0):
    global c, img, sprite
    c.delete(sprite)
    lens_flare(img, x, y, a)
    c.handle = ImageTk.PhotoImage(img)
    sprite = c.create_image(img.size[0] / 2, img.size[1] / 2, image=c.handle)

def create_cursor():
    global c
    #ring = c.create_

poo()
cr = Cursor(c)
tk.Button(root, text='open', command=poo).pack()

root.bind('<Double-Button-1>', lambda e: lens(cr.x, cr.y, cr.get_angle()))
root.mainloop()
