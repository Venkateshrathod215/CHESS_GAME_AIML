import chess
import random
from math import inf

"""
Chess Game using python-chess library with a graphical terminal board.

Features:
- Human vs Human
- Human vs Computer (Random)
- Human vs Computer (Minimax AI)
- Proper chess rules validation
- Colored graphical board in the terminal
"""

class ChessGame:
    def __init__(self):
        self.board = chess.Board()

    def print_board(self):
        """
        UPDATED: This method now translates the logic board into a graphical
        board for printing, using the style from your chess_board.py file.
        """
        piece_symbols = {
            'P': '♙', 'R': '♖', 'N': '♘', 'B': '♗', 'Q': '♕', 'K': '♔',
            'p': '♟', 'r': '♜', 'n': '♞', 'b': '♝', 'q': '♛', 'k': '♚'
        }
        
        visual_board = [['.' for _ in range(8)] for _ in range(8)]
        
        for i in range(64):
            piece = self.board.piece_at(i)
            if piece:
                row = 7 - (i // 8)
                col = i % 8
                visual_board[row][col] = piece_symbols[piece.symbol()]
                
        WHITE_BG = "\033[47m"  
        BLACK_BG = "\033[42m"   
        RESET = "\033[0m"

        print("\n    a  b  c  d  e  f  g  h")
        print("  " + "-"*25)
        for row_idx, row in enumerate(visual_board):
            row_str = f"{8-row_idx} |"
            for col_idx, square in enumerate(row):
                if (row_idx + col_idx) % 2 == 0:
                    row_str += WHITE_BG + f" {square} " + RESET
                else:
                    row_str += BLACK_BG + f" {square} " + RESET
            print(row_str + f"| {8-row_idx}")
        print("  " + "-"*25)
        print("    a  b  c  d  e  f  g  h\n")

    def get_random_move(self):
        """Get a random legal move"""
        legal_moves = list(self.board.legal_moves)
        return random.choice(legal_moves) if legal_moves else None

    def minimax(self, depth=3, alpha=-inf, beta=inf, is_maximizing=True):
        """
        Minimax algorithm with alpha-beta pruning for chess AI
        Returns: (score, best_move)
        """
        if depth == 0 or self.board.is_game_over():
            return self.evaluate_board(), None

        legal_moves = list(self.board.legal_moves)
        best_move = None

        if is_maximizing:
            max_eval = -inf
            for move in legal_moves:
                self.board.push(move)
                eval_score, _ = self.minimax(depth - 1, alpha, beta, False)
                self.board.pop()
                
                if eval_score > max_eval:
                    max_eval = eval_score
                    best_move = move
                
                alpha = max(alpha, eval_score)
                if beta <= alpha:
                    break
            return max_eval, best_move
        else:
            min_eval = inf
            for move in legal_moves:
                self.board.push(move)
                eval_score, _ = self.minimax(depth - 1, alpha, beta, True)
                self.board.pop()
                
                if eval_score < min_eval:
                    min_eval = eval_score
                    best_move = move
                
                beta = min(beta, eval_score)
                if beta <= alpha:
                    break
            return min_eval, best_move

    def evaluate_board(self):
        """
        Simple board evaluation function
        Returns positive score if white is winning, negative if black is winning
        """
        if self.board.is_checkmate():
            return -1000 if self.board.turn else 1000
        
        if self.board.is_stalemate():
            return 0
        
        # Piece values
        piece_values = {
            chess.PAWN: 1, chess.KNIGHT: 3, chess.BISHOP: 3,
            chess.ROOK: 5, chess.QUEEN: 9, chess.KING: 0
        }
        
        score = 0
        for square in chess.SQUARES:
            piece = self.board.piece_at(square)
            if piece:
                value = piece_values.get(piece.piece_type, 0)
                score += value if piece.color == chess.WHITE else -value
        return score

    def ask_human_move(self):
        """Get a move from human player"""
        while True:
            try:
                move_input = input("Enter your move (e.g., e2e4): ").strip()
                move = self.board.parse_san(move_input)
                return move
            except (ValueError, chess.InvalidMoveError, chess.IllegalMoveError):
                print("Invalid or illegal move! Use algebraic notation (e.g., e2e4, Nf3). Try again.")

    def play_game(self, mode='hvh'):
        """
        Play a chess game with specified mode
        """
        print("Starting Chess Game | Mode:", mode)
        
        while not self.board.is_game_over():
            self.print_board()
            
            turn_color = "White" if self.board.turn == chess.WHITE else "Black"
            print(f"{turn_color}'s move")
            
            is_ai_turn = (mode == 'hvr' and self.board.turn == chess.BLACK) or \
                         (mode == 'hvm' and self.board.turn == chess.BLACK)

            if is_ai_turn:
                print("Computer is thinking...")
                if mode == 'hvr':
                    move = self.get_random_move()
                else:  # hvm
                    _, move = self.minimax(depth=3)
                print(f"Computer plays: {self.board.san(move)}")
            else:
                move = self.ask_human_move()
            
            self.board.push(move)

        # Game over
        self.print_board()
        result = self.board.result()
        print("Game over!")
        if self.board.is_checkmate():
            winner = "Black" if self.board.turn == chess.WHITE else "White"
            print(f"Checkmate! {winner} wins!")
        else:
            print("It's a draw!", result)

def main():
    """Main function to select game mode"""
    print("\n--- Chess Game Modes ---")
    print("1: Human vs Human")
    print("2: Human vs Computer (Random)")
    print("3: Human vs Computer (Minimax AI)")
    
    choice = input("Choose mode (1/2/3): ").strip()
    
    game = ChessGame()
    if choice == '1':
        game.play_game('hvh')
    elif choice == '2':
        game.play_game('hvr')
    elif choice == '3':
        game.play_game('hvm')
    else:
        print("Invalid choice. Exiting.")

if __name__ == "__main__":
    main()
