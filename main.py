import logging
from pprint import pprint
import json


class Element:
    def __init__(self, name, symbol, row, column):
        self.name = name
        self.symbol = symbol
        self.row = row
        self.column = column


class Knight(Element):

    def __init__(self, name, symbol, row, column):
        super().__init__(name, symbol, row, column)
        self.defence = 1
        self.attack = 1
        self.status = "LIVE"
        self.special_item = None

    def __gt__(self, other):
        return self.attack + 0.5 > other.defence

    def output_repr(self):
        position = None if self.row is None else [self.row, self.column]
        return [position, self.status, self.special_item, self.attack, self.defence]

    def change_position(self, new_row, new_column, position_map):
        position_map[self.row][self.column]['knights'].remove(self)
        position_map[new_row][new_column]['knights'].append(self)
        self.row, self.column = new_row, new_column
        if self.special_item:
            self.special_item.change_position(new_row, new_column)

    def set_dead(self, position_map, death_type="DEAD"):
        self.attack, self.defence = 0, 0
        self.status = death_type
        position_map[self.row][self.column]['knights'].remove(self)
        if death_type == "DROWNED":
            self.row, self.column = None, None
        if self.special_item:
            self.special_item.make_available(position_map)
        self.special_item = None

    def perform_attack(self, other, position_map):
        if self > other:
            other.set_dead(position_map)
        else:
            self.set_dead(position_map)

    def take_item(self, item, position_map):
        self.special_item = item
        self.attack += item.attack
        self.defence += item.defence
        item.assign(position_map)

    def get_new_position(self, direction):
        if direction == 'N':
            row, column = self.row - 1, self.column
        elif direction == 'E':
            row, column = self.row, self.column + 1
        elif direction == 'S':
            row, column = self.row + 1, self.column
        elif direction == 'W':
            row, column = self.row, self.column - 1
        else:
            raise ValueError("Invalid direction")
        return row, column

    @staticmethod
    def get_elements_on_position(row, column, position_map):
        position_dict = position_map[row][column]
        return position_dict['knights'], position_dict['items']

    def move(self, direction, position_map):
        if self.status != "LIVE":
            logging.info("No moving for death knight")
            return

        new_row, new_column = self.get_new_position(direction)

        if new_row in [-1, 8] or new_column in [-1, 8]:
            self.set_dead(position_map, death_type="DROWNED")
            return

        knights, items = self.get_elements_on_position(new_row, new_column, position_map)
        self.change_position(new_row, new_column, position_map)

        if items and not self.special_item:
                best_item = sorted(items)[0]
                self.take_item(best_item, position_map)

        if len(knights) == 2:
            self.perform_attack(knights[0], position_map)


class Item(Element):
    def __init__(self, name, symbol, row, column, attack=None, defence=None, priority=None):
        super().__init__(name, symbol, row, column)
        self.attack = attack
        self.defence = defence
        self.priority = priority
        self.equipped = False

    def __gt__(self, other):
        return self.priority < other.priority

    def change_position(self, new_row, new_column):
        self.row, self.column = new_row, new_column

    def make_available(self, position_map):
        self.equipped = False
        position_map[self.row][self.column]['items'].append(self)

    def assign(self, position_map):
        self.equipped = True
        position_map[self.row][self.column]['items'].remove(self)

    def output_repr(self):
        return [[self.row, self.column], self.equipped]


class Game:
    valid_directions = ['N', 'E', 'S', 'W']

    def __init__(self):
        """Init the game, prepare all the knights and the items and initialize map that keeps track of position of all
        the elements
        """
        self.red = Knight("red", "R", 0, 0)
        self.blue = Knight("blue", "B", 7, 0)
        self.green = Knight("green", "G", 7, 7)
        self.yellow = Knight("yellow", "Y", 0, 7)
        self.knights = {
            self.red.symbol: self.red, self.blue.symbol: self.blue, self.green.symbol: self.green,
            self.yellow.symbol: self.yellow
        }

        self.axe = Item("axe", "A", 2, 2, attack=2, defence=0, priority=4)
        self.dagger = Item("dagger", "D", 2, 5, attack=1, defence=0, priority=2)
        self.helmet = Item("helmet", "H", 5, 5, attack=0, defence=1, priority=1)
        self.magic_stuff = Item("magic_stuff", "M", 5, 2, attack=1, defence=1, priority=3)
        self.items = [self.axe, self.dagger, self.helmet, self.magic_stuff]

        self.position_map = self.init_position_map()

    def init_position_map(self):
        position_map = [[self.create_map_element() for _ in range(8)] for _ in range(8)]

        for knight in self.knights.values():
            position_map[knight.row][knight.column] = self.create_map_element(knight=knight)

        for item in self.items:
            position_map[item.row][item.column] = self.create_map_element(item=item)
        return position_map

    @staticmethod
    def create_map_element(item=None, knight=None):
        items = [item] if item else []
        knights = [knight] if knight else []
        return {"knights": knights, "items": items}

    def print_map(self):
        graphic_map = [['_' for _ in range(8)] for _ in range(8)]
        for r, row in enumerate(self.position_map):
            for c, element in enumerate(row):
                knights, items = element.get("knights"), element.get("items")
                if knights or items:
                    graphic_map[r][c] = knights[0].symbol if knights else items[0].symbol
        for graphic_row in graphic_map:
            print(graphic_row)
        print()

    def make_output(self):
        output = {}
        for knight in self.knights.values():
            output[knight.name] = knight.output_repr()
        for item in self.items:
            output[item.name] = item.output_repr()
        return output

    def is_valid_instruction(self, instruction):
        if ':' not in instruction:
            return False
        knight, direction = instruction.split(':')
        if knight not in self.knights.keys():
            return False
        if direction not in self.valid_directions:
            return False
        return True

    def load_instructions(self):
        instructions = []
        with open('moves.txt') as f:
            f.readline()
            for line in f:
                line = line.rstrip('\n')
                if line == "GAME-END":
                        break
                elif self.is_valid_instruction(line):
                    instructions.append(line.split(':'))
                else:
                    raise ValueError("Invalid instruction provided")
        return instructions

    def save_output(self):
        with open('final_state.json', 'w') as f:
            json.dump(self.make_output(), f)

    def perform_move(self, knight_symbol, direction):
        self.knights[knight_symbol].move(direction, self.position_map)

    def execute_instructions(self, instructions):
        for instruction in instructions:
            self.perform_move(*instruction)


def testing_execution():
    game = Game()

    instructions = list()

    instructions.append(('Y', 'S'))
    instructions.append(('Y', 'S'))

    game.execute_instructions(instructions)

    game.print_map()
    pprint(game.make_output())


def main():
    game = Game()

    instructions = game.load_instructions()
    game.execute_instructions(instructions)

    game.save_output()


if __name__ == "__main__":
    #main()
    testing_execution()
