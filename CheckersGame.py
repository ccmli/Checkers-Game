# Author: Chungman Chan
# Description: The program is a Checkers game, a two-player board game where each player tries to capture
#              all of the opponent's pieces or block them so that they cannot make any more moves.
#              The Checkers class contains information about the board and the players. The board is initialized
#              when the Checkers object is created.
#              It also contains several methods, including create_player, play_game, get_checker_details, print_board,
#              and game_winner.
#              The Player class represents the player in the game. It is initialized with player_name and checker_color
#              that the player has chosen.
#              The parameter piece_color is a string of value "Black" or "White". The Player class contains several
#              methods, including get_king_count, get_triple_king_count, and get_captured_pieces_count.
#              There's also Board class, Square Class and Piece Class. Represents the Checker boards, the square on
#              the checker board, and the piece information.

class OutofTurn(Exception):
    """Exception raise if a player attempts to move a piece out of turn"""
    pass

class InvalidSquare(Exception):
    """
    Exception raise if a player does not own the checker present in the square_location
    or square_location does not exist on the board
    """
    pass

class InvalidPlayer(Exception):
    """Exception raise if the player name is not valid"""
    pass

class Checkers:
    """Represents the checker game as played"""

    def __init__(self):
        self._game_board = Board()
        self._players = {}
        self._current_turn = None
        self._last_move = None  # Piece object

    def create_player(self, player_name, piece_color):
        """
        Create a player object given player's name and piece color
        """
        new_player = Player(player_name, piece_color)
        # Adds the new Player object to dictionary, name is the key
        self._players[player_name] = new_player
        if piece_color == "Black":
            self._current_turn = player_name
        self.initiate_pieces(player_name, piece_color)

        return new_player


    def initiate_pieces(self, player, piece_color):
        """Helper method to initiate 12 pieces, add it to the board and player's piece list"""
        if piece_color == "White":
            for row in range(3):
                for col in range(8):
                    if row % 2 == 0 and col % 2 == 1:
                        new_location = (row, col)
                        new_piece = Piece(player, piece_color, new_location)
                        self._game_board.add_piece_to_board(new_location, new_piece)
                        self._players[player].add_piece(new_piece)
                    elif row % 2 == 1 and col % 2 == 0:
                        new_location = (row, col)
                        new_piece = Piece(player, piece_color, new_location)
                        self._game_board.add_piece_to_board(new_location, new_piece)
                        self._players[player].add_piece(new_piece)
        elif piece_color == "Black":
            for row in range(5, 8):
                for col in range(8):
                    if row % 2 == 0 and col % 2 == 1:
                        new_location = (row, col)
                        new_piece = Piece(player, piece_color, new_location)
                        self._game_board.add_piece_to_board(new_location, new_piece)
                        self._players[player].add_piece(new_piece)
                    elif row % 2 == 1 and col % 2 == 0:
                        new_location = (row, col)
                        new_piece = Piece(player, piece_color, new_location)
                        self._game_board.add_piece_to_board(new_location, new_piece)
                        self._players[player].add_piece(new_piece)

    def play_game(self, player_name, starting_square_location, destination_square_location):
        """
        Takes as parameter player_name, starting_square_location and destination_square_location of the piece
        that the player wants to move
        Moves the player piece from starting_square location to destination_square_location
        Returns the number of captured pieces if there's any, return 0 otherwise.
        :exception: OutofTurn, InvalidSquare, InvalidPlayer
        """

        # player name not exist -> InvalidPlayer
        if player_name not in self._players:
            raise InvalidPlayer
        # starting_square_location// destination_square_location -> not exist ->> InvalidSquare
        if (not self.is_valid_square(starting_square_location)
                and not self.is_valid_square(destination_square_location)):
            raise InvalidSquare
        if (not self.is_black_square(starting_square_location)
                and not self.is_black_square(destination_square_location)):
            raise InvalidSquare

        picked_square = self.get_picked_checker(starting_square_location)

        if self._last_move is not None:
            last_move_owner = self._last_move.get_owner()
            if last_move_owner == self._current_turn:
                # check if current turn need to be switched after a capture move
                if last_move_owner != player_name:
                    self._current_turn = player_name

                # The same owner as the previous turn, but the piece picked is not the same as the previous piece
                if (last_move_owner == player_name
                        and (picked_square is not self._last_move)):
                    raise OutofTurn

        # current turn not player -> OutofTurn
        if self._current_turn != player_name:
            raise OutofTurn

        # starting_square_location's piece not player's -> InvalidSquare
        if picked_square.get_owner() != player_name:
            raise InvalidSquare
        # destination_square_location has piece -> InvalidSquare
        if self.get_picked_checker(destination_square_location) is not None:
            raise InvalidSquare

        current_piece_captured = 0
        # Check the distance between starting and destination
        distance = abs(destination_square_location[0] - starting_square_location[0])
        row_distance = destination_square_location[0] - starting_square_location[0]
        col_distance = destination_square_location[1] - starting_square_location[1]

        """
        Calculate how many opponent piece player captured, update current_piece_captured
        Update piece's location
        Remove captured opponent's Piece from the board
        """
        current_piece_captured = self.check_captured_pieces(player_name, starting_square_location, distance - 1,
                                                            row_distance, col_distance)

        # Add current_piece_captured to player's _captured_pieces_count by add_captured_pieces method
        self._players[player_name].add_captured_pieces(current_piece_captured)

        # Move the picked Piece to destination square
        # Remove the picked Piece from starting_square_location
        self.move_destination(starting_square_location, destination_square_location)
        picked_piece = self.get_picked_checker(destination_square_location)
        if current_piece_captured == 0:
            self.next_turn()

        self._last_move = picked_piece

        # If the destination piece reaches the end of opponent's side, promoted it as a king on the board.
        # i.e. for Black -> reach row 0; for White -> reach row 7
        # and piece is not triple king

        # If the piece crosses back to its original side -> set is_triple_king be True, and set is_king be False.

        if self._players[player_name].get_piece_color() == "Black":
            if destination_square_location[0] == 0 and not picked_piece.is_triple_king():
                picked_piece.make_king()
            elif destination_square_location[0] == 7:
                picked_piece.make_triple_king()

        if self._players[player_name].get_piece_color() == "White":
            if destination_square_location[0] == 7 and not picked_piece.is_triple_king():
                picked_piece.make_king()
            elif destination_square_location[0] == 0:
                picked_piece.make_triple_king()

        return current_piece_captured

    def check_captured_pieces(self, player, location, distance, row_dist, col_dist):
        """Helper method that calculate the pieces captured in a turn"""
        if distance == 0:
            return 0

        if row_dist < 0 and col_dist < 0:
            new_location = (location[0] - 1, location[1] - 1)
        elif row_dist < 0 and col_dist > 0:
            new_location = (location[0] - 1, location[1] + 1)
        elif row_dist > 0 and col_dist < 0:
            new_location = (location[0] + 1, location[1] - 1)
        elif row_dist > 0 and col_dist > 0:
            new_location = (location[0] + 1, location[1] + 1)

        piece_on_board = self.get_picked_checker(new_location)
        if distance == 1:
            if piece_on_board is None or piece_on_board.get_owner() is player:
                return 0
            elif piece_on_board.get_owner() is not player:
                self._game_board.remove_piece_from_board(new_location)
                return 1

        if ((piece_on_board is None)
                or (piece_on_board.get_owner() is player)):
            return 0 + self.check_captured_pieces(player, new_location, distance - 1, row_dist, col_dist)
        elif piece_on_board.get_owner() is not player:
            self._game_board.remove_piece_from_board(new_location)
            return 1 + self.check_captured_pieces(player, new_location, distance - 1, row_dist, col_dist)

    def move_destination(self, starting_square_location, destination_square_location):
        """Helper method that move the piece from starting square to destination"""
        picked_piece = self.get_picked_checker(starting_square_location)
        picked_piece.set_location(destination_square_location)
        self._game_board.add_piece_to_board(destination_square_location, picked_piece)
        self._game_board.remove_piece_from_board(starting_square_location, destination_square_location)

    def get_checker_details(self, square_location):
        """
        Returns the checker details present in the square_location,
        takes as parameter a square_location on the board
        """
        # if location not exist -> InvalidSquare
        if not self.is_valid_square(square_location):
            raise InvalidSquare
        # returns the piece object
        if self.get_picked_checker(square_location) is None:
            return None
        return self.get_picked_checker(square_location).get_details()

    def get_picked_checker(self, square_location):
        """Returns the piece object given the square location"""
        if self._game_board.get_piece(square_location) is None:
            return None
        return self._game_board.get_piece(square_location)

    def print_board(self):
        """Prints the current board in the form of an array"""
        board = []
        for row in self._game_board.get_board():
            piece_row = []
            for square in row:
                if square.get_piece() is None:
                    piece_row.append(None)
                else:
                    piece_row.append(square.get_piece().get_details())
            board.append(piece_row)
        print(board)

    def game_winner(self):
        """
        Returns the name of the player who won the game, or "Game has not ended" if the game has not ended
        """
        for player in self._players:
            if self._players[player].get_captured_pieces_count() == 12:
                return player
        return "Game has not ended"

    def next_turn(self):
        """Switches the game to next turn, by changing the name in _current_turn'"""
        next_player = None
        for player in self._players:
            if player != self._current_turn:
                next_player = player
        self._current_turn = next_player

    def is_valid_square(self, square_location):
        """Return True if the square location is valid, returns False otherwise"""
        if square_location[0] in range(0, 8) and square_location[1] in range(0, 8):
            return True
        return False

    def is_black_square(self, square_location):
        """Return True if the square is Black, returns False otherwise"""
        if ((square_location[0] % 2 == 0 and square_location[1] % 2 == 1)
                or (square_location[0] % 2 == 1 and square_location[1] % 2 == 0)):
            return True
        return False


class Player:
    """Represents a player in the game"""

    def __init__(self, player_name, piece_color):
        self._player_name = player_name
        self._piece_color = piece_color
        self._pieces_list = []  # Piece object: color, location, is_king/is_triple_king
        self._captured_pieces_count = 0

    def get_piece_color(self):
        """Returns the pieces color of the player"""
        return self._piece_color

    def get_king_count(self):
        """Returns the number of king pieces that the player has"""
        king_count = 0
        for piece in self._pieces_list:
            if piece.is_king() and piece.get_location() is not None:
                king_count += 1
        return king_count

    def get_triple_king_count(self):
        """Returns the number of triple king pieces that the player has"""
        triple_king_count = 0
        for piece in self._pieces_list:
            if piece.is_triple_king() and piece.get_location() is not None:
                triple_king_count += 1
        return triple_king_count

    def get_captured_pieces_count(self):
        """Returns the number of opponent pieces that the player has captured"""
        return self._captured_pieces_count

    def add_piece(self, new_piece_object):
        """Adds a piece to player's piece list"""
        self._pieces_list.append(new_piece_object)

    def add_captured_pieces(self, piece_num):
        """Adds captured pieces count"""
        self._captured_pieces_count += piece_num


class Board:
    """Represents a checker board with 8 rows and 8 columns."""

    def __init__(self):
        self._board = []
        for row in range(8):
            row_list = []
            for col in range(8):
                row_list.append(Square())
            self._board.append(row_list)

    def get_board(self):
        """Returns board"""
        return self._board

    def add_piece_to_board(self, location, new_piece):
        """Adds piece to board"""
        self._board[location[0]][location[1]].add_piece(new_piece)

    def remove_piece_from_board(self, location, next_destination=None):
        """Removes piece from board"""
        if next_destination is None:
            self._board[location[0]][location[1]].get_piece().set_location_to_none()
        self._board[location[0]][location[1]].remove_piece()

    def get_piece(self, location):
        """Returns piece in the board"""
        return self._board[location[0]][location[1]].get_piece()


class Square:
    """Represents a square of the checkerboard"""

    def __init__(self, piece=None):
        self._piece = piece

    def add_piece(self, new_piece):
        """Adds a piece to this square"""
        self._piece = new_piece

    def get_piece(self):
        """Returns piece in the square"""
        return self._piece

    def remove_piece(self):
        """Removes the piece from square"""
        self._piece = None


class Piece:
    """Represents a checker piece"""

    def __init__(self, player_name, color, location):
        self._owner = player_name
        self._color = color
        self._location = location
        self._is_king = False
        self._is_triple_king = False

    def set_location_to_none(self):
        """Sets the piece location to none"""
        self._location = None

    def set_location(self, location):
        """Sets the location of piece"""
        self._location = location

    def get_details(self):
        """The substitute string prints when printing the Piece object."""
        if self._color == "White":
            if self.is_triple_king():
                return "White_Triple_King"
            elif self.is_king():
                return "White_king"
            else:
                return "White"

        elif self._color == "Black":
            if self.is_triple_king():
                return "Black_Triple_King"
            elif self.is_king():
                return "Black_king"
            else:
                return "Black"

    def get_color(self):
        """Returns the color of the piece."""
        return self._color

    def get_location(self):
        """Returns the location of the piece."""
        return self._location

    def get_owner(self):
        """Returns the owner name of the piece"""
        return self._owner

    def make_king(self):
        """Promotes the piece to king."""
        self._is_king = True

    def make_triple_king(self):
        """Promotes the piece to triple king."""
        self._is_king = False
        self._is_triple_king = True

    def is_king(self):
        """Returns True if the piece is king, False otherwise."""
        return self._is_king

    def is_triple_king(self):
        """Returns True if the piece is triple king, False otherwise."""
        return self._is_triple_king
