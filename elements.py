import tkinter as tk
from tkinter import PhotoImage
import contants as const


class Element:
    def __init__(self, element, x, y, anchor):
        self.element = element
        self.x = x
        self.y = y
        self.anchor = anchor
        self.element.place(x=x, y=y, anchor=anchor)


# Defines the Frame attributes


class Frame(Element):
    # Uses constants to create the frame
    def __init__(self, master, bg=const.primary_colour, height=800, width=1250, x=0, y=0, bd=0, relief=tk.FLAT,
                 anchor=None):
        self.element = tk.Frame(master=master, height=height, width=width, bg=bg, bd=bd, relief=relief)
        self.element.pack()
        super().__init__(self.element, x=x, y=y, anchor=anchor)


# Defines the Button attributes


class Button(Element):
    def __init__(self, master, text, x, y, sequence='<Button-1>', width=10, height=2, func=None, font=None,
                 bg=const.secondary_colour,
                 bd=4,
                 relief=tk.FLAT,
                 anchor=None, animation=True, toggle=False):
        self.animation = animation
        self.master = master
        # Attempt as toggle display functionality
        self.on = False
        self.toggle = toggle

        self.element = tk.Label(master=master, text=text, font=font, bg=bg, bd=bd, relief=relief, width=width,
                                height=height)
        self.element.bind(sequence=sequence, func=lambda x: self.clicked(execute=func))
        super().__init__(self.element, x=x, y=y, anchor=anchor)

    # Provides instructions for what to do when clicked

    def clicked(self, execute, *args):
        # Currently not working - ignore this
        if self.toggle:
            if self.on:
                pass
            else:
                self.element.config(bd=2, highlightcolor="deep pink")

        if self.animation:
            self.element.config(bg=const.active_colour)
            self.element.after(100, lambda: self.element.config(bg=const.secondary_colour))
            self.master.after(100, lambda: execute())

        else:
            execute()


# Defines the Label attributes


class Label(Element):
    def __init__(self, master, text, x, y, width=None, height=None, bg=const.primary_colour, bd=0, relief=tk.FLAT,
                 font=None,
                 anchor=None, image=None,
                 fg='Black'):
        self.element = tk.Label(master=master, bg=bg, text=text, bd=bd, relief=relief, font=font, width=width,
                                height=height,
                                image=image,
                                fg=fg)
        super().__init__(self.element, x=x, y=y, anchor=anchor)


# Defines the Photo attributes


class Photo(Element):
    def __init__(self, master, x, y, imgpath, width=None, height=None, bg=const.primary_colour, bd=0, relief=tk.FLAT,
                 anchor=None):
        self.image = PhotoImage(file=imgpath)
        self.element = tk.Label(master=master, bg=bg, bd=bd, relief=relief, width=width,
                                height=height,
                                image=self.image)
        super().__init__(self.element, x=x, y=y, anchor=anchor)


class Selector(Element):
    def __init__(self, master, x, y, bg='LightSkyBlue1', font=None, options=[], callback=None, width=10, modifier=1,
                 selector_id=None, locked=False):
        self.used_ids = []
        self.callback = callback
        self.selector_id = selector_id
        self.locked = locked
        self.bg = bg

        self.options_elements = []
        for i in range(len(options)):
            if i == 0:
                self.options_elements.append(
                    Button(master=master, x=x + i * 50 * modifier, y=y, text='{}'.format(options[i]), width=width,
                           animation=False,
                           font=font,
                           func=lambda arg=self.id_gen(): self.clicked(arg), relief='sunken'))
            else:
                self.options_elements.append(
                    Button(master=master, x=x + i * 50 * modifier, y=y, text='{}'.format(options[i]), width=width,
                           animation=False,
                           font=font,
                           func=lambda arg=self.id_gen(): self.clicked(arg)))
        self.selected = 0

        if self.locked:
            self.lock()

    def lock(self):
        self.locked = True
        for i in range(len(self.options_elements)):
            self.options_elements[i].element.config(bg='grey')

    def unlock(self):
        self.locked = False
        for i in range(len(self.options_elements)):
            self.options_elements[i].element.config(bg=self.bg)

    def id_gen(self):
        if len(self.used_ids) == 0:
            self.used_ids.append(0)
            return 0

        else:
            self.used_ids.append(self.used_ids[-1] + 1)
            return self.used_ids[-1]

    def clicked(self, *args):
        if not self.locked:
            if not args[0] == self.selected:
                self.options_elements[args[0]].element.config(relief='sunken')
                self.options_elements[self.selected].element.config(relief='raised')
                self.selected = args[0]
                if self.callback is not None:
                    if self.selector_id is None:
                        self.callback(self.options_elements[args[0]].element.cget('text'))
                    else:
                        self.callback(new_selected=self.options_elements[args[0]].element.cget('text'),
                                      selector_id=self.selector_id)
