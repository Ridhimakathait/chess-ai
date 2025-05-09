
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