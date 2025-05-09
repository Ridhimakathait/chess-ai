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
        self.scoreboard_width = 200
        self.screen = pygame.display.set_mode((self.screen_size + self.scoreboard_width, self.screen_size))
        print("Screen created...")
        pygame.display.set_caption("Chess AI with Backtracking")
        self.font = pygame.font.SysFont('Arial', 24)
        self.score_font = pygame.font.SysFont('Arial', 16)
        self.selected_square = None
        
        if getattr(sys, 'frozen', False):
            base_path = sys._MEIPASS
            print(f"Running from executable, base path: {base_path}")
        else:
            base_path = os.path.dirname(__file__)
            print(f"Running from script, base path: {base_path}")
        
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
        self.screen.fill((0, 0, 0), (0, 0, self.screen_size, self.screen_size))
        for square in chess.SQUARES:
            rank = chess.square_rank(square)
            file = chess.square_file(square)
            color = (238, 238, 210) if (rank + file) % 2 == 0 else (118, 150, 86)
            
            if self.selected_square == square:
                color = (186, 202, 68)
            
            pygame.draw.rect(self.screen, color, 
                           (file * self.square_size, 
                            (7 - rank) * self.square_size, 
                            self.square_size, 
                            self.square_size))
        
        print("Drawing pieces...")
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

    def draw_scoreboard(self, white_score, black_score, turn, move_history):
        scoreboard_rect = (self.screen_size, 0, self.scoreboard_width, self.screen_size)
        pygame.draw.rect(self.screen, (200, 200, 200), scoreboard_rect)

        white_score_text = self.score_font.render(f"White Score: {white_score}", True, (0, 0, 0))
        self.screen.blit(white_score_text, (self.screen_size + 10, 10))
        black_score_text = self.score_font.render(f"Black Score: {black_score}", True, (0, 0, 0))
        self.screen.blit(black_score_text, (self.screen_size + 10, 40))

        turn_text = self.score_font.render(f"Turn: {'White' if turn else 'Black'}", True, (0, 0, 0))
        self.screen.blit(turn_text, (self.screen_size + 10, 70))

        history_title = self.score_font.render("Move History:", True, (0, 0, 0))
        self.screen.blit(history_title, (self.screen_size + 10, 100))
        for i, move in enumerate(move_history[-10:]):
            move_text = self.score_font.render(move, True, (0, 0, 0))
            self.screen.blit(move_text, (self.screen_size + 10, 130 + i * 20))

    def get_human_move(self, board):
        print("Waiting for move input...")
        self.selected_square = None
        while self.selected_square is None:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    return None
                if event.type == pygame.MOUSEBUTTONDOWN:
                    x, y = pygame.mouse.get_pos()
                    if x >= self.screen_size:
                        continue
                    file = x // self.square_size
                    rank = 7 - (y // self.square_size)
                    if 0 <= file <= 7 and 0 <= rank <= 7:
                        self.selected_square = chess.square(file, rank)
                        print(f"Selected square: {chess.square_name(self.selected_square)}")
                    else:
                        print(f"Click outside board at x={x}, y={y}")
                    self.draw_board(board)
                    # Pass placeholder scores during move selection
                    self.update_display(board, 0, 0, 0, board.turn, [])

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
                    if x >= self.screen_size:
                        continue
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
            # Pass placeholder scores during move selection
            self.update_display(board, 0, 0, 0, board.turn, [])
            pygame.event.pump()
            pygame.time.wait(50)
        print("Max attempts reached, canceling move...")
        self.selected_square = None
        return None

    def update_display(self, board, score, white_score, black_score, turn, move_history):
        print("Updating display...")
        self.draw_board(board)
        self.draw_scoreboard(white_score, black_score, turn, move_history)
        pygame.display.flip()