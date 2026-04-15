import pygame
import chess
import os

# Init
pygame.init()

BOARD_WIDTH = 640
WIDTH = BOARD_WIDTH + 200
HEIGHT = 640
SQ_SIZE = BOARD_WIDTH // 8

screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Chess UI")
pygame.font.init()
font = pygame.font.SysFont("Arial", 32)

clock = pygame.time.Clock()
game_state = "SPLASH"
splash_timer = 0
splash_img = None
splash_img_orig = None
chess_logo_img = None
try:
    base_dir = os.path.dirname(__file__)
    splash_path = os.path.join(base_dir, "images", "splash_anim.jpg")
    splash_img_raw = pygame.image.load(splash_path).convert_alpha()
    w, h = splash_img_raw.get_size()
    scale_factor = WIDTH / w
    splash_img_orig = pygame.transform.scale(splash_img_raw, (int(w * scale_factor), int(h * scale_factor)))
    splash_img = splash_img_orig
except Exception as e:
    print("Could not load splash abstract image:", e)
    
try:
    # Load the generated AI chess logo image
    logo_path = r"C:\vs_programs\.vscode\chess\images\chesslogo"
    chess_logo_img = pygame.image.load(logo_path)
    chess_logo_img = pygame.transform.scale(chess_logo_img, (200, 200))
except Exception as e:
    print("Could not load splash images:", e)

start_menu_img = None
try:
    start_menu_path = os.path.join(base_dir, "images", "start_menu_art.jpg")
    start_menu_img = pygame.image.load(start_menu_path)
    start_menu_img = pygame.transform.scale(start_menu_img, (WIDTH, HEIGHT))
except Exception as e:
    print("Could not load start menu image:", e)

# --- TIMER CODE: Initialization ---
global_timer = 0
# ----------------------------------
game_over = False

board = chess.Board()

# Colors
LIGHT = (240, 217, 181)
DARK = (181, 136, 99)
HIGHLIGHT = (0, 255, 0)

# Piece → file mapping
PIECE_MAP = {
    "P": "white-pawn.png",
    "R": "white-rook.png",
    "N": "white-knight.png",
    "B": "white-bishop.png",
    "Q": "white-queen.png",
    "K": "white-king.png",

    "p": "black-pawn.png",
    "r": "black-rook.png",
    "n": "black-knight.png",
    "b": "black-bishop.png",
    "q": "black-queen.png",
    "k": "black-king.png",
}

IMAGES = {}


# Load images
def load_images():

    base = os.path.dirname(__file__)
    folder = os.path.join(base, "images")

    for key in PIECE_MAP:

        path = os.path.join(folder, PIECE_MAP[key])

        if not os.path.exists(path):
            print(" Missing:", path)

        img = pygame.image.load(path)

        IMAGES[key] = pygame.transform.scale(
            img, (SQ_SIZE, SQ_SIZE)
        )


load_images()


# Draw board
def draw_board():

    for r in range(8):
        for c in range(8):

            color = LIGHT if (r + c) % 2 == 0 else DARK

            pygame.draw.rect(
                screen,
                color,
                (c * SQ_SIZE, r * SQ_SIZE, SQ_SIZE, SQ_SIZE)
            )


# Draw pieces
def draw_pieces():

    for sq in chess.SQUARES:

        piece = board.piece_at(sq)

        if piece:

            sym = piece.symbol()

            col = chess.square_file(sq)
            row = 7 - chess.square_rank(sq)

            screen.blit(
                IMAGES[sym],
                (col * SQ_SIZE, row * SQ_SIZE)
            )


# Mouse → square
def get_square(pos):

    x, y = pos
    if x >= BOARD_WIDTH:
        return None

    return chess.square(
        x // SQ_SIZE,
        7 - (y // SQ_SIZE)
    )


selected = None
running = True


# Main loop
while running:

    dt = clock.tick(60) / 1000.0

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

        if event.type == pygame.MOUSEBUTTONDOWN:
            if game_state == "START_MENU":
                x, y = event.pos
                if WIDTH // 2 - 100 <= x <= WIDTH // 2 + 100:
                    if 250 <= y <= 310:
                        game_state = "TIME_SELECTION"
                    elif 330 <= y <= 390:
                        running = False
            elif game_state == "TIME_SELECTION":
                x, y = event.pos
                if WIDTH // 2 - 100 <= x <= WIDTH // 2 + 100:
                    if 200 <= y <= 250:
                        # --- TIMER CODE: Assigns 10 mins (in seconds) ---
                        global_timer = 10 * 60
                        # ------------------------------------------------
                        game_state = "PLAYING"
                    elif 300 <= y <= 350:
                        # --- TIMER CODE: Assigns 15 mins (in seconds) ---
                        global_timer = 15 * 60
                        # ------------------------------------------------
                        game_state = "PLAYING"
                    elif 400 <= y <= 450:
                        # --- TIMER CODE: Assigns 25 mins (in seconds) ---
                        global_timer = 25 * 60
                        # ------------------------------------------------
                        game_state = "PLAYING"

            elif game_state == "PLAYING":
                sq = get_square(event.pos)
                if sq is None:
                    continue

                if selected is None:
                    p = board.piece_at(sq)
                    if p and p.color == board.turn:
                        selected = sq
                else:
                    move = chess.Move(selected, sq)

                    # Pawn promotion → Queen
                    if board.piece_at(selected).piece_type == chess.PAWN:
                        if chess.square_rank(sq) in [0, 7]:
                            move = chess.Move(
                                selected, sq,
                                promotion=chess.QUEEN
                            )

                    if move in board.legal_moves and not game_over:
                        board.push(move)

                    selected = None

    if game_state == "SPLASH":
        splash_timer += dt
        
        # Dark artistic background
        screen.fill((25, 30, 55))
        
        if splash_img:
            # Smooth fade in for the full scene image
            alpha = min(255, int((splash_timer / 1.5) * 255))
            
            # Zoom effect: scale from 1.0 to 1.15 over 4.5 seconds
            zoom = 1.0 + (splash_timer / 4.5) * 0.15
            orig_w, orig_h = splash_img_orig.get_size()
            new_w, new_h = int(orig_w * zoom), int(orig_h * zoom)
            
            img_copy = pygame.transform.scale(splash_img_orig, (new_w, new_h))
            img_copy.set_alpha(alpha)
            
            # Center the image vertically and horizontally
            screen.blit(img_copy, (WIDTH // 2 - new_w // 2, HEIGHT // 2 - new_h // 2))
            
            # Add Generated CHESS logo image to the top right of the image
            if splash_timer > 1.0 and chess_logo_img:
                logo_alpha = min(255, int(((splash_timer - 1.0) / 1.0) * 255))
                logo_copy = chess_logo_img.copy()
                logo_copy.set_alpha(logo_alpha)
                
                logo_x = WIDTH - 230
                logo_y = 30
                screen.blit(logo_copy, (logo_x, logo_y))

        if splash_timer > 4.5:
            game_state = "START_MENU"

    elif game_state == "START_MENU":
        screen.fill((40, 40, 40))

        if start_menu_img:
            screen.blit(start_menu_img, (0, 0))

        title_font = pygame.font.SysFont("Arial", 64, bold=True)
        title = title_font.render("CHESS", True, (255, 215, 0))
        screen.blit(title, (WIDTH // 2 - title.get_width() // 2, 100))

        pygame.draw.rect(screen, (50, 150, 50), (WIDTH // 2 - 100, 250, 200, 60), border_radius=10)
        play_text = font.render("Play", True, (255, 255, 255))
        screen.blit(play_text, (WIDTH // 2 - play_text.get_width() // 2, 260))

        pygame.draw.rect(screen, (150, 50, 50), (WIDTH // 2 - 100, 330, 200, 60), border_radius=10)
        quit_text = font.render("Quit", True, (255, 255, 255))
        screen.blit(quit_text, (WIDTH // 2 - quit_text.get_width() // 2, 340))

    elif game_state == "TIME_SELECTION":
        screen.fill((50, 50, 50))
        title = font.render("Select Time Control", True, (255, 255, 255))
        screen.blit(title, (WIDTH // 2 - title.get_width() // 2, 100))

        pygame.draw.rect(screen, (100, 100, 100), (WIDTH // 2 - 100, 200, 200, 50))
        text_10 = font.render("10 Minutes", True, (255, 255, 255))
        screen.blit(text_10, (WIDTH // 2 - text_10.get_width() // 2, 210))

        pygame.draw.rect(screen, (100, 100, 100), (WIDTH // 2 - 100, 300, 200, 50))
        text_15 = font.render("15 Minutes", True, (255, 255, 255))
        screen.blit(text_15, (WIDTH // 2 - text_15.get_width() // 2, 310))

        pygame.draw.rect(screen, (100, 100, 100), (WIDTH // 2 - 100, 400, 200, 50))
        text_25 = font.render("25 Minutes", True, (255, 255, 255))
        screen.blit(text_25, (WIDTH // 2 - text_25.get_width() // 2, 410))

    elif game_state == "PLAYING":
        if not board.is_game_over() and not game_over:
            # --- TIMER CODE: Count down logic ticking 60 times a second ---
            global_timer -= dt
            if global_timer <= 0:
                global_timer = 0
                game_over = True
            # --------------------------------------------------------------

        draw_board()

        # Highlight
        if selected:
            c = chess.square_file(selected)
            r = 7 - chess.square_rank(selected)

            pygame.draw.rect(
                screen,
                HIGHLIGHT,
                (c * SQ_SIZE, r * SQ_SIZE, SQ_SIZE, SQ_SIZE),
                3
            )

        draw_pieces()

        # Draw UI right panel
        pygame.draw.rect(screen, (50, 50, 50), (BOARD_WIDTH, 0, WIDTH - BOARD_WIDTH, HEIGHT))
        turn_text = "White to move" if board.turn == chess.WHITE else "Black to move"
        text1 = font.render(turn_text, True, (255, 255, 255))
        screen.blit(text1, (BOARD_WIDTH + 20, 50))

        # --- TIMER CODE: Converts logic into an on-screen visual clock ---
        m, s = int(global_timer) // 60, int(global_timer) % 60

        color = (255, 50, 50) if global_timer < 60 else (255, 255, 255)
        text2 = font.render(f"Time: {m}:{s:02d}", True, color)
        screen.blit(text2, (BOARD_WIDTH + 20, 100))
        # -----------------------------------------------------------------

    if game_over:
        winner = "Black Wins!" if board.turn == chess.WHITE else "White Wins!"
        text4 = font.render(winner + " (Time Out)", True, (255, 0, 0))
        screen.blit(text4, (BOARD_WIDTH + 20, 200))
    elif board.is_game_over():
            result = board.result()
            if result == "1-0":
                msg = "White Wins!"
                color = (0, 255, 0)
            elif result == "0-1":
                msg = "Black Wins!"
                color = (0, 255, 0)
            else:   
                msg = "Draw!"
                color = (255, 255, 0)


            text4 = font.render(msg, True, color)
            screen.blit(text4, (BOARD_WIDTH + 20, 200))

    pygame.display.update()


pygame.quit()
