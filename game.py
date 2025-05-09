import chess
import pygame
from ai import ChessAI
from gui import ChessGUI

class ChessGame:
    def __init__(self):
        self.board = chess.Board()
        self.ai = ChessAI(self.board)
        self.gui = ChessGUI()
        self.score = 0  # Initialize score
    
    def run(self):
        print("Starting game loop...")
        running = True
        self.gui.draw_board(self.board)
        self.gui.update_display(self.board, self.score)
        pygame.display.flip()
        pygame.time.wait(1000)  # Wait 1 second to see if board appears
        
        while running and not self.board.is_game_over():
            print("Calling draw_board...")
            self.gui.draw_board(self.board)
            print("Draw board completed...")
            
            print("Calling update_display (initial)...")
            self.gui.update_display(self.board, self.score)
            print("Initial update_display completed...")
            
            if self.board.turn == chess.WHITE:
                print("Waiting for human move...")
                move = self.gui.get_human_move(self.board)
                print("Move received...")
                if move is None:
                    running = False
                    print("Window closed or move canceled, exiting...")
                    break
                try:
                    print(f"Legal moves: {[move.uci() for move in self.board.legal_moves]}")
                    if self.board.is_legal(move):
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
                    self.board.push(ai_move)
                    self.score = self.ai._evaluate_board()
                    print(f"AI played: {ai_move.uci()}, score: {self.score}")
            
            print("Calling update_display (post-move)...")
            self.gui.update_display(self.board, self.score)
            print("Post-move update_display completed...")
        
        print("Game over or quit...")
        pygame.quit()

if __name__ == "__main__":
    game = ChessGame()
    game.run()