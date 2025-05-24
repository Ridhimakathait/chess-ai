import chess
import math

class ChessAI:
    def __init__(self, board):
        self.board = board

    def _evaluate_board(self):
        piece_values = {
            chess.PAWN: 1,
            chess.KNIGHT: 3,
            chess.BISHOP: 3,
            chess.ROOK: 5,
            chess.QUEEN: 9,
            chess.KING: 1000
        }
        score = 0
        for square in chess.SQUARES:
            piece = self.board.piece_at(square)
            if piece is not None:
                value = piece_values.get(piece.piece_type, 0)
                if piece.color == chess.WHITE:
                    score += value
                else:
                    score -= value
        return score

    def minimax(self, board, depth, maximizing_player, alpha=-math.inf, beta=math.inf):
        if depth == 0 or board.is_game_over():
            return self._evaluate_board(), None

        best_move = None
        if maximizing_player:
            max_eval = -math.inf
            for move in board.legal_moves:
                board.push(move)
                eval_score, _ = self.minimax(board, depth - 1, False, alpha, beta)
                board.pop()
                if eval_score > max_eval:
                    max_eval = eval_score
                    best_move = move
                alpha = max(alpha, eval_score)
                if beta <= alpha:
                    break  # Prune
            return max_eval, best_move
        else:
            min_eval = math.inf
            for move in board.legal_moves:
                board.push(move)
                eval_score, _ = self.minimax(board, depth - 1, True, alpha, beta)
                board.pop()
                if eval_score < min_eval:
                    min_eval = eval_score
                    best_move = move
                beta = min(beta, eval_score)
                if beta <= alpha:
                    break  # Prune
            return min_eval, best_move

    def find_best_move(self, depth=3):
        _, best_move = self.minimax(self.board, depth, False)
        return best_move