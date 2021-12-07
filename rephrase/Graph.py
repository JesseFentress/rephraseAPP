
from rephrase.Queue import Queue
from rephrase.Stack import Stack


class Graph:

    def __init__(self, graph_dict):
        if graph_dict is None:
            graph_dict

        self.graph_dict = graph_dict

    def generate_edges(self):
        edges = []
        for node in self.graph_dict:
            for neighbour in self.graph_dict[node]:
                edges.append((node, neighbour))
        return edges

    def find_isolated_nodes(self):
        """ returns a list of isolated nodes. """
        isolated = []
        for node in self.graph_dict:
            if not self.graph_dict[node]:
                isolated += node
        return isolated

    def find_path(self, start_vertex, end_vertex, path=None):
        """ find a path from start_vertex to end_vertex in graph """
        if path is None:
            path = []
        path = path + [start_vertex]
        if start_vertex == end_vertex:
            return path
        if start_vertex not in self.graph_dict:
            return None
        for vertex in graph[start_vertex]:
            if vertex not in path:
                extended_path = self.find_path(vertex, end_vertex, path)
                if extended_path:
                    return extended_path
        return None

    def find_all_paths(self, start_vertex, end_vertex, path=[]):
        """ find all paths from start_vertex to
            end_vertex in graph """
        path = path + [start_vertex]
        if start_vertex == end_vertex:
            return [path]
        if start_vertex not in self.graph_dict:
            return []
        paths = []
        for vertex in self.graph_dict[start_vertex]:
            if vertex not in path:
                extended_paths = self.find_all_paths(vertex, end_vertex, path)
                for p in extended_paths:
                    paths.append(p)
        return paths

    def is_connected(self, vertices_encountered=None, start_vertex=None):
        """ determines if the graph is connected """
        if vertices_encountered is None:
            vertices_encountered = set()
        vertices = list(self.graph_dict.keys())  # "list" necessary in Python 3
        if not start_vertex:
            # cho0se a vertex from graph as a starting point
            start_vertex = vertices[0]
        vertices_encountered.add(start_vertex)
        if len(vertices_encountered) != len(vertices):
            for vertex in self.graph_dict[start_vertex]:
                if vertex not in vertices_encountered:
                    if self.is_connected(vertices_encountered, vertex):
                        return True
        else:
            return True
        return False

    def find_shortest_path(self, start, end, path=[]):
        path = path + [start]
        if start == end:
            return path
        shortest = None
        for node in self.graph_dict[start]:
            if node not in path:
                newpath = self.find_shortest_path(node, end, path)
                if newpath:
                    if not shortest or len(newpath) < len(shortest):
                        shortest = newpath
        return shortest

    def is_complete(self):
        keys = list(self.graph_dict.keys())  # List of underlying dictionary keys (vertices)
        edges = []  # Will hold the edges attached to a vertex
        for vertex in self.graph_dict:  # Iterates through every vertex
            for edge in self.graph_dict[vertex]:  # Iterates through every edge
                if edge not in edges:  # If an edge is not already in edges
                    edges.append(edge)  # Add that edge to edges
            if len(edges) == len(keys) - 1:  # If length of edges = length of keys -1, then that vertex is complete
                edges = []  # Reset edges
            else:   # If length is not equal then it cannot be a complete graph
                return False  # Return False because not complete
        return True  # Return True because complete

    def bfs_traversal(self, start_index):  # Prints out BFS traversal
        queue = Queue()  # Holds visited vertices in this queue for printing once their connections are being looked at
        queue.enqueue(start_index)  # Adds start_index to the queue since it is the first visited index
        visited = [start_index]  # List to hold visited indices so that they do not get visited again
        friends = set()
        while not queue.is_Empty():  # As long as there are indices in the queue
            vertex = queue.dequeue()  # Vertex whose edges we want to look at is dequeued from the queue
            friends.add(vertex)  # Print the vertex being looked at
            for edge in self.graph_dict[vertex]:  # For all the connections to the targeted vertex
                if edge not in visited:  # If the connected vertex has not been visited
                    queue.enqueue(edge)  # Add unvisited vertex to queue
                    visited.append(edge)  # Mark the vertex as visited
        return friends

    def bfs(self):
        friends = set()  # Empty set
        for indices in self.graph_dict:  # Iterate through the indices
            friends = friends.union(set(self.bfs_traversal(indices)))  # Perform bfs traversal on all friends to get their friends
        f = list(friends)  # Convert the set to a list to return
        return f  # Return the list


    def dfs_traversal(self, start_vertex):  # Prints out DFS traversal
        stack = Stack()  # Holds vertices that need to be come back to
        stack.push(start_vertex)  # Pushes start_vertex onto the stack
        visited = [start_vertex]  # List t hold visited indices so that they do not get visited again
        while not stack.is_Empty():  # As long as there are vertices to come back to
            vertex = stack.pop()  # Vertex whose edges we want to check is popped from the stack
            print(vertex)  # Prints the looked at vertex
            for edge in self.graph_dict[vertex]:  # For all connections to the targeted vertex
                if edge not in visited:  # If the connected vertex has not already been visited
                    stack.push(edge)  # Push the edge onto the stack to evaluate it
                    visited.append(edge)  # Mark the new index as visited
