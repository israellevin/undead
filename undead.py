#!/usr/bin/python3
import collections


class Board:
    def __init__(self):
        self.rows = collections.defaultdict(lambda: collections.defaultdict(bool))

    def is_alive(self, row_index, cell_index):
        return (row_index in self.rows) and (cell_index in self.rows[row_index])

    def neighbors(self, row_index, cell_index):
        live_neighbors, dead_neighbors = [], []
        for neighbor_row_index in range(row_index - 1, row_index + 2):
            for neighbor_cell_index in range(cell_index - 1, cell_index + 2):
                if neighbor_row_index == row_index and neighbor_cell_index == cell_index:
                    continue
                if self.is_alive(neighbor_row_index, neighbor_cell_index):
                    live_neighbors.append((neighbor_row_index, neighbor_cell_index))
                else:
                    dead_neighbors.append((neighbor_row_index, neighbor_cell_index))
        return live_neighbors, dead_neighbors

    def evolve(self):
        next_generation_rows = collections.defaultdict(lambda: collections.defaultdict(bool))
        life_touch_counter = collections.defaultdict(lambda: collections.defaultdict(int))

        # Get the next generation of living cells while counting every time a dead neighbor is checked.
        for row_index in self.rows.keys():
            for cell_index in self.rows[row_index].keys():
                live_neighbors, dead_neighbors = self.neighbors(row_index, cell_index)
                if len(live_neighbors) > 1 and len(live_neighbors) < 4:
                    next_generation_rows[row_index][cell_index] = True
                for dead_neighbor in dead_neighbors:
                    life_touch_counter[dead_neighbor[0]][dead_neighbor[1]] += 1

        # The number of times a dead neighbor is checked will be the number of living neighbors for that cell.
        for row_index in life_touch_counter.keys():
            for cell_index in life_touch_counter[row_index].keys():
                if life_touch_counter[row_index][cell_index] == 3:
                    next_generation_rows[row_index][cell_index] = True

        self.rows = next_generation_rows

    def load(self, file_name):
        with open(file_name, 'r') as file:
            lines = file.readlines()
        for line_index, line in enumerate(lines):
            for char_index, cell in enumerate(line):
                if cell == '.':
                    self.rows[line_index][char_index] = True

    def cell_string(self, row_index, cell_index):
        return '.' if self.is_alive(row_index, cell_index) else ' '

    def row_string(self, row_index, from_cell, to_cell):
        return ''.join([self.cell_string(row_index, cell_index) for cell_index in range(from_cell, to_cell)])

    def print(self, from_row, to_row, from_cell, to_cell):
        print("-" * (to_cell - from_cell + 1))
        print("\n".join([self.row_string(row_index, from_cell, to_cell) for row_index in range(from_row, to_row)]))
        print("-" * (to_cell - from_cell + 1))


if __name__ == "__main__":
    board = Board()
    board.load('undead.txt')

    while True:
        board.print(0, 10, 0, 20)
        input("Press Enter to continue...")
        board.evolve()
