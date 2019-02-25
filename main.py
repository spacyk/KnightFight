import logging
from pprint import pprint
import json


class Element:
    def __init__(self, name, symbol, position):
        self.name = name
        self.position = position
        self.symbol = symbol


class Knight(Element):

    def __init__(self, name, symbol, position):
        super().__init__(name, symbol, position)
        self.defence = 1
        self.attack = 1
        self.status = "LIVE"
        self.special_item = None

    def __gt__(self, other):
        self_attack = 0.5 + self.attack
        if self.special_item:
            self_attack += self.special_item.attack

        other_defence = other.defence
        if other.special_item:
            other_defence += other.special_item.defence

        return self_attack > other_defence

    def output_repr(self):
        return [self.position, self.status, self.special_item, self.attack, self.defence]

    def change_position(self, new_position, position_map):
        position_map[self.position]['knights'].remove(self)
        position_map[new_position]['knights'].append(self)
        self.position = new_position

        if self.special_item:
            self.special_item.change_position(new_position)

    def set_dead(self, position_map, death_type="DEAD"):
        self.attack, self.defence = 0, 0
        self.status = death_type
        position_map[self.position]['knights'].remove(self)
        self.position = None
        if self.special_item:
            self.special_item.make_available()

    def perform_attack(self, other, position_map):
        if self > other:
            other.set_dead(position_map)
        else:
            self.set_dead(position_map)

    def take_item(self, item, position_map):
        self.special_item = item
        item.assign(position_map)

    def get_new_position(self, direction):
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
        return new_position

    @staticmethod
    def get_elements_on_position(position, position_map):
        position_dict = position_map.get(position)
        return position_dict['knights'], position_dict['items']

    def move(self, direction, position_map):
        if self.status != "LIVE":
            logging.info("Dead knight can't move anymore")
            return

        new_position = self.get_new_position(direction)

        if -1 in new_position or 8 in new_position:
            self.set_dead(position_map, death_type="DROWNED")
            return

        knights, items = self.get_elements_on_position(new_position, position_map)
        self.change_position(new_position, position_map)

        if len(knights) == 2:
            self.perform_attack(knights[0], position_map)

        if items:
            if self.status == "LIVE" and not self.special_item:
                best_item = sorted(items)[0]
                self.take_item(best_item, position_map)


class Item(Element):
    def __init__(self, name, symbol, position, attack, defence, priority):
        super().__init__(name, symbol, position)
        self.attack = attack
        self.defence = defence
        self.priority = priority
        self.equipped = False

    def __gt__(self, other):
        return self.priority < other.priority

    def change_position(self, new_position):
        self.position = new_position

    def make_available(self, position_map):
        position_map[self.position]['items'].append(self)

    def assign(self, position_map):
        self.equipped = True
        position_map[self.position].remove(self)

    def output_repr(self):
        return [list(self.position), self.equipped]


class Game:
    valid_directions = ['N', 'E', 'S', 'W']

    def __init__(self):
        self.axe = Item("axe", "A", (2, 2), 2, 0, 4)
        self.dagger = Item("dagger", "D", (2, 5), 1, 0, 2)
        self.helmet = Item("helmet", "H", (5, 5), 0, 1, 1)
        self.magic_stuff = Item("magic_stuff", "M", (5, 2), 1, 1, 3)
        self.items = [self.axe, self.dagger, self.helmet, self.magic_stuff]

        self.red = Knight("red", "R", (0, 0))
        self.blue = Knight("blue", "B", (7, 0))
        self.green = Knight("green", "G", (7, 7))
        self.yellow = Knight("yellow", "Y", (0, 7))
        self.knights = {
            self.red.symbol: self.red, self.blue.symbol: self.blue, self.green.symbol: self.green,
            self.yellow.symbol: self.yellow
        }

        self.position_map = self.init_position_map()

    def init_position_map(self):
        position_map = {(c, r): self.create_map_element() for c in range(8) for r in range(8)}

        for knight in self.knights.values():
            position_map[knight.position] = self.create_map_element(knight=knight)

        for item in self.items:
            position_map[item.position] = self.create_map_element(item=item)
        return position_map

    @staticmethod
    def create_map_element(item=None, knight=None):
        items = [item] if item else []
        knights = [knight] if knight else []
        return {"knights": knights, "items": items}

    def print_map(self):
        graphic_map = [['_' for _ in range(8)] for _ in range(8)]
        for element_position, element in self.position_map.items():
            knights, items = element.get("knights"), element.get("items")
            row, column = element_position
            if knights or items:
                graphic_map[row][column] = knights[0].symbol if knights else items[0].symbol
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
    instructions.append(('R', 'S'))
    instructions.append(('R', 'S'))
    instructions.append(('B', 'E'))
    instructions.append(('G', 'N'))
    instructions.append(('Y', 'N'))

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
