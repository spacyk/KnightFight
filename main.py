class Knight:

    def __init__(self, name, position):
        self.name = name
        self.defense = 1
        self.attack = 1
        self.alive = True
        self.position = position
        self.special_item = None

    def __repr__(self):
        return f'{self.name}'

    def pop_element(self, position, positions_map):
        return positions_map.pop(position, None)

    def move(self, direction, positions_map):

        if not self.alive:
            print("you can't move, ya dead")
            return

        del positions_map[self.position]

        # switch maybe ak to ma python
        new_position = ()
        if direction == 'N':
            row, column = self.position
            new_position = row - 1, column
        if direction == 'E':
            row, column = self.position
            new_position = row, column + 1
        if direction == 'S':
            row, column = self.position
            new_position = row + 1, column
        if direction == 'W':
            row, column = self.position
            new_position = row, column - 1

        if -1 in new_position or 8 in new_position:
            print('invalid maybe you die')

        element_on_position = positions_map.pop(self.position, None)
        if not element_on_position:
            self.position = new_position
            positions_map[self.position] = self

class Item:

    def __init__(self, name, attack, defence, position, priority):
        self.name = name
        self.attack = attack
        self.defence = defence
        self.position = position
        self.priority = priority
        self. assigned = False

    def __repr__(self):
        return f'{self.name}'


class Game:
    def __init__(self):

        self.axe = Item("A", 2, 0, (2, 2), 4)
        self.dagger = Item("D", 1, 0, (2, 5), 2)
        self.helmet = Item("H", 0, 1, (5, 5), 1)
        self.magicStuff = Item("M", 1, 1, (5, 2), 3)

        self.red = Knight("R", (0, 0))
        self.blue = Knight("B", (7, 0))
        self.green = Knight("G", (7, 7))
        self.yellow = Knight("Y", (0, 7))

        # Bude sa mozno hodit aj opacna mapa ale len na ulahcenie pristupu, ta sa nebude menit

        self.positions_map = {
            element.position: element for element in
            [self.red, self.blue, self.green, self.yellow, self.axe, self.dagger, self.helmet, self.magicStuff]
        }

    def print_map(self):
        graphic_map = [['_' for _ in range(8)] for _ in range(8)]
        for element_position, element in self.positions_map.items():
            row, column = element_position
            graphic_map[row][column] = element.name
        for graphic_row in graphic_map:
            print(graphic_row)

def main():

    game = Game()

    print(game.positions_map)
    game.print_map()

    game.red.move('S', game.positions_map)
    game.red.move('S', game.positions_map)
    game.blue.move('E', game.positions_map)
    game.green.move('N', game.positions_map)

    print(game.positions_map)
    game.print_map()



if __name__ == "__main__":

    main()
