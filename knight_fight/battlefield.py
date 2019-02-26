import json

from element import Item, Knight


def serialize_element(obj):
    """Serialize item element"""
    if isinstance(obj, Item):
        serial = repr(obj)
        return serial
    else:
        raise TypeError("Type not serializable")


class Battlefield:
    valid_directions = ['N', 'E', 'S', 'W']

    def __init__(self):
        """Init the game, prepare all knights and items and initialize map that keeps track of position of all
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
        """Knights and items are placed on their positions in the map"""
        position_map = [[self.create_map_element() for _ in range(8)] for _ in range(8)]

        for knight in self.knights.values():
            position_map[knight.row][knight.column] = self.create_map_element(knight=knight)

        for item in self.items:
            position_map[item.row][item.column] = self.create_map_element(item=item)
        return position_map

    @staticmethod
    def create_map_element(item=None, knight=None):
        """Elements on each position are represented as arrays of knights and items

        :param item: item to init position with
        :param knight: knight to init position with
        :return: dict of one map element
        """
        items = [item] if item else []
        knights = [knight] if knight else []
        return {"knights": knights, "items": items}

    def print_map(self):
        """For debugging, see map in graphical format"""
        graphic_map = [['_' for _ in range(8)] for _ in range(8)]
        for r, row in enumerate(self.position_map):
            for c, element in enumerate(row):
                knights, items = element.get("knights"), element.get("items")
                if knights or items:
                    graphic_map[r][c] = knights[0].symbol if knights else items[0].symbol
        for graphic_row in graphic_map:
            print(graphic_row)
        print()

    def is_valid_instruction(self, instruction):
        if ':' not in instruction:
            return False
        knight, direction = instruction.split(':')
        if knight not in self.knights.keys():
            return False
        if direction not in self.valid_directions:
            return False
        return True

    def perform_move(self, knight_symbol, direction):
        self.knights[knight_symbol].move(direction, self.position_map)

    def execute_instructions(self, instructions):
        for instruction in instructions:
            self.perform_move(*instruction)

    def load_file_instructions(self):
        """Load, validate and return instruction from the instruction file

        :return: List of instruction tuples in format (knight symbol, direction symbol)
        """
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

    def create_output(self):
        """Creates output json to see the status of the game"""
        output = {}
        for knight in self.knights.values():
            output[knight.name] = knight.output_repr()
        for item in self.items:
            output[item.name] = item.output_repr()
        return output

    def save_output(self):
        """Save json output to the output file"""
        with open('final_state.json', 'w') as f:
            json.dump(self.create_output(), f, default=serialize_element)
