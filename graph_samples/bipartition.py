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