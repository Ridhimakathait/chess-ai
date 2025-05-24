import chess
import pygame
from ai import ChessAI
from gui import ChessGUI

class ChessGame:
    def __init__(self):
        self.board = chess.Board()
        self.ai = ChessAI(self.board)
        self.gui = ChessGUI()
        self.score = 0
        self.white_score = 0
        self.black_score = 0
        self.move_history = []
    
    def run(self):
        print("Starting game loop...")
        running = True
        while running and not self.board.is_game_over():
            self.gui.draw_board(self.board)
            self.gui.update_display(self.board, self.score, self.white_score, self.black_score, self.board.turn, self.move_history)
            pygame.display.flip()

            if self.board.turn == chess.WHITE:
                move = self.gui.get_human_move(self.board)
                if move is None:
                    for event in pygame.event.get():
                        if event.type == pygame.QUIT:
                            running = False
                            break
                    continue
                if self.board.is_legal(move):
                    captured_piece = self.board.piece_at(move.to_square)
                    if captured_piece:
                        piece_value = {chess.PAWN: 1, chess.KNIGHT: 3, chess.BISHOP: 3,
                                    chess.ROOK: 5, chess.QUEEN: 9, chess.KING: 1000}.get(captured_piece.piece_type, 0)
                        self.white_score += piece_value
                    self.move_history.append(self.board.san(move))  # Use SAN
                    self.board.push(move)
                    self.score = self.ai._evaluate_board()
                else:
                    print(f"Invalid move: {move.uci()}")
            else:
                ai_move = self.ai.find_best_move()
                if ai_move:
                    captured_piece = self.board.piece_at(ai_move.to_square)
                    if captured_piece:
                        piece_value = {chess.PAWN: 1, chess.KNIGHT: 3, chess.BISHOP: 3,
                                    chess.ROOK: 5, chess.QUEEN: 9, chess.KING: 1000}.get(captured_piece.piece_type, 0)
                        self.black_score += piece_value
                    self.move_history.append(self.board.san(ai_move))  # Use SAN
                    self.board.push(ai_move)
                    self.score = self.ai._evaluate_board()

        # Display game result
        result = "Game Over: " + self.board.result()
        self.gui.show_game_result(result)
        pygame.time.wait(2000)  # Show result for 2 seconds
        pygame.quit()

if __name__ == "__main__":
    game = ChessGame()
    game.run()