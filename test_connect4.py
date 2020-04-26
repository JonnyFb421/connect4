import unittest
from unittest.mock import MagicMock

import connect4


class Connect4Tests(unittest.TestCase):
    def test_grid_creation_size(self):
        """ Asserts initialization creates a grid the appropriate size """
        test_width = 2
        test_height = 3
        expected_grid = [[connect4.Connect4Pieces.EMPTY.value] * test_height]*test_width
        test_grid = connect4.Connect4Grid(width=test_width, height=test_height).grid
        self.assertEqual(test_grid, expected_grid)

    @unittest.mock.patch('connect4.Player')
    @unittest.mock.patch('connect4.input', return_value='1')
    def test_drop_piece(self, player_mock, input_mock):
        """ Asserts calling drop_piece updates the grid in the appropriate spot """
        test_game_piece = 'X'
        player_mock.game_piece.value = test_game_piece
        test_grid = connect4.Connect4Grid()
        test_grid.drop_piece(player_mock)
        test_grid.drop_piece(player_mock)
        self.assertEqual(test_grid.grid[0][0], test_game_piece)
        self.assertEqual(test_grid.grid[0][1], test_game_piece)
        self.assertEqual(test_grid.grid[0][1], test_game_piece)

    @unittest.mock.patch('connect4.input', return_value='1')
    def test_get_winner_returns_correct_user(self, input_mock):
        player_1 = MagicMock()
        player_1.name = 'player_1'
        player_1.game_piece.value = 'X'
        player_2 = MagicMock()
        player_2.name = 'player_2'
        player_2.game_piece.value = 'O'
        players = [player_1, player_2]
        test_grid = connect4.Connect4Grid()
        test_grid.drop_piece(player_1)
        test_grid.drop_piece(player_1)
        test_grid.drop_piece(player_1)
        test_grid.drop_piece(player_1)
        winner = test_grid.get_winner(players)
        self.assertEqual(winner, player_1)
