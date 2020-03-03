import logging

logger = logging.getLogger("Topological-Navigation-Editor")


class Tmap:
    def __int__(self, master):
        self.master = master


# Function to add an action to an existing node,
# 3 parameters ([node dataset], [name of current node being manipulated],
#   [name of the node being connected to from current node])
# Info needed: action, edge_id, inflation_radius, map_2d, node, recovery_behaviours_config, top_vel
def add_action(self, node_name, node_connection):
    pos = get_node_pos(self, node_name)
    if pos != -1:
        actions_list = self.master.tmapdata[pos]["node"]["edges"]
        if node_connection != "":
            new_edge_id = node_name + "_" + node_connection
        else:
            new_edge_id = node_name
        connection_exists = 0
        for x in range(len(actions_list)):
            if actions_list[x]["edge_id"] == new_edge_id:
                connection_exists = 1
        if connection_exists == 0:
            new_action = {"action": "move_base", "edge_id": new_edge_id, "inflation_radius": "0.0",
                          "map_2d": self.master.tmapdata[pos - 1]["meta"]["map"], "node": node_connection,
                          "recovery_behaviours_config": "", "top_vel": "0.55"}
            actions_list.append(new_action)
            self.master.tmapdata[pos]["node"]["edges"] = actions_list
            logger.info("Connection established between nodes " + node_name + " and " + node_connection)
            logger.info(actions_list)
        else:
            logger.info("Connection already exists between nodes " + node_name + " and " + node_connection)


# Function to add an action to an existing node,
# 3 parameters ([node dataset], [name of current node being manipulated],
#   [name of a node connected to the current node])
def delete_action(self, node_name, node_connection):
    pos = get_node_pos(self, node_name)
    if pos != -1:
        actions_list = self.master.tmapdata[pos]["node"]["edges"]
        edge_id = node_name + "_" + node_connection
        connection_exists, connection_pos = 0, 0
        if len(actions_list) != 0:
            for x in range(len(actions_list)):
                if actions_list[x]["edge_id"] == edge_id:
                    connection_exists = 1
                    connection_pos = x
            if connection_exists == 1:
                del actions_list[connection_pos]
                logger.info("Action removed between nodes " + node_name + " and " + node_connection)
                logger.info(actions_list)
            else:
                logger.info("No action exists between nodes " + node_name + " and " + node_connection)
        else:
            logger.info(node_name + " node has no actions")


# Function to create a new node,
# Info needed: map, pointset, edges(action), orienation[w,x,y,z],
#   position[x,y,z], verts(8x[x,y])
# 6 parameters ([node dataset], [map name], [name of pointset], [orientation as list of 4 values],
#   [position as list of 3 values], [vertices of node as list of 8 lists of 2 values each])
def add_node(self, top_map, point_set, orientation, position):
    name = 1
    name_found, count = 0, 0
    while name_found == 0:
        for points in self.master.tmapdata:
            current_name = points["meta"]["node"].replace("WayPoint", "")
            if int(current_name) != name:
                count += 1
        if count != len(self.master.tmapdata) - 1:
            name_found = 1
        else:
            name += 1
            count = 0
    name = "WayPoint" + str(name)
    meta_dict = {"map": top_map, "node": name, "pointset": point_set}
    ori_dict = {"w": orientation[0], "x": orientation[1], "y": orientation[2], "z": orientation[3]}
    pos_dict = {"x": position[0], "y": position[1], "z": position[2]}
    verts_dict = [{"x": 0.689999997616, "y": 0.287000000477}, {"x": 0.287000000477, "y": 0.490000009537},
                  {"x": -0.287000000477, "y": 0.490000009537}, {"x": -0.689999997616, "y": 0.287000000477},
                  {"x": -0.689999997616, "y": -0.287000000477}, {"x": -0.287000000477, "y": -0.490000009537},
                  {"x": 0.287000000477, "y": -0.490000009537}, {"x": 0.689999997616, "y": -0.287000000477}]
    if len(verts_dict) == 8:
        if len(position) == 3:
            if len(orientation) == 4:
                new_node = {"meta": meta_dict, "node": {"edges": [], "localise_by_topic": "", "map": top_map,
                                                        "name": name, "pointset": point_set,
                                                        "pose": {"orienation": ori_dict, "position": pos_dict},
                                                        "verts": verts_dict,
                                                        "xy_goal_tolerance": "0.3", "yaw_goal_tolerance": "0.1"}}
                self.master.tmapdata.append(new_node)
                logger.info("Node created " + str(name))
                logger.info(new_node)
                return name
            else:
                logger.info("Invalid orientation items")
        else:
            logger.info("Invalid position items")
    else:
        logger.info("Invalid number of vertices")


def update_pos(self, node, new_pos):
    node_pos = get_node_pos(self, node)
    node_data = self.master.tmapdata[node_pos]["node"]["pose"]["position"]
    logger.info("Old position X: {} Y: {}".format(new_pos[0], new_pos[1]))
    metre_pos_x, metre_pos_y = swap_to_metre(self, new_pos[0], new_pos[1])
    node_data["x"], node_data["y"] = metre_pos_x, metre_pos_y
    logger.info("Position updated to X:{} Y:{}".format(metre_pos_x, metre_pos_y))


# Function to delete a node
# 2 parameters ([node dataset], [name of node to be deleted])
def delete_node(self, node_name):
    pos = get_node_pos(self, node_name)
    if pos != -1:
        del self.master.tmapdata[pos]
        for nodes in self.master.tmapdata:
            for link in nodes["node"]["edges"][:]:
                if link != "":
                    node_connection = link["edge_id"]
                    if node_connection.split("_")[1] == node_name:
                        nodes["node"]["edges"].remove(link)
                        self.logging.info("ACTIONS: {}".format(nodes["node"]["edges"]))
        logger.info(node_name + " deleted")


# Function to find node location in array,
#   2 parameters ([node dataset], [name of the node])
def get_node_pos(self, node_name):
    pos, count = -1, 0
    while count < len(self.master.tmapdata):
        if self.master.tmapdata[count]["meta"]["node"] == node_name:
            pos = count
        count += 1
    if pos != -1:
        return pos
    else:
        logger.info("Position not found for node " + node_name)
        return pos


def get_pos(self, node):
    for point in self.master.tmapdata:
        if point["meta"]["node"] == node:
            pos = point["node"]["pose"]["position"]
            return pos["x"], pos["y"]


# Converts the X and Y metre values from the node into pixel values for displaying on cavas
# Returns 2 values
def swap_to_px(self, pos1, pos2):
    pos1 = (pos1 - self.master.yaml_data["origin"][0]) / self.master.yaml_data["resolution"]
    pos2 = self.master.pgm["height"] - (
            (pos2 - self.master.yaml_data["origin"][1]) / self.master.yaml_data["resolution"])
    return pos1, pos2


# Converts the X and Y pixel values from the node into metre values for storing in file
# Returns 2 values
def swap_to_metre(self, pos1, pos2):
    pos1 = (float(pos1) * self.master.yaml_data["resolution"]) + self.master.yaml_data["origin"][0]
    pos2 = ((self.master.pgm["height"] - float(pos2)) * self.master.yaml_data["resolution"]) + \
           self.master.yaml_data["origin"][1]
    return pos1, pos2


def get_display_info(self, node):
    pos = get_node_pos(self, node)
    node = self.master.tmapdata[pos]
    pos_x, pos_y = swap_to_px(self, node["node"]["pose"]["position"]["x"], node["node"]["pose"]["position"]["y"])
    info_packet = {"name": node["meta"]["node"], "set": node["meta"]["pointset"], "x": pos_x, "y": pos_y,
                   "z": node["node"]["pose"]["position"]["z"]}
    return info_packet


def print_node_names(data):
    nodes = []
    for x in range(len(data)):
        nodes.append(data[x]["meta"]["node"])
    logger.info(nodes)


def print_node(data, node):
    pos = get_node_pos(data, node)
    if pos != -1:
        logger.info(data[pos])
