from battlefield import Battlefield


def test_drowned_no_item():
    battlefield = Battlefield()
    instructions = [('R', 'W')]
    battlefield.execute_instructions(instructions)

    red = battlefield.red
    assert red.status == "DROWNED"
    assert red.row is None
    assert red.attack == 0


def test_drowned_item():
    battlefield = Battlefield()
    instructions = [('R', 'E'), ('R', 'E'), ('R', 'S'), ('R', 'S'), ('R', 'N'), ('R', 'N'), ('R', 'N')]
    battlefield.execute_instructions(instructions)

    red = battlefield.red
    assert red.status == "DROWNED"
    assert red.row is None
    assert red.attack == 0
    assert red.attack == 0
    assert not red.special_item

    axe = battlefield.axe
    assert not axe.equipped
    assert axe.row == 0 and axe.column == 2


def test_battlefield_no_item_win():
    battlefield = Battlefield()
    instructions = [('R', 'S'), ('R', 'S'), ('R', 'S'), ('R', 'S'), ('R', 'S'), ('R', 'S'), ('R', 'S')]
    battlefield.execute_instructions(instructions)

    red = battlefield.red
    blue = battlefield.blue
    assert red.status == "LIVE"
    assert blue.status == "DEAD"
    assert blue.attack == 0
    assert blue.defence == 0
    assert blue.row == 7 and blue.column == 0


def test_battlefield_item_win():
    battlefield = Battlefield()
    instructions = [
        ('R', 'S'), ('R', 'S'), ('R', 'E'), ('R', 'E'), ('R', 'W'), ('R', 'W'), ('R', 'S'), ('R', 'S'), ('R', 'S'),
        ('R', 'S'), ('R', 'S')
    ]
    battlefield.execute_instructions(instructions)

    red = battlefield.red
    blue = battlefield.blue
    assert red.status == "LIVE"
    assert red.special_item
    assert red.row == 7 and red.column == 0
    assert red.attack == 3
    assert red.defence == 1
    assert red.special_item.row == red.row and red.special_item.column == red.column
    assert blue.status == "DEAD"
    assert blue.attack == 0
    assert blue.defence == 0


def test_battlefield_item_lose():
    battlefield = Battlefield()
    instructions = [
        ('R', 'S'), ('R', 'S'), ('R', 'E'), ('R', 'E'), ('R', 'W'), ('R', 'W'), ('B', 'N'), ('B', 'N'), ('B', 'N'),
        ('B', 'N'), ('B', 'N')
    ]
    battlefield.execute_instructions(instructions)

    red = battlefield.red
    blue = battlefield.blue
    assert red.status == "DEAD"
    assert not red.special_item
    assert blue.status == "LIVE"
    assert not blue.special_item

    axe = battlefield.axe
    assert not axe.equipped
    assert axe.row == 2 and axe.column == 0


def test_keep_item():
    battlefield = Battlefield()
    instructions = [
        ('G', 'W'), ('G', 'W'), ('G', 'N'), ('G', 'N'), ('G', 'N'), ('G', 'N'), ('G', 'N')
    ]
    battlefield.execute_instructions(instructions)

    green = battlefield.green
    assert green.special_item == battlefield.helmet
    assert battlefield.helmet.equipped
    assert not battlefield.dagger.equipped


def test_pick_item_and_battlefield():
    battlefield = Battlefield()
    instructions = [
        ('G', 'W'), ('G', 'W'), ('G', 'N'), ('G', 'N'), ('G', 'N'), ('G', 'N'), ('G', 'N'), ('Y', 'W'), ('Y', 'W'),
        ('Y', 'S'), ('Y', 'S')
    ]
    battlefield.execute_instructions(instructions)

    green = battlefield.green
    yellow = battlefield.yellow
    assert green.status == "DEAD"
    assert yellow.special_item == battlefield.dagger
    assert not battlefield.helmet.equipped
    assert battlefield.dagger.equipped


def test_pick_best_item():
    battlefield = Battlefield()
    instructions = [
        ('G', 'W'), ('G', 'W'), ('G', 'N'), ('G', 'N'), ('G', 'N'), ('G', 'N'), ('G', 'N'), ('Y', 'W'), ('Y', 'W'),
        ('Y', 'S'), ('Y', 'S'), ('R', 'S'), ('R', 'S'), ('R', 'E'), ('R', 'E'), ('R', 'E'), ('R', 'E'), ('R', 'E'),
        ('R', 'E'), ('B', 'E'), ('B', 'E'), ('B', 'E'), ('B', 'E'), ('B', 'E'), ('B', 'N'), ('B', 'N'),
        ('B', 'N'), ('B', 'N'), ('B', 'N'), ('B', 'N')
    ]
    battlefield.execute_instructions(instructions)

    blue = battlefield.blue
    assert blue.special_item == battlefield.dagger
    assert battlefield.dagger.equipped
