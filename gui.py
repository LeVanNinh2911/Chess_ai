import os

import pygame

# Kích thước cửa sổ và ô bàn cờ
WIDTH, HEIGHT = 640, 720  # Chiều cao tăng lên để có chỗ cho các nút
SQUARE_SIZE = WIDTH // 8

# Màu sắc
WHITE = (240, 217, 181)
BLACK = (181, 136, 99)
HIGHLIGHT_COLOR = (186, 202, 68)  # Màu khi ô được chọn
BUTTON_COLOR = (70, 130, 180)
BUTTON_TEXT_COLOR = (255, 255, 255)

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
                piece = self.board.board[row][col]
                if piece != ".":
                    color = "black" if piece.islower() else "white"
                    piece_key = f"{color[0]}{piece.upper()}"
                    if piece_key in self.piece_images:
                        self.window.blit(self.piece_images[piece_key], (col * SQUARE_SIZE, row * SQUARE_SIZE))

    def draw_buttons(self):
        # Vẽ nút "Bắt đầu lại"
        pygame.draw.rect(self.window, BUTTON_COLOR, (120, 660, 160, 40))
        self.draw_text("Reset", 200, 680, BUTTON_TEXT_COLOR, 24)

        # Vẽ nút "Thoát"
        pygame.draw.rect(self.window, BUTTON_COLOR, (360, 660, 160, 40))
        self.draw_text("Log out", 440, 680, BUTTON_TEXT_COLOR, 24)

    def draw_text(self, text, x, y, color, size):
        font = pygame.font.Font(None, size)
        text_surface = font.render(text, True, color)
        text_rect = text_surface.get_rect(center=(x, y))
        self.window.blit(text_surface, text_rect)

    def highlight_square(self, row, col):
        self.selected_square = (row, col)

    def clear_highlight(self):
        self.selected_square = None

    def update(self):
        # Vẽ bàn cờ, quân cờ, và kiểm tra trạng thái trò chơi
        self.draw_board()
        self.draw_pieces()
        self.draw_buttons()

        if self.board.is_checkmate(self.current_turn):
            winner = "Black" if self.current_turn == "white" else "White"
            self.show_game_over_message(f"Checkmate! {winner} wins!")
            self.board.reset_game()  # Reset game after checkmate
        elif self.board.is_stalemate(self.current_turn):
            self.show_game_over_message("Stalemate! It's a draw!")
            self.board.reset_game()  # Reset game after stalemate

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

    def handle_button_click(self, mouse_pos):
        x, y = mouse_pos
        if 120 <= x <= 280 and 660 <= y <= 700:  # Vùng nút "Bắt đầu lại"
            self.board.reset_game()
            self.current_turn = 'white'  # Reset lại lượt chơi về trắng
        elif 360 <= x <= 520 and 660 <= y <= 700:  # Vùng nút "Thoát"
            pygame.quit()
            exit()

    def show_game_over_message(self, message):
        # Hiển thị thông báo kết thúc trò chơi
        self.window.fill((0, 0, 0))  # Xóa màn hình
        self.draw_board()
        self.draw_pieces()
        self.draw_buttons()

        font = pygame.font.Font(None, 60)
        text_surface = font.render(message, True, (255, 255, 255))
        text_rect = text_surface.get_rect(center=(WIDTH // 2, HEIGHT // 2))
        self.window.blit(text_surface, text_rect)

        pygame.display.update()
        pygame.time.delay(3000)  # Hiển thị thông báo trong 3 giây