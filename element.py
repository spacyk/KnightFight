class Element:
    def __init__(self, name, symbol, row, column):
        self.name = name
        self.symbol = symbol
        self.row = row
        self.column = column

    def __repr__(self):
        return f'{self.name}'


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
