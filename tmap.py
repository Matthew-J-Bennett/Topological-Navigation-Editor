import logging

logger = logging.getLogger("Topological-Navigation-Editor")

# Function to add an action to an existing node,
# 3 parameters ([node dataset], [name of current node being manipulated],
#   [name of the node being connected to from current node])
# Info needed: action, edge_id, inflation_radius, map_2d, node, recovery_behaviours_config, top_vel
def addAction(data, nodename, nodeconnection):
    pos = getNodePos(data, nodename)
    if pos != -1:
        actionslist = data[pos]["node"]["edges"]
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
                             "map_2d": data[pos - 1]["meta"]["map"], "node": nodeconnection,
                             "recovery_behaviours_config": "", "top_vel": "0.55"}
            actionslist.append(newaction)
            logger.info("Connection established between nodes "+nodename+" and "+nodeconnection)
            logger.info(actionslist)
        else:
            logger.info("Connection already exists between nodes "+nodename+" and "+nodeconnection)
    return data


# Function to add an action to an existing node,
# 3 parameters ([node dataset], [name of current node being manipulated],
#   [name of a node connected to the current node])
def deleteAction(data, nodename, nodeconnection):
    pos = getNodePos(data, nodename)
    if pos != -1:
        actionslist = data[pos]["node"]["edges"]
        edge_id = nodename + "_" + nodeconnection
        connectionexists, connectionpos = 0, 0
        if len(actionslist) != 0:
            for x in range(len(actionslist)):
                if actionslist[x]["edge_id"] == edge_id:
                    connectionexists = 1
                    connectionpos = x
            if connectionexists == 1:
                del actionslist[connectionpos]
                logger.info("Action removed between nodes "+nodename+" and "+nodeconnection)
                logger.info(actionslist)
            else:
                logger.info("No action exists between nodes "+nodename+" and "+nodeconnection)
        else:
            logger.info(nodename+" node has no actions")
    return data


# Function to create a new node,
# Info needed: map, node, pointset, edges(action), orienation[w,x,y,z],
#   position[x,y,z], verts(8x[x,y])
# 7 parameters ([node dataset], [map name], [new name of node], [name of pointset], [orientation as list of 4 values],
#   [position as list of 3 values], [vertices of node as list of 8 lists of 2 values each])
def addNode(data, map, node, pointset, orientation, position, verts):
    metadict = {"map": map, "node": node, "pointset": pointset}
    oridict = {"w": orientation[0], "x": orientation[1], "y": orientation[2], "z": orientation[3]}
    posdict = {"x": position[0], "y": position[1], "z": position[2]}
    vertsdict = []
    if len(verts) == 8:
        if len(position) == 3:
            if len(orientation) == 4:
                for x in range(8):
                    vertsdict.append({"x": verts[x][0], "y": verts[x][1]})
                newnode = {"meta": metadict, "node": {"edges": []}, "localise_by_topic": "", "map": map, "name": node,
                               "pointset": pointset, "pose": {"orienation": oridict, "position": posdict}, "verts": vertsdict,
                               "xy_goal_tolerance": "0.3", "yaw_goal_tolerance": "0.1"}
                data.append(newnode)
                logger.info("Node created "+node)
                logger.info(newnode)
            else:
                logger.info("Invalid orientation items")
        else:
            logger.info("Invalid position items")
    else:
        logger.info("Invalid number of vertices")
    return data


# Function to delete a node
# 2 parameters ([node dataset], [name of node to be deleted])
def deleteNode(data, nodename):
    pos = getNodePos(data, nodename)
    if pos != -1:
        del data[pos]
        logger.info(nodename+" deleted")
    return data


# Function to find node location in array,
#   2 parameters ([node dataset], [name of the node])
def getNodePos(data, nodename):
    pos, count = -1, 0
    while count < len(data):
        if data[count]["meta"]["node"] == nodename:
            pos = count
        count += 1
    if pos != -1:
        return pos
    else:
        logger.info("Position not found for node " + nodename)
        return pos

def printNodeNames(data):
    nodes = []
    for x in range(len(data)):
        nodes.append(data[x]["meta"]["node"])
    logger.info(nodes)

def printNode(data,node):
    pos = getNodePos(data,node)
    if pos != -1:
        logger.info(data[pos])