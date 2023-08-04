# Author: Chungman Chan
# Description: unittests for CheckersGame

import unittest
from CheckersGame import Checkers, InvalidPlayer, InvalidSquare, OutofTurn, Player, Board, Square, Piece


class TestSquare(unittest.TestCase):
    def test_str_when_piece_is_none(self):
        square = Square()
        self.assertIsNone(square.get_piece())

    def test_str_when_piece_is_not_none(self):
        piece = Piece("Lili", "Black", (0, 0))
        square = Square(piece)
        self.assertEqual(square.get_piece().get_color(), "Black")


class TestPiece(unittest.TestCase):
    def test_piece(self):
        # Initialize a black piece
        black_piece = Piece("Black Player", "Black", (7, 0))
        # Initialize a white piece
        white_piece = Piece("White Player", "White", (0, 1))

        # Test get_color method
        self.assertEqual(black_piece.get_color(), "Black")
        self.assertEqual(white_piece.get_color(), "White")

        # Test get_location method
        self.assertEqual(black_piece.get_location(), (7, 0))
        self.assertEqual(white_piece.get_location(), (0, 1))

        # Test make_king & _is_king method
        black_piece.make_king()
        self.assertTrue(black_piece.is_king())
        self.assertFalse(white_piece.is_king())
        white_piece.make_king()
        self.assertTrue(white_piece.is_king())

        # Test make_triple_king & _is_triple_king method
        black_piece.make_triple_king()
        self.assertTrue(black_piece.is_triple_king())
        self.assertFalse(white_piece.is_triple_king())
        white_piece.make_triple_king()
        self.assertTrue(white_piece.is_triple_king())


class TestPlayer(unittest.TestCase):
    def setUp(self):
        self.player1 = Player("Sara", "Black")
        self.piece1 = Piece("Sara", "Black", (0, 0))
        self.piece2 = Piece("Sara", "Black", (1, 1))
        self.piece3 = Piece("Sara", "Black", (2, 2))
        self.piece3.make_king()
        self.piece3.make_triple_king()
        self.piece2.make_king()
        self.player2 = Player("Lili", "Black")
        self.piece4 = Piece("Lili", "White", (3, 3))
        self.piece4.make_king()
        self.player1.add_piece(self.piece1)
        self.player1.add_piece(self.piece2)
        self.player1.add_piece(self.piece3)
        self.player2.add_piece(self.piece4)

    def test_get_king_count(self):
        self.assertEqual(self.player1.get_king_count(), 1)

    def test_get_triple_king_count(self):
        self.assertEqual(self.player1.get_triple_king_count(), 1)

    def test_get_captured_pieces_count(self):
        self.assertEqual(self.player1.get_captured_pieces_count(), 0)


class TestBoard(unittest.TestCase):
    def test_init(self):
        board = Board()
        self.assertEqual(len(board._board), 8)
        for row in board._board:
            self.assertEqual(len(row), 8)
            for square in row:
                self.assertIsInstance(square, Square)

    def test_add_piece(self):
        board = Board()
        piece = Piece("Lili", 'White', (0, 1))
        board.add_piece_to_board((0, 1), piece)
        self.assertEqual(board._board[0][1].get_piece().get_color(), "White")


class TestCheckers(unittest.TestCase):
    def setUp(self):
        self.game = Checkers()
        self.player1 = self.game.create_player("Rei", "Black")
        self.player2 = self.game.create_player("Ceci", "White")

    def test_InvalidPlayer(self):
        # Test InvalidPlayer exception
        self.assertRaises(InvalidPlayer, self.game.play_game, "Cei", (5, 6), (4, 7))

    def test_InvalidSquare(self):
        # Test InvalidSquare exception
        self.assertRaises(InvalidSquare, self.game.play_game, "Rei", (9, 9), (8, 8))

    def test_OutofTurn(self):
        # Test OutofTurn exception
        self.assertRaises(OutofTurn, self.game.play_game, "Ceci", (5, 6), (4, 7))
        self.assertRaises(OutofTurn, self.game.play_game, "Ceci", (4, 7), (3, 6))

    def test_play_game(self):
        # Test valid move
        captured_pieces = self.game.play_game("Rei", (5, 6), (4, 5))
        self.assertEqual(captured_pieces, 0)
        self.assertEqual(self.game.get_checker_details((4, 5)), "Black")

    def test_get_checker_details(self):
        # Test None return
        self.assertIsNone(self.game.get_checker_details((0, 2)))

        # Test piece returns
        self.assertEqual(self.game.get_checker_details((2, 1)), "White")
        self.assertEqual(self.game.get_checker_details((7, 0)), "Black")

        # Test InvalidSquare exception
        self.assertRaises(InvalidSquare, self.game.get_checker_details, (9, 9))

    def test_game_winner(self):
        # Test game has not ended
        self.assertEqual(self.game.game_winner(), "Game has not ended")
        # Test player1 wins


class TestCheckersGame(unittest.TestCase):
    def setUp(self):
        self.game_1 = Checkers()
        self.player_1 = self.game_1.create_player("White Player", "White")
        self.player_2 = self.game_1.create_player("Black Player", "Black")

    def test_pieces_in_correct_place(self):
        black_location = [(5, 0), (5, 2), (5, 4), (5, 6), (6, 1), (6, 3), (6, 5), (6, 7), (7, 0), (7, 2), (7, 4),
                          (7, 6)]
        white_location = [(0, 1), (0, 3), (0, 5), (0, 7), (1, 0), (1, 2), (1, 4), (1, 6), (2, 1), (2, 3), (2, 5),
                          (2, 7)]

        for i in range(len(self.game_1._players["Black Player"]._pieces_list)):
            self.assertEqual(self.game_1._players["Black Player"]._pieces_list[i].get_location(), black_location[i])

        for j in range(len(self.game_1._players["White Player"]._pieces_list)):
            self.assertEqual(self.game_1._players["White Player"]._pieces_list[j].get_location(), white_location[j])

    def test_default_current_turn(self):
        self.assertEqual(self.game_1._current_turn, "Black Player")

    def test_invalid_player(self):
        self.assertRaises(InvalidPlayer, self.game_1.play_game, "Red Player", (0, 1), (1, 2))

    def test_OutofTurn(self):
        self.assertRaises(OutofTurn, self.game_1.play_game, "White Player", (0, 1), (1, 2))

    def test_InvalidSquare(self):
        self.assertRaises(InvalidSquare, self.game_1.play_game, "Black Player", (9, 1), (8, 1))
        self.assertRaises(InvalidSquare, self.game_1.play_game, "Black Player", (0, 1), (1, 2))
        self.assertRaises(InvalidSquare, self.game_1.play_game, "Black Player", (7, 0), (6, 1))

    def test_play_game(self):
        round_1 = self.game_1.play_game("Black Player", (5, 4), (4, 3))
        self.assertEqual(round_1, 0)
        round_2 = self.game_1.play_game("White Player", (2, 5), (3, 4))
        self.assertEqual(round_2, 0)
        round_3 = self.game_1.play_game("Black Player", (6, 3), (5, 4))
        self.assertEqual(round_3, 0)
        round_4 = self.game_1.play_game("White Player", (2, 3), (3, 2))
        self.assertEqual(round_4, 0)
        round_5 = self.game_1.play_game("Black Player", (4, 3), (2, 5))
        self.assertEqual(round_5, 1)
        round_6 = self.game_1.play_game("White Player", (1, 4), (2, 3))
        self.assertEqual(round_6, 0)
        round_7 = self.game_1.play_game("Black Player", (5, 2), (4, 3))
        self.assertEqual(round_7, 0)
        round_8 = self.game_1.play_game("White Player", (3, 2), (4, 1))
        self.assertEqual(round_8, 0)
        round_9 = self.game_1.play_game("Black Player", (5, 0), (3, 2))
        self.assertEqual(round_9, 1)
        round_10 = self.game_1.play_game("Black Player", (3, 2), (1, 4))
        self.assertEqual(round_10, 1)
        round_11 = self.game_1.play_game("White Player", (1, 2), (2, 3))
        self.assertEqual(round_11, 0)
        round_12 = self.game_1.play_game("Black Player", (6, 1), (5, 2))
        self.assertEqual(round_12, 0)
        round_13 = self.game_1.play_game("White Player", (0, 3), (1, 2))
        self.assertEqual(round_13, 0)
        round_14 = self.game_1.play_game("Black Player", (1, 4), (0, 3))
        self.assertEqual(self.game_1.get_checker_details((0, 3)), "Black_king")
        self.assertEqual(round_14, 0)
        round_15 = self.game_1.play_game("White Player", (1, 6), (3, 4))
        self.assertEqual(round_15, 1)
        round_16 = self.game_1.play_game("Black Player", (0, 3), (1, 4))
        self.assertEqual(round_16, 0)
        round_17 = self.game_1.play_game("White Player", (2, 3), (3, 2))
        self.assertEqual(round_17, 0)
        round_18 = self.game_1.play_game("Black Player", (1, 4), (4, 1))
        self.assertEqual(round_18, 1)
        round_19 = self.game_1.play_game("White Player", (2, 1), (3, 0))
        self.assertEqual(round_19, 0)
        round_20 = self.game_1.play_game("Black Player", (7, 4), (6, 3))
        self.assertEqual(round_20, 0)
        round_21 = self.game_1.play_game("White Player", (1, 0), (2, 1))
        self.assertEqual(round_21, 0)

        # Test game_winner method
        self.assertEqual(self.game_1.game_winner(), "Game has not ended")

        # Test Player method
        self.assertEqual(self.player_1.get_king_count(), 0)
        self.assertEqual(self.player_2.get_king_count(), 1)

        force_become_triple_king = self.game_1.play_game("Black Player", (4, 1), (7, 4))
        self.assertEqual(self.game_1.get_checker_details((7, 4)), "Black_Triple_King")
        self.assertEqual(self.player_1.get_triple_king_count(), 0)
        self.assertEqual(self.player_2.get_king_count(), 0)
        self.assertEqual(self.player_2.get_triple_king_count(), 1)

        self.assertEqual(self.player_1.get_captured_pieces_count(), 1)
        self.assertEqual(self.player_2.get_captured_pieces_count(), 4)


if __name__ == '__main__':
    unittest.main()
