import datetime
import os
import sys
import tkinter as tk
from tkinter import messagebox
import elements
import frames
import map_function


class MainFrame:
    def __init__(self, master):
        self.master = master
        self.logging = master.logger
        self.window = master.master
        self.frame = elements.Frame(master=self.window)

        # Creates a button to switch between frames
        swap_frame_tmp = elements.Button(master=master.master, x=10, y=750, text="Swap Frame to Launch Frame",
                                         width=30, func=lambda: self.master.frame_swap(old_frame=self.frame,
                                                                                       new_frame=lambda:
                                                                                       frames.LaunchFrame(
                                                                                           master=self.master)))
        # This block imports the pgm file.
        # Sets a variable for the background image
        self.master.img = tk.PhotoImage(file=self.master.files["pgm"])
        # Creates a imgcanvas and sets the size of the imgcanvas - NEED TO USE IMAGE VARIABLE WIDTHS
        self.map_canvas = tk.Canvas(self.window, width=850, height=800, scrollregion=(0, 0,
                                                                                      self.master.pgm["width"],
                                                                                      self.master.pgm["height"]))
        self.map_canvas.pack(expand=tk.YES, side=tk.LEFT, fill=tk.BOTH)
        # Adds the image to the imgcanvas
        self.map_canvas.create_image(0, 0, anchor=tk.NW, image=self.master.img)

        # Creates the Properties Canvas
        properties_canvas = tk.Canvas(self.window, width=450, height=800, scrollregion=(850, 800, 1250, 800))
        properties_canvas.pack(expand=tk.NO, side=tk.RIGHT, fill=tk.BOTH)

        # String variables used to store the values obtained from the dictionary to put in the labels
        name_label_text, set_label_text, map_label_text = tk.StringVar(), tk.StringVar(), tk.StringVar()
        self.master.connection_label_text = tk.StringVar()
        self.master.connection_label_text.set("-Select Node-")
        self.master.verts_label_text = tk.StringVar()
        self.master.verts_label_text.set("-Select Vert-")
        self.master.option_list, self.master.verts_option_list = [""], [""]
        self.master.verts_options = ["Vert 1", "Vert 2", "Vert 3", "Vert 4", "Vert 5", "Vert 6", "Vert 7", "Vert 8"]
        self.master.selected_connection, self.master.selected_vert = "", ""
        self.master.verts_data, self.master.connection_data = [], []

        # Populates text Labels
        tk.Label(properties_canvas, text="Node Properties").grid(row=0)
        tk.Label(properties_canvas, text=" ").grid(row=1)
        tk.Label(properties_canvas, text="Meta").grid(row=2)
        tk.Label(properties_canvas, text="Map:").grid(row=3)
        tk.Label(properties_canvas, text="Node:").grid(row=4)
        tk.Label(properties_canvas, text="Pointset:").grid(row=5)
        tk.Label(properties_canvas, text=" ").grid(row=6)
        tk.Label(properties_canvas, text="Position").grid(row=7)
        tk.Label(properties_canvas, text="X Co-ord: ").grid(row=8)
        tk.Label(properties_canvas, text="Y Co-ord: ").grid(row=9)
        tk.Label(properties_canvas, text="Z Co-ord: ").grid(row=10)
        tk.Label(properties_canvas, text=" ").grid(row=11)
        tk.Label(properties_canvas, text="Orientation").grid(row=12)
        tk.Label(properties_canvas, text="W: ").grid(row=13)
        tk.Label(properties_canvas, text="X: ").grid(row=14)
        tk.Label(properties_canvas, text="Y: ").grid(row=15)
        tk.Label(properties_canvas, text="Z: ").grid(row=16)
        tk.Label(properties_canvas, text=" ").grid(row=17)
        tk.Label(properties_canvas, text="Edges").grid(row=18)
        tk.Label(properties_canvas, text="Node").grid(row=20)
        tk.Label(properties_canvas, text="Map 2D").grid(row=19)
        tk.Label(properties_canvas, text="Action:").grid(row=21)
        tk.Label(properties_canvas, text="Inflation Radius:").grid(row=22)
        tk.Label(properties_canvas, text="Recovery Behaviors Config: ").grid(row=23)
        tk.Label(properties_canvas, text="Top Velocity:").grid(row=24)
        tk.Label(properties_canvas, text=" ").grid(row=25)
        tk.Label(properties_canvas, text="Verts").grid(row=26)

        tk.Label(properties_canvas, text="Vert").grid(row=27)
        tk.Label(properties_canvas, text="X:").grid(row=28)
        tk.Label(properties_canvas, text="Y:").grid(row=29)
        tk.Label(properties_canvas, text=" ").grid(row=43)
        tk.Label(properties_canvas, text="XY Goal Tolerance").grid(row=44)
        tk.Label(properties_canvas, text="Yaw Goal Tolerance").grid(row=45)

        # Uses two labels and three entry's as the name and nodeset are static values whereas the position is changeable
        name = tk.Label(properties_canvas, textvariable=name_label_text).grid(row=3, column=1)
        nodeset = tk.Label(properties_canvas, textvariable=set_label_text).grid(row=4, column=1)
        pointset = tk.Label(properties_canvas, textvariable=name_label_text).grid(row=5, column=1)

        x_entry = tk.Entry(properties_canvas)
        y_entry = tk.Entry(properties_canvas)
        z_entry = tk.Entry(properties_canvas)
        x_entry.grid(row=8, column=1)
        y_entry.grid(row=9, column=1)
        z_entry.grid(row=10, column=1)

        w_orientation = tk.Entry(properties_canvas)
        x_orientation = tk.Entry(properties_canvas)
        y_orientation = tk.Entry(properties_canvas)
        z_orientation = tk.Entry(properties_canvas)
        w_orientation.grid(row=13, column=1)
        x_orientation.grid(row=14, column=1)
        y_orientation.grid(row=15, column=1)
        z_orientation.grid(row=16, column=1)

        map_2d = tk.Label(properties_canvas, textvariable=map_label_text)
        self.master.node_box = tk.OptionMenu(properties_canvas, self.master.connection_label_text,
                                             *self.master.option_list)
        action = tk.Entry(properties_canvas)
        inflation_radius = tk.Entry(properties_canvas)
        recovery_behaviours_config = tk.Entry(properties_canvas)
        top_vel = tk.Entry(properties_canvas)
        map_2d.grid(row=19, column=1)
        self.master.node_box.grid(row=20, column=1)
        action.grid(row=21, column=1)
        inflation_radius.grid(row=22, column=1)
        recovery_behaviours_config.grid(row=23, column=1)
        top_vel.grid(row=24, column=1)

        self.master.verts_box = tk.OptionMenu(properties_canvas, self.master.verts_label_text,
                                              *self.master.verts_option_list)
        self.master.verts_box.grid(row=27, column=1)
        verts_x = tk.Entry(properties_canvas)
        verts_y = tk.Entry(properties_canvas)
        verts_x.grid(row=28, column=1)
        verts_y.grid(row=29, column=1)

        verts_labels = [verts_x, verts_y]

        xy_goal_tolerance = tk.Entry(properties_canvas)
        yaw_goal_tolerance = tk.Entry(properties_canvas)
        xy_goal_tolerance.grid(row=44, column=1)
        yaw_goal_tolerance.grid(row=45, column=1)

        self.master.labels = [name_label_text, set_label_text, x_entry, y_entry, z_entry, w_orientation, x_orientation,
                              y_orientation, z_orientation, map_label_text, self.master.connection_label_text, action,
                              inflation_radius, recovery_behaviours_config, top_vel, verts_labels, xy_goal_tolerance,
                              yaw_goal_tolerance]

        for vert in self.master.verts_options:
            self.master.verts_box['menu'].add_command(label=vert, command=lambda value=vert: [
                self.master.verts_label_text.set(value), map_function.select_vert(self)])

        # Adds an update button at the top
        tk.Button(properties_canvas, text="Update", command=lambda: map_function.update_node(self, 1)).grid(row=0,
                                                                                                            column=1)

        # Creates a horizontal scrollbar
        scroll_x = tk.Scrollbar(self.map_canvas, orient="horizontal", command=self.map_canvas.xview, jump=1)
        # Sets the location of the scroll bar
        scroll_x.pack(side=tk.BOTTOM, fill=tk.X)
        # Defines what the scroll bar will do
        scroll_x.config(command=self.map_canvas.xview)
        self.map_canvas.config(xscrollcommand=scroll_x.set)

        # Creates a vertical scrollbar
        scroll_y = tk.Scrollbar(self.map_canvas, orient="vertical", command=self.map_canvas.yview, jump=1)
        # Sets the location of the scroll bar
        scroll_y.pack(side=tk.RIGHT, fill=tk.Y)
        # Defines what the scroll bar will do
        scroll_y.config(command=self.map_canvas.yview)
        self.map_canvas.config(yscrollcommand=scroll_y.set)
        map_function.plot_canvas(self)

        # Variables used for the associated click mode and storing the users currently selected item(s)
        self.master.clicked_item = 0
        self.master.multi_clicked_item = []
        self.master.clicked_pos = []
        self.master.click_mode = 0

        # Just an absolute shit show
        # The onclick function obtains the position that the user clicked on the canvas and finds the nearest object,
        #   this will either be the canvas (image) or a node (oval). The function also discerns what mode the user is
        #   in either single (0) or multi (1).
        def onclick(event):
            self.map_canvas.delete("clickspot")
            item = self.map_canvas.find_closest(self.map_canvas.canvasx(event.x), self.map_canvas.canvasy(event.y))
            item_type = self.map_canvas.type(item)
            self.logging.info(
                "Clicked Object: " + item_type + " X: " + str(self.map_canvas.canvasx(event.x)) + " Y: " + str(
                    self.map_canvas.canvasy(event.y)))
            self.map_canvas.itemconfig("connection", dash=1, fill='black')
            if self.master.click_mode == 0:
                if item_type == "oval":
                    tags = self.map_canvas.gettags(item)
                    node = tags[1]
                    self.logging.info(str(tags[1]))
                    if self.master.clicked_item != 0:
                        item2 = self.map_canvas.find_withtag(self.master.clicked_item)
                        for x in item2:
                            self.map_canvas.itemconfig(x, fill='blue')
                    if self.master.clicked_item == 0 or self.master.clicked_item != node:
                        self.map_canvas.itemconfig(item, fill='red')
                        self.master.clicked_item = node
                        map_function.display_node_info(self, node)
                    elif self.master.clicked_item == node:
                        self.map_canvas.itemconfig(item, fill='blue')
                        self.master.clicked_item = 0
                    self.master.clicked_pos = []
                elif item_type == "image":
                    x = self.map_canvas.canvasx(event.x)
                    y = self.map_canvas.canvasy(event.y)
                    self.map_canvas.create_line(x + 3, y + 3, x - 3, y - 3, width=1.5, fill="red", tags="clickspot")
                    self.map_canvas.create_line(x + 3, y - 3, x - 3, y + 3, width=1.5, fill="red", tags="clickspot")
                    self.master.clicked_pos = [self.map_canvas.canvasx(event.x), self.map_canvas.canvasy(event.y)]
                    map_function.deselect_node_info(self)
                    self.map_canvas.itemconfig("connection", dash=1, fill='black')
                    if self.master.clicked_item != 0:
                        item2 = self.map_canvas.find_withtag(self.master.clicked_item)
                        for x in item2:
                            self.map_canvas.itemconfig(x, fill='blue')
                        self.master.clicked_item = 0
            else:
                if item_type == "oval":
                    tags = self.map_canvas.gettags(item)
                    node = tags[1]
                    self.logging.info(str(tags[1]))
                    if self.master.multi_clicked_item:
                        num_items = len(self.master.multi_clicked_item)
                        for y in self.master.multi_clicked_item:
                            item2 = self.map_canvas.find_withtag(y)
                            if y != node and num_items < 2:
                                self.map_canvas.itemconfig(item, fill='red')
                                self.master.multi_clicked_item.append(node)
                                break
                            elif y == node:
                                self.map_canvas.itemconfig(item, fill='blue')
                                self.master.multi_clicked_item.remove(node)
                    else:
                        self.map_canvas.itemconfig(item, fill='red')
                        self.master.multi_clicked_item.append(node)
                    self.master.clicked_pos = []
                self.logging.info(self.master.multi_clicked_item)

        def drag_begin(event):
            self.logging.info("drag_begin active")
            item = self.map_canvas.find_closest(self.map_canvas.canvasx(event.x), self.map_canvas.canvasy(event.y))
            item_type = self.map_canvas.type(item)
            tags = self.map_canvas.gettags(item)
            self.master.drag_data["item"] = tags[1]
            if self.master.click_mode == 0 and item_type == "oval":
                self.master.drag_data["x"] = self.map_canvas.canvasx(event.x)
                self.master.drag_data["y"] = self.map_canvas.canvasy(event.y)
                self.logging.info("Drag object: {}, Tag:{}".format(item_type, tags[1]))
                self.logging.info(
                    "Drag start x:{}, y:{}".format(self.master.drag_data["x"], self.master.drag_data["y"]))

        def drag_move(event):
            diff_x = self.map_canvas.canvasx(event.x) - self.master.drag_data["x"]
            diff_y = self.map_canvas.canvasy(event.y) - self.master.drag_data["y"]
            item = self.map_canvas.find_withtag(self.master.drag_data["item"])
            self.logging.info("Object:{},{}".format(self.master.drag_data["item"], item))
            self.map_canvas.move(item, diff_x, diff_y)
            self.master.drag_data["x"] = self.map_canvas.canvasx(event.x)
            self.master.drag_data["y"] = self.map_canvas.canvasy(event.y)

        def drag_end(event):
            self.logging.info("drag_end active")
            map_function.update_node(self, 0)
            self.master.drag_data["x"] = 0
            self.master.drag_data["y"] = 0

        self.master.drag_data = {"x": 0, "y": 0, "item": None}

        # Activates the onclick event when any location on the canvas is clicked
        self.map_canvas.bind('<Button-1>', onclick)
        self.map_canvas.tag_bind("point", '<ButtonPress-3>', drag_begin)
        self.map_canvas.tag_bind("point", '<B3-Motion>', drag_move)
        self.map_canvas.tag_bind("point", '<ButtonRelease-3>', drag_end)

        master.master.bind('<Control-BackSpace>', self.delete_canvas_node_event)
        master.master.bind('<Shift-BackSpace>', self.delete_canvas_node__connection_event)

        master.master.bind('<Control-1>', self.add_canvas_node_event)
        master.master.bind('<Control-3>', self.add_canvas_node__connection_event)
        master.master.bind('<Control-d>', self.deselect_node_event)
        master.master.bind('<Control-D>', self.deselect_node_event)

        master.master.bind('<Enter>', self._bind_to_mousewheel)

        self.master.editmenu.add_command(label="Deselect Node(s)                        CTRL + D", command=lambda:
                                                                    self.deselect_node_event(self.master.clicked_item))

        self.master.editmenu.add_command(label="Add Node                                         CTRL + Mouse 1",
                                         command=lambda: map_function.add_canvas_node(self, self.master.clicked_pos))
        self.master.editmenu.add_command(label="Add Node Connection                   CTRL + Mouse 2",
                                         command=lambda: map_function.add_canvas_connection(self, self.master.multi_clicked_item))
        self.master.editmenu.add_command(label="Delete Node                                     CTRL + Backspace",
                                         command=lambda: map_function.delete_canvas_node(self, self.master.clicked_item))
        self.master.editmenu.add_command(label="Delete Node Connection               SHIFT + Backspace",
                                         command=lambda: map_function.delete_connection(self,
                                                                                        self.master.multi_clicked_item))
        self.master.filemenu.add_command(label="Close Project",
                                         command=lambda: self._save_and_close())

        single_item_button = elements.Button(master=master.master, x=790, y=20, text="Single Mode", width=20,
                                             func=lambda: map_function.change_mode(self, 0))

        multi_item_button = elements.Button(master=master.master, x=790, y=70, text="Multi Mode",
                                            width=20,
                                            func=lambda: map_function.change_mode(self, 1))

        tk.mainloop()

    def _save_and_close(self):
        msg_box = tk.messagebox.askquestion('Exit Application', 'Would you like to save before quitting?',
                                            icon='warning')
        # if conformation is true, save and quit, else just quit
        if msg_box == 'yes':
            self.master.save_filename()
            os.execl(sys.executable, sys.executable, *sys.argv)
        else:
            os.execl(sys.executable, sys.executable, *sys.argv)

    def _on_mousewheel_y_view(self, event):
        self.map_canvas.yview_scroll(int(-1 * (event.delta / 120)), "units")

    def _on_mousewheel_x_view(self, event):
        self.map_canvas.xview_scroll(int(-1 * (event.delta / 120)), "units")

    def _bind_to_mousewheel(self, event):
        self.map_canvas.bind_all("<MouseWheel>", self._on_mousewheel_y_view)
        self.map_canvas.bind_all("<Control-MouseWheel>", self._on_mousewheel_x_view)

    def delete_canvas_node_event(self, event):
        map_function.delete_canvas_node(self, self.master.clicked_item)

    def delete_canvas_node__connection_event(self, event):
        map_function.delete_connection(self, self.master.multi_clicked_item)

    def add_canvas_node__connection_event(self, event):
        map_function.add_canvas_connection(self, self.master.multi_clicked_item)

    def add_canvas_node_event(self, event):
        map_function.add_canvas_node(self, self.master.clicked_pos)

    def deselect_node_event(self, event):
        map_function.deselect_all(self)
