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

def test_color_cascadia_4(cascadia):
    coloration = find_coloration(cascadia, 4)

    # Assert
    assert coloration is not None

def test_color_cascadia_5(cascadia):
    coloration = find_coloration(cascadia, 5)

    # Assert
    assert coloration is not None

