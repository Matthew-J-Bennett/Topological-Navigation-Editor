import logging

logger = logging.getLogger("Topological-Navigation-Editor")


class Tmap:
    def __int__(self, master):
        self.master = master


# Function to add an action to an existing node,
# 3 parameters ([node dataset], [name of current node being manipulated],
#   [name of the node being connected to from current node])
# Info needed: action, edge_id, inflation_radius, map_2d, node, recovery_behaviours_config, top_vel
def addAction(self, nodename, nodeconnection):
    pos = getNodePos(self, nodename)
    if pos != -1:
        actionslist = self.master.tmapdata[pos]["node"]["edges"]
        if nodeconnection != "":
            newedge_id = nodename + "_" + nodeconnection
        else:
            newedge_id = nodename
        connectionexists = 0
        for x in range(len(actionslist)):
            if actionslist[x]["edge_id"] == newedge_id:
                connectionexists = 1
        if connectionexists == 0:
            newaction = {"action": "move_base", "edge_id": newedge_id, "inflation_radius": "0.0",
                         "map_2d": self.master.tmapdata[pos - 1]["meta"]["map"], "node": nodeconnection,
                         "recovery_behaviours_config": "", "top_vel": "0.55"}
            actionslist.append(newaction)
            self.master.tmapdata[pos]["node"]["edges"] = actionslist
            logger.info("Connection established between nodes " + nodename + " and " + nodeconnection)
            logger.info(actionslist)
        else:
            logger.info("Connection already exists between nodes " + nodename + " and " + nodeconnection)


# Function to add an action to an existing node,
# 3 parameters ([node dataset], [name of current node being manipulated],
#   [name of a node connected to the current node])
def deleteAction(self, nodename, nodeconnection):
    pos = getNodePos(self, nodename)
    if pos != -1:
        actionslist = self.master.tmapdata[pos]["node"]["edges"]
        edge_id = nodename + "_" + nodeconnection
        connectionexists, connectionpos = 0, 0
        if len(actionslist) != 0:
            for x in range(len(actionslist)):
                if actionslist[x]["edge_id"] == edge_id:
                    connectionexists = 1
                    connectionpos = x
            if connectionexists == 1:
                del actionslist[connectionpos]
                logger.info("Action removed between nodes " + nodename + " and " + nodeconnection)
                logger.info(actionslist)
            else:
                logger.info("No action exists between nodes " + nodename + " and " + nodeconnection)
        else:
            logger.info(nodename + " node has no actions")


# Function to create a new node,
# Info needed: map, pointset, edges(action), orienation[w,x,y,z],
#   position[x,y,z], verts(8x[x,y])
# 6 parameters ([node dataset], [map name], [name of pointset], [orientation as list of 4 values],
#   [position as list of 3 values], [vertices of node as list of 8 lists of 2 values each])
def addNode(self, topmap, pointset, orientation, position):
    name = 1
    namefound, count = 0, 0
    while namefound == 0:
        for points in self.master.tmapdata:
            current_name = points["meta"]["node"].replace("WayPoint", "")
            if int(current_name) != name:
                count += 1
        if count != len(self.master.tmapdata)-1:
            namefound = 1
        else:
            name += 1
            count = 0
    name = "WayPoint" + str(name)
    metadict = {"map": topmap, "node": name, "pointset": pointset}
    oridict = {"w": orientation[0], "x": orientation[1], "y": orientation[2], "z": orientation[3]}
    posdict = {"x": position[0], "y": position[1], "z": position[2]}
    vertsdict = [{"x":0.689999997616, "y":0.287000000477}, {"x":0.287000000477, "y":0.490000009537},
                 {"x":-0.287000000477, "y":0.490000009537}, {"x":-0.689999997616, "y":0.287000000477},
                 {"x":-0.689999997616, "y":-0.287000000477}, {"x":-0.287000000477, "y":-0.490000009537},
                 {"x":0.287000000477, "y":-0.490000009537} , {"x":0.689999997616, "y":-0.287000000477}]
    if len(vertsdict) == 8:
        if len(position) == 3:
            if len(orientation) == 4:
                newnode = {"meta": metadict, "node": {"edges": [], "localise_by_topic": "", "map": topmap,
                           "name": name, "pointset": pointset, "pose": {"orienation": oridict, "position": posdict},
                           "verts": vertsdict,
                           "xy_goal_tolerance": "0.3", "yaw_goal_tolerance": "0.1"}}
                self.master.tmapdata.append(newnode)
                logger.info("Node created " + str(name))
                logger.info(newnode)
                return name
            else:
                logger.info("Invalid orientation items")
        else:
            logger.info("Invalid position items")
    else:
        logger.info("Invalid number of vertices")

def updatePos(self, node, newPos):
    nodePos = getNodePos(self, node)
    nodeData = self.master.tmapdata[nodePos]["node"]["pose"]["position"]
    logger.info("Old position X: {} Y: {}".format(newPos[0], newPos[1]))
    metrePosX, metrePosY = swapToMetre(self, newPos[0], newPos[1])
    nodeData["x"], nodeData["y"] = metrePosX, metrePosY
    logger.info("Position updated to X:{} Y:{}".format(metrePosX, metrePosY))

# Function to delete a node
# 2 parameters ([node dataset], [name of node to be deleted])
def deleteNode(self, nodename):
    pos = getNodePos(self, nodename)
    if pos != -1:
        del self.master.tmapdata[pos]
        for nodes in self.master.tmapdata:
            for link in nodes["node"]["edges"][:]:
                if link != "":
                    nodecon = link["edge_id"]
                    if nodecon.split("_")[1] == nodename:
                        nodes["node"]["edges"].remove(link)
                        self.logging.info("ACTIONS: {}".format(nodes["node"]["edges"]))
        logger.info(nodename + " deleted")


# Function to find node location in array,
#   2 parameters ([node dataset], [name of the node])
def getNodePos(self, nodename):
    pos, count = -1, 0
    while count < len(self.master.tmapdata):
        if self.master.tmapdata[count]["meta"]["node"] == nodename:
            pos = count
        count += 1
    if pos != -1:
        return pos
    else:
        logger.info("Position not found for node " + nodename)
        return pos


def getPos(self, node):
    for point in self.master.tmapdata:
        if point["meta"]["node"] == node:
            pos = point["node"]["pose"]["position"]
            return pos["x"], pos["y"]

def swapToPix(self, node):
    pos1, pos2 = node["node"]["pose"]["position"]["x"], node["node"]["pose"]["position"]["y"]
    pos1 = (pos1-self.master.yamldata["origin"][0])/self.master.yamldata["resolution"]
    pos2 = self.master.pgm["height"] - ((pos2-self.master.yamldata["origin"][1])/self.master.yamldata["resolution"])
    return pos1, pos2

# Converts the X and Y metre values from the node into pixel values for displaying on cavas
# Returns 2 values
def swapToPix(self, pos1, pos2):
    pos1 = (pos1-self.master.yamldata["origin"][0])/self.master.yamldata["resolution"]
    pos2 = self.master.pgm["height"] - ((pos2-self.master.yamldata["origin"][1])/self.master.yamldata["resolution"])
    return pos1, pos2

def swapToMetre(self, node):
    pos1, pos2 = node["node"]["pose"]["position"]["x"], node["node"]["pose"]["position"]["y"]
    pos1 = (pos1*self.master.yamldata["resolution"])+self.master.yamldata["origin"][0]
    pos2 = ((self.master.pgm["height"]-pos2)*self.master.yamldata["resolution"])+self.master.yamldata["origin"][1]
    return pos1, pos2

# Converts the X and Y pixel values from the node into metre values for storing in file
# Returns 2 values
def swapToMetre(self, pos1, pos2):
    pos1 = (float(pos1)*self.master.yamldata["resolution"])+self.master.yamldata["origin"][0]
    pos2 = ((self.master.pgm["height"]-float(pos2))*self.master.yamldata["resolution"])+self.master.yamldata["origin"][1]
    return pos1, pos2

def getDisplayInfo(self, node):
    pos = getNodePos(self, node)
    node = self.master.tmapdata[pos]
    posX, posY = swapToPix(self, node["node"]["pose"]["position"]["x"], node["node"]["pose"]["position"]["y"])
    infoPacket = {"name": node["meta"]["node"], "set": node["meta"]["pointset"], "x": posX, "y": posY,
                  "z": node["node"]["pose"]["position"]["z"]}
    return infoPacket

def printNodeNames(data):
    nodes = []
    for x in range(len(data)):
        nodes.append(data[x]["meta"]["node"])
    logger.info(nodes)


def printNode(data, node):
    pos = getNodePos(data, node)
    if pos != -1:
        logger.info(data[pos])
