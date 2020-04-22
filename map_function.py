import tkinter as tk
from tkinter import messagebox, simpledialog
import tmap
import logging

logger = logging.getLogger("Topological-Navigation-Editor")


# Function to plot all the points on the canvas, first cycles through all the nodes and plots them then cycles
#   through all the links and plots them.
def plot_canvas(self):
    if self.master.tmapdata:
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
                    create_node_link(self, [pos_x, pos_y], link)
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
        self.map_canvas.delete("clickspot")
        deselect_all(self)
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
        self.map_canvas.itemconfig("connection", dash=1, fill='black')


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
        new_node = tmap.add_node(self, "riseholme", "riseholme", [0, 0, 0, 0],
                                 [metre_pos_x, metre_pos_y, 0.0])
        node = self.map_canvas.create_oval(pos_x - 4, pos_y - 4, pos_x + 4, pos_y + 4, fill="blue",
                                           tags=("point", new_node))
        self.map_canvas.itemconfig(node, fill='red')
        self.master.clicked_item = new_node
        display_node_info(self, new_node)


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


# Function to plot a connected line of nodes between two already existing nodes, requires the user to be in multi-mode
#   and prompts the user to input a number (must be an integer greater than zero). The connections are plotted from the
#   first selected node to the selected to the selected (one way only)
def add_node_string(self, nodes):
    if check_selected(self, 1):
        error = 0
        num_nodes = simpledialog.askstring(title="Connected Nodes Plotting",
                                           prompt="Please enter the number of nodes to be plotted between the selected "
                                                  "nodes:")
        try:
            val = int(num_nodes)
            if val <= 0:
                error = 1
                messagebox.showerror("Error", "Must be a positive number.")
        except ValueError:
            error = 1
            messagebox.showerror("Error", "Must be an interger value.")
        if error == 0:
            num_nodes = int(num_nodes)
            new_nodes = []
            canvas_nodes = []
            pos_x1, pos_y1 = tmap.swap_to_px(self, tmap.get_pos(self, nodes[0])[0], tmap.get_pos(self, nodes[0])[1])
            pos_x2, pos_y2 = tmap.swap_to_px(self, tmap.get_pos(self, nodes[1])[0], tmap.get_pos(self, nodes[1])[1])
            diff_x = (pos_x1 - pos_x2) / (num_nodes + 1)
            diff_y = (pos_y1 - pos_y2) / (num_nodes + 1)
            for count in range(num_nodes):
                pos_x = pos_x1 - (diff_x * (count + 1))
                pos_y = pos_y1 - (diff_y * (count + 1))
                metre_pos_x, metre_pos_y = tmap.swap_to_metre(self, pos_x, pos_y)
                new_node = tmap.add_node(self, "riseholme", "riseholme", [0, 0, 0, 0],
                                         [metre_pos_x, metre_pos_y, 0.0])
                node = self.map_canvas.create_oval(pos_x - 4, pos_y - 4, pos_x + 4, pos_y + 4, fill="blue",
                                                   tags=("point", new_node))
                new_nodes.append(new_node)
                canvas_nodes.append(node)
                if count != 0:
                    self.logging.info(count)
                    add_canvas_connection(self, (new_nodes[count - 1], new_nodes[count]))
            add_canvas_connection(self, (nodes[0], new_nodes[0]))
            add_canvas_connection(self, (new_nodes[num_nodes - 1], nodes[1]))


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
                    self.master.connection_label_text.set(value), select_connection(self)])
            self.master.labels[9].set(data[9][0]["map"])
            select_connection(self)
        else:
            self.master.connection_label_text.set("")
            self.master.node_box['menu'].delete(0, 'end')
            for label in self.master.labels[11:15]:
                label.delete(0, tk.END)
                x = x + 1
    self.master.verts_box['menu'].delete(0, 'end')
    verts_options = ["Vert 1", "Vert 2", "Vert 3", "Vert 4", "Vert 5", "Vert 6", "Vert 7", "Vert 8"]
    self.master.verts_label_text.set(verts_options[0])
    for vert in verts_options:
        self.master.verts_box['menu'].add_command(label=vert, command=lambda value=vert: [
            self.master.verts_label_text.set(value), select_vert(self)])
    self.master.labels[15][0].delete(0, tk.END)
    self.master.labels[15][1].delete(0, tk.END)
    self.master.verts_data = [data[10]]
    select_vert(self)
    self.master.labels[16].delete(0, tk.END)
    self.master.labels[17].delete(0, tk.END)
    self.master.labels[16].insert(0, data[11])
    self.master.labels[17].insert(0, data[12])


# Function bound to each of the options in the node connections drop-down menu, retrieves the value in the selected
#   option and fills the input boxes with the data from that connection
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
        self.master.connect_name = origin_node + "_" + connect_node
        self.map_canvas.itemconfig("connection", dash=1, fill='black')
        self.map_canvas.itemconfig(self.master.connect_name, dash=(4, 2), fill='red')
        self.map_canvas.tag_raise(self.master.connect_name)
        self.map_canvas.tag_raise("point")


# Similar to select_connection but used for the verts drop-down menu
def select_vert(self):
    selected_vert = self.master.verts_label_text.get()
    self.logging.info("Select vert active with: {}".format(selected_vert))
    data = []
    if self.master.verts_data:
        data = self.master.verts_data
    self.logging.info("Data: {}".format(data))
    if data:
        vert = int(selected_vert.split(" ")[1]) - 1
        self.logging.info("Vert index: {}".format(vert))
        self.master.labels[15][0].delete(0, tk.END)
        self.master.labels[15][1].delete(0, tk.END)
        self.master.labels[15][0].insert(0, data[0][vert]["x"])
        self.master.labels[15][1].insert(0, data[0][vert]["y"])
        self.master.selected_vert = selected_vert


# Function to update a position of a node through the sidebar options, updates position in tmap dictionary then
#   deletes all canvas objects associated to the node and replots the node, connections and searches for any
#   connections adjacent nodes have to the updated node to plot
def update_node(self, from_labels):
    self.logging.info("Update node called.")
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
            new_ori = [float(labels[5].get()), float(labels[6].get()), float(labels[7].get()), float(labels[8].get())]
        self.logging.info("Selected connection: {}".format(self.master.selected_connection))
        if self.master.selected_connection != "":
            new_action = [self.master.selected_connection, labels[11].get(), labels[12].get(),
                          labels[13].get(), labels[14].get()]
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
                data = self.master.connection_data[0]
                location, count = 0, 0
                for connection in data:
                    if connection["node"] == self.master.selected_connection:
                        location = count
                    else:
                        count = count + 1
                data[location]["action"] = labels[11].get()
                data[location]["inflation"] = labels[12].get()
                data[location]["recovery"] = labels[13].get()
                data[location]["vel"] = labels[14].get()
                self.master.connection_data[0] = data
            if self.master.selected_vert != "":
                tmap.update_verts(self, node_name, new_verts)
                data = self.master.verts_data
                vert = int(self.master.verts_label_text.get().split(" ")[1]) - 1
                data[0][vert]["x"] = new_verts[0]
                data[0][vert]["y"] = new_verts[1]
                self.master.verts_data = data
            tmap.update_tolerance(self, node_name, new_tolerance)
        if from_labels == 0 and self.master.clicked_item == node_name:
            display_node_info(self, node_name)
        node_pos = tmap.get_node_pos(self, node_name)
        self.map_canvas.delete(node_name)
        self.map_canvas.delete(str("Connect" + node_name))
        node = self.map_canvas.create_oval(new_pos[0] - 4, new_pos[1] - 4, new_pos[0] + 4, new_pos[1] + 4, fill="blue",
                                           tags=("point", node_name))
        if from_labels == 1 or self.master.clicked_item == node_name:
            self.map_canvas.itemconfig(node, fill='red')
        for link in self.master.tmapdata[node_pos]["node"]["edges"]:
            create_node_link(self, new_pos, link)
        for nodes in self.master.tmapdata:
            for link in nodes["node"]["edges"]:
                node_connection = link["edge_id"]
                if node_connection.split("_")[1] == node_name:
                    new_pos[0], new_pos[1] = tmap.swap_to_px(self, tmap.get_pos(self, node_connection.split("_")[0])[0],
                                                             tmap.get_pos(self, node_connection.split("_")[0])[1])
                    create_node_link(self, new_pos, link)
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
    self.master.labels[15][0].delete(0, tk.END)
    self.master.labels[15][1].delete(0, tk.END)
    self.master.labels[16].delete(0, tk.END)
    self.master.labels[17].delete(0, tk.END)


def deselect_all(self):
    self.master.clicked_item = 0
    self.master.multi_clicked_item = []
    self.master.clicked_pos = []
    self.master.option_list = [""]
    self.master.selected_connection, self.master.selected_vert = "", ""
    self.master.connection_data, self.master.verts_data = [], []
    self.map_canvas.itemconfig("point", fill='blue')
    self.map_canvas.itemconfig("connection", dash=1, fill='black')
    deselect_node_info(self)


# Checks the user is in the correct mode for certain functions
def check_selected(self, mode_req):
    if mode_req == 1 and self.master.click_mode == 1:
        if len(self.master.multi_clicked_item) == 2 and self.master.multi_clicked_item[0] != \
                self.master.multi_clicked_item[1]:
            return 1
        else:
            return None
    elif mode_req == 0 and self.master.click_mode == 0:
        if self.master.clicked_item:
            return 1
        else:
            return None
    else:
        return None
