from graph_samples.bipartition import possible_bipartition

def test_example_1():
    # Arrange
    dislikes = {
      "Fido": [],
      "Rufus": ["James", "Alfie"],
      "James": ["Rufus", "T-Bone"],
      "Alfie": ["Rufus"],
      "T-Bone": ["James"]
    }

    # Act
    answer = possible_bipartition(dislikes)

    # Assert
    assert answer

def test_example_2():
    dislikes = {
      "Fido": [],
      "Rufus": ["James", "Alfie"],
      "James": ["Rufus", "Alfie"],
      "Alfie": ["Rufus", "James"]
    }

    # Act
    answer = possible_bipartition(dislikes)

    # Assert
    assert not answer

def test_example_3():
    # Arrange
    dislikes = {
      "Fido": [],
      "Rufus": ["James", "Scruffy"],
      "James": ["Rufus", "Alfie"],
      "Alfie": ["T-Bone", "James"],
      "T-Bone": ["Alfie", "Scruffy"],
      "Scruffy": ["Rufus", "T-Bone"]
    }

    # Act
    answer = possible_bipartition(dislikes)

    # Assert
    assert not answer

def test_will_return_true_for_a_graph_which_can_be_bipartitioned():
    # Arrange
    dislikes = {
      "Fido": ["Alfie", "Bruno"],
      "Rufus": ["James", "Scruffy"],
      "James": ["Rufus", "Alfie"],
      "Alfie": ["Fido", "James"],
      "T-Bone": ["Scruffy"],
      "Scruffy": ["Rufus", "T-Bone"],
      "Bruno": ["Fido"]
    }

    # Act
    answer = possible_bipartition(dislikes)

    # Assert
    assert answer

def test_will_return_false_for_graph_which_cannot_be_bipartitioned():
    # Arrange
    dislikes = {
      "Fido": ["Alfie", "Bruno"],
      "Rufus": ["James", "Scruffy"],
      "James": ["Rufus", "Alfie"],
      "Alfie": ["Fido", "James", "T-Bone"],
      "T-Bone": ["Alfie", "Scruffy"],
      "Scruffy": ["Rufus", "T-Bone"],
      "Bruno": ["Fido"]
    }

    # Act
    answer = possible_bipartition(dislikes)

    # Assert
    assert not answer


def test_will_return_true_for_empty_graph():
    assert possible_bipartition({})
  
def test_will_return_false_for_another_graph_which_cannot_be_bipartitioned():
    # Arrange
    dislikes = {
      "Fido": ["Alfie", "Bruno"],
      "Rufus": ["James", "Scruffy"],
      "James": ["Rufus", "Alfie"],
      "Alfie": ["Fido", "James", "T-Bone"],
      "T-Bone": ["Alfie", "Scruffy"],
      "Scruffy": ["Rufus", "T-Bone"],
      "Bruno": ["Fido"],
      "Calico": ["Nala"],
      "Nala": ["Calico"]
    }

    # Act
    answer = possible_bipartition(dislikes)

    # Assert
    assert not answer

def test_multiple_dogs_at_beginning_dont_dislike_any_others():
  # Arrange
    dislikes = {
      "Fido": [],
      "Rufus": [],
      "James": [],
      "Alfie": ["T-Bone"],
      "T-Bone": ["Alfie", "Scruffy"],
      "Scruffy": ["T-Bone"],
      "Bruno": ["Nala"],
      "Calico": ["Nala"],
      "Nala": ["Bruno", "Calico"]
    }

    # Act
    answer = possible_bipartition(dislikes)

    # Assert
    assert answer


def test_multiple_dogs_in_middle_dont_dislike_any_others():
    # Arrange
    dislikes = {
      "Fido": ["Alfie"],
      "Rufus": ["James", "Scruffy"],
      "James": ["Rufus", "Alfie"],
      "Alfie": ["Fido", "James"],
      "T-Bone": [],
      "Scruffy": ["Rufus"],
      "Bruno": [],
      "Spot": ["Nala"],
      "Nala": ["Spot"]
    }

    # Act
    answer = possible_bipartition(dislikes)

    # Assert
    assert answer

def test_will_return_false_for_disconnected_graph_which_cannot_be_bipartitioned():
    # Arrange
    dislikes = {
      "Katie": ["Michiko"],
      "Michiko": ["Katie"],
      "Fido": ["Alfie", "Bruno"],
      "Rufus": ["James", "Scruffy"],
      "James": ["Rufus", "Alfie"],
      "Alfie": ["Fido", "James", "T-Bone"],
      "T-Bone": ["Alfie", "Scruffy"],
      "Scruffy": ["Rufus", "T-Bone"],
      "Bruno": ["Fido"]
    }

    # Act
    answer = possible_bipartition(dislikes)

    # Assert
    assert not answer
