import pygame
import chess
import os
import sys

class ChessGUI:
    def __init__(self):
        pygame.init()
        print("Pygame initialized...")
        self.screen_size = 600
        self.square_size = self.screen_size // 8
        self.screen = pygame.display.set_mode((self.screen_size, self.screen_size))
        print("Screen created...")
        pygame.display.set_caption("Chess AI with Backtracking")
        self.font = pygame.font.SysFont('Arial', 32)  # Fallback font
        self.selected_square = None
        
        # Determine base path for file loading
        if getattr(sys, 'frozen', False):  # Running as executable
            base_path = sys._MEIPASS
            print(f"Running from executable, base path: {base_path}")
        else:  # Running as script
            base_path = os.path.dirname(__file__)
            print(f"Running from script, base path: {base_path}")
        
        # Load piece images
        self.piece_images = {}
        piece_files = {
            'P': 'white_pawn.png', 'N': 'white_knight.png', 'B': 'white_bishop.png',
            'R': 'white_rook.png', 'Q': 'white_queen.png', 'K': 'white_king.png',
            'p': 'black_pawn.png', 'n': 'black_knight.png', 'b': 'black_bishop.png',
            'r': 'black_rook.png', 'q': 'black_queen.png', 'k': 'black_king.png'
        }
        for symbol, filename in piece_files.items():
            image_path = os.path.join(base_path, 'pieces', filename)
            if os.path.exists(image_path):
                self.piece_images[symbol] = pygame.image.load(image_path).convert_alpha()
                self.piece_images[symbol] = pygame.transform.scale(self.piece_images[symbol], (self.square_size, self.square_size))
            else:
                print(f"Warning: {image_path} not found")

    def draw_board(self, board):
        print("Drawing board...")
        # Draw squares (temporarily remove fill to test persistence)
        # self.screen.fill((0, 0, 0))  # Commented out to test
        for square in chess.SQUARES:
            rank = chess.square_rank(square)
            file = chess.square_file(square)
            color = (238, 238, 210) if (rank + file) % 2 == 0 else (118, 150, 86)
            
            if self.selected_square == square:
                color = (186, 202, 68)  # Highlight selected square
            
            pygame.draw.rect(self.screen, color, 
                           (file * self.square_size, 
                            (7 - rank) * self.square_size, 
                            self.square_size, 
                            self.square_size))
        
        print("Drawing pieces...")
        # Draw pieces
        for square in chess.SQUARES:
            piece = board.piece_at(square)
            if piece:
                rank = chess.square_rank(square)
                file = chess.square_file(square)
                symbol = piece.symbol()
                image = self.piece_images.get(symbol)
                if image:
                    self.screen.blit(image, (file * self.square_size, (7 - rank) * self.square_size))
                else:
                    text = self.font.render(symbol, True, (0, 0, 0) if piece.color == chess.BLACK else (255, 255, 255))
                    text_rect = text.get_rect(center=((file + 0.5) * self.square_size, (7.5 - rank) * self.square_size))
                    self.screen.blit(text, text_rect)

    def get_human_move(self, board):
        print("Waiting for move input...")
        self.selected_square = None
        while self.selected_square is None:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    return None
                if event.type == pygame.MOUSEBUTTONDOWN:
                    x, y = pygame.mouse.get_pos()
                    file = x // self.square_size
                    rank = 7 - (y // self.square_size)
                    if 0 <= file <= 7 and 0 <= rank <= 7:
                        self.selected_square = chess.square(file, rank)
                        print(f"Selected square: {chess.square_name(self.selected_square)}")
                    else:
                        print(f"Click outside board at x={x}, y={y}")
                    self.draw_board(board)
                    self.update_display(board, 0)

        print("Waiting for second click...")
        attempt = 0
        max_attempts = 3
        while attempt < max_attempts:
            print(f"Checking for second click (attempt {attempt + 1}/{max_attempts})...")
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    return None
                if event.type == pygame.MOUSEBUTTONDOWN:
                    x, y = pygame.mouse.get_pos()
                    print(f"Second click at x={x}, y={y}")
                    file = x // self.square_size
                    rank = 7 - (y // self.square_size)
                    if 0 <= file <= 7 and 0 <= rank <= 7:
                        target_square = chess.square(file, rank)
                        if self.selected_square == target_square:
                            print("Same square selected, please choose a different target.")
                            attempt += 1
                            continue
                        try:
                            move = chess.Move(self.selected_square, target_square)
                            move_from = chess.square_name(self.selected_square)
                            move_to = chess.square_name(target_square)
                            self.selected_square = None
                            print(f"Move attempted: {move_from} to {move_to}")
                            return move
                        except ValueError:
                            print(f"Invalid move: {chess.square_name(self.selected_square)} to {chess.square_name(target_square)}")
                            attempt += 1
                            continue
                    else:
                        print(f"Second click outside board at x={x}, y={y}")
                        attempt += 1
                        continue
            self.update_display(board, 0)
            pygame.event.pump()
            pygame.time.wait(50)
        print("Max attempts reached, canceling move...")
        self.selected_square = None
        return None

    def update_display(self, board, score):
        print("Updating display...")
        self.draw_board(board)
        score_text = self.font.render(f"Score: {score:.1f}", True, (255, 255, 255))
        self.screen.blit(score_text, (10, 10))
        pygame.display.flip()