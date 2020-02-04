import tkinter as tk


class Element:
    def __init__(self, element, x, y, anchor):
        self.element = element
        self.x = x
        self.y = y
        self.anchor = anchor
        self.element.place(x=x, y=y, anchor=anchor)


class Frame(Element):
    def __init__(self, master, bg='grey24', height=800, width=1250):
        self.element = tk.Frame(master=master, height=height, width=width, bg=bg)
        self.element.pack()
        super()


class Button(Element):
    def __init__(self, master, text, x, y, sequence='<Button-1>', width=10, height=2, func=None, font=None,
                 bg='Gray90',
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
    def __init__(self, master, text, x, y, width=None, bg='white', font=None, anchor=None):
        self.element = tk.Label(master=master, bg=bg, text=text, font=font, width=width)
        super().__init__(self.element, x=x, y=y, anchor=anchor)
