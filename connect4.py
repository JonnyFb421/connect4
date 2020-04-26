""" Connect 4 game via Command Line! """
from enum import Enum
from itertools import cycle


class Connect4Pieces(Enum):
    EMPTY = '-'
    X = 'X'
    O = 'O'
    J = 'J'
    S = 'S'
    C = 'C'


class Connect4Grid:
    """ Class to encapsulate the state of the Connect4 Grid """
    def __init__(self, width=7, height=6):
        self.width = width
        self.height = height
        self.grid = [
            [Connect4Pieces.EMPTY.value for _ in range(self.height)]
            for _ in range(self.width)
        ]
        # Can also be written as
        # self.grid = []
        # for _ in range(width):
        #     column = []
        #     for _ in range(height):
        #         column.append(Connect4Pieces.EMPTY.value)
        #     self.grid.append(column)

    def drop_piece(self, current_player):
        """ Adds a game piece into the grid """
        valid_column_selected = False
        while not valid_column_selected:
            print('\n' * 3)
            self.print_gird()
            column = input(f"It is {current_player.name}'s turn,"
                           f" select a column to drop a {current_player.game_piece.value} game piece in:\n")
            if column.isdigit() and int(column) > 0 and int(column) <= self.width:
                column_no = int(column) - 1
                column = self.grid[column_no]
                if '-' in column:
                    next_available_slot = column.index(Connect4Pieces.EMPTY.value)
                    self.grid[column_no][next_available_slot] = current_player.game_piece.value
                    valid_column_selected = True

    def print_gird(self):
        """ Display the current state of the grid in console """
        print(" ".join([str(x + 1) for x in range(self.width)]))
        for row_number in reversed(range(len(self.grid[0]))):
            column_as_string = ''
            for column_number in range(len(self.grid)):
                column_as_string += f"{self.grid[column_number][row_number]} "
            print(column_as_string)

    def get_winner(self, players):
        """ Determine who won, if anybody """
        winning_game_piece = (
                self.get_vertical_winner() or
                self.get_horizontal_winner() or
                self.get_rtl_diagonal_winner() or
                self.get_ltr_diagonal_winner() or
                False
        )
        if winning_game_piece:
            for player in players:
                if player.game_piece.value == winning_game_piece:
                    return player

    def get_vertical_winner(self):
        """ Determines if a player won with a vertical connect """
        for column in self.grid:
            previous_value = None
            consecutive_pieces = 0
            for cell in column:
                if cell != previous_value or cell == Connect4Pieces.EMPTY.value:
                    previous_value = cell
                    consecutive_pieces = 1
                else:
                    consecutive_pieces += 1
                if consecutive_pieces >= 4:
                    return cell
        return False

    def get_horizontal_winner(self):
        """ Determines if a player won with a horizontal connect """
        previous_value = None
        for row in range(len(self.grid[0])):
            consecutive_pieces = 0
            for column in range(len(self.grid)):
                cell = self.grid[column][row]
                if cell != previous_value or cell == Connect4Pieces.EMPTY.value:
                    previous_value = cell
                    consecutive_pieces = 1
                else:
                    consecutive_pieces += 1
                if consecutive_pieces >= 4:
                    return cell
        return False

    def get_ltr_diagonal_winner(self):
        """ Scans grid starting from the bottom left going until bottom right
            looking for a winning diagonal connect
        """
        previous_value = None
        consecutive_pieces = 0
        for width in range(len(self.grid)):
            height = 0
            while width + 1 < len(self.grid) and height + 1 < len(self.grid[0]):
                if previous_value is None:
                    cell = self.grid[width][height]
                else:
                    width += 1
                    height += 1
                    cell = self.grid[width][height]
                if cell != previous_value or cell == Connect4Pieces.EMPTY.value:
                    previous_value = cell
                    consecutive_pieces = 1
                else:
                    consecutive_pieces += 1
                if consecutive_pieces >= 4:
                    return cell

    def get_rtl_diagonal_winner(self):
        """ Scans grid starting from the bottom right going until bottom left
            looking for a winning diagonal connect
        """
        previous_value = None
        consecutive_pieces = 0
        for width in reversed(range(len(self.grid))):
            height = 0
            while width - 1 >= 0 and height + 1 < len(self.grid[0]):
                if previous_value is None:
                    cell = self.grid[width][height]
                else:
                    width -= 1
                    height += 1
                    cell = self.grid[width][height]
                if cell != previous_value or cell == Connect4Pieces.EMPTY.value:
                    previous_value = cell
                    consecutive_pieces = 1
                else:
                    consecutive_pieces += 1
                if consecutive_pieces >= 4:
                    return cell
        return False


class Player:
    """ Class to store player name and their game piece """
    def __init__(self, name, game_piece):
        self.name = name
        self.game_piece = game_piece


def create_new_player(current_players, available_game_pieces):
    """ Gets user for input and uses it to create new Player object"""
    available_game_pieces = available_game_pieces
    available_game_pieces_prompt = '\n '.join([f'{i+1}: {piece}' for i, piece in enumerate(available_game_pieces)])
    player_name = input(f"Enter player {len(current_players) + 1}'s name:\n").strip()
    valid_game_piece_selected = False
    while not valid_game_piece_selected:
        game_piece_selector = input(f"Select a game piece:\n {available_game_pieces_prompt}\n").strip()
        if game_piece_selector.isdigit() and int(game_piece_selector) <= len(available_game_pieces):
            game_piece_value = available_game_pieces[int(game_piece_selector) - 1]
            return Player(player_name, Connect4Pieces[game_piece_value])


def get_available_game_pieces(current_players):
    """ Gets list of game pieces which are not already taken """
    available_game_pieces = list(Connect4Pieces.__members__.keys())
    unavailable_game_pieces = [player.game_piece.name for player in current_players]
    for unavailable_game_piece in unavailable_game_pieces:
        available_game_pieces.remove(unavailable_game_piece)
    available_game_pieces.remove(Connect4Pieces.EMPTY.name)
    return available_game_pieces


def get_players(existing_players=None):
    """ Prompts user to create one or more Player objects """
    if not existing_players:
        existing_players = []
    available_game_pieces = get_available_game_pieces(existing_players)
    existing_players.append(create_new_player(existing_players, available_game_pieces))
    add_more_players_prompt = "Would you like to add another player?\n1: Yes\n2: No\n"
    add_more_players_flag = input(add_more_players_prompt).strip().lower()
    while (add_more_players_flag == '1' or add_more_players_flag.startswith('y')) and available_game_pieces:
        available_game_pieces = get_available_game_pieces(existing_players)
        if available_game_pieces:
            existing_players.append(create_new_player(existing_players, available_game_pieces))
            add_more_players_flag = input(add_more_players_prompt).strip().lower()
    return existing_players


def game_loop():
    """ Entry point to game """
    play_again = True
    active_players = None
    while play_again:
        grid = Connect4Grid()
        if not active_players:
            active_players = get_players()
        current_turn = cycle(active_players)
        for currnet_player in current_turn:
            grid.drop_piece(currnet_player)
            winner = grid.get_winner(active_players)
            if winner:
                print('\n' * 3)
                grid.print_gird()
                print(f"WE'VE GOT A WINNER WINNER CHICKEN DINNER!!!\n"
                      f"Congratulations to {winner.name} and their lucky game piece {winner.game_piece.value}")
                break
        play_again_flag = input("Would you like to play again?\n1: Play again\n2: Reset players\n3: Quit\n").lower()
        if play_again_flag == '2' or play_again_flag.startswith('y'):
            active_players = []
        elif play_again_flag != '1' and not play_again_flag.startswith('y'):
            play_again = False


if __name__ == '__main__':
    game_loop()
