import pygame
from gui import ChessGUI, SQUARE_SIZE
from board import Board
from minimax import find_best_move
from utils import validate_user_move


def main():
    pygame.init()
    clock = pygame.time.Clock()

    board = Board()  # Khởi tạo bàn cờ
    gui = ChessGUI(board)  # Khởi tạo giao diện bàn cờ
    move_history = []  # Lịch sử các nước đi

    running = True
    selected_piece = None
    player_color, ai_color = "white", "black"  # Người chơi màu trắng, AI màu đen

    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

            if event.type == pygame.MOUSEBUTTONDOWN:
                pos = pygame.mouse.get_pos()
                row, col = pos[1] // SQUARE_SIZE, pos[0] // SQUARE_SIZE

                # Kiểm tra nút bấm Undo, Reset, hoặc Log out
                if 40 <= pos[0] <= 200 and 660 <= pos[1] <= 700:  # Nút Undo
                    if len(move_history) >= 2:
                        # Undo nước đi của AI
                        board.undo_move()
                        move_history.pop()
                        # Undo nước đi của người chơi
                        board.undo_move()
                        move_history.pop()
                        gui.update()
                    continue
                elif 240 <= pos[0] <= 400 and 660 <= pos[1] <= 700:  # Nút Reset
                    board.reset_game()
                    move_history.clear()
                    selected_piece = None
                    gui.clear_highlight()
                    gui.update()
                    continue
                elif 440 <= pos[0] <= 600 and 660 <= pos[1] <= 700:  # Nút Log out
                    pygame.quit()
                    return

                if selected_piece:
                    start = selected_piece
                    end = (row, col)
                    move_str = f"{chr(start[1] + ord('a'))}{8 - start[0]} {chr(end[1] + ord('a'))}{8 - end[0]}"

                    if validate_user_move(board.board, move_str, player_color):  # Kiểm tra tính hợp lệ
                        board.move(start, end)  # Thực hiện di chuyển
                        move_history.append((start, end))  # Ghi lại lịch sử nước đi

                        # Kiểm tra nếu vua bị chiếu
                        if board.is_in_check(player_color):
                            print(f"Không thể đi! Vua của {player_color} bị chiếu.")
                            board.undo_move()
                            move_history.pop()
                            selected_piece = None
                            gui.clear_highlight()
                            break

                        selected_piece = None
                        gui.clear_highlight()

                        # Kiểm tra kết thúc trò chơi
                        if board.is_checkmate(player_color):
                            print(f"Chiếu hết! {player_color.capitalize()} thua!")
                            board.reset_game()
                            move_history.clear()
                            break
                        elif board.is_stalemate(player_color):
                            print("Hòa! Ván cờ kết thúc!")
                            board.reset_game()
                            move_history.clear()
                            break

                        # Đến lượt AI di chuyển
                        ai_move = find_best_move(board, 2, ai_color)
                        if ai_move:
                            board.move(ai_move[0], ai_move[1])
                            move_history.append(ai_move)  # Ghi lại lịch sử nước đi của AI

                        # Kiểm tra kết thúc trò chơi với AI
                        if board.is_checkmate(ai_color):
                            print("Chiếu hết! Trắng thắng!")
                            board.reset_game()
                            move_history.clear()
                            break
                        elif board.is_stalemate(ai_color):
                            print("Hòa! Ván cờ kết thúc!")
                            board.reset_game()
                            move_history.clear()
                            break
                    else:
                        print("Nước đi không hợp lệ! Vui lòng thử lại.")
                        selected_piece = None
                        gui.clear_highlight()
                else:
                    selected_piece = (row, col)  # Chọn quân cờ
                    gui.highlight_square(row, col)

        gui.update()  # Cập nhật giao diện
        clock.tick(60)  # Giới hạn FPS

    pygame.quit()  # Thoát trò chơi


if __name__ == "__main__":
    main()
