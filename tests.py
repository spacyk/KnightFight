from main import Game


def test_drowned_no_item():
    game = Game()
    instructions = [('R', 'W')]
    game.execute_instructions(instructions)

    red = game.red
    assert red.status == "DROWNED"
    assert red.row is None
    assert red.attack == 0


def test_drowned_item():
    game = Game()
    instructions = [('R', 'E'), ('R', 'E'), ('R', 'S'), ('R', 'S'), ('R', 'N'), ('R', 'N'), ('R', 'N')]
    game.execute_instructions(instructions)

    red = game.red
    assert red.status == "DROWNED"
    assert red.row is None
    assert red.attack == 0
    assert red.attack == 0
    assert not red.special_item

    axe = game.axe
    assert not axe.equipped
    assert axe.row == 0 and axe.column == 2


def test_fight_no_item_win():
    game = Game()
    instructions = [('R', 'S'), ('R', 'S'), ('R', 'S'), ('R', 'S'), ('R', 'S'), ('R', 'S'), ('R', 'S')]
    game.execute_instructions(instructions)

    red = game.red
    blue = game.blue
    assert red.status == "LIVE"
    assert blue.status == "DEAD"
    assert blue.attack == 0
    assert blue.defence == 0
    assert blue.row == 7 and blue.column == 0


def test_fight_item_win():
    game = Game()
    instructions = [
        ('R', 'S'), ('R', 'S'), ('R', 'E'), ('R', 'E'), ('R', 'W'), ('R', 'W'), ('R', 'S'), ('R', 'S'), ('R', 'S'),
        ('R', 'S'), ('R', 'S')
    ]
    game.execute_instructions(instructions)

    red = game.red
    blue = game.blue
    assert red.status == "LIVE"
    assert red.special_item
    assert red.row == 7 and red.column == 0
    assert red.attack == 3
    assert red.defence == 1
    assert red.special_item.row == red.row and red.special_item.column == red.column
    assert blue.status == "DEAD"
    assert blue.attack == 0
    assert blue.defence == 0


def test_fight_item_lose():
    game = Game()
    instructions = [
        ('R', 'S'), ('R', 'S'), ('R', 'E'), ('R', 'E'), ('R', 'W'), ('R', 'W'), ('B', 'N'), ('B', 'N'), ('B', 'N'),
        ('B', 'N'), ('B', 'N')
    ]
    game.execute_instructions(instructions)

    red = game.red
    blue = game.blue
    assert red.status == "DEAD"
    assert not red.special_item
    assert blue.status == "LIVE"
    assert not blue.special_item

    axe = game.axe
    assert not axe.equipped
    assert axe.row == 2 and axe.column == 0


def test_keep_item():
    game = Game()
    instructions = [
        ('G', 'W'), ('G', 'W'), ('G', 'N'), ('G', 'N'), ('G', 'N'), ('G', 'N'), ('G', 'N')
    ]
    game.execute_instructions(instructions)

    green = game.green
    assert green.special_item == game.helmet
    assert game.helmet.equipped
    assert not game.dagger.equipped


def test_pick_item_and_fight():
    game = Game()
    instructions = [
        ('G', 'W'), ('G', 'W'), ('G', 'N'), ('G', 'N'), ('G', 'N'), ('G', 'N'), ('G', 'N'), ('Y', 'W'), ('Y', 'W'),
        ('Y', 'S'), ('Y', 'S')
    ]
    game.execute_instructions(instructions)

    green = game.green
    yellow = game.yellow
    assert green.status == "DEAD"
    assert yellow.special_item == game.dagger
    assert not game.helmet.equipped
    assert game.dagger.equipped


def test_pick_best_item():
    game = Game()
    instructions = [
        ('G', 'W'), ('G', 'W'), ('G', 'N'), ('G', 'N'), ('G', 'N'), ('G', 'N'), ('G', 'N'), ('Y', 'W'), ('Y', 'W'),
        ('Y', 'S'), ('Y', 'S'), ('R', 'S'), ('R', 'S'), ('R', 'E'), ('R', 'E'), ('R', 'E'), ('R', 'E'), ('R', 'E'),
        ('R', 'E'), ('B', 'E'), ('B', 'E'), ('B', 'E'), ('B', 'E'), ('B', 'E'), ('B', 'N'), ('B', 'N'),
        ('B', 'N'), ('B', 'N'), ('B', 'N'), ('B', 'N')
    ]
    game.execute_instructions(instructions)

    blue = game.blue
    assert blue.special_item == game.dagger
    assert game.dagger.equipped
