# Jack Huffman and Nathaniel Li
# CS252 Algorithms
# Binary Space Partitioning Implementation in 2D
# To install networkx library (py -m pip install numpy, networkx)
import numpy as np
from graphics import *
import matplotlib.pyplot as plt
from time import sleep

# GLOBAL CONFIG VARIABLES
scale_factor = 50
sleep_time = 0.4
click_through = False

# This is a simple implementation of a binary tree
class Binary_Tree:
    def __init__(self):
        self.back = None
        self.front = None
        self.scene = None

    def __init__(self, scene):
        self.back = None
        self.front = None
        self.scene = scene

    def set_front(self, tree):
        self.front = tree

    def set_back(self, tree):
        self.back = tree

    def printInorder(self, root):
        if root:
            # First recur on back child
            self.printInorder(root.back)

            # Then print the data of node
            print("Scene Edges:")
            for i in range(len(root.scene.edges)):
                point_1, point_2 = root.scene.get_edge(i)
                print("({}, {})".format(point_1, point_2))

            # Now recur on front child 
            self.printInorder(root.front)   

# 2D scene described by list of lines. Similar to the .obj file format, but in 2D
class Scene:
    def __init__(self, vertices, edges):
        self.vertices = np.array(vertices)
        self.edges = np.array(edges)

    def get_vertices(self):
        return self.vertices
    
    def add_vertex(self, point):
        self.vertices = np.append(self.vertices, [point], axis = 0)
        return len(self.vertices) - 1
    
    def add_edge(self, edge):
        self.edges = np.append(self.edges, [edge], axis = 0)

    # Return coordinates of endpoints as two lists
    def get_edge(self, index):
        point_1 = self.vertices[self.edges[index][0]]
        point_2 = self.vertices[self.edges[index][1]]
        return point_1, point_2

# Split any lines cut by the bisecting edge 
# Math used based on this description: 
# https://stackoverflow.com/questions/563198/how-do-you-detect-where-two-line-segments-intersect
def intersect(scene, bisecting_edge_ind):
    vectors = scene.vertices[scene.edges[:,1]] - scene.vertices[scene.edges[:,0]]
    b_point = scene.get_edge(bisecting_edge_ind)[0] # q
    b_vec = vectors[bisecting_edge_ind] # s
    for i in range(len(vectors)):
        point = scene.get_edge(i)[0] # p
        vector = vectors[i] # r

        numerator = np.cross((b_point - point), b_vec) # (q - p) x s
        denominator = np.cross(vector, b_vec) # (r x s)
        if not np.isclose(denominator, 0):
            # the lines intersect
            t = numerator / denominator # ((q - p) x s) / (r x s)
            if 0 < t < 1:
                intersection = point + t * vector
                intersection_vertex_index = scene.add_vertex(intersection)
                second_point = scene.edges[i][1]
                scene.edges[i][1] = intersection_vertex_index
                scene.add_edge([intersection_vertex_index, second_point])   


# Bisect scene along a line.
def bisect(input_scene, line):
    intersect(input_scene, bisecting_edge_ind = line)

    colinear_edges = []
    front_edges = []
    back_edges = []

    line_point_1, line_point_2 = input_scene.get_edge(line)

    for i in range(len(input_scene.edges)):
        point_1, point_2 = input_scene.get_edge(i)

        # Check if both endpoints of the edge are on the same side of the line
        side_1 = np.cross(line_point_2 - line_point_1, point_1 - line_point_1)
        side_2 = np.cross(line_point_2 - line_point_1, point_2 - line_point_1)

        if side_1 > 0 and side_2 > 0:
            # The edge is to the front of the line
            front_edges.append(input_scene.edges[i])
        elif side_1 < 0 and side_2 < 0:
            # The edge is to the back of the line
            back_edges.append(input_scene.edges[i])
        else:
            # Check if the edge is colinear with the line
            if np.isclose(side_1, 0) and np.isclose(side_2, 0):
                # Both endpoints are on the line segment
                colinear_edges.append(input_scene.edges[i])
            elif np.isclose(side_1, 0):
                # Endpoint 1 lies on the line segment
                if side_2 > 0:
                    front_edges.append(input_scene.edges[i])
                else:
                    back_edges.append(input_scene.edges[i])
            elif np.isclose(side_2, 0):
                # Endpoint 2 lies on the line segment
                if side_1 > 0:
                    front_edges.append(input_scene.edges[i])
                else:
                    back_edges.append(input_scene.edges[i])

    back_scene = Scene(input_scene.get_vertices(), back_edges)
    colinear_scene = Scene(input_scene.get_vertices(), colinear_edges)
    front_scene = Scene(input_scene.get_vertices(), front_edges)

    return back_scene, colinear_scene, front_scene

# Recursive calling which generates the BSP tree
def generate_bsp(scene):
    rng = np.random.default_rng(12345)
    rints = rng.integers(low=0, high=len(scene.edges), size=1)
    back, center, front = bisect(scene, rints[0])
    tree = Binary_Tree(scene = center)
    if len(back.edges) != 0: 
        tree.set_back(generate_bsp(back))  
    if len(front.edges) != 0:
        tree.set_front(generate_bsp(front))  
    return tree

# Draws the lines of a scene onto the window. The lines can be drawn in any order because they are colinear
def render_scene(scene, win, color="black"):
    edges = scene.edges
    for i in range(len(edges)):
        if click_through:
            win.getMouse()
        else:
            sleep(sleep_time)
        p1, p2 = scene.get_edge(i)
        line = Line(Point(p1[0]*scale_factor, p1[1]*scale_factor), Point(p2[0]*scale_factor, p2[1]*scale_factor))
        line.setFill(color)
        line.draw(win) 
    
# Calculates the relative position of a view point and the edge
def relative_position(scene, viewpoint):
    # Since all the edges of a scene within the BSP are colinear, only one 
    # edge of the scene needs to be tested against. In other words, a viewpoint in 
    # front of one edge will be in front of all the other edges of a scene, and so on.
    p1, p2 = scene.get_edge(0)

    side_1 = np.cross(p2 - p1, viewpoint - p1) 
    
    if np.isclose(side_1, 0):
        # On
        return 0
    elif side_1 > 0:
        # Back
        return -1
    else:
        # Front
        return 1

# Recursive algorithm to traverse the tree in such a way as to mimic painter's algorithm
def traverse(bsp_tree, viewpoint, win):
    if bsp_tree == None:
        return
    
    position = relative_position(bsp_tree.scene, viewpoint)
    
    if position < 0:
        # back, middle, front
        traverse(bsp_tree.back, viewpoint, win)
        render_scene(bsp_tree.scene, win, color="black")
        traverse(bsp_tree.front, viewpoint, win)
        
    elif position > 0:
        # front, middle, back
        traverse(bsp_tree.front, viewpoint, win)
        render_scene(bsp_tree.scene, win, color="black")
        traverse(bsp_tree.back, viewpoint, win)
       
    else: 
        # front, back, middle?
        traverse(bsp_tree.front, viewpoint, win)
        traverse(bsp_tree.back, viewpoint, win)
        # The below edges are technically invisible to the viewer since they are collinear with the view
        # However, we render them since we have a bird's eye view of the scene
        render_scene(bsp_tree.scene, win, color="black") 

# Helper function to clear the window to better visualize
def clear(win):
    for item in win.items[:]:
        item.undraw()
    win.update()

def main():
    # # This code renders the points which represent the doom logo, uncomment it to produce BSP rendering of Doom logo
    segments = np.loadtxt("points.csv")
    for i in range(1, len(segments), 2):
        segments[i] = -(segments[i] - 15)

    # # Run a basic test to test parallel lines being rendered correctly
    # segments = np.loadtxt("test_parallel_lines.csv")
    
    # # Runs a basic test that can be simply walked through to understand BSP, referenced
    # segments = np.loadtxt("test_points.csv")
    
    # Runs a more complex test which renders a scenario with a more complex shape and more points
    # segments = np.loadtxt("test_more_points.csv")


    vertices = segments.reshape((-1, 2))
    edges = []
    for i in range(0, np.shape(vertices)[0], 2):
        edges.append([i, i+1])
    scene = Scene(vertices, edges)
    tree = generate_bsp(scene)

    window_width = scale_factor * 20
    window_height = scale_factor * 20
    win = GraphWin("BSP Tree", window_width, window_height)

    for i in range(10):
        view_x = np.random.randint(0, 9)
        view_y = np.random.randint(0, 9)
        v_point = [view_x, view_y]
        v_point_graphics = Point(v_point[0] * scale_factor, v_point[1] * scale_factor)
        v_circle = Circle(v_point_graphics, 3)
        v_circle.draw(win)
        traverse(tree, v_point, win)
        sleep(1)
        clear(win)
    
    win.getMouse()
    win.close()

if __name__ == "__main__":
    main()