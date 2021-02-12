from queue import PriorityQueue
import math

# Vertex data structure holds square and incident edges for a node
class Vertex:
    def __init__(self, square):
        self.square = square
        self.edges = []
        
    # add edge to list of edges for this node
    # edge = (neighbor, distance)
    def add_edge(self, n, dist):
        self.edges.append((n, dist))

# Uniform Cost Search
# returns solution path, cost, and number of nodes visited
def ucs(graph, source, dest):
    closed = set()
    fringe = PriorityQueue()
    # priority queue holds cost, node ID, and path to that node
    
    fringe.put((0, source, [source])) # start with source node
    
    while True:
        # if fringe is empty return failure
        if fringe.empty():
            return [], 0, len(closed)
        
        # remove least cost node from fringe
        cost, node, path = fringe.get()
        closed.add(node) # add to closed set
        
        # if goal then return solution
        if node == dest:
            return path, cost, len(closed)
        
        # add non-visited neighbors to fringe
        for i in graph[node].edges:
             if i[0] not in closed:
                g = cost + i[1] #backward cost
                fringe.put((g, i[0], path + [i[0]]))

# A* Search
# returns solution path, cost, and number of nodes visited
def a_star(graph, source, dest):
    closed = set()
    fringe = PriorityQueue()
    # priority queue holds cost, node ID, and path to that node
    
    fringe.put((0, source, [source])) # start with source node
    
    while True:
        # if fringe is empty return failure
        if fringe.empty():
            return [], 0, len(closed)
        
        # remove least cost node from fringe
        cost, node, path = fringe.get()
        closed.add(node) # add to closed set
        
        # since we use g+h as cost in queue
        # remove cost of heuristic to get just g
        # unless it is source node (h not calculated for source)
        if node != source:
            cost = cost - heuristic(node, dest, graph)
            
        # if goal then return solution
        if node == dest:
            return path, cost, len(closed)
        
        # add non-visited neighbors to fringe
        for i in graph[node].edges:
            n = i[0] # neighbor id
            if n not in closed:
                g = cost + i[1] # backward cost
                h = heuristic(n, dest, graph) # forward cost
                fringe.put((g+h, n, path + [n]))

# find distance from node to dest based on heuristic
# using estimated euclidian distance
def heuristic(node, dest, graph):
    #find row and column number with a 10x10 board
    n_square = graph[node].square
    n_row = n_square//10
    n_column = n_square%10
    
    d_square = graph[dest].square
    d_row = d_square//10
    d_column = d_square%10
    
    # find number of rows and columns apart
    column_dist = d_column - n_column
    row_dist = d_row - n_row
    
    # since we don't know exact location of node,
    # node location could be at very edge of square
    # so subtract 1 from column and row distances
    # except when distance is already 0
    r = 0; c = 0    
    if column_dist != 0:
        c = abs(column_dist) - 1
    if row_dist != 0:
        r = abs(row_dist) - 1
        
    # assuming squares are 100 by 100 units
    r *= 100; c *= 100
        
    # return sqrt((x2-x1)^2 + (y2-y1)^2)
    return math.sqrt(c**2 + r**2)
    



graph = {} # dictionary of vertices, id : Vertex

# read in graph from input file
f = input("file name: ")
with open(f, 'r') as file:
    # add vertices
    while True:
        line = file.readline()
        if line.startswith('#'):   # skip comments
            continue
        if len(line) == 1:         # breaks at empty line
            break                  # which is end of vertices 
        
        data = line.split(',')     # data = Vertex ID, Square ID
        ID = int(data[0]); square = int(data[1])
        # add new Vertex to dictionary
        graph[ID] = Vertex(square)
    
    # add edges
    while True:
        line = file.readline()
        if line.startswith('#'):   # skip comments
            continue
        if len(line) == 1:         # breaks at empty line
            break                  # which is end of edges 
        
        data = line.split(',')     # data = From, To, Distance  
        fr = int(data[0]); to = int(data[1]); dist = int(data[2])
        # add edge to both From and To Vertex
        graph[fr].add_edge(to, dist)
        graph[to].add_edge(fr, dist)
        
    # get start and end points
    while line:
        line = file.readline()
        data = line.split(',')
        if data[0] == 'S':
            source = int(data[1])
        if data[0] == 'D':
            dest = int(data[1])
           
# Run UCS
solution, cost, count = ucs(graph, source, dest)
if len(solution) == 0: solution = "no solution" # failure
print("Uniform Cost Search")

# print solution and cost
# number of visited nodes as comparison of informed/uninformed
print("\tsolution: %s\n\tcost: %s\n\t%s nodes visited"
      %(solution, cost, count))

# Run A*
solution, cost, count = a_star(graph, source, dest)
if len(solution) == 0: solution = "no solution" # failure
print("A* Search")
print("\tsolution: %s\n\tcost: %s\n\t%s nodes visited"
      %(solution, cost, count))
