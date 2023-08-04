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
        return self._board

    def add_piece_to_board(self, location, new_piece):
        self._board[location[0]][location[1]].add_piece(new_piece)

    def remove_piece_from_board(self, location):
        self._board[location[0]][location[1]].get_piece().set_location_to_none()
        self._board[location[0]][location[1]].remove_piece()

    def get_piece(self, location):
        return self._board[location[0]][location[1]].get_piece()

class Square:
    """Represents a square of the checkerboard"""
    def __init__(self, piece=None):
        self._piece = piece

    def add_piece(self, new_piece):
        """Adds a piece to this square"""
        self._piece = new_piece

    def get_piece(self):
        """Returns a piece in this square"""
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