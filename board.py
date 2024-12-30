class Board:
    def __init__(self):
        self.board = self.create_initial_board()  # Khởi tạo bàn cờ với trạng thái ban đầu
        self.move_log = []  # Lưu trữ lịch sử các nước đi
        self.reset_game()

    def create_initial_board(self):
        # Trả về một bàn cờ ban đầu với các quân cờ ở vị trí chuẩn
        return [
            ['r', 'n', 'b', 'q', 'k', 'b', 'n', 'r'],  # Dòng 1 - Quân đen
            ['p', 'p', 'p', 'p', 'p', 'p', 'p', 'p'],  # Dòng 2 - Tốt đen
            ['.', '.', '.', '.', '.', '.', '.', '.'],  # Dòng 3 - Chỗ trống
            ['.', '.', '.', '.', '.', '.', '.', '.'],  # Dòng 4 - Chỗ trống
            ['.', '.', '.', '.', '.', '.', '.', '.'],  # Dòng 5 - Chỗ trống
            ['.', '.', '.', '.', '.', '.', '.', '.'],  # Dòng 6 - Chỗ trống
            ['P', 'P', 'P', 'P', 'P', 'P', 'P', 'P'],  # Dòng 7 - Tốt trắng
            ['R', 'N', 'B', 'Q', 'K', 'B', 'N', 'R']   # Dòng 8 - Quân trắng
        ]

    def move(self, start, end):
        # Lưu trạng thái bàn cờ trước khi thực hiện nước đi
        self.history.append([row[:] for row in self.board])

        start_row, start_col = start
        end_row, end_col = end
        self.board[end_row][end_col] = self.board[start_row][start_col]
        self.board[start_row][start_col] = "."

    def undo_move(self):
        if self.history:
            self.board = self.history.pop()


    def get_piece_moves(self, piece, row, col):
        # Trả về tất cả các nước đi hợp lệ của một quân cờ tại vị trí `row, col`
        moves = []
        directions = {
            'p': self.pawn_moves,  # Quân tốt
            'r': self.rook_moves,  # Quân xe
            'n': self.knight_moves,  # Quân mã
            'b': self.bishop_moves,  # Quân tượng
            'q': self.queen_moves,  # Quân hậu
            'k': self.king_moves,  # Quân vua
        }
        return directions.get(piece.lower(), lambda *args: [])(piece, row, col)

    def pawn_moves(self, piece, row, col):
        # Các nước đi hợp lệ của quân tốt (pawn)
        direction = -1 if piece.isupper() else 1  # Hướng di chuyển của quân tốt (lên hay xuống)
        start_row = 6 if piece.isupper() else 1  # Dòng xuất phát của quân tốt
        moves = []

        # Di chuyển 1 ô về phía trước
        if 0 <= row + direction < 8 and self.board[row + direction][col] == '.':
            moves.append(((row, col), (row + direction, col)))

        # Di chuyển 2 ô nếu quân tốt chưa di chuyển
        if row == start_row and self.board[row + 2 * direction][col] == '.' and self.board[row + direction][col] == '.':
            moves.append(((row, col), (row + 2 * direction, col)))

        # Ăn chéo quân địch
        for col_offset in [-1, 1]:
            if 0 <= col + col_offset < 8 and 0 <= row + direction < 8:
                target = self.board[row + direction][col + col_offset]
                if target != '.' and self._is_enemy(piece, target):
                    moves.append(((row, col), (row + direction, col + col_offset)))
        return moves

    def rook_moves(self, piece, row, col):
        # Các nước đi hợp lệ của quân xe (rook)
        return self.sliding_moves(piece, row, col, [(1, 0), (-1, 0), (0, 1), (0, -1)])

    def knight_moves(self, piece, row, col):
        # Các nước đi hợp lệ của quân mã (knight)
        return self.jumping_moves(piece, row, col, [(2, 1), (2, -1), (-2, 1), (-2, -1),
                                                    (1, 2), (1, -2), (-1, 2), (-1, -2)])

    def bishop_moves(self, piece, row, col):
        # Các nước đi hợp lệ của quân tượng (bishop)
        return self.sliding_moves(piece, row, col, [(1, 1), (1, -1), (-1, 1), (-1, -1)])

    def queen_moves(self, piece, row, col):
        # Các nước đi hợp lệ của quân hậu (queen), kết hợp di chuyển của xe và tượng
        return self.rook_moves(piece, row, col) + self.bishop_moves(piece, row, col)

    def king_moves(self, piece, row, col):
        # Các nước đi hợp lệ của quân vua (king)
        return self.jumping_moves(piece, row, col, [(1, 0), (-1, 0), (0, 1), (0, -1),
                                                    (1, 1), (1, -1), (-1, 1), (-1, -1)])

    def sliding_moves(self, piece, row, col, directions):
        # Hàm xử lý các quân cờ có thể di chuyển theo hướng liên tục (xe, tượng, hậu)
        moves = []
        for d_row, d_col in directions:
            for i in range(1, 8):  # Lặp qua các ô trong cùng một hướng
                new_row, new_col = row + d_row * i, col + d_col * i
                if 0 <= new_row < 8 and 0 <= new_col < 8:
                    target = self.board[new_row][new_col]
                    if target == '.':
                        moves.append(((row, col), (new_row, new_col)))
                    elif self._is_enemy(piece, target):
                        moves.append(((row, col), (new_row, new_col)))
                        break  # Dừng nếu gặp quân địch
                    else:
                        break  # Dừng nếu gặp quân đồng minh
        return moves

    def jumping_moves(self, piece, row, col, directions):
        # Hàm xử lý các quân cờ có thể nhảy (mã, vua)
        moves = []
        for d_row, d_col in directions:
            new_row, new_col = row + d_row, col + d_col
            if 0 <= new_row < 8 and 0 <= new_col < 8:
                target = self.board[new_row][new_col]
                if target == '.' or self._is_enemy(piece, target):
                    moves.append(((row, col), (new_row, new_col)))
        return moves

    def _is_enemy(self, piece, target):
        # Kiểm tra xem quân cờ `target` có phải quân địch của quân `piece` hay không
        return (piece.isupper() and target.islower()) or (piece.islower() and target.isupper())

    def _try_move(self, start, end, color):
        # Thử một nước đi và kiểm tra xem quân vua có bị chiếu không sau khi di chuyển
        self.move(start, end)
        is_safe = not self.is_in_check(color)
        self.undo_move()
        return is_safe


    def _is_piece_color(self, piece, color):
        # Kiểm tra xem quân cờ có đúng màu hay không (trắng hoặc đen)
        return (color == 'white' and piece.isupper()) or (color == 'black' and piece.islower())

    def king_position_in_check(self, king_position, piece, row, col, opponent_color):
        # Kiểm tra xem quân vua có bị đe dọa bởi quân `piece` hay không
        return king_position in [move[1] for move in self.get_piece_moves(piece, row, col)]

    def find_king(self, color):
        # Tìm vị trí quân vua của màu `color` (trắng hoặc đen)
        for row in range(8):
            for col in range(8):
                piece = self.board[row][col]
                if (color == "white" and piece == 'K') or (color == "black" and piece == 'k'):
                    return (row, col)
        return None

    def is_checkmate(self, color):
        # Kiểm tra xem có phải tình huống chiếu hết không
        return self.is_in_check(color) and not any(
            self._try_move(start, end, color) for start, end in self.get_all_moves(color)
        )

    def is_stalemate(self, color):
        # Kiểm tra xem có phải tình huống hòa không
        return not self.is_in_check(color) and not self.get_all_moves(color)

    def is_in_check(self, color):
        # Kiểm tra xem quân vua của màu `color` có bị chiếu không
        king_position = self.find_king(color)
        opponent_color = 'black' if color == 'white' else 'white'
        return any(
            self.king_position_in_check(king_position, piece, row, col, opponent_color)
            for row in range(8) for col in range(8)
            if (piece := self.board[row][col]) != '.' and self._is_piece_color(piece, opponent_color)
        )
    def get_all_moves(self, color):
        # Trả về tất cả nước đi hợp lệ cho quân màu `color` (trắng hoặc đen)
        return [
            move
            for row in range(8)
            for col in range(8)
            if (piece := self.board[row][col]) != '.' and self._is_piece_color(piece, color)
            for move in self.get_piece_moves(piece, row, col)
        ]

    def reset_game(self):
        self.board = [
            ["r", "n", "b", "q", "k", "b", "n", "r"],
            ["p", "p", "p", "p", "p", "p", "p", "p"],
            [".", ".", ".", ".", ".", ".", ".", "."],
            [".", ".", ".", ".", ".", ".", ".", "."],
            [".", ".", ".", ".", ".", ".", ".", "."],
            [".", ".", ".", ".", ".", ".", ".", "."],
            ["P", "P", "P", "P", "P", "P", "P", "P"],
            ["R", "N", "B", "Q", "K", "B", "N", "R"]
        ]
        self.history = []  # Xóa lịch sử khi reset
