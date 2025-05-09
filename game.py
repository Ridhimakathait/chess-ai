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
        self.gui.draw_board(self.board)
        self.gui.update_display(self.board, self.score, self.white_score, self.black_score, self.board.turn, self.move_history)
        pygame.display.flip()
        pygame.time.wait(1000)
        
        while running and not self.board.is_game_over():
            print("Calling draw_board...")
            self.gui.draw_board(self.board)
            print("Draw board completed...")
            
            print("Calling update_display (initial)...")
            self.gui.update_display(self.board, self.score, self.white_score, self.black_score, self.board.turn, self.move_history)
            print("Initial update_display completed...")
            
            if self.board.turn == chess.WHITE:
                print("Board state:", self.board)
                print("Legal moves:", [move.uci() for move in self.board.legal_moves])
                print("Waiting for human move...")
                move = self.gui.get_human_move(self.board)
                print("Move received...")
                if move is None:
                    running = False
                    print("Window closed or move canceled, exiting...")
                    break
                try:
                    if self.board.is_legal(move):
                        captured_piece = self.board.piece_at(move.to_square)
                        if captured_piece:
                            piece_value = {
                                chess.PAWN: 1, chess.KNIGHT: 3, chess.BISHOP: 3,
                                chess.ROOK: 5, chess.QUEEN: 9, chess.KING: 1000
                            }.get(captured_piece.piece_type, 0)
                            self.black_score += piece_value
                            print(f"White captured {captured_piece.symbol()}, Black score increased by {piece_value} to {self.black_score}")
                        move_notation = f"{move.uci()}"
                        self.move_history.append(move_notation)
                        self.board.push(move)
                        self.score = self.ai._evaluate_board()
                        print(f"Legal move made, score: {self.score}")
                    else:
                        print(f"Invalid move: {chess.square_name(move.from_square)} to {chess.square_name(move.to_square)}")
                except ValueError:
                    print(f"Error processing move: {move}")
            else:
                print("AI thinking...")
                ai_move = self.ai.find_best_move()
                if ai_move:
                    captured_piece = self.board.piece_at(ai_move.to_square)
                    if captured_piece:
                        piece_value = {
                            chess.PAWN: 1, chess.KNIGHT: 3, chess.BISHOP: 3,
                            chess.ROOK: 5, chess.QUEEN: 9, chess.KING: 1000
                        }.get(captured_piece.piece_type, 0)
                        self.white_score += piece_value
                        print(f"Black captured {captured_piece.symbol()}, White score increased by {piece_value} to {self.white_score}")
                    move_notation = f"{ai_move.uci()}"
                    self.move_history.append(move_notation)
                    self.board.push(ai_move)
                    self.score = self.ai._evaluate_board()
                    print(f"AI played: {ai_move.uci()}, score: {self.score}")
            
            print("Calling update_display (post-move)...")
            self.gui.update_display(self.board, self.score, self.white_score, self.black_score, self.board.turn, self.move_history)
            print("Post-move update_display completed...")
        
        print("Game over or quit...")
        pygame.quit()

if __name__ == "__main__":
    game = ChessGame()
    game.run()