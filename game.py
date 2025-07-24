#!/usr/bin/env python3
import pygame
import pygame.locals

import undead


STATUSES = {
    'alive': (255, 255, 255),
    'dead': (0, 0, 0),
    'burried': (40, 40, 40),
    'zombie': (0, 255, 0)
}

EVENTS = {
    'evolve': pygame.event.Event(pygame.locals.USEREVENT + 1, delay=1000),
}


class VisualBoard():

    class Cell():

        def __init__(self, cell_size, status):
            self.surf = pygame.Surface((cell_size, cell_size))
            self.status = status

    def __init__(self, pygame_window, board, width, height, cell_size):
        self.pygame_window = pygame_window
        self.board = board
        self.width = width
        self.height = height
        self.cell_size = cell_size
        self.cells = [[self.Cell(self.cell_size, STATUSES['alive']) for _ in range(width)] for _ in range(height)]

    def draw(self):
        for row_index, row_cells in enumerate(self.cells):
            for col_index, cell in enumerate(row_cells):
                if board.is_alive(row_index, col_index):
                    cell.status = STATUSES['alive']
                else:
                    cell.status = STATUSES['dead']

                cell.surf.fill(cell.status)
                self.pygame_window.blit(cell.surf, (
                    col_index * self.cell_size,
                    row_index * self.cell_size
                ))
        pygame.display.flip()


board = undead.Board()
board.load('undead.txt')

pygame.init()
win = pygame.display.set_mode((2000, 2000))
visual_board = VisualBoard(win, board, 100, 100, 20)
evolution_timer = pygame.event.Event(EVENTS['evolve'].type, delay=EVENTS['evolve'].delay)


running = True
while running:
    for pygame_event in pygame.event.get():
        if pygame_event.type == pygame.locals.QUIT or (
            pygame_event.type == pygame.locals.KEYDOWN and pygame_event.key == pygame.locals.K_BACKSPACE
        ):
            running = False
            break

        if (
            pygame_event.type == EVENTS['evolve'].type or
            (pygame_event.type == pygame.locals.MOUSEBUTTONDOWN and pygame_event.button == 1)
        ):
            visual_board.draw()
            board.evolve()
