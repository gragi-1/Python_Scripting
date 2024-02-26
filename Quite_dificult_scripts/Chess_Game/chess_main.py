# Python
# pygame, python-chess, chess.engine
import pygame
import chess
import chess.engine
import os

# Path to the Stockfish engine
engine_path = r"C:\Users\Usuario\Downloads\stockfish-windows-x86-64-modern\stockfish\stockfish-windows-x86-64-modern.exe"

# Initialize pygame
pygame.init()

# Set the dimensions of the window
size = (800, 800)
screen = pygame.display.set_mode(size)

# Directory where the images for the chess pieces are located
image_dir = r"C:\Users\Usuario\Desktop\Utiles\Proyectos\Python_Scripts\Quite_dificult_scripts\Chess_Game\images"

# Load the images for the chess pieces
pieces = {}
for piece in ['bp', 'bn', 'bb', 'br', 'bq', 'bk', 'wp', 'wn', 'wb', 'wr', 'wq', 'wk']:
    pieces[piece] = pygame.image.load(os.path.join(image_dir, f"{piece}.png"))

# Initialize an empty chess board
board = chess.Board()

# Initialize the chess engine
engine = chess.engine.SimpleEngine.popen_uci(engine_path)

# Variables for selected piece and legal moves
selected_piece = None
legal_moves = []

# Main game loop
running = True
while running and not board.is_checkmate() and not board.is_stalemate():
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.MOUSEBUTTONDOWN:
            if event.button == 1:  # Left mouse button
                pos = pygame.mouse.get_pos()
                square = chess.square(pos[0] // 100, 7 - pos[1] // 100)
                piece = board.piece_at(square)
                if piece and piece.color == board.turn:
                    selected_piece = square
                    legal_moves = [move.to_square for move in board.legal_moves if move.from_square == square]
                elif selected_piece is not None and square in legal_moves:
                    move = chess.Move(selected_piece, square)
                    board.push(move)
                    selected_piece = None
                    legal_moves = []

    # Draw the chess board and the legal moves
    for i in range(8):
        for j in range(8):
            square = chess.square(i, 7-j)
            if (i + j) % 2 == 0:
                pygame.draw.rect(screen, (255, 206, 158), pygame.Rect(i*100, j*100, 100, 100))
            else:
                pygame.draw.rect(screen, (209, 139, 71), pygame.Rect(i*100, j*100, 100, 100))
            if square in legal_moves:
                pygame.draw.circle(screen, (255, 0, 0), (i*100 + 50, j*100 + 50), 20)

    # Draw the chess pieces
    for i in range(8):
        for j in range(8):
            piece = board.piece_at(chess.square(i, 7-j))
            if piece and str(piece) in pieces:
                screen.blit(pieces[str(piece)], pygame.Rect(i*100, j*100, 100, 100))

    # Get the AI's move
    if not board.turn and not selected_piece:
        result = engine.play(board, chess.engine.Limit(time=2.0))
        board.push(result.move)

    pygame.display.flip()

# Close the engine
engine.quit()

pygame.quit()

# Print the final board
print(board)

# Print the result of the game
if board.is_checkmate():
    print("Checkmate!")
elif board.is_stalemate():
    print("Stalemate!")