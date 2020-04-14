import os
import sys
import tkinter as tk
from tkinter import messagebox

import elements
import frames
import tmap


class MainFrame:
    def __init__(self, master):
        self.master = master
        self.logging = master.logger
        self.window = master.master
        self.frame = elements.Frame(master=self.window)

        # Creates a button to switch between frames
        swap_frame_tmp = elements.Button(master=master.master, x=10, y=750, text="Swap Frame to Launch Frame",
                                         width=30, func=lambda: self.master.frame_swap(old_frame=self.frame,
                                                                                       new_frame=lambda: frames.LaunchFrame(
                                                                                           master=self.master)))
        # This block imports the pgm file.
        # Sets a variable for the background image
        img = tk.PhotoImage(file=self.master.files["pgm"])
        # Creates a imgcanvas and sets the size of the imgcanvas - NEED TO USE IMAGE VARIABLE WIDTHS
        self.map_canvas = tk.Canvas(self.window, width=850, height=800, scrollregion=(0, 0,
                                                                                      self.master.pgm["width"],
                                                                                      self.master.pgm["height"]))
        self.map_canvas.pack(expand=tk.YES, side=tk.LEFT, fill=tk.BOTH)
        # Adds the image to the imgcanvas
        self.map_canvas.create_image(0, 0, anchor=tk.NW, image=img)

        # Creates the Properties Canvas
        properties_canvas = tk.Canvas(self.window, width=450, height=800)
        properties_canvas.pack(expand=tk.NO, side=tk.RIGHT, fill=tk.BOTH)

        # String variables used to store the values obtained from the dictionary to put in the labels
        name_label_text, set_label_text, map_label_text = tk.StringVar(), tk.StringVar(), tk.StringVar()
        self.master.connection_label_text = tk.StringVar()
        self.master.connection_label_text.set("-Select Node-")
        self.master.option_list = [""]
        self.master.selected_connection = ""
        self.master.connection_data = []

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

        grid_spot = 27
        for loop in range(8):
            tk.Label(properties_canvas, text="X:").grid(row=grid_spot)
            tk.Label(properties_canvas, text="Y:").grid(row=grid_spot + 1)
            grid_spot += 2
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

        grid_spot = 27
        verts_labels = []
        for x in range(8):
            verts_x = tk.Entry(properties_canvas)
            verts_y = tk.Entry(properties_canvas)
            verts_x.grid(row=grid_spot, column=1)
            verts_y.grid(row=grid_spot + 1, column=1)
            verts_labels.append(verts_x)
            verts_labels.append(verts_y)
            grid_spot += 2

        xy_goal_tolerance = tk.Entry(properties_canvas)
        yaw_goal_tolerance = tk.Entry(properties_canvas)
        xy_goal_tolerance.grid(row=44, column=1)
        yaw_goal_tolerance.grid(row=45, column=1)

        self.master.labels = [name_label_text, set_label_text, x_entry, y_entry, z_entry, w_orientation, x_orientation,
                              y_orientation, z_orientation, map_label_text, self.master.connection_label_text, action,
                              inflation_radius, recovery_behaviours_config, top_vel, verts_labels, xy_goal_tolerance,
                              yaw_goal_tolerance]

        # Adds an update button at the top
        tk.Button(properties_canvas, text="Update", command=lambda: self.update_node(1)).grid(row=0, column=1)

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
        self.plot_canvas()

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
                        self.display_node_info(node)
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
                    self.deselect_node_info()
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
            self.update_node(0)
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

        self.master.editmenu.add_command(label="Deselect Node(s)                             CTRL + D",
                                         command=lambda: self.deselect_node_event(self.master.multi_clicked_item))

        self.master.editmenu.add_command(label="Add Node                                         CTRL + Mouse 1",
                                         command=lambda: self.add_canvas_node(self.master.clicked_pos))
        self.master.editmenu.add_command(label="Add Node Connection                   CTRL + Mouse 2",
                                         command=lambda: self.add_canvas_connection(self.master.multi_clicked_item))
        self.master.editmenu.add_command(label="Delete Node                                     CTRL + Backspace",
                                         command=lambda: self.delete_canvas_node(self.master.clicked_item))
        self.master.editmenu.add_command(label="Delete Node Connection               SHIFT + Backspace",
                                         command=lambda: self.delete_connection(self.master.multi_clicked_item))

        self.master.filemenu.add_command(label="Close Project",
                                         command=lambda: self._save_and_close())

        single_item_button = elements.Button(master=master.master, x=790, y=20, text="Single Mode", width=20,
                                             func=lambda: self.change_mode(0))

        multi_item_button = elements.Button(master=master.master, x=790, y=70, text="Multi Mode",
                                            width=20,
                                            func=lambda: self.change_mode(1))

        tk.mainloop()

    def _save_and_close(self):
        msg_box = tk.messagebox.askquestion('Exit Application', 'Would you like to save before quitting?',
                                            icon='warning')
        if msg_box == 'yes':
            self.master.save_filename()
            os.execl(sys.executable, sys.executable, *sys.argv)
        else:
            os.execl(sys.executable, sys.executable, *sys.argv)

            # if conformation is true, save and quit, else just quit

    def _on_mousewheel_y_view(self, event):
        self.map_canvas.yview_scroll(int(-1 * (event.delta / 120)), "units")

    def _on_mousewheel_x_view(self, event):
        self.map_canvas.xview_scroll(int(-1 * (event.delta / 120)), "units")

    def _bind_to_mousewheel(self, event):
        self.map_canvas.bind_all("<MouseWheel>", self._on_mousewheel_y_view)
        self.map_canvas.bind_all("<Control-MouseWheel>", self._on_mousewheel_x_view)

    def delete_canvas_node_event(self, event):
        self.delete_canvas_node(self.master.clicked_item)

    def delete_canvas_node__connection_event(self, event):
        self.delete_connection(self.master.multi_clicked_item)

    def add_canvas_node__connection_event(self, event):
        self.add_canvas_connection(self.master.multi_clicked_item)

    def add_canvas_node_event(self, event):
        self.add_canvas_node(self.master.clicked_pos)

    def deselect_node_event(self, event):
        self.deselect_all()

    # Function to plot all the points on the canvas, first cycles through all the nodes and plots them then cycles
    #   through all the links and plots them.
    def plot_canvas(self):
        for point in self.master.tmapdata:
            name = point["node"]["name"]
            position = point["node"]["pose"]["position"]
            pos_x, pos_y = tmap.swap_to_px(self, position["x"], position["y"])
            node = self.map_canvas.create_oval(pos_x - 4, pos_y - 4, pos_x + 4, pos_y + 4, fill="blue",
                                               tags=("point", name))
        for point in self.master.tmapdata:
            links = point["node"]["edges"]
            position = point["node"]["pose"]["position"]
            pos_x, pos_y = tmap.swap_to_px(self, position["x"], position["y"])
            for link in links:
                if link != "":
                    self.create_node_link([pos_x, pos_y], link)
        self.map_canvas.tag_raise("point")

    # Function for plotting a single canvas node connection, used by some other functions
    def create_node_link(self, pos, link):
        if self.map_canvas.find_withtag(link["edge_id"]) == ():
            connection = link["edge_id"]
            next_node = connection.split("_")[1]
            next_pos1, next_pos2 = tmap.get_pos(self, next_node)
            next_pos_x, next_pos_y = tmap.swap_to_px(self, next_pos1, next_pos2)
            self.map_canvas.create_line(pos[0], pos[1], next_pos_x, next_pos_y, dash=(4, 2), arrow=tk.LAST,
                                        tags=("connection",
                                              str("Connect" +
                                                  connection.split("_")[
                                                      0]),
                                              str("Connect" +
                                                  connection.split("_")[
                                                      1]),
                                              str(connection)))

    # Function that changes the users current operating "mode", single mode is for selecting one object either a node
    #   or a location on the canvas, multimode is for selecting two different nodes. When changing modes the function
    #   deselects any currently selected items and reverts them to their natural state
    def change_mode(self, mode):
        if self.master.click_mode != mode:
            self.deselect_all()
            self.map_canvas.delete("clickspot")
            self.master.click_mode = mode
            if self.master.clicked_item != 0:
                item = self.map_canvas.find_withtag(self.master.clicked_item)
                for x in item:
                    self.map_canvas.itemconfig(x, fill='blue')
                self.master.clicked_item = 0
            elif self.master.multi_clicked_item:
                for x in self.master.multi_clicked_item:
                    item = self.map_canvas.find_withtag(x)
                    for y in item:
                        self.map_canvas.itemconfig(y, fill='blue')
                self.master.multi_clicked_item = []
            self.master.clicked_pos = []

    # Function to create a new node on a selected location on the canvas and add to the dictionary as well as plot it on
    #   the canvas and make it the currently selected item. Currently only takes in the x and y coordinates the rest of
    #   the values are hard coded (EXCEPT FOR NAME WHICH IS AUTO GENERATED, MUCH IMPORTANT VERY PRIMARY KEY)
    def add_canvas_node(self, pos):
        if pos != [] and self.master.click_mode == 0:
            self.logging.info(pos)
            pos_x, pos_y = pos[0], pos[1]
            metre_pos_x, metre_pos_y = tmap.swap_to_metre(self, pos_x, pos_y)
            self.logging.info(metre_pos_x)
            self.logging.info(metre_pos_y)
            new_node = tmap.add_node(self, "riseholme", "riseholme", [0.5, 0.6, 0.7, 0.8],
                                     [metre_pos_x, metre_pos_y, 0.0])
            node = self.map_canvas.create_oval(pos_x - 4, pos_y - 4, pos_x + 4, pos_y + 4, fill="blue",
                                               tags=("point", new_node))
            self.map_canvas.itemconfig(node, fill='red')
            self.master.clicked_item = new_node
            self.display_node_info(new_node)

    # Function to create a new connection between two selected nodes in the tmap dictionary and to plot the connection
    #   on the canvas, stores the position in the dictionary as metre value then converts to pixels for plotting
    def add_canvas_connection(self, nodes):
        if len(nodes) == 2 and self.master.click_mode == 1:
            tmap.add_action(self, nodes[0], nodes[1])
            pos_x1, pos_y1 = tmap.swap_to_px(self, tmap.get_pos(self, nodes[0])[0], tmap.get_pos(self, nodes[0])[1])
            pos_x2, pos_y2 = tmap.swap_to_px(self, tmap.get_pos(self, nodes[1])[0], tmap.get_pos(self, nodes[1])[1])
            self.logging.info("posX1:{} posY1:{} posX2:{} posY2:{}".format(pos_x1, pos_y1, pos_x2, pos_y2))
            self.map_canvas.create_line(pos_x1, pos_y1, pos_x2, pos_y2, dash=(4, 2), arrow=tk.LAST, tags=("connection",
                                                                                                          str(
                                                                                                              "Connect" +
                                                                                                              nodes[0]),
                                                                                                          str(
                                                                                                              "Connect" +
                                                                                                              nodes[1]),
                                                                                                          str(nodes[
                                                                                                                  0] + "_" +
                                                                                                              nodes[
                                                                                                                  1])))
            self.map_canvas.tag_raise("point")

    # Function to delete a connection between two selected nodes and remove that connection from the dictionary, checks
    # both the nodes to see if they have the connection and deletes from both if necessary
    def delete_connection(self, nodes):
        if len(nodes) == 2 and self.master.click_mode == 1:
            action_val1 = nodes[0] + "_" + nodes[1]
            action_val2 = nodes[1] + "_" + nodes[0]
            tmap.delete_action(self, nodes[0], nodes[1])
            tmap.delete_action(self, nodes[1], nodes[0])
            self.map_canvas.delete(str(action_val1))
            self.map_canvas.delete(str(action_val2))

    # Function to delete a node from the tmap dictionary and any associated canvas options
    def delete_canvas_node(self, node):
        if self.master.click_mode == 0 and self.map_canvas.type(node) == "oval":
            tmap.delete_node(self, node)
            self.map_canvas.delete(node)
            self.map_canvas.delete(str("Connect" + node))

    # Function to update the sidebar labels with the info obtained from the tmap dictionary
    def display_node_info(self, node):
        data = tmap.get_display_info(self, node)
        if self.master.click_mode == 0:
            self.master.labels[0].set(data[1])
            self.master.labels[1].set(data[0])
            x = 2
            for label in self.master.labels[2:9]:
                label.delete(0, tk.END)
                label.insert(0, data[x])
                x = x + 1
            if data[9]:
                names_list = []
                for item in data[9]:
                    name = item["node"]
                    names_list.append(name)
                x = x + 2
                for label in self.master.labels[11:15]:
                    label.delete(0, tk.END)
                    x = x + 1
                self.master.option_list = names_list
                self.master.connection_data = [data[9]]
                self.master.connection_label_text.set(names_list[0])
                self.master.node_box['menu'].delete(0, 'end')
                for name in names_list:
                    self.master.node_box['menu'].add_command(label=name, command=lambda value=name: [
                        self.master.connection_label_text.set(value), self.select_connection()])
                self.master.labels[9].set(data[9][0]["map"])
        count = 0
        for loop in range(8):
            x, y = data[10][int(count / 2)]["x"], data[10][int(count / 2)]["y"]
            self.master.labels[15][count].delete(0, tk.END)
            self.master.labels[15][count + 1].delete(0, tk.END)
            self.master.labels[15][count].insert(0, x)
            self.master.labels[15][count + 1].insert(0, y)
            count += 2
        self.master.labels[16].delete(0, tk.END)
        self.master.labels[17].delete(0, tk.END)
        self.master.labels[16].insert(0, data[11])
        self.master.labels[17].insert(0, data[12])

    def select_connection(self):
        connect_node = self.master.connection_label_text.get()
        origin_node = self.master.labels[1].get()
        self.logging.info("Select connection active with: {}".format(connect_node))
        data = []
        if self.master.connection_data:
            data = self.master.connection_data[0]
        self.logging.info("Data: {}".format(data))
        if data:
            x, list_location = 0, 0
            for y in data:
                if y["node"] == connect_node:
                    list_location = x
                else:
                    x = x + 1
            for label in self.master.labels[11:15]:
                label.delete(0, tk.END)
            self.master.labels[11].insert(0, data[list_location]["action"])
            self.master.labels[12].insert(0, data[list_location]["inflation"])
            self.master.labels[13].insert(0, data[list_location]["recovery"])
            self.master.labels[14].insert(0, data[list_location]["vel"])
            self.master.selected_connection = connect_node
            connect_name = origin_node + "_" + connect_node
            self.map_canvas.itemconfig("connection", dash=1, fill='black')
            self.map_canvas.itemconfig(connect_name, dash=(4, 2), fill='red')

    # Function to update a position of a node through the sidebar options, updates position in tmap dictionary then
    #   deletes all canvas objects associated to the node and replots the node, connections and searches for any
    #   connections adjacent nodes have to the updated node to plot
    def update_node(self, from_labels):
        labels = self.master.labels
        new_pos, new_ori, new_action, new_verts, new_tolerance = [], [], [], [], []
        error = 0
        if from_labels == 1:
            # Checks position and orientation input values are numbers and X/Y are positive
            for x in range(2, 9):
                if error == 0:
                    try:
                        val = float(labels[x].get())
                        if val < 0 and error == 0 and (x == 2 or x == 3):
                            messagebox.showerror("Error", "Position must be a positive value")
                            self.logging.info("Error val: {}".format(val))
                            error = 1
                    except ValueError:
                        error = 1
                        if x < 5:
                            messagebox.showerror("Error", "Position must be a number")
                        else:
                            messagebox.showerror("Error", "Orientation must be a number")
            if error == 0:
                new_pos = [float(labels[2].get()), float(labels[3].get()), float(labels[4].get())]
                new_ori = [float(labels[5].get()), float(labels[6].get()), float(labels[7].get()),
                           float(labels[8].get())]
            self.logging.info("Selected connection: {}".format(self.master.selected_connection))
            if self.master.selected_connection != "":
                new_action = [self.master.connection_label_text.get(), labels[11].get(), labels[12].get(),
                              labels[13].get(), float(labels[14].get())]
            for entry in labels[15]:
                new_verts.append(entry.get())
            new_tolerance = [float(labels[16].get()), float(labels[17].get())]
            node_name = labels[1].get()
        else:
            node_pos = tmap.get_node_pos(self, self.master.drag_data["item"])
            new_pos = [float(self.master.drag_data["x"]), float(self.master.drag_data["y"]),
                       float(self.master.tmapdata[node_pos]["node"]["pose"]["position"]["z"])]
            node_name = self.master.drag_data["item"]
            tmap.update_pos(self, node_name, new_pos)
        self.logging.info("Error at update call: {}".format(error))
        if error == 0:
            if from_labels == 1:
                tmap.update_pos(self, node_name, new_pos)
                tmap.update_ori(self, node_name, new_ori)
                if self.master.selected_connection != "":
                    tmap.update_action(self, node_name, new_action)
                tmap.update_verts(self, node_name, new_verts)
                tmap.update_tolerance(self, node_name, new_tolerance)
            if from_labels == 0 and self.master.clicked_item == node_name:
                self.display_node_info(node_name)
            node_pos = tmap.get_node_pos(self, node_name)
            self.map_canvas.delete(node_name)
            self.map_canvas.delete(str("Connect" + node_name))
            node = self.map_canvas.create_oval(new_pos[0] - 4, new_pos[1] - 4, new_pos[0] + 4, new_pos[1] + 4,
                                               fill="blue",
                                               tags=("point", node_name))
            if from_labels == 1 or self.master.clicked_item == node_name:
                self.map_canvas.itemconfig(node, fill='red')
            for link in self.master.tmapdata[node_pos]["node"]["edges"]:
                self.create_node_link(new_pos, link)
            for nodes in self.master.tmapdata:
                for link in nodes["node"]["edges"]:
                    node_connection = link["edge_id"]
                    if node_connection.split("_")[1] == node_name:
                        new_pos[0], new_pos[1] = tmap.swap_to_px(self,
                                                                 tmap.get_pos(self, node_connection.split("_")[0])[0],
                                                                 tmap.get_pos(self, node_connection.split("_")[0])[1])
                        self.create_node_link(new_pos, link)
        self.map_canvas.tag_raise("point")

    def deselect_node_info(self):
        self.master.labels[0].set("")
        self.master.labels[1].set("")
        for label in self.master.labels[2:9]:
            label.delete(0, tk.END)
        for label in self.master.labels[11:15]:
            label.delete(0, tk.END)
        self.master.option_list = []
        self.master.connection_data = []
        self.master.connection_label_text.set("")
        self.master.node_box['menu'].delete(0, 'end')
        for loop in range(16):
            self.master.labels[15][loop].delete(0, tk.END)
        self.master.labels[16].delete(0, tk.END)
        self.master.labels[17].delete(0, tk.END)

    def deselect_all(self):
        self.master.clicked_item = 0
        self.master.multi_clicked_item = []
        self.master.clicked_pos = []
        self.master.click_mode = 0
        self.master.option_list = [""]
        self.master.selected_connection = ""
        self.master.connection_data = []
        self.map_canvas.itemconfig("point", fill='blue')
        self.map_canvas.itemconfig("connection", dash=1, fill='black')
        self.deselect_node_info()
