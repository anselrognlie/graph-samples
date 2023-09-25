from graph_samples.bipartition import find_maze_path

def test_path_through_degenerate_maze():
    maze = [" "]
    start = (0, 0)
    end = (0, 0)

    path = find_maze_path(maze, start, end)

    assert path == [(0, 0)]

def test_path_through_small_maze():
    maze = [
        "  #",
        "# #",
        "#  ",
        ]
    start = (0, 0)
    end = (2, 2)

    path = find_maze_path(maze, start, end)

    assert path == [(0, 0), (0, 1), (1, 1), (2, 1), (2, 2)]

def test_path_through_small_up_branch_maze():
    maze = [
        "#  ",
        "  #",
        "#  ",
        ]
    start = (1, 0)
    end = (0, 2)

    path = find_maze_path(maze, start, end)

    assert path == [(1, 0), (1, 1), (0, 1), (0, 2)]

def test_path_through_small_down_branch_maze():
    maze = [
        "#  ",
        "  #",
        "#  ",
        ]
    start = (1, 0)
    end = (2, 2)

    path = find_maze_path(maze, start, end)

    assert path == [(1, 0), (1, 1), (2, 1), (2, 2)]
    
def test_path_through_medium_branch_maze():
    maze = [
        "    #     ",
        " ## # # # ",
        " #  # ### ",
        " #### #   ",
        "      # # ",
        ]
    start = (0, 0)
    end = (4, 9)

    path = find_maze_path(maze, start, end)

    assert path == [
        (0, 0), (1, 0), (2, 0), (3, 0), (4, 0), 
        (4, 1), (4, 2), (4, 3), (4, 4), (4, 5), 
        (3, 5), (2, 5), (1, 5), (0, 5), 
        (0, 6), (0, 7), (0, 8), (0, 9), 
        (1, 9), (2, 9), (3, 9), (4, 9), 
        ] 
    
def test_path_through_large_branch_maze():
    maze = [
        "      #         #            #",
        "##### # ####### # ########## #",
        "## ## #       # #            #",
        "## ## #### #### ###### #######",
        "         # #        ## # #    ",
        "## ## #### #### ### ## # ## # ",
        "## ####### #### #         # # ",
        "              # ### ## # ## # ",
        "## ####### ######## ## # ## # ",
        "## #       #        ## #    # ",
        ]
    start = (0, 0)
    end = (9, 29)

    path = find_maze_path(maze, start, end)

    assert path == [
        (0, 0), (0, 1), (0, 2), (0, 3), (0, 4), (0, 5), (1, 5), 
        (2, 5), (3, 5), (4, 5), (4, 4), (4, 3), (4, 2), (5, 2), 
        (6, 2), (7, 2), (7, 3), (7, 4), (7, 5), (7, 6), (7, 7), 
        (7, 8), (7, 9), (7, 10), (6, 10), (5, 10), (4, 10), (3, 10), 
        (2, 10), (2, 9), (2, 8), (2, 7), (1, 7), (0, 7), (0, 8), 
        (0, 9), (0, 10), (0, 11), (0, 12), (0, 13), (0, 14), (0, 15), 
        (1, 15), (2, 15), (3, 15), (4, 15), (4, 16), (4, 17), (4, 18), 
        (4, 19), (5, 19), (6, 19), (6, 20), (6, 21), (6, 22), (6, 23), 
        (6, 24), (7, 24), (8, 24), (9, 24), (9, 25), (9, 26), (9, 27), 
        (8, 27), (7, 27), (6, 27), (5, 27), (4, 27), (4, 28), (4, 29), 
        (5, 29), (6, 29), (7, 29), (8, 29), (9, 29)
        ]
    