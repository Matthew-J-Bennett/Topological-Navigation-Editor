class Tmap():
    def __init__(self, map, pointset):
        self.map = map
        self.pointset = pointset
        self.nodelist = []
        self.nodes = []
        self.nodetotal = 0

    def addNode(self, nodename, node):
        self.nodelist.append(nodename)
        self.nodes.append(node)
        self.nodetotal = len(self.nodelist)


class Node(Tmap):
    def __init__(self, map, name, pointset, edges, pose, xy, yaw):
        self.map = map
        self.name = name
        self.pointset = pointset
        self.edges = edges
        self.pose = pose
        self.verts = []
        self.xy_goal_tolerance = xy
        self.yaw_goal_tolerance = yaw
        super()
