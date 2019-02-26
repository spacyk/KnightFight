from knight_fight import KnightFight


def test_drowned_no_item():
    fight = KnightFight()
    instructions = [('R', 'W')]
    fight.execute_instructions(instructions)

    red = fight.red
    assert red.status == "DROWNED"
    assert red.row is None
    assert red.attack == 0


def test_drowned_item():
    fight = KnightFight()
    instructions = [('R', 'E'), ('R', 'E'), ('R', 'S'), ('R', 'S'), ('R', 'N'), ('R', 'N'), ('R', 'N')]
    fight.execute_instructions(instructions)

    red = fight.red
    assert red.status == "DROWNED"
    assert red.row is None
    assert red.attack == 0
    assert red.attack == 0
    assert not red.special_item

    axe = fight.axe
    assert not axe.equipped
    assert axe.row == 0 and axe.column == 2


def test_fight_no_item_win():
    fight = KnightFight()
    instructions = [('R', 'S'), ('R', 'S'), ('R', 'S'), ('R', 'S'), ('R', 'S'), ('R', 'S'), ('R', 'S')]
    fight.execute_instructions(instructions)

    red = fight.red
    blue = fight.blue
    assert red.status == "LIVE"
    assert blue.status == "DEAD"
    assert blue.attack == 0
    assert blue.defence == 0
    assert blue.row == 7 and blue.column == 0


def test_fight_item_win():
    fight = KnightFight()
    instructions = [
        ('R', 'S'), ('R', 'S'), ('R', 'E'), ('R', 'E'), ('R', 'W'), ('R', 'W'), ('R', 'S'), ('R', 'S'), ('R', 'S'),
        ('R', 'S'), ('R', 'S')
    ]
    fight.execute_instructions(instructions)

    red = fight.red
    blue = fight.blue
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
    fight = KnightFight()
    instructions = [
        ('R', 'S'), ('R', 'S'), ('R', 'E'), ('R', 'E'), ('R', 'W'), ('R', 'W'), ('B', 'N'), ('B', 'N'), ('B', 'N'),
        ('B', 'N'), ('B', 'N')
    ]
    fight.execute_instructions(instructions)

    red = fight.red
    blue = fight.blue
    assert red.status == "DEAD"
    assert not red.special_item
    assert blue.status == "LIVE"
    assert not blue.special_item

    axe = fight.axe
    assert not axe.equipped
    assert axe.row == 2 and axe.column == 0


def test_keep_item():
    fight = KnightFight()
    instructions = [
        ('G', 'W'), ('G', 'W'), ('G', 'N'), ('G', 'N'), ('G', 'N'), ('G', 'N'), ('G', 'N')
    ]
    fight.execute_instructions(instructions)

    green = fight.green
    assert green.special_item == fight.helmet
    assert fight.helmet.equipped
    assert not fight.dagger.equipped


def test_pick_item_and_fight():
    fight = KnightFight()
    instructions = [
        ('G', 'W'), ('G', 'W'), ('G', 'N'), ('G', 'N'), ('G', 'N'), ('G', 'N'), ('G', 'N'), ('Y', 'W'), ('Y', 'W'),
        ('Y', 'S'), ('Y', 'S')
    ]
    fight.execute_instructions(instructions)

    green = fight.green
    yellow = fight.yellow
    assert green.status == "DEAD"
    assert yellow.special_item == fight.dagger
    assert not fight.helmet.equipped
    assert fight.dagger.equipped


def test_pick_best_item():
    fight = KnightFight()
    instructions = [
        ('G', 'W'), ('G', 'W'), ('G', 'N'), ('G', 'N'), ('G', 'N'), ('G', 'N'), ('G', 'N'), ('Y', 'W'), ('Y', 'W'),
        ('Y', 'S'), ('Y', 'S'), ('R', 'S'), ('R', 'S'), ('R', 'E'), ('R', 'E'), ('R', 'E'), ('R', 'E'), ('R', 'E'),
        ('R', 'E'), ('B', 'E'), ('B', 'E'), ('B', 'E'), ('B', 'E'), ('B', 'E'), ('B', 'N'), ('B', 'N'),
        ('B', 'N'), ('B', 'N'), ('B', 'N'), ('B', 'N')
    ]
    fight.execute_instructions(instructions)

    blue = fight.blue
    assert blue.special_item == fight.dagger
    assert fight.dagger.equipped
