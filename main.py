import pygame
from gui import ChessGUI, SQUARE_SIZE
from board import Board
from minimax import find_best_move
from utils import validate_user_move  # Nhập hàm kiểm tra tính hợp lệ của nước đi

def main():
    pygame.init()
    clock = pygame.time.Clock()

    board = Board()  # Khởi tạo bàn cờ
    gui = ChessGUI(board.board)  # Khởi tạo giao diện bàn cờ

    running = True
    selected_piece = None
    player_color = "white"  # Người chơi sẽ chơi quân trắng
    ai_color = "black"  # AI sẽ chơi quân đen

    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

            if event.type == pygame.MOUSEBUTTONDOWN:
                pos = pygame.mouse.get_pos()
                row, col = pos[1] // SQUARE_SIZE, pos[0] // SQUARE_SIZE

                if selected_piece:  # Nếu đã chọn quân cờ
                    start = selected_piece
                    end = (row, col)

                    # Chuyển đổi nước đi sang ký hiệu cờ vua chuẩn (ví dụ, 'e2 e4')
                    start_pos = f"{chr(start[1] + ord('a'))}{8 - start[0]}"
                    end_pos = f"{chr(end[1] + ord('a'))}{8 - end[0]}"
                    move_str = f"{start_pos} {end_pos}"

                    # Kiểm tra tính hợp lệ của nước đi
                    if validate_user_move(board.board, move_str, player_color):
                        board.move(start, end)  # Thực hiện di chuyển
                        selected_piece = None  # Bỏ chọn quân cờ
                        gui.clear_highlight()  # Xóa bất kỳ ô nào đang được đánh dấu

                        # Kiểm tra xem người chơi có thắng hoặc ván cờ đã kết thúc chưa
                        if board.is_checkmate(player_color):
                            print(f"Chiếu hết! {player_color.capitalize()} thua!")
                            board.reset_game()  # Reset lại trò chơi
                            break  # Kết thúc vòng lặp
                        elif board.is_stalemate(player_color):
                            print("Hòa! Ván cờ kết thúc!")
                            board.reset_game()  # Reset lại trò chơi
                            break  # Kết thúc vòng lặp

                        # Đến lượt di chuyển của AI
                        ai_move = find_best_move(board, 2, ai_color)
                        if ai_move:
                            board.move(ai_move[0], ai_move[1])

                        # Kiểm tra xem AI có thắng hay ván cờ đã kết thúc chưa
                        if board.is_checkmate(ai_color):
                            print("Chiếu hết! Trắng thắng!")
                            board.reset_game()  # Reset lại trò chơi
                            break  # Kết thúc vòng lặp
                        elif board.is_stalemate(ai_color):
                            print("Hòa! Ván cờ kết thúc!")
                            board.reset_game()  # Reset lại trò chơi
                            break  # Kết thúc vòng lặp
                    else:
                        print("Nước đi không hợp lệ! Vui lòng thử lại.")
                        selected_piece = None  # Bỏ chọn quân cờ
                        gui.clear_highlight()  # Xóa bất kỳ ô nào đang được đánh dấu
                else:
                    # Nếu chưa chọn quân cờ, chọn quân cờ ban đầu
                    selected_piece = (row, col)
                    gui.highlight_square(row, col)  # Đánh dấu ô đã chọn

        gui.update()  # Cập nhật giao diện người dùng
        clock.tick(60)  # Giới hạn tốc độ khung hình ở 60 FPS

    pygame.quit()  # Thoát Pygame khi kết thúc

if __name__ == "__main__":
    main()
