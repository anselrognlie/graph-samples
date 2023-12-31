COLORS = ["red", "green"]

def dfs(dislikes, current_node, painted_graph, current_color):
    neighbors = dislikes[current_node]
    next_color = (current_color + 1) % len(COLORS)

    for neighbor in neighbors:
        color = painted_graph.get(neighbor)

        if not color:
            painted_graph[neighbor] = COLORS[next_color]
            if not dfs(dislikes=dislikes, current_node=neighbor, painted_graph=painted_graph, current_color=next_color):
                return False
        elif color != COLORS[next_color]:
            return False
    
    return True

# learn implementation for detecting a bipartite graph
# for each node (to handle disconnected graphs), perform a dfs that colors each
# visited node in alternating colors. As soon as we can find a conflict
# (adjacent nodes with the same color) we know this is not colorable with 2 colors.
# NOTE: this observation would not apply to graph colors with k > 2, which require
# backtracking to check other variants.

# def possible_bipartition(dislikes):
#     painted_graph = {}
#     current_color = 0

#     for node in dislikes.keys():
#         neighbors = dislikes[node]
#         if not painted_graph.get(node):
#             painted_graph[node] = COLORS[current_color]

#             if not dfs(dislikes=dislikes, current_node=node, painted_graph=painted_graph, current_color=current_color):
#                 return False
#     return True


def color_dfs(adj, node, colors, num_colors):
    work = colors.copy()
    if node in work:
       return work
    
    coloration = None
    neighbor_colors = set(work.get(n) for n in adj[node])
    node_work = work
    for color in range(num_colors):
        found_coloration = True
        if color not in neighbor_colors:
            work[node] = color
            print("descend")
            print(work)
            for neighbor in adj[node]:
                coloration = color_dfs(adj, neighbor, work, num_colors)
                if coloration is None:
                    # could not color neighbors with current color
                    work = node_work  # throw away any work done on the neighbors
                    print("backtrack")
                    print(work)
                    found_coloration = False
                    break
                else:
                    work = coloration

            if found_coloration:
                # if we find a coloration for all neighbors, then we have colored
                # everything reachable from this node and we're done
                return work            

    return coloration

# an arbitrary dfs-based graph coloring approach, which can be used to solve
# bipartitioning, as well as more general coloring (maps, schedules, etc). This
# is accomplished by using backtracking to undo a step that leads to an uncolorable
# arrangement. When such an arrangement is found, it is not sufficient solely to 
# pop the current node from the color data, as a prior neighbor "branch" could 
# have already been colored, such that artificial restrictions are placed on the
# next color we attempt (test_challenge_spur_3 presents a graph that exhibits this
# issue, "locking in" a failed coloration such that even after backtracking, a
# coloration cannot be found), so we need to restore the entire color map to what
# it was when we entered this call. The easiest way to do this is by making a local
# copy of the color info (leading to unfavorable space requirements). Alternatively,
# we could track the traversed path through the graph and use that to roll back 
# any color values that were made post coloration of the current node. In the end,
# there is little benefit to using the edge relationships for the coloring, as we
# are still making local decisions about the colors that could lead to conflicts
# further on, just as with the canonical coloring approach.

# def find_coloration(adj, num_colors):
#     colors = {}
#     coloration = {}

#     for node in adj.keys():
#         coloration = color_dfs(adj, node, colors, num_colors)
#         if coloration is None:
#             return None
#         else:
#             colors = coloration
        
#     print(coloration)
#     return coloration

    


def possible_bipartition(dislikes):
    coloration = find_coloration(dislikes, 2)
    return coloration is not None

def find_coloration_impl(adj, keys, node_idx, colors, num_colors):
    if node_idx == len(keys):
        return colors
    
    node = keys[node_idx]
    colors[node] = -1
    for color in range(num_colors):
        neighbors = adj[node]
        neighbor_colors = set(colors.get(n) for n in neighbors)
        if color not in neighbor_colors:
            colors[node] = color
            coloration = find_coloration_impl(adj, keys, node_idx + 1, colors, num_colors)
            if coloration:
                return coloration
            
    # no valid color
    colors.pop(node)
    return None

# a more typical map coloring approach which visits nodes in a fixed, arbitrary
# order (here, order of the nodes in the graph structure) rather than using
# edges to traverse. because there is a linear path through the nodes, when
# backtracking, only the current node needs to be undone (no side branches)
def find_coloration(adj, num_colors):
    colors = {}

    keys = list(adj.keys())
    coloration = find_coloration_impl(adj, keys, 0, colors, num_colors)
    if coloration is None:
        return None
        
    print(coloration)
    return coloration


# constants representing the walls and corridor
MAZE_WALL = "#"
MAZE_CORRIDOR = " "

# # Builds an adjacency-list based graph from a grid-based maze representation
# # starting from a supplied (row, column) location.
# # The start location isn't strictly necessary to build the graph, but it
# # saves us from needing to find a corridor space to kick off the rest of the
# # process from.
# # Note how similar this process is to a bfs/dfs of a more typical graph. This
# # illustrates that a grid really can be viewed as a kind of graph with
# # implicit edges between adjacent cells. Using a pending list is a useful way
# # to keep track of the cells left to visit. In this case, we don't need a
# # separate visited list, since adding the location as a key in the adjacency
# # list allows us to check whether we've already visited that location.
# def convert_maze_to_graph(maze, start):
#     graph = {}
#     pending = set([start])  # use a set for the pending list since we don't
#                             # particularly care about the order of visitation
#                             # (a python set will behave more like a queue than
#                             # a stack), but do want to avoid enqueuing the same
#                             # location multiple times.

#     while pending:
#         next = pending.pop()
#         if next in graph:
#             # skip this location if it was already visited
#             continue

#         # Which directions can we move in?
#         # Check each of the 4 locations by using a delta row and delta column
#         # pair. Delta typically refers to a change in a value, so here, dr is
#         # the delta row, the change in value of the row, and dc is the delta
#         # column, the change in value of the column.
#         directions = []
#         for dr, dc in ((-1, 0), (0, 1), (1, 0), (0, -1)):
#             loc = (next[0] + dr, next[1] + dc)  # calculate the offset location

#             # Use a helper to get the location value, treating invalid locations
#             # (outside the grid) as though they were walls
#             if cell_lookup(maze, loc[0], loc[1]) == MAZE_CORRIDOR:
#                 # Add this computed location to the valid directions from the
#                 # initial location
#                 directions.append(loc)
#                 if loc not in graph:
#                     pending.add(loc)

#         graph[next] = directions

#     return graph

# Builds an adjacency-list based graph from a grid-based maze representation.
def convert_maze_to_graph(maze):
    graph = {}

    # iterate over all the cells in the grid
    for r in range(len(maze)):
        for c in range(len(maze[0])):
            # skip this cell if it's not a corridor
            if maze[r][c] != MAZE_CORRIDOR:
                continue

            cell = (r, c)

            # Which directions can we move in?
            # Check each of the 4 locations by using a delta row and delta 
            # column pair. Delta typically refers to a change in a value, so 
            # here, dr is the delta row, the change in value of the row, and dc 
            # is the delta column, the change in value of the column.
            directions = []
            for dr, dc in ((-1, 0), (0, 1), (1, 0), (0, -1)):
                loc = (cell[0] + dr, cell[1] + dc)  # neighbor location

                # Use a helper to get the location value, treating invalid 
                # locations (outside the grid) as though they were walls
                if cell_lookup(maze, loc[0], loc[1]) == MAZE_CORRIDOR:
                    # Add this computed location to the valid directions from
                    # current cell
                    directions.append(loc)

            graph[cell] = directions

    return graph

# Helper method to safely get the value for the cell at the supplied row and
# columns. Invalid locations (outside the grid) are treated as walls.
def cell_lookup(maze, r, c):
    if r < 0 or r >= len(maze):
        return MAZE_WALL
    
    row = maze[r]
    if c < 0 or c >= len(row):
        return MAZE_WALL
    
    return row[c]

# def find_graph_path(graph, start, end, visited=None, path=None, scratch=None):
#     if path is None:
#         path = []
#         visited = set()

#     if start in visited:
#         return None
    
#     visited.add(start)
#     if scratch:
#         scratch[start[0]][start[1]] = "."

#     path.append(start)
#     if start == end:
#         return path
    
#     for move in graph[start]:
#         if move in visited:
#             continue

#         found_path = find_graph_path(graph, move, end, visited, path, scratch)
#         if found_path:
#             return path
        
#     # couldn't find path
#     path.pop()
#     if scratch:
#         scratch[start[0]][start[1]] = "X"

#     return None

# def find_graph_path(graph, start, end):
#     visited = set()  # use set for O(1) in lookups
#     path = []  # list we'll use to track our path through the graph
#     return find_graph_path_helper(graph, start, end, visited, path)

# def find_graph_path_helper(graph, start, end, visited, path):
#     # If the node we're about to visit has already been visited, we know this
#     # path doesn't lead to a solution
#     if start in visited:
#         return None
    
#     # mark this node as now visited
#     visited.add(start)

#     # NEW - provisionally consider this node as part of the path
#     path.append(start)

#     # NEW - If the node is the end that we were looking for, we're done! Return
#     # the path that we constructed. This differs from basic depth first search
#     # which traverses through the entire graph. Here, we can stop as soon as we
#     # find the end node.
#     if start == end:
#         return path
    
#     # If we reach this point, the node was not the end, but it may have
#     # neighbors for us to visit.
#     for move in graph[start]:
#         # Don't bother traversing to a node that's already been visited. This
#         # check isn't strictly necessary, but it can save a few recursive calls.
#         if move in visited:
#             continue

#         # Try to find a path from this adjacent node to the end. NEW - If a 
#         # path can be found, this call will return the path. If no path can be 
#         # found, it will return None.
#         found_path = find_graph_path_helper(graph, move, end, visited, path)

#         # NEW - If we got a path back, we're done. Continue returning the path
#         # up the call chain.
#         if found_path:
#             return path
        
#     # NEW - If we make it through all the neighbors without having found a path
#     # (we would have returned before reaching this code) then the current node
#     # is not part of the path.
#     path.pop()

#     # NEW - We didn't find a path through this node, so return None
#     return None

# ITERATIVE DFS PATHING WITH BACKTRACK
def find_graph_path(graph, start, end, path=None, visited=None, scratch=None):
    path = []
    visited = set()
    seen = set()
    pending = [start]
    depths = [0]

    while pending:
        depth = depths.pop()
        while len(path) > depth:
            last_next = path.pop()
            if scratch:
                scratch[last_next[0]][last_next[1]] = "X"

        next = pending.pop()
        if next in visited:
            continue
        
        visited.add(next)
        if scratch:
            scratch[next[0]][next[1]] = "."

        path.append(next)
        if next == end:
            return path
        
        for move in graph[next]:
            if move in visited:
                continue

            if move not in seen:
                seen.add(move)
                pending.append(move)
                depths.append(depth + 1)

    return path

def print_maze(maze):
    print()
    for row in maze:
        print("".join(row))

def find_maze_path(maze, start, exit):
    scratch = [list(row) for row in maze]
    # maze_graph = convert_maze_to_graph(maze, start)
    maze_graph = convert_maze_to_graph(maze)
    # print(maze_graph)
    path = find_graph_path(maze_graph, start, exit, scratch=scratch)
    # path = find_graph_path(maze_graph, start, exit)
    print_maze(scratch)
    return path