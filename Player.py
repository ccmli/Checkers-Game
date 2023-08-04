from Board import Board, Piece


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