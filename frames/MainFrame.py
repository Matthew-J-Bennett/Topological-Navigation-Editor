import tkinter as tk
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
        properties_canvas = tk.Canvas(self.window, width=400, height=800)
        properties_canvas.pack(expand=tk.NO, side=tk.RIGHT, fill=tk.BOTH)

        # String variables used to store the values obtained from the dictionary to put in the labels
        name_label_text, set_label_text = tk.StringVar(), tk.StringVar()

        # Populates text Labels
        tk.Label(properties_canvas, text="Node Properties").grid(row=0)
        tk.Label(properties_canvas, text="Node Name").grid(row=1)
        tk.Label(properties_canvas, text="Node Set").grid(row=2)
        tk.Label(properties_canvas, text="X Co-ord").grid(row=3)
        tk.Label(properties_canvas, text="Y Co-ord").grid(row=4)
        tk.Label(properties_canvas, text="Z Co-ord").grid(row=5)

        # Uses two labels and three entry's as the name and nodeset are static values whereas the position is changeable
        name = tk.Label(properties_canvas, textvariable=name_label_text)
        nodeset = tk.Label(properties_canvas, textvariable=set_label_text)
        x_entry = tk.Entry(properties_canvas)
        y_entry = tk.Entry(properties_canvas)
        z_entry = tk.Entry(properties_canvas)
        self.master.labels = [name_label_text, set_label_text, x_entry, y_entry, z_entry]

        # Puts the labels in the correct spots in the grid
        name.grid(row=1, column=1)
        nodeset.grid(row=2, column=1)
        x_entry.grid(row=3, column=1)
        y_entry.grid(row=4, column=1)
        z_entry.grid(row=5, column=1)
        # Adds an update button at the bottom
        tk.Button(properties_canvas, text="Update", command=lambda: self.update_node(self.master.labels)).grid(row=6,
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
                        self.display_node_info(node, self.master.labels)
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

        # Activates the onclick event when any location on the canvas is clicked
        self.map_canvas.bind('<Button-1>', onclick)

        # All the buttons for the various different functions (Currently temporary as they look shit anyway)
        add_button = elements.Button(master=master.master, x=800, y=550, text="Add Node", width=20,
                                     func=lambda: self.add_canvas_node(self.master.clicked_pos))

        delete_button = elements.Button(master=master.master, x=800, y=600, text="Delete Node", width=20,
                                        func=lambda: self.delete_canvas_node(self.master.clicked_item))

        add_connection_button = elements.Button(master=master.master, x=800, y=650, text="Add Connection", width=20,
                                                func=lambda: self.add_canvas_connection(self.master.multi_clicked_item))

        delete_connection_button = elements.Button(master=master.master, x=800, y=700, text="Delete Connection",
                                                   width=20,
                                                   func=lambda: self.delete_connection(self.master.multi_clicked_item))

        single_item_button = elements.Button(master=master.master, x=600, y=650, text="Single Mode", width=20,
                                             func=lambda: self.change_mode(0))

        multi_item_button = elements.Button(master=master.master, x=600, y=700, text="Multi Mode", width=20,
                                            func=lambda: self.change_mode(1))

        temp_save_button = elements.Button(master=master.master, x=50, y=700, text="Save File", width=20,
                                           func=lambda: frames.LaunchFrame.save_filename(self))

        tk.mainloop()

    # Function to plot all the points on the canvas, first cycles through all the nodes and plots them then cycles
    #   through all the links and plots them.
    def plot_canvas(self):
        for point in self.master.tmapdata:
            name = point["meta"]["node"]
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
            self.master.click_mode = mode
            self.map_canvas.delete("clickspot")
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
            self.display_node_info(new_node, self.master.labels)

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
        if self.master.click_mode == 0:
            tmap.delete_node(self, node)
            self.map_canvas.delete(node)
            self.map_canvas.delete(str("Connect" + node))

    # Function to update the sidebar labels with the info obtained from the tmap dictionary
    def display_node_info(self, node, labels):
        data = tmap.get_display_info(self, node)

        labels[0].set(data["name"])
        labels[1].set(data["set"])

        labels[2].delete(0, tk.END)
        labels[3].delete(0, tk.END)
        labels[4].delete(0, tk.END)
        labels[2].insert(0, data["x"])
        labels[3].insert(0, data["y"])
        labels[4].insert(0, data["z"])

    # Function to update a position of a node through the sidebar options, updates position in tmap dictionary then
    #   deletes all canvas objects associated to the node and replots the node, connections and searches for any
    #   connections adjacent nodes have to the updated node to plot
    def update_node(self, labels):
        new_pos = [float(labels[2].get()), float(labels[3].get())]
        node_name = labels[0].get()
        tmap.update_pos(self, node_name, new_pos)
        node_pos = tmap.get_node_pos(self, node_name)
        self.map_canvas.delete(node_name)
        self.map_canvas.delete(str("Connect" + node_name))
        node = self.map_canvas.create_oval(new_pos[0] - 4, new_pos[1] - 4, new_pos[0] + 4, new_pos[1] + 4, fill="blue",
                                           tags=("point", node_name))
        self.map_canvas.itemconfig(node, fill='red')
        for link in self.master.tmapdata[node_pos]["node"]["edges"]:
            self.create_node_link(new_pos, link)
        for nodes in self.master.tmapdata:
            for link in nodes["node"]["edges"]:
                node_connection = link["edge_id"]
                if node_connection.split("_")[1] == node_name:
                    new_pos[0], new_pos[1] = tmap.swap_to_px(self, tmap.get_pos(self, node_connection.split("_")[0])[0],
                                                             tmap.get_pos(self, node_connection.split("_")[0])[1])
                    self.create_node_link(new_pos, link)
        self.map_canvas.tag_raise("point")
