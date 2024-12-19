import math
from board import Board

def evaluate_board(board):
    """
    Đánh giá bàn cờ bằng cách tính tổng giá trị của các quân cờ.
    Thêm vào đánh giá các yếu tố như bảo vệ quân vua và vị trí chiến lược.
    """
    piece_values = {'p': -1, 'r': -5, 'n': -3, 'b': -3, 'q': -9, 'k': -100,
                    'P': 1, 'R': 5, 'N': 3, 'B': 3, 'Q': 9, 'K': 100}

    value = 0
    for row in board.board:
        for piece in row:
            if piece in piece_values:
                value += piece_values[piece]

    # Thêm đánh giá chiến lược, như bảo vệ quân vua, tiến quân tốt...
    for row in range(8):
        for col in range(8):
            piece = board.board[row][col]
            if piece == 'P':  # Tốt trắng
                if row == 6:  # Tốt gần tới hàng cuối
                    value += 0.5
                if row == 4:  # Tiến được ra trung tâm
                    value += 0.2
            elif piece == 'p':  # Tốt đen
                if row == 1:  # Tốt đen gần tới hàng cuối
                    value -= 0.5
                if row == 3:  # Tiến được ra trung tâm
                    value -= 0.2

    # Bảo vệ quân vua
    white_king_pos = board.find_king("white")
    black_king_pos = board.find_king("black")
    if white_king_pos:
        value += 0.5  # Giá trị bảo vệ cho quân vua trắng
    if black_king_pos:
        value -= 0.5  # Giá trị bảo vệ cho quân vua đen

    # Đánh giá kiểm soát trung tâm (các ô c4, d4, c5, d5)
    central_squares = [(3, 3), (3, 4), (4, 3), (4, 4)]
    for x, y in central_squares:
        piece = board.board[x][y]
        if piece == 'P':
            value += 0.5
        elif piece == 'p':
            value -= 0.5

    return value

def minimax(board, depth, is_maximizing, alpha, beta):
    """
    Hàm minimax với alpha-beta pruning để tìm kiếm nước đi tốt nhất.
    Thêm logic kiểm tra các tình huống checkmate và stalemate.
    """
    if depth == 0:
        return evaluate_board(board)

    # Nếu là người chơi tối đa (trắng), tìm nước đi tối ưu
    if is_maximizing:
        max_eval = -math.inf
        for move in board.get_all_moves('white'):
            board.move(move[0], move[1])
            if board.is_in_check('white'):
                board.undo_move()
                continue  # Bỏ qua nếu quân vua trắng bị chiếu
            eval = minimax(board, depth - 1, False, alpha, beta)
            board.undo_move()
            max_eval = max(max_eval, eval)
            alpha = max(alpha, eval)
            if beta <= alpha:
                break  # Cắt tỉa nếu không cần tiếp tục
        return max_eval
    else:
        # Nếu là người chơi tối thiểu (đen), tìm nước đi tối ưu
        min_eval = math.inf
        for move in board.get_all_moves('black'):
            board.move(move[0], move[1])
            if board.is_in_check('black'):
                board.undo_move()
                continue  # Bỏ qua nếu quân vua đen bị chiếu
            eval = minimax(board, depth - 1, True, alpha, beta)
            board.undo_move()
            min_eval = min(min_eval, eval)
            beta = min(beta, eval)
            if beta <= alpha:
                break  # Cắt tỉa nếu không cần tiếp tục
        return min_eval

def iterative_deepening_search(board, max_depth, color):
    """
    Tìm kiếm nước đi tốt nhất bằng phương pháp Tìm kiếm sâu dần kết hợp với Minimax Alpha-Beta Pruning.
    """
    best_move = None
    for depth in range(1, max_depth + 1):
        best_move = find_best_move(board, depth, color)
    return best_move

def find_best_move(board, depth, color):
    """
    Tìm nước đi tốt nhất cho bên màu `color` (trắng hoặc đen) sử dụng thuật toán minimax với alpha-beta pruning.
    """
    best_move = None
    if color == 'white':
        max_eval = -math.inf
        for move in board.get_all_moves('white'):
            board.move(move[0], move[1])
            if board.is_in_check('white'):
                board.undo_move()
                continue  # Bỏ qua nếu quân vua trắng bị chiếu
            eval = minimax(board, depth - 1, False, -math.inf, math.inf)
            board.undo_move()
            if eval > max_eval:
                max_eval = eval
                best_move = move
    else:
        min_eval = math.inf
        for move in board.get_all_moves('black'):
            board.move(move[0], move[1])
            if board.is_in_check('black'):
                board.undo_move()
                continue  # Bỏ qua nếu quân vua đen bị chiếu
            eval = minimax(board, depth - 1, True, -math.inf, math.inf)
            board.undo_move()
            if eval < min_eval:
                min_eval = eval
                best_move = move
    return best_move
