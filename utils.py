def parse_move(move):
    """
    Chuyển nước đi dạng chuỗi (ví dụ: 'e2 e4') thành tọa độ.
    :param move: Chuỗi nước đi, dạng 'e2 e4' (bắt đầu và kết thúc).
    :return: Tuple tọa độ start và end ((x1, y1), (x2, y2))
    """
    try:
        parts = move.split()
        if len(parts) != 2:
            return None, None

        # Chuyển đổi từ 'e2' -> (6, 4) (Vì hàng bắt đầu từ 8, do đó 'e' = 4, '2' = 6)
        start = (8 - int(parts[0][1]), ord(parts[0][0]) - ord('a'))
        end = (8 - int(parts[1][1]), ord(parts[1][0]) - ord('a'))
        return start, end
    except (IndexError, ValueError):
        print("Lỗi: Nước đi không đúng định dạng!")
        return None, None

def is_within_bounds(position):
    """
    Kiểm tra xem một vị trí có nằm trong giới hạn bàn cờ hay không.
    :param position: Tuple tọa độ (x, y)
    :return: True nếu nằm trong bàn cờ, False nếu không.
    """
    x, y = position
    return 0 <= x < 8 and 0 <= y < 8

def validate_user_move(board, move, color):
    """
    Kiểm tra nước đi của người dùng từ đầu vào.
    :param board: Trạng thái bàn cờ hiện tại (list 2D).
    :param move: Chuỗi nước đi dạng 'e2 e4'.
    :param color: Màu của người chơi ('white' hoặc 'black').
    :return: True nếu nước đi hợp lệ, False nếu không.
    """
    # Chuyển nước đi từ chuỗi sang tọa độ
    start, end = parse_move(move)

    # Kiểm tra nước đi có hợp lệ không
    if start is None or end is None:
        print("Lỗi: Nước đi không đúng định dạng! Hãy nhập theo dạng 'e2 e4'.")
        return False

    sx, sy = start
    ex, ey = end

    # Kiểm tra ô bắt đầu có quân cờ của người chơi
    piece = board[sx][sy]
    if piece == ".":
        print("Lỗi: Không có quân cờ nào tại vị trí bắt đầu.")
        return False

    if color == "white" and piece.islower():
        print("Lỗi: Bạn không thể di chuyển quân đen.")
        return False
    if color == "black" and piece.isupper():
        print("Lỗi: Bạn không thể di chuyển quân trắng.")
        return False

    # Kiểm tra nước đi có hợp lệ không
    if not is_valid_move(board, start, end, color):
        print("Lỗi: Nước đi không hợp lệ theo quy tắc cờ vua!")
        return False

    print("Nước đi hợp lệ!")
    return True


def is_valid_move(board, start, end, color):
    """
    Kiểm tra tính hợp lệ của nước đi từ `start` đến `end` theo các quy tắc của từng quân.
    :param board: Trạng thái bàn cờ (list 2D)
    :param start: Tuple tọa độ (x1, y1)
    :param end: Tuple tọa độ (x2, y2)
    :param color: 'white' hoặc 'black' để chỉ màu người chơi.
    :return: True nếu nước đi hợp lệ, False nếu không.
    """
    sx, sy = start
    ex, ey = end

    # Kiểm tra giới hạn bàn cờ
    if not (is_within_bounds(start) and is_within_bounds(end)):
        print("Lỗi: Nước đi ra ngoài bàn cờ!")
        return False

    piece = board[sx][sy]
    target = board[ex][ey]

    # Kiểm tra ô bắt đầu có quân cờ đúng màu
    if piece == ".":
        return False  # Không có quân cờ để di chuyển
    if color == "white" and piece.islower():
        return False  # Quân đen không được di chuyển
    if color == "black" and piece.isupper():
        return False  # Quân trắng không được di chuyển

    # Không được ăn quân cùng màu
    if (color == "white" and target.isupper()) or (color == "black" and target.islower()):
        return False

    # Quy tắc cơ bản cho từng loại quân cờ
    if piece.lower() == "p":  # Quân Tốt
        return is_valid_pawn_move(board, start, end, color)
    if piece.lower() == "r":  # Quân Xe
        return is_valid_rook_move(board, start, end)
    if piece.lower() == "n":  # Quân Mã
        return is_valid_knight_move(start, end)
    if piece.lower() == "b":  # Quân Tượng
        return is_valid_bishop_move(board, start, end)
    if piece.lower() == "q":  # Quân Hậu
        return is_valid_queen_move(board, start, end)
    if piece.lower() == "k":  # Quân Vua
        return is_valid_king_move(start, end)

    return False

def is_valid_pawn_move(board, start, end, color):
    """
    Kiểm tra nước đi của quân Tốt.
    """
    direction = -1 if color == "white" else 1  # Hướng di chuyển của quân Tốt
    sx, sy = start
    ex, ey = end

    # Tiến lên 1 ô
    if sy == ey and board[ex][ey] == "." and ex == sx + direction:
        return True

    # Tiến lên 2 ô (nước đi đầu tiên)
    if sy == ey and board[ex][ey] == "." and ex == sx + 2 * direction and (sx == 6 or sx == 1):
        return board[sx + direction][sy] == "."

    # Ăn chéo quân đối phương
    if abs(ey - sy) == 1 and ex == sx + direction and board[ex][ey] != ".":
        return True

    return False


def is_valid_rook_move(board, start, end):
    """
    Kiểm tra nước đi của quân Xe.
    """
    sx, sy = start
    ex, ey = end

    if sx != ex and sy != ey:
        return False  # Xe chỉ đi theo hàng hoặc cột

    # Kiểm tra có bị chặn trên đường đi không
    return is_path_clear(board, start, end)


def is_valid_knight_move(start, end):
    """
    Kiểm tra nước đi của quân Mã.
    """
    sx, sy = start
    ex, ey = end
    return (abs(sx - ex), abs(sy - ey)) in [(2, 1), (1, 2)]


def is_valid_bishop_move(board, start, end):
    """
    Kiểm tra nước đi của quân Tượng.
    """
    sx, sy = start
    ex, ey = end

    if abs(sx - ex) != abs(sy - ey):
        return False  # Tượng chỉ đi chéo

    return is_path_clear(board, start, end)


def is_valid_queen_move(board, start, end):
    """
    Kiểm tra nước đi của quân Hậu (kết hợp Xe và Tượng).
    """
    return is_valid_rook_move(board, start, end) or is_valid_bishop_move(board, start, end)


def is_valid_king_move(start, end):
    """
    Kiểm tra nước đi của quân Vua.
    """
    sx, sy = start
    ex, ey = end
    return max(abs(sx - ex), abs(sy - ey)) == 1


def is_path_clear(board, start, end):
    """
    Kiểm tra đường đi có bị chặn không (dùng cho Xe, Tượng, Hậu).
    """
    sx, sy = start
    ex, ey = end
    dx = (ex - sx) // max(1, abs(ex - sx)) if sx != ex else 0
    dy = (ey - sy) // max(1, abs(ey - sy)) if sy != ey else 0

    x, y = sx + dx, sy + dy
    while (x, y) != (ex, ey):
        if board[x][y] != ".":
            return False
        x += dx
        y += dy
    return True

def validate_user_move(board, move, color):
    """
    Kiểm tra nước đi của người dùng từ đầu vào.
    :param board: Trạng thái bàn cờ hiện tại (list 2D).
    :param move: Chuỗi nước đi dạng 'e2 e4'.
    :param color: Màu của người chơi ('white' hoặc 'black').
    :return: True nếu nước đi hợp lệ, False nếu không.
    """
    # Chuyển nước đi từ chuỗi sang tọa độ
    start, end = parse_move(move)

    # Kiểm tra nước đi có hợp lệ không
    if start is None or end is None:
        print("Lỗi: Nước đi không đúng định dạng! Hãy nhập theo dạng 'e2 e4'.")
        return False

    sx, sy = start
    ex, ey = end

    # Kiểm tra ô bắt đầu có quân cờ của người chơi
    piece = board[sx][sy]
    if piece == ".":
        print("Lỗi: Không có quân cờ nào tại vị trí bắt đầu.")
        return False

    if color == "white" and piece.islower():
        print("Lỗi: Bạn không thể di chuyển quân đen.")
        return False
    if color == "black" and piece.isupper():
        print("Lỗi: Bạn không thể di chuyển quân trắng.")
        return False

    # Kiểm tra nước đi có hợp lệ không
    if not is_valid_move(board, start, end, color):
        print("Lỗi: Nước đi không hợp lệ theo quy tắc cờ vua!")
        return False

    print("Nước đi hợp lệ!")
    return True


def print_board(board):
    """
    In bàn cờ ra console (hữu ích khi debug).
    """
    for row in board:
        print(' '.join(row))
    print()
