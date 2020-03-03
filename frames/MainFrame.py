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
        self.mapcanvas = tk.Canvas(self.window, width=850, height=800, scrollregion=(0, 0,
                                                                                  self.master.pgm["width"],
                                                                                  self.master.pgm["height"]))
        self.mapcanvas.pack(expand=tk.YES, side=tk.LEFT, fill=tk.BOTH)
        # Adds the image to the imgcanvas
        self.mapcanvas.create_image(0, 0, anchor=tk.NW, image=img)

        # Creates the Properties Canvas
        propcanvas = tk.Canvas(self.window, width=400, height=800)
        propcanvas.pack(expand=tk.NO, side=tk.RIGHT, fill=tk.BOTH)

        # String variables used to store the values obtained from the dictionary to put in the labels
        nameLabelText, setLabelText = tk.StringVar(), tk.StringVar()

        # Populates text Labels
        tk.Label(propcanvas, text="Node Properties").grid(row=0)
        tk.Label(propcanvas, text="Node Name").grid(row=1)
        tk.Label(propcanvas, text="Node Set").grid(row=2)
        tk.Label(propcanvas, text="X Co-ord").grid(row=3)
        tk.Label(propcanvas, text="Y Co-ord").grid(row=4)
        tk.Label(propcanvas, text="Z Co-ord").grid(row=5)

        # Uses two labels and three entrys as the name and nodeset are static values whereas the position is changeable
        name = tk.Label(propcanvas, textvariable=nameLabelText)
        nodeset = tk.Label(propcanvas, textvariable=setLabelText)
        xentry = tk.Entry(propcanvas)
        yentry = tk.Entry(propcanvas)
        zentry = tk.Entry(propcanvas)
        self.master.labels = [nameLabelText, setLabelText, xentry, yentry, zentry]

        # Puts the labels in the correct spots in the grid
        name.grid(row=1, column=1)
        nodeset.grid(row=2, column=1)
        xentry.grid(row=3, column=1)
        yentry.grid(row=4, column=1)
        zentry.grid(row=5, column=1)
        # Adds an update buttom at the bottom
        tk.Button(propcanvas, text="Update", command=lambda: self.updateNode(self.master.labels)).grid(row=6, column=1)

        # Creates a horizontal scrollbar
        scroll_x = tk.Scrollbar(self.mapcanvas, orient="horizontal", command=self.mapcanvas.xview, jump=1)
        # Sets the location of the scroll bar
        scroll_x.pack(side=tk.BOTTOM, fill=tk.X)
        # Defines what the scroll bar will do
        scroll_x.config(command=self.mapcanvas.xview)
        self.mapcanvas.config(xscrollcommand=scroll_x.set)

        # Creates a vertical scrollbar
        scroll_y = tk.Scrollbar(self.mapcanvas, orient="vertical", command=self.mapcanvas.yview, jump=1)
        # Sets the location of the scroll bar
        scroll_y.pack(side=tk.RIGHT, fill=tk.Y)
        # Defines what the scroll bar will do
        scroll_y.config(command=self.mapcanvas.yview)
        self.mapcanvas.config(yscrollcommand=scroll_y.set)
        self.plotCanvas()

        # Variables used for the associated click mode and storing the users currently selected item(s)
        self.master.clickeditem = 0
        self.master.multiclickeditem = []
        self.master.clickedpos = []
        self.master.clickmode = 0

        # Just an absolute shit show
        # The onclick function obtains the position that the user clicked on the canvas and finds the nearest object,
        #   this will either be the canvas (image) or a node (oval). The function also discerns what mode the user is
        #   in either single (0) or multi (1).
        def onclick(event):
            self.mapcanvas.delete("clickspot")
            item = self.mapcanvas.find_closest(self.mapcanvas.canvasx(event.x), self.mapcanvas.canvasy(event.y))
            item_type = self.mapcanvas.type(item)
            self.logging.info(item_type+str(self.mapcanvas.canvasx(event.x))+str(self.mapcanvas.canvasy(event.y)))
            if self.master.clickmode == 0:
                if item_type == "oval":
                    tags = self.mapcanvas.gettags(item)
                    node = tags[1]
                    self.logging.info(str(tags[1]))
                    if self.master.clickeditem != 0:
                        item2 = self.mapcanvas.find_withtag(self.master.clickeditem)
                        for x in item2:
                            self.mapcanvas.itemconfig(x, fill='blue')
                    if self.master.clickeditem == 0 or self.master.clickeditem != node:
                        self.mapcanvas.itemconfig(item, fill='red')
                        self.master.clickeditem = node
                        self.displayNodeInfo(node, self.master.labels)
                    elif self.master.clickeditem == node:
                        self.mapcanvas.itemconfig(item, fill='blue')
                        self.master.clickeditem = 0
                    self.master.clickedpos = []
                elif item_type == "image":
                    x = self.mapcanvas.canvasx(event.x)
                    y = self.mapcanvas.canvasy(event.y)
                    self.mapcanvas.create_line(x+3, y+3, x-3, y-3, width=1.5, fill="red", tags="clickspot")
                    self.mapcanvas.create_line(x+3, y-3, x-3, y+3, width=1.5, fill="red", tags="clickspot")
                    self.master.clickedpos = [self.mapcanvas.canvasx(event.x),self.mapcanvas.canvasy(event.y)]
                    if self.master.clickeditem != 0:
                        item2 = self.mapcanvas.find_withtag(self.master.clickeditem)
                        for x in item2:
                            self.mapcanvas.itemconfig(x, fill='blue')
                        self.master.clickeditem = 0
            else:
                if item_type == "oval":
                    tags = self.mapcanvas.gettags(item)
                    node = tags[1]
                    self.logging.info(str(tags[1]))
                    if self.master.multiclickeditem:
                        numitems = len(self.master.multiclickeditem)
                        for y in self.master.multiclickeditem:
                            item2 = self.mapcanvas.find_withtag(y)
                            if y != node and numitems < 2:
                                self.mapcanvas.itemconfig(item, fill='red')
                                self.master.multiclickeditem.append(node)
                                break
                            elif y == node:
                                self.mapcanvas.itemconfig(item, fill='blue')
                                self.master.multiclickeditem.remove(node)
                    else:
                        self.mapcanvas.itemconfig(item, fill='red')
                        self.master.multiclickeditem.append(node)
                    self.master.clickedpos = []
                self.logging.info(self.master.multiclickeditem)

        # Activates the onclick event when any location on the canvas is clicked
        self.mapcanvas.bind('<Button-1>', onclick)

        # All the buttons for the various different functions (Currently temporary as they look shit anyway)
        add_button = elements.Button(master=master.master, x=800, y=550, text="Add Node", width=20,
                                        func=lambda: self.addCanvasNode(self.master.clickedpos))

        delete_button = elements.Button(master=master.master, x=800, y=600, text="Delete Node", width=20,
                                        func=lambda: self.deleteCanvasNode(self.master.clickeditem))

        add_connection_button = elements.Button(master=master.master, x=800, y=650, text="Add Connection", width=20,
                                     func=lambda: self.addCanvasConnection(self.master.multiclickeditem))

        delete_connection_button = elements.Button(master=master.master, x=800, y=700, text="Delete Connection", width=20,
                                     func=lambda: self.deleteConnection(self.master.multiclickeditem))

        single_item_button = elements.Button(master=master.master, x=600, y=650, text="Single Mode", width=20,
                                        func=lambda: self.changeMode(0))

        multi_item_button = elements.Button(master=master.master, x=600, y=700, text="Multi Mode", width=20,
                                     func=lambda: self.changeMode(1))

        temp_save_button = elements.Button(master=master.master, x=50, y=700, text="Save File", width=20,
                                           func=lambda: frames.LaunchFrame.savefilename(self))

        tk.mainloop()

    # Function to plot all the points on the canvas, first cycles through all the nodes and plots them then cycles
    #   through all the links and plots them.
    def plotCanvas(self):
        for point in self.master.tmapdata:
            name = point["meta"]["node"]
            position = point["node"]["pose"]["position"]
            posX, posY = tmap.swapToPix(self, position["x"], position["y"])
            node = self.mapcanvas.create_oval(posX - 4, posY - 4, posX + 4, posY + 4, fill="blue", tags=("point", name))
        for point in self.master.tmapdata:
            links = point["node"]["edges"]
            position = point["node"]["pose"]["position"]
            posX, posY = tmap.swapToPix(self, position["x"], position["y"])
            for link in links:
                if link != "":
                    self.createNodeLink([posX, posY], link)
        self.mapcanvas.tag_raise("point")

    # Function for plotting a single canvas node connection, used by some other functions
    def createNodeLink(self, pos, link):
        if (self.mapcanvas.find_withtag(link["edge_id"]) == ()):
            nodecon = link["edge_id"]
            nextnode = nodecon.split("_")[1]
            nextpos1, nextpos2 = tmap.getPos(self, nextnode)
            nextposX, nextposY = tmap.swapToPix(self, nextpos1, nextpos2)
            self.mapcanvas.create_line(pos[0], pos[1], nextposX, nextposY, dash=(4, 2), arrow=tk.LAST, tags=("connection",
                                                                                                    str("Connect" +
                                                                                                        nodecon.split("_")[
                                                                                                            0]),
                                                                                                    str("Connect" +
                                                                                                        nodecon.split("_")[
                                                                                                            1]),
                                                                                                    str(nodecon)))

    # Function that changes the users current operating "mode", single mode is for selecting one object either a node
    #   or a location on the canvas, multimode is for selecting two different nodes. When changing modes the function
    #   deselects any currently selected items and reverts them to their natural state
    def changeMode(self, mode):
        if self.master.clickmode != mode:
            self.master.clickmode = mode
            self.mapcanvas.delete("clickspot")
            if self.master.clickeditem != 0:
                item = self.mapcanvas.find_withtag(self.master.clickeditem)
                for x in item:
                    self.mapcanvas.itemconfig(x, fill='blue')
                self.master.clickeditem = 0
            elif self.master.multiclickeditem:
                for x in self.master.multiclickeditem:
                    item = self.mapcanvas.find_withtag(x)
                    for y in item:
                        self.mapcanvas.itemconfig(y, fill='blue')
                self.master.multiclickeditem = []
            self.master.clickedpos = []

    # Function to create a new node on a selected location on the canvas and add to the dictionary as well as plot it on
    #   the canvas and make it the currently selected item. Currently only takes in the x and y coordinates the rest of
    #   the values are hard coded (EXCEPT FOR NAME WHICH IS AUTO GENERATED, MUCH IMPORTANT VERY PRIMARY KEY)
    def addCanvasNode(self, pos):
        if pos != [] and self.master.clickmode == 0:
            self.logging.info(pos)
            posX, posY = pos[0], pos[1]
            metreposX, metreposY = tmap.swapToMetre(self, posX, posY)
            self.logging.info(metreposX)
            self.logging.info(metreposY)
            newnode = tmap.addNode(self, "riseholme", "riseholme", [0.5, 0.6, 0.7, 0.8], [metreposX, metreposY, 0.0])
            node = self.mapcanvas.create_oval(posX - 4, posY - 4, posX + 4, posY + 4, fill="blue", tags=("point", newnode))
            self.mapcanvas.itemconfig(node, fill='red')
            self.master.clickeditem = newnode
            self.displayNodeInfo(newnode, self.master.labels)

    # Function to create a new connection between two selected nodes in the tmap dictionary and to plot the connection
    #   on the canvas, stores the position in the dictionary as metre value then converts to pixels for plotting
    def addCanvasConnection(self, nodes):
        if len(nodes) == 2 and self.master.clickmode == 1:
            tmap.addAction(self, nodes[0], nodes[1])
            posX1, posY1 = tmap.swapToPix(self, tmap.getPos(self, nodes[0])[0], tmap.getPos(self, nodes[0])[1])
            posX2, posY2 = tmap.swapToPix(self, tmap.getPos(self, nodes[1])[0], tmap.getPos(self, nodes[1])[1])
            self.logging.info("posX1:{} posY1:{} posX2:{} posY2:{}".format(posX1,posY1,posX2,posY2))
            self.mapcanvas.create_line(posX1, posY1, posX2, posY2, dash=(4, 2), arrow=tk.LAST, tags=("connection",
                                                                                        str("Connect" + nodes[0]),
                                                                                        str("Connect" + nodes[1]),
                                                                                        str(nodes[0]+"_"+nodes[1])))
            self.mapcanvas.tag_raise("point")

    # Function to delete a connection between two selected nodes and remove that connection from the dictionary, checks
    # both the nodes to see if they have the connection and deletes from both if necessary
    def deleteConnection(self, nodes):
        if len(nodes) == 2 and self.master.clickmode == 1:
            actionVal1 = nodes[0]+"_"+nodes[1]
            actionVal2 = nodes[1]+"_"+nodes[0]
            tmap.deleteAction(self, nodes[0], nodes[1])
            tmap.deleteAction(self, nodes[1], nodes[0])
            self.mapcanvas.delete(str(actionVal1))
            self.mapcanvas.delete(str(actionVal2))

    # Function to delete a node from the tmap dictionary and any associated canvas options
    def deleteCanvasNode(self, node):
        if self.master.clickmode == 0:
            tmap.deleteNode(self, node)
            self.mapcanvas.delete(node)
            self.mapcanvas.delete(str("Connect" + node))

    # Function to update the sidebar labels with the info obtained from the tmap dictionary
    def displayNodeInfo(self, node, labels):
        data = tmap.getDisplayInfo(self, node)

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
    def updateNode(self, labels):
        newPos = [float(labels[2].get()), float(labels[3].get())]
        nodeName = labels[0].get()
        tmap.updatePos(self, nodeName, newPos)
        nodePos = tmap.getNodePos(self, nodeName)
        self.mapcanvas.delete(nodeName)
        self.mapcanvas.delete(str("Connect" + nodeName))
        node = self.mapcanvas.create_oval(newPos[0] - 4, newPos[1] - 4, newPos[0] + 4, newPos[1] + 4, fill="blue", tags=("point", nodeName))
        self.mapcanvas.itemconfig(node, fill='red')
        for link in self.master.tmapdata[nodePos]["node"]["edges"]:
            self.createNodeLink(newPos, link)
        for nodes in self.master.tmapdata:
            for link in nodes["node"]["edges"]:
                nodecon = link["edge_id"]
                if nodecon.split("_")[1] == nodeName:
                    newPos[0], newPos[1] = tmap.swapToPix(self, tmap.getPos(self, nodecon.split("_")[0])[0], tmap.getPos(self, nodecon.split("_")[0])[1])
                    self.createNodeLink(newPos, link)
        self.mapcanvas.tag_raise("point")
