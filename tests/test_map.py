from pytest import fixture
from graph_samples.bipartition import find_coloration

@fixture
def cascadia():
    return {
        "AK": ["BC"],
        "BC": ["AK", "WA", "ID", "MT"],
        "WA": ["BC", "ID", "OR"],
        "OR": ["WA", "ID", "NV", "CA"],
        "CA": ["OR"],
        "ID": ["WA", "BC", "MT", "WY", "UT", "NV", "OR"],
        "MT": ["BC", "ID"],
        "NV": ["OR", "ID", "UT"],
        "UT": ["NV", "ID"],
        "WY": ["ID"],
    }

@fixture
def pentagon():
    return {
        0: [1, 2, 8],
        1: [0],
        2: [3, 4, 0],
        3: [2],
        4: [5, 6, 2],
        5: [4],
        6: [7, 8, 4],
        7: [6],
        8: [9, 0, 6],
        9: [8],
    }

@fixture
def challenge():
    return {
        0: [1, 8],
        1: [0, 2, 8],
        2: [1, 3, 4],
        3: [2, 4, 5],
        4: [2, 3, 5, 6],
        5: [3, 4, 6, 7],
        6: [4, 5, 7, 8],
        7: [5, 6, 8],
        8: [0, 1, 6, 7],
    }

@fixture
def challenge_spur():
    return {
        0: [1, 8],
        1: [0, 2, 8],
        2: [1, 11, 12, 3, 4],
        3: [2, 9, 10, 4, 5],
        4: [2, 3, 5, 6],
        5: [3, 4, 6, 7],
        6: [4, 5, 7, 8],
        7: [5, 6, 8],
        8: [0, 1, 6, 7],
        9: [3, 10],
        10: [3, 9],
        11: [2, 12],
        12: [2, 11]
    }

def fully_connected_graph(num_nodes):
    graph = {}
    for n in range(num_nodes):
        neighbors = list(filter(lambda x: x != n, range(num_nodes)))
        graph[n] = neighbors

    return graph

def validate_coloration(graph, coloration):
    for node, neighbors in graph.items():
        node_color = coloration[node]
        for neighbor in neighbors:
            if coloration[neighbor] == node_color:
                return False
            
    return True

def test_color_cascadia_1(cascadia):
    coloration = find_coloration(cascadia, 1)

    # Assert
    assert coloration is None

def test_color_cascadia_2(cascadia):
    coloration = find_coloration(cascadia, 2)

    # Assert
    assert coloration is None

def test_color_cascadia_3(cascadia):
    coloration = find_coloration(cascadia, 3)

    # Assert
    assert coloration is not None
    assert validate_coloration(cascadia, coloration)

def test_color_cascadia_4(cascadia):
    coloration = find_coloration(cascadia, 4)

    # Assert
    assert coloration is not None
    assert validate_coloration(cascadia, coloration)

def test_color_cascadia_5(cascadia):
    coloration = find_coloration(cascadia, 5)

    # Assert
    assert coloration is not None
    assert validate_coloration(cascadia, coloration)

def test_pentagon_1(pentagon):
    coloration = find_coloration(pentagon, 1)

    # Assert
    assert coloration is None

def test_pentagon_2(pentagon):
    coloration = find_coloration(pentagon, 2)

    # Assert
    assert coloration is None

def test_pentagon_3(pentagon):
    coloration = find_coloration(pentagon, 3)

    # Assert
    assert coloration is not None
    assert validate_coloration(pentagon, coloration)

def test_pentagon_4(pentagon):
    coloration = find_coloration(pentagon, 4)

    # Assert
    assert coloration is not None
    assert validate_coloration(pentagon, coloration)

def test_pentagon_5(pentagon):
    coloration = find_coloration(pentagon, 5)

    # Assert
    assert coloration is not None
    assert validate_coloration(pentagon, coloration)

def test_4_connected_1():
    graph = fully_connected_graph(4)
    coloration = find_coloration(graph, 1)

    # Assert
    assert coloration is None

def test_4_connected_2():
    graph = fully_connected_graph(4)
    coloration = find_coloration(graph, 2)

    # Assert
    assert coloration is None

def test_4_connected_3():
    graph = fully_connected_graph(4)
    coloration = find_coloration(graph, 3)

    # Assert
    assert coloration is None

def test_4_connected_4():
    graph = fully_connected_graph(4)
    coloration = find_coloration(graph, 4)

    # Assert
    assert coloration is not None
    assert validate_coloration(graph, coloration)

def test_challenge_1(challenge):
    coloration = find_coloration(challenge, 1)

    # Assert
    assert coloration is None

def test_challenge_2(challenge):
    coloration = find_coloration(challenge, 2)

    # Assert
    assert coloration is None

def test_challenge_3(challenge):
    coloration = find_coloration(challenge, 3)

    # Assert
    assert coloration is not None
    assert validate_coloration(challenge, coloration)

def test_challenge_spur_3(challenge_spur):
    coloration = find_coloration(challenge_spur, 3)

    # Assert
    assert coloration is not None
    assert validate_coloration(challenge_spur, coloration)

