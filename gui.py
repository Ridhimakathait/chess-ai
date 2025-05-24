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
        self.error_message = None
        self.error_timer = 0

        # Determine base path for piece images
        if getattr(sys, 'frozen', False):
            base_path = sys._MEIPASS
            print(f"Running from executable, base path: {base_path}")
        else:
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
        self.screen.fill((0, 0, 0), (0, 0, self.screen_size, self.screen_size))
        for square in chess.SQUARES:
            rank = chess.square_rank(square)
            file = chess.square_file(square)
            color = (238, 238, 210) if (rank + file) % 2 == 0 else (118, 150, 86)

            # Highlight selected square and legal moves
            if self.selected_square == square:
                color = (186, 202, 68)  # Selected square
            elif self.selected_square is not None:
                # Check legal moves for the selected piece
                piece = board.piece_at(self.selected_square)
                if piece and board.is_legal(chess.Move(self.selected_square, square)):
                    color = (150, 200, 255)  # Legal move highlight

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
        for i, move in enumerate(move_history[-10:]):  # Show last 10 moves
            move_text = self.score_font.render(move, True, (0, 0, 0))
            self.screen.blit(move_text, (self.screen_size + 10, 130 + i * 20))

        # Display error message if present
        if self.error_message and self.error_timer > 0:
            error_text = self.score_font.render(self.error_message, True, (255, 0, 0))
            self.screen.blit(error_text, (self.screen_size + 10, self.screen_size - 30))
            self.error_timer -= 1

    def get_promotion_choice(self):
        promotion_options = {
            chess.QUEEN: "Queen", chess.ROOK: "Rook",
            chess.BISHOP: "Bishop", chess.KNIGHT: "Knight"
        }
        choice = None
        while choice is None:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    return None
                if event.type == pygame.MOUSEBUTTONDOWN:
                    x, y = pygame.mouse.get_pos()
                    if self.screen_size + 10 <= x <= self.screen_size + 190:
                        if 100 <= y < 130:
                            choice = chess.QUEEN
                        elif 130 <= y < 160:
                            choice = chess.ROOK
                        elif 160 <= y < 190:
                            choice = chess.BISHOP
                        elif 190 <= y < 220:
                            choice = chess.KNIGHT
            # Draw promotion menu
            pygame.draw.rect(self.screen, (200, 200, 200), (self.screen_size + 10, 100, 180, 120))
            for i, (piece_type, name) in enumerate(promotion_options.items()):
                text = self.score_font.render(name, True, (0, 0, 0))
                self.screen.blit(text, (self.screen_size + 20, 110 + i * 30))
            pygame.display.flip()
            pygame.event.pump()
            pygame.time.wait(50)
        return choice

    def get_human_move(self, board):
        print("Waiting for move input...")
        self.selected_square = None
        while self.selected_square is None:
            event = pygame.event.wait()  # Wait for an event to reduce CPU usage
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
                    self.error_message = "Click outside board"
                    self.error_timer = 120  # Display for ~4 seconds at 30 FPS
                self.draw_board(board)
                self.update_display(board, 0, 0, 0, board.turn, [])

        print("Waiting for second click...")
        while True:
            event = pygame.event.wait()
            if event.type == pygame.QUIT:
                return None
            if event.type == pygame.MOUSEBUTTONDOWN:
                x, y = pygame.mouse.get_pos()
                if x >= self.screen_size:
                    self.error_message = "Click outside board"
                    self.error_timer = 120
                    continue
                print(f"Second click at x={x}, y={y}")
                file = x // self.square_size
                rank = 7 - (y // self.square_size)
                if 0 <= file <= 7 and 0 <= rank <= 7:
                    target_square = chess.square(file, rank)
                    if self.selected_square == target_square:
                        print("Same square selected, resetting selection.")
                        self.error_message = "Same square selected"
                        self.error_timer = 120
                        self.selected_square = None
                        return self.get_human_move(board)  # Restart move selection
                    try:
                        piece = board.piece_at(self.selected_square)
                        promotion = None
                        if piece and piece.piece_type == chess.PAWN:
                            target_rank = chess.square_rank(target_square)
                            if (piece.color == chess.WHITE and target_rank == 7) or \
                               (piece.color == chess.BLACK and target_rank == 0):
                                promotion = self.get_promotion_choice()
                                if promotion is None:
                                    return None  # User closed window during promotion
                                print(f"Promoting to {promotion}")
                        move = chess.Move(self.selected_square, target_square, promotion=promotion)
                        move_from = chess.square_name(self.selected_square)
                        move_to = chess.square_name(target_square)
                        if board.is_legal(move):
                            self.selected_square = None
                            print(f"Move attempted: {move_from} to {move_to}")
                            return move
                        else:
                            if board.piece_at(target_square):
                                print(f"Move {move_from} to {move_to} is illegal: Target square occupied")
                                self.error_message = f"Cannot move to {move_to}: Occupied"
                            else:
                                print(f"Move {move_from} to {move_to} is illegal")
                                self.error_message = f"Illegal move {move_from} to {move_to}"
                            self.error_timer = 120
                            self.selected_square = None
                            return self.get_human_move(board)  # Restart move selection
                    except ValueError as e:
                        print(f"Invalid move: {chess.square_name(self.selected_square)} to {chess.square_name(target_square)}, error: {e}")
                        self.error_message = f"Invalid move: {e}"
                        self.error_timer = 120
                        self.selected_square = None
                        return self.get_human_move(board)  # Restart move selection
                else:
                    print(f"Second click outside board at x={x}, y={y}")
                    self.error_message = "Click outside board"
                    self.error_timer = 120
                    self.selected_square = None
                    return self.get_human_move(board)  # Restart move selection
            self.update_display(board, 0, 0, 0, board.turn, [])
            pygame.event.pump()

    def show_game_result(self, result):
        """Display the game result (e.g., '1-0', '0-1', '1/2-1/2')"""
        result_text = {
            '1-0': 'Checkmate: White wins!',
            '0-1': 'Checkmate: Black wins!',
            '1/2-1/2': 'Draw!',
            '*': 'Game ended'
        }.get(result, 'Game ended')
        print(f"Displaying game result: {result_text}")
        result_surface = self.font.render(result_text, True, (255, 255, 255))
        result_rect = result_surface.get_rect(center=(self.screen_size // 2, self.screen_size // 2))
        pygame.draw.rect(self.screen, (50, 50, 50), (self.screen_size // 4, self.screen_size // 4, self.screen_size // 2, self.screen_size // 4))
        self.screen.blit(result_surface, result_rect)
        pygame.display.flip()

    def update_display(self, board, score, white_score, black_score, turn, move_history):
        print("Updating display...")
        self.draw_board(board)
        self.draw_scoreboard(white_score, black_score, turn, move_history)
        pygame.display.flip()

    def quit(self):
        """Properly clean up Pygame resources"""
        print("Cleaning up Pygame resources...")
        pygame.quit()