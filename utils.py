def parse_move(move):
    """Chuyển nước đi dạng chuỗi (ví dụ: 'e2 e4') thành tọa độ."""
    try:
        start, end = move.split()
        start = (8 - int(start[1]), ord(start[0]) - ord('a'))
        end = (8 - int(end[1]), ord(end[0]) - ord('a'))
        return start, end
    except (IndexError, ValueError):
        print("Lỗi: Nước đi không đúng định dạng!")
        return None, None

def is_within_bounds(position):
    """Kiểm tra xem vị trí có nằm trong bàn cờ không."""
    x, y = position
    return 0 <= x < 8 and 0 <= y < 8

def validate_user_move(board, move, color):
    """Kiểm tra tính hợp lệ của nước đi người chơi."""
    start, end = parse_move(move)
    if start is None or end is None:
        return False

    sx, sy = start
    piece = board[sx][sy]

    if piece == "." or (color == "white" and piece.islower()) or (color == "black" and piece.isupper()):
        print("Lỗi: Quân cờ không hợp lệ!")
        return False

    if not is_valid_move(board, start, end, color):
        return False

    print("Nước đi hợp lệ!")
    return True

def is_valid_move(board, start, end, color):
    """Kiểm tra tính hợp lệ của nước đi từ start đến end."""
    sx, sy = start
    ex, ey = end

    if not is_within_bounds(start) or not is_within_bounds(end):
        print("Lỗi: Nước đi ra ngoài bàn cờ!")
        return False

    piece = board[sx][sy]
    target = board[ex][ey]

    if piece == "." or (color == "white" and piece.islower()) or (color == "black" and piece.isupper()):
        return False

    if (color == "white" and target.isupper()) or (color == "black" and target.islower()):
        return False

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
    """Kiểm tra nước đi của quân Tốt."""
    direction = -1 if color == "white" else 1
    sx, sy = start
    ex, ey = end

    if sy == ey and board[ex][ey] == "." and ex == sx + direction:
        return True

    if sy == ey and board[ex][ey] == "." and ex == sx + 2 * direction and (sx == 6 or sx == 1):
        return board[sx + direction][sy] == "."

    if abs(ey - sy) == 1 and ex == sx + direction and board[ex][ey] != ".":
        return True

    return False

def is_valid_rook_move(board, start, end):
    """Kiểm tra nước đi của quân Xe."""
    sx, sy = start
    ex, ey = end

    if sx != ex and sy != ey:
        return False

    return is_path_clear(board, start, end)

def is_valid_knight_move(start, end):
    """Kiểm tra nước đi của quân Mã."""
    sx, sy = start
    ex, ey = end
    return (abs(sx - ex), abs(sy - ey)) in [(2, 1), (1, 2)]

def is_valid_bishop_move(board, start, end):
    """Kiểm tra nước đi của quân Tượng."""
    sx, sy = start
    ex, ey = end

    if abs(sx - ex) != abs(sy - ey):
        return False

    return is_path_clear(board, start, end)

def is_valid_queen_move(board, start, end):
    """Kiểm tra nước đi của quân Hậu."""
    return is_valid_rook_move(board, start, end) or is_valid_bishop_move(board, start, end)

def is_valid_king_move(start, end):
    """Kiểm tra nước đi của quân Vua."""
    sx, sy = start
    ex, ey = end
    return max(abs(sx - ex), abs(sy - ey)) == 1

def is_path_clear(board, start, end):
    """Kiểm tra đường đi có bị chặn không (dùng cho Xe, Tượng, Hậu)."""
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

def print_board(board):
    """In bàn cờ ra console (hữu ích khi debug)."""
    for row in board:
        print(' '.join(row))
    print()
