import math
from board import Board


def evaluate_board(board):
    """Đánh giá bàn cờ dựa trên giá trị quân cờ và yếu tố chiến lược."""

    # Dictionary chứa giá trị các quân cờ
    piece_values = {'p': -1, 'r': -5, 'n': -3, 'b': -3, 'q': -9, 'k': -100,
                    'P': 1, 'R': 5, 'N': 3, 'B': 3, 'Q': 9, 'K': 100}

    # Tính tổng giá trị các quân cờ trên bàn cờ
    value = sum(piece_values.get(piece, 0) for row in board.board for piece in row)

    # Điều chỉnh giá trị của quân Tốt của người trắng trên các hàng cụ thể
    for row, col in [(6, 0.5), (4, 0.2)]:
        value += sum(0.5 if board.board[row][col] == 'P' else -0.5 for col in range(8))

    # Điều chỉnh giá trị của quân Tốt của người đen trên các hàng cụ thể
    for row, col in [(1, -0.5), (3, -0.2)]:
        value += sum(-0.5 if board.board[row][col] == 'p' else 0 for col in range(8))

    # Tính giá trị của quân vua nếu tìm thấy
    if board.find_king("white"): value += 0.5
    if board.find_king("black"): value -= 0.5

    # Đánh giá các ô trung tâm của bàn cờ
    central_squares = [(3, 3), (3, 4), (4, 3), (4, 4)]
    for x, y in central_squares:
        if board.board[x][y] == 'P':
            value += 0.5
        elif board.board[x][y] == 'p':
            value -= 0.5

    return value


def minimax(board, depth, is_maximizing, alpha, beta):
    if depth == 0:
        return evaluate_board(board)  # Nếu độ sâu là 0, đánh giá bàn cờ hiện tại
    best_eval = -math.inf if is_maximizing else math.inf  # Giá trị tốt nhất ban đầu
    moves = board.get_all_moves('white' if is_maximizing else 'black')  # Lấy danh sách các nước đi hợp lệ

    # Duyệt qua tất cả các nước đi hợp lệ
    for move in moves:
        board.move(move[0], move[1])  # Thực hiện nước đi
        if board.is_in_check('white' if is_maximizing else 'black'):  # Kiểm tra xem có tạo ra tình huống "check" không
            board.undo_move()  # Nếu có, hoàn tác nước đi
            continue

        # Đệ quy gọi minimax cho bước tiếp theo
        eval = minimax(board, depth - 1, not is_maximizing, alpha, beta)
        board.undo_move()  # Hoàn tác nước đi

        # Cập nhật giá trị tốt nhất dựa trên người chơi
        if is_maximizing:
            best_eval = max(best_eval, eval)  # Tối đa hóa giá trị cho người chơi trắng
            alpha = max(alpha, eval)  # Cập nhật alpha
        else:
            best_eval = min(best_eval, eval)  # Tối thiểu hóa giá trị cho người chơi đen
            beta = min(beta, eval)  # Cập nhật beta

        # Cắt tỉa nếu không cần phải duyệt thêm
        if beta <= alpha:
            break

    return best_eval


def find_best_move(board, depth, color):
    """Tìm nước đi tốt nhất cho người chơi dựa trên thuật toán Minimax."""
    best_move, best_eval = None, -math.inf if color == 'white' else math.inf  # Khởi tạo giá trị tốt nhất ban đầu

    # Duyệt qua tất cả các nước đi hợp lệ của người chơi
    for move in board.get_all_moves(color):
        board.move(move[0], move[1])  # Thực hiện nước đi
        if board.is_in_check(color):  # Kiểm tra xem có tạo ra tình huống "check" không
            board.undo_move()  # Nếu có, hoàn tác nước đi
            continue

        # Gọi minimax để đánh giá nước đi
        eval = minimax(board, depth - 1, color != 'white', -math.inf, math.inf)
        board.undo_move()  # Hoàn tác nước đi

        # Cập nhật nước đi tốt nhất dựa trên đánh giá
        if (color == 'white' and eval > best_eval) or (color == 'black' and eval < best_eval):
            best_eval, best_move = eval, move

    return best_move

def iterative_deepening_search(board, max_depth, color):
    """Tìm nước đi tốt nhất bằng thuật toán tìm kiếm sâu dần."""
    best_move = None

    # Duyệt qua các độ sâu từ 1 đến max_depth
    for depth in range(1, max_depth + 1):
        best_move = find_best_move(board, depth, color)  # Tìm nước đi tốt nhất cho từng độ sâu
    return best_move
