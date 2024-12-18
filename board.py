
class Board:
    def __init__(self):
        self.board = self.create_initial_board()
        self.move_log = []  # Lịch sử các nước đi

    def create_initial_board(self):
        # Bàn cờ ban đầu
        return [
            ['r', 'n', 'b', 'q', 'k', 'b', 'n', 'r'],
            ['p', 'p', 'p', 'p', 'p', 'p', 'p', 'p'],
            ['.', '.', '.', '.', '.', '.', '.', '.'],
            ['.', '.', '.', '.', '.', '.', '.', '.'],
            ['.', '.', '.', '.', '.', '.', '.', '.'],
            ['.', '.', '.', '.', '.', '.', '.', '.'],
            ['P', 'P', 'P', 'P', 'P', 'P', 'P', 'P'],
            ['R', 'N', 'B', 'Q', 'K', 'B', 'N', 'R']
        ]

    def move(self, start, end):
        # Di chuyển quân cờ
        sx, sy = start
        ex, ey = end
        captured_piece = self.board[ex][ey]
        self.move_log.append((start, end, captured_piece))  # Lưu trạng thái
        self.board[ex][ey] = self.board[sx][sy]
        self.board[sx][sy] = '.'

    def undo_move(self):
        # Hoàn tác nước đi gần nhất
        if not self.move_log:
            return
        start, end, captured_piece = self.move_log.pop()
        sx, sy = start
        ex, ey = end
        self.board[sx][sy] = self.board[ex][ey]
        self.board[ex][ey] = captured_piece

    def get_all_moves(self, color):
        # Trả về tất cả nước đi hợp lệ cho màu `color`
        moves = []
        for row in range(8):
            for col in range(8):
                piece = self.board[row][col]
                if piece != '.' and ((color == 'white' and piece.isupper()) or (color == 'black' and piece.islower())):
                    moves.extend(self.get_piece_moves(piece, row, col))
        return moves

    def get_piece_moves(self, piece, row, col):
        moves = []
        if piece.lower() == 'p':  # Pawn
            direction = -1 if piece.isupper() else 1
            start_row = 6 if piece.isupper() else 1  # Quân tốt trắng bắt đầu từ hàng 6, quân tốt đen bắt đầu từ hàng 1

            # Tiến 1 ô
            if 0 <= row + direction < 8 and self.board[row + direction][col] == '.':
                moves.append(((row, col), (row + direction, col)))

            # Tiến 2 ô nếu quân tốt chưa di chuyển (chỉ có thể đi 2 ô nếu đang ở hàng xuất phát)
            if row == start_row and self.board[row + 2 * direction][col] == '.':
                moves.append(((row, col), (row + 2 * direction, col)))

            # Ăn chéo
            for col_offset in [-1, 1]:
                if 0 <= col + col_offset < 8 and 0 <= row + direction < 8:
                    target = self.board[row + direction][col + col_offset]
                    if target != '.' and (
                            (piece.isupper() and target.islower()) or (piece.islower() and target.isupper())):
                        moves.append(((row, col), (row + direction, col + col_offset)))

        elif piece.lower() == 'r':  # Rook
            for d_row, d_col in [(1, 0), (-1, 0), (0, 1), (0, -1)]:
                for i in range(1, 8):
                    new_row, new_col = row + d_row * i, col + d_col * i
                    if 0 <= new_row < 8 and 0 <= new_col < 8:
                        if self.board[new_row][new_col] == '.':
                            moves.append(((row, col), (new_row, new_col)))
                        elif (self.board[new_row][new_col].isupper() and piece.islower()) or (
                                self.board[new_row][new_col].islower() and piece.isupper()):
                            moves.append(((row, col), (new_row, new_col)))
                            break
                        else:
                            break
        # Các quân cờ khác (Knight, Bishop, Queen, King) không thay đổi
        elif piece.lower() == 'n':  # Knight
            for d_row, d_col in [(2, 1), (2, -1), (-2, 1), (-2, -1), (1, 2), (1, -2), (-1, 2), (-1, -2)]:
                new_row, new_col = row + d_row, col + d_col
                if 0 <= new_row < 8 and 0 <= new_col < 8:
                    target = self.board[new_row][new_col]
                    if target == '.' or (target.isupper() and piece.islower()) or (
                            target.islower() and piece.isupper()):
                        moves.append(((row, col), (new_row, new_col)))
        elif piece.lower() == 'b':  # Bishop
            for d_row, d_col in [(1, 1), (1, -1), (-1, 1), (-1, -1)]:
                for i in range(1, 8):
                    new_row, new_col = row + d_row * i, col + d_col * i
                    if 0 <= new_row < 8 and 0 <= new_col < 8:
                        if self.board[new_row][new_col] == '.':
                            moves.append(((row, col), (new_row, new_col)))
                        elif (self.board[new_row][new_col].isupper() and piece.islower()) or (
                                self.board[new_row][new_col].islower() and piece.isupper()):
                            moves.append(((row, col), (new_row, new_col)))
                            break
                        else:
                            break
        elif piece.lower() == 'q':  # Queen
            moves.extend(self.get_piece_moves('r', row, col))  # Combine Rook and Bishop moves
            moves.extend(self.get_piece_moves('b', row, col))
        elif piece.lower() == 'k':  # King
            for d_row, d_col in [(1, 0), (-1, 0), (0, 1), (0, -1), (1, 1), (1, -1), (-1, 1), (-1, -1)]:
                new_row, new_col = row + d_row, col + d_col
                if 0 <= new_row < 8 and 0 <= new_col < 8:
                    target = self.board[new_row][new_col]
                    if target == '.' or (target.isupper() and piece.islower()) or (
                            target.islower() and piece.isupper()):
                        moves.append(((row, col), (new_row, new_col)))
        return moves

    def is_in_check(self, color):
        """
        Kiểm tra xem tướng của màu `color` có bị chiếu không.
        """
        king_position = self.find_king(color)
        opponent_color = "black" if color == "white" else "white"

        for row in range(8):
            for col in range(8):
                piece = self.board[row][col]
                if piece != '.' and ((piece.isupper() and opponent_color == 'white') or (piece.islower() and opponent_color == 'black')):
                    if (row, col) in self.get_piece_moves(piece, row, col):
                        return True
        return False

    def find_king(self, color):
        """
        Tìm vị trí của quân tướng (King) của màu `color`.
        """
        for row in range(8):
            for col in range(8):
                piece = self.board[row][col]
                if (color == "white" and piece == 'K') or (color == "black" and piece == 'k'):
                    return (row, col)
        return None

    def is_checkmate(self, color):
        """
        Kiểm tra xem có phải là checkmate không.
        """
        if not self.is_in_check(color):
            return False

        # Nếu tướng bị chiếu, kiểm tra xem có nước đi hợp lệ nào giúp thoát khỏi chiếu không.
        all_moves = self.get_all_moves(color)
        for start, end in all_moves:
            self.move(start, end)
            if not self.is_in_check(color):
                self.undo_move()
                return False
            self.undo_move()
        return True

    def is_stalemate(self, color):
        """
        Kiểm tra xem có phải là stalemate không.
        """
        if self.is_in_check(color):
            return False

        all_moves = self.get_all_moves(color)
        if not all_moves:
            return True

        return False

    def reset_game(self):
        """
        Reset lại bàn cờ về trạng thái ban đầu.
        """
        self.board = self.create_initial_board()
        self.move_log = []

    def end_game(self):
        """
        Kết thúc ván đấu, có thể là checkmate hoặc stalemate.
        """
        if self.is_checkmate("white"):
            print("Checkmate! Black wins!")
        elif self.is_checkmate("black"):
            print("Checkmate! White wins!")
        elif self.is_stalemate("white") or self.is_stalemate("black"):
            print("Stalemate! It's a draw!")
        else:
            print("Game continues...")
