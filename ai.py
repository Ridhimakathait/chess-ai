import chess

class ChessAI:
    def __init__(self, board, depth=3):
        self.board = board
        self.max_depth = depth
        self.piece_values = {
            chess.PAWN: 1,
            chess.KNIGHT: 3,
            chess.BISHOP: 3,
            chess.ROOK: 5,
            chess.QUEEN: 9,
            chess.KING: 0
        }
        # Positional tables (simplified) for pawns, knights, and kings
        self.pawn_table = [
            [0.0,  0.0,  0.0,  0.0,  0.0,  0.0,  0.0,  0.0],
            [0.5,  1.0,  1.0, -2.0, -2.0,  1.0,  1.0,  0.5],
            [0.1, -0.5, -1.0,  0.0,  0.0, -1.0, -0.5, 0.1],
            [0.0,  0.0,  0.0,  0.5,  0.5,  0.0,  0.0,  0.0],
            [0.1,  0.1,  0.1,  0.5,  0.5,  0.1,  0.1,  0.1],
            [0.2,  0.2,  0.2,  0.2,  0.2,  0.2,  0.2,  0.2],
            [0.5,  0.5,  0.5,  0.5,  0.5,  0.5,  0.5,  0.5],
            [0.0,  0.0,  0.0,  0.0,  0.0,  0.0,  0.0,  0.0]
        ]
        self.knight_table = [
            [-0.5, -0.4, -0.3, -0.3, -0.3, -0.3, -0.4, -0.5],
            [-0.4, -0.2,  0.0,  0.0,  0.0,  0.0, -0.2, -0.4],
            [-0.3,  0.0,  0.2,  0.3,  0.3,  0.2,  0.0, -0.3],
            [-0.3,  0.0,  0.3,  0.4,  0.4,  0.3,  0.0, -0.3],
            [-0.3,  0.0,  0.3,  0.4,  0.4,  0.3,  0.0, -0.3],
            [-0.3,  0.0,  0.2,  0.3,  0.3,  0.2,  0.0, -0.3],
            [-0.4, -0.2,  0.0,  0.0,  0.0,  0.0, -0.2, -0.4],
            [-0.5, -0.4, -0.3, -0.3, -0.3, -0.3, -0.4, -0.5]
        ]
        self.king_table_midgame = [
            [-0.3, -0.4, -0.4, -0.5, -0.5, -0.4, -0.4, -0.3],
            [-0.4, -0.5, -0.5, -0.5, -0.5, -0.5, -0.5, -0.4],
            [-0.4, -0.5, -0.6, -0.6, -0.6, -0.6, -0.5, -0.4],
            [-0.5, -0.5, -0.6, -0.7, -0.7, -0.6, -0.5, -0.5],
            [-0.5, -0.5, -0.6, -0.7, -0.7, -0.6, -0.5, -0.5],
            [-0.4, -0.5, -0.6, -0.6, -0.6, -0.6, -0.5, -0.4],
            [-0.4, -0.5, -0.5, -0.5, -0.5, -0.5, -0.5, -0.4],
            [-0.3, -0.4, -0.4, -0.5, -0.5, -0.4, -0.4, -0.3]
        ]

    def find_best_move(self):
        best_move = None
        best_score = -float('inf')
        
        for move in self.board.legal_moves:
            self.board.push(move)
            score = -self._backtrack(self.max_depth - 1)
            self.board.pop()
            
            if score > best_score:
                best_score = score
                best_move = move
                
        return best_move
    
    def _backtrack(self, depth):
        if depth == 0 or self.board.is_game_over():
            return self._evaluate_board()
            
        best_score = -float('inf')
        
        for move in self.board.legal_moves:
            self.board.push(move)
            score = -self._backtrack(depth - 1)
            self.board.pop()
            
            if score > best_score:
                best_score = score
                
        return best_score
    
    def _evaluate_board(self):
        """Enhanced material and positional evaluation"""
        score = 0
        
        # Material evaluation
        for piece_type in self.piece_values:
            white_pieces = len(self.board.pieces(piece_type, chess.WHITE))
            black_pieces = len(self.board.pieces(piece_type, chess.BLACK))
            score += white_pieces * self.piece_values[piece_type]
            score -= black_pieces * self.piece_values[piece_type]
            
            # Positional evaluation
            for square in chess.SQUARES:
                piece = self.board.piece_at(square)
                if piece:
                    rank = chess.square_rank(square)
                    file = chess.square_file(square)
                    if piece.color == chess.WHITE:
                        if piece.piece_type == chess.PAWN:
                            score += self.pawn_table[rank][file]
                        elif piece.piece_type == chess.KNIGHT:
                            score += self.knight_table[rank][file]
                        elif piece.piece_type == chess.KING:
                            score += self.king_table_midgame[rank][file]
                    else:  # Black pieces (invert rank for symmetry)
                        if piece.piece_type == chess.PAWN:
                            score -= self.pawn_table[7 - rank][file]
                        elif piece.piece_type == chess.KNIGHT:
                            score -= self.knight_table[7 - rank][file]
                        elif piece.piece_type == chess.KING:
                            score -= self.king_table_midgame[7 - rank][file]

        # Add bonuses
        if self.board.is_check():
            score += 0.5 if self.board.turn == chess.BLACK else -0.5
        
        # Bonus for center control (e.g., d4, d5, e4, e5)
        center_squares = [chess.D4, chess.D5, chess.E4, chess.E5]
        for square in center_squares:
            if self.board.piece_at(square) and self.board.piece_at(square).color == chess.WHITE:
                score += 0.3
            elif self.board.piece_at(square) and self.board.piece_at(square).color == chess.BLACK:
                score -= 0.3

        return score