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

# to color a node
# if already colored, done
# make a working copy of the current colors
# set current color to the lowest color that doesn't conflict with neighbors
# try to color each neighbor
# if we fail to color a neighbor
# 

def color_dfs(adj, node, colors, num_colors):
    if node in colors:
       return colors
    
    coloration = None
    neighbor_colors = set(colors.get(n) for n in adj[node])
    for color in range(num_colors):
        found_coloration = True
        if color not in neighbor_colors:
            colors[node] = color
            print("descend")
            print(colors)
            for neighbor in adj[node]:
                coloration = color_dfs(adj, neighbor, colors, num_colors)
                if coloration is None:
                    # could not color neighbors with current color
                    print("backtrack")
                    colors.pop(node)  # undo the color assignment for this node (children have already been undone)
                    print(colors)
                    found_coloration = False
                    break
                else:
                    colors = coloration

            if found_coloration:
                # if we find a coloration for all neighbors, then we have colored
                # everything reachable from this node and we're done
                return colors            

    return coloration

def find_coloration(adj, num_colors):
    colors = {}
    coloration = {}

    for node in adj.keys():
        coloration = color_dfs(adj, node, colors, num_colors)
        if coloration is None:
            return None
        else:
            colors = coloration
        
    print(coloration)
    return coloration

    

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

def possible_bipartition(dislikes):
    coloration = find_coloration(dislikes, 2)
    return coloration is not None

MAZE_WALL = "#"
MAZE_CORRIDOR = " "

def cell_lookup(maze, r, c):
    if r < 0 or r >= len(maze):
        return MAZE_WALL
    
    row = maze[r]
    if c < 0 or c >= len(row):
        return MAZE_WALL
    
    return row[c]

def convert_maze_to_graph(maze, start):
    graph = {}
    pending = [start]
    while pending:
        next = pending.pop()
        if next in graph:
            continue

        # which directions can we move in?
        directions = []
        for dr, dc in ((-1, 0), (0, 1), (1, 0), (0, -1)):
            loc = (next[0] + dr, next[1] + dc)
            if cell_lookup(maze, loc[0], loc[1]) == MAZE_CORRIDOR:
                directions.append(loc)
                if loc not in graph:
                    pending.append(loc)

        graph[next] = directions

    return graph

def find_graph_path_from_to(graph, start, end, path=None, visited=None, scratch=None):
    if path is None:
        path = []
        visited = set()

    if start in visited:
        return None
    
    visited.add(start)
    if scratch:
        scratch[start[0]][start[1]] = "."

    path.append(start)
    if start == end:
        return path
    
    for move in graph[start]:
        if move in visited:
            continue

        found_path = find_graph_path_from_to(graph, move, end, path, visited, scratch)
        if found_path:
            return path
        
    # couldn't find path
    path.pop()
    if scratch:
        scratch[start[0]][start[1]] = "X"

    return None

def print_maze(maze):
    print()
    for row in maze:
        print("".join(row))

def find_maze_path(maze, start, exit):
    scratch = [list(row) for row in maze]
    maze_graph = convert_maze_to_graph(maze, start)
    # print(maze_graph)
    path = find_graph_path_from_to(maze_graph, start, exit, scratch=scratch)
    print_maze(scratch)
    return path