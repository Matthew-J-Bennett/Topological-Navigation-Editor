import tkinter as tk
from tkinter import PhotoImage


class Element:
    def __init__(self, element, x, y, anchor):
        self.element = element
        self.x = x
        self.y = y
        self.anchor = anchor
        self.element.place(x=x, y=y, anchor=anchor)


class Frame(Element):
    def __init__(self, master, bg='#222831', height=800, width=1250, x=0, y=0, bd=0, relief=tk.FLAT, anchor=None):
        self.element = tk.Frame(master=master, height=height, width=width, bg=bg, bd=bd, relief=relief)
        self.element.pack()
        super().__init__(self.element, x=x, y=y, anchor=anchor)


class Button(Element):
    def __init__(self, master, text, x, y, sequence='<Button-1>', width=10, height=2, func=None, font=None,
                 bg='#00ADB5',
                 bd=4,
                 relief='raised',
                 anchor=None, animation=True):
        self.animation = animation
        self.master = master
        self.element = tk.Label(master=master, text=text, font=font, bg=bg, bd=bd, relief=relief, width=width,
                                height=height)
        self.element.bind(sequence=sequence, func=lambda x: self.clicked(execute=func))
        super().__init__(self.element, x=x, y=y, anchor=anchor)

    def clicked(self, execute, *args):
        if self.animation:
            self.element.config(relief='sunken')
            self.element.after(100, lambda: self.element.config(relief='raised'))
            self.master.after(100, lambda: execute())
        else:
            execute()


class Label(Element):
    def __init__(self, master, text, x, y, width=None, height=None, bg="#222831", bd=0, relief=tk.FLAT, font=None,
                 anchor=None, image=None,
                 fg='Black'):
        self.element = tk.Label(master=master, bg=bg, text=text, bd=bd, relief=relief, font=font, width=width,
                                height=height,
                                image=image,
                                fg=fg)
        super().__init__(self.element, x=x, y=y, anchor=anchor)


class Photo(Element):
    def __init__(self, master, x, y, imgpath, width=None, height=None, bg="#222831", bd=0, relief=tk.FLAT,
                 anchor=None):
        self.image = PhotoImage(file=imgpath)
        self.element = tk.Label(master=master, bg=bg, bd=bd, relief=relief, width=width,
                                height=height,
                                image=self.image)
        super().__init__(self.element, x=x, y=y, anchor=anchor)
