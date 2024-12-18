import pygame
import os

# Kích thước cửa sổ và ô bàn cờ
WIDTH, HEIGHT = 640, 640
SQUARE_SIZE = WIDTH // 8

# Màu sắc
WHITE = (240, 217, 181)
BLACK = (181, 136, 99)
HIGHLIGHT_COLOR = (186, 202, 68)  # Màu khi ô được chọn



class ChessGUI:
    def __init__(self, board):
        self.board = board
        self.window = pygame.display.set_mode((WIDTH, HEIGHT))
        pygame.display.set_caption("Chess")
        self.piece_images = self.load_piece_images()
        self.selected_square = None
        self.current_turn = 'white'

    def load_piece_images(self):
        piece_images = {}
        pieces = ["P", "R", "N", "B", "Q", "K"]
        colors = {"black": "b", "white": "w"}

        for color, color_code in colors.items():
            for piece in pieces:
                filename = f"{color_code}{piece}.png"
                image_path = os.path.join("pieces_image", filename)

                if not os.path.exists(image_path):
                    raise FileNotFoundError(f"File {image_path} không tồn tại. Kiểm tra thư mục pieces_image.")

                piece_images[f"{color_code}{piece}"] = pygame.transform.scale(
                    pygame.image.load(image_path), (SQUARE_SIZE, SQUARE_SIZE)
                )
        return piece_images

    def draw_board(self):
        for row in range(8):
            for col in range(8):
                color = WHITE if (row + col) % 2 == 0 else BLACK
                if self.selected_square == (row, col):
                    color = HIGHLIGHT_COLOR
                pygame.draw.rect(self.window, color, (col * SQUARE_SIZE, row * SQUARE_SIZE, SQUARE_SIZE, SQUARE_SIZE))

    def draw_pieces(self):
        for row in range(8):
            for col in range(8):
                piece = self.board[row][col]
                if piece != ".":
                    color = "black" if piece.islower() else "white"
                    piece_key = f"{color[0]}{piece.upper()}"
                    if piece_key in self.piece_images:
                        self.window.blit(self.piece_images[piece_key], (col * SQUARE_SIZE, row * SQUARE_SIZE))

    def highlight_square(self, row, col):
        self.selected_square = (row, col)

    def clear_highlight(self):
        self.selected_square = None

    def update(self):
        self.draw_board()
        self.draw_pieces()
        pygame.display.update()

    def handle_click(self, row, col):
        if self.selected_square:
            start_row, start_col = self.selected_square
            if (start_row, start_col) != (row, col):
                self.board.move((start_row, start_col), (row, col))
                self.clear_highlight()
                self.current_turn = 'black' if self.current_turn == 'white' else 'white'
        else:
            self.highlight_square(row, col)
