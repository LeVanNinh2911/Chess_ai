import os
import pygame

# Kích thước cửa sổ và ô bàn cờ
WIDTH, HEIGHT = 640, 720
SQUARE_SIZE = WIDTH // 8

# Màu sắc
WHITE, BLACK = (240, 217, 181), (181, 136, 99)
HIGHLIGHT_COLOR = (186, 202, 68)
BUTTON_COLOR, BUTTON_TEXT_COLOR = (70, 130, 180), (255, 255, 255)

class ChessGUI:
    def __init__(self, board):
        self.board = board  # Bàn cờ
        self.window = pygame.display.set_mode((WIDTH, HEIGHT))  # Cửa sổ trò chơi
        pygame.display.set_caption("Chess")  # Tiêu đề cửa sổ
        self.piece_images = self.load_piece_images()  # Tải hình ảnh quân cờ
        self.selected_square = None  # Ô được chọn
        self.current_turn = 'white'  # Lượt chơi hiện tại

    def load_piece_images(self):
        piece_images = {}
        pieces = ["P", "R", "N", "B", "Q", "K"]
        colors = {"black": "b", "white": "w"}

        for color, color_code in colors.items():
            for piece in pieces:
                filename = f"{color_code}{piece}.png"
                image_path = os.path.join("pieces_image", filename)

                if not os.path.exists(image_path):  # Kiểm tra file hình ảnh
                    raise FileNotFoundError(f"File {image_path} không tồn tại.")

                piece_images[f"{color_code}{piece}"] = pygame.transform.scale(
                    pygame.image.load(image_path), (SQUARE_SIZE, SQUARE_SIZE)
                )
        return piece_images

    def draw_board(self):
        # Vẽ bàn cờ
        for row in range(8):
            for col in range(8):
                color = WHITE if (row + col) % 2 == 0 else BLACK
                if self.selected_square == (row, col):
                    color = HIGHLIGHT_COLOR
                pygame.draw.rect(self.window, color, (col * SQUARE_SIZE, row * SQUARE_SIZE, SQUARE_SIZE, SQUARE_SIZE))

    def draw_pieces(self):
        # Vẽ quân cờ trên bàn
        for row in range(8):
            for col in range(8):
                piece = self.board.board[row][col]
                if piece != ".":
                    color = "black" if piece.islower() else "white"
                    piece_key = f"{color[0]}{piece.upper()}"
                    self.window.blit(self.piece_images[piece_key], (col * SQUARE_SIZE, row * SQUARE_SIZE))

    def draw_buttons(self):
        pygame.draw.rect(self.window, BUTTON_COLOR, (40, 660, 160, 40))
        self.draw_text("Undo", 120, 680, BUTTON_TEXT_COLOR, 24)

        pygame.draw.rect(self.window, BUTTON_COLOR, (240, 660, 160, 40))
        self.draw_text("Reset", 320, 680, BUTTON_TEXT_COLOR, 24)

        pygame.draw.rect(self.window, BUTTON_COLOR, (440, 660, 160, 40))
        self.draw_text("Log out", 520, 680, BUTTON_TEXT_COLOR, 24)

    def draw_text(self, text, x, y, color, size):
        # Vẽ thông báo lên màn hình
        font = pygame.font.Font(None, size)
        text_surface = font.render(text, True, color)
        text_rect = text_surface.get_rect(center=(x, y))
        self.window.blit(text_surface, text_rect)

    def highlight_square(self, row, col):
        # Đánh dấu ô đã chọn
        self.selected_square = (row, col)

    def clear_highlight(self):
        # Xóa đánh dấu ô
        self.selected_square = None

    def update(self):
        # Cập nhật màn hình
        self.draw_board()
        self.draw_pieces()
        self.draw_buttons()

        if self.board.is_checkmate(self.current_turn):  # Kiểm tra checkmate
            winner = "Black" if self.current_turn == "white" else "White"
            self.show_game_over_message(f"Checkmate! {winner} wins!")
            self.board.reset_game()
        elif self.board.is_stalemate(self.current_turn):  # Kiểm tra stalemate
            self.show_game_over_message("Stalemate! It's a draw!")
            self.board.reset_game()

        pygame.display.update()

    def handle_click(self, row, col):
        # Xử lý khi click vào bàn cờ
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
        if 40 <= x <= 200 and 660 <= y <= 700:  # Nút Undo
            self.board.undo_move()
            self.current_turn = 'black' if self.current_turn == 'white' else 'white'
            self.update()
        elif 240 <= x <= 400 and 660 <= y <= 700:  # Nút Reset
            self.board.reset_game()
            self.current_turn = 'white'
            self.update()
        elif 440 <= x <= 600 and 660 <= y <= 700:  # Nút Log out
            pygame.quit()
            exit()

    def show_game_over_message(self, message):
        # Hiển thị thông báo kết thúc trò chơi
        self.window.fill((0, 0, 0))
        self.draw_board()
        self.draw_pieces()
        self.draw_buttons()

        font = pygame.font.Font(None, 60)
        text_surface = font.render(message, True, (255, 255, 255))
        text_rect = text_surface.get_rect(center=(WIDTH // 2, HEIGHT // 2))
        self.window.blit(text_surface, text_rect)

        pygame.display.update()
        pygame.time.delay(3000)  # Hiển thị thông báo trong 3 giây
