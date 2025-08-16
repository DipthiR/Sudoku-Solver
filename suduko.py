import pygame, time, random, copy

# ---------------- INITIALIZE ----------------
pygame.init()

# ---------------- WINDOW ----------------
WIDTH, HEIGHT = 540, 700
WIN = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("AI Sudoku Solver")

# ---------------- COLORS ----------------
BG_COLOR = (245, 245, 245)
LINE_COLOR = (30, 30, 30)
SELECT_COLOR = (100, 149, 237)
BUTTON_BLUE = (70, 130, 180)
BUTTON_GREEN = (60, 179, 113)
BUTTON_YELLOW = (255, 215, 0)
BUTTON_RED = (220,20,60)
BLACK = (0,0,0)
CONFETTI_COLORS = [(255,0,0),(0,255,0),(0,0,255),(255,255,0),(255,0,255),(0,255,255)]

# ---------------- FONTS ----------------
FONT = pygame.font.SysFont("comicsans", 40)
SMALL_FONT = pygame.font.SysFont("comicsans", 25)
BIG_FONT = pygame.font.SysFont("comicsans", 60)

# ---------------- VARIABLES ----------------
selected = None
wrong_cells = []
start_time = time.time()
score = 100
confetti = []

# ---------------- PUZZLE GENERATION ----------------
def valid_board(num,pos,b):
    for j in range(9):
        if b[pos[0]][j]==num and pos[1]!=j: return False
    for i in range(9):
        if b[i][pos[1]]==num and pos[0]!=i: return False
    box_x,box_y = pos[1]//3,pos[0]//3
    for i in range(box_y*3,box_y*3+3):
        for j in range(box_x*3,box_x*3+3):
            if b[i][j]==num and (i,j)!=pos: return False
    return True

def find_empty_cell(b):
    for i in range(9):
        for j in range(9):
            if b[i][j]==0: return (i,j)
    return None

def solve_board(b):
    empty = find_empty_cell(b)
    if not empty: return True
    row,col = empty
    for num in range(1,10):
        if valid_board(num,(row,col),b):
            b[row][col]=num
            if solve_board(b): return True
            b[row][col]=0
    return False

def generate_puzzle(difficulty="medium"):
    base_board = [[0 for _ in range(9)] for _ in range(9)]
    solve_board(base_board)
    puzzle = copy.deepcopy(base_board)
    if difficulty=="easy": to_remove=random.randint(31,41)
    elif difficulty=="medium": to_remove=random.randint(42,51)
    else: to_remove=random.randint(52,61)
    while to_remove>0:
        i,j=random.randint(0,8),random.randint(0,8)
        if puzzle[i][j]!=0:
            puzzle[i][j]=0
            to_remove-=1
    return puzzle, base_board

# ---------------- DRAW FUNCTIONS ----------------
def draw_grid():
    WIN.fill(BG_COLOR)
    gap = WIDTH//9
    for i in range(10):
        thickness = 4 if i%3==0 else 1
        pygame.draw.line(WIN, LINE_COLOR, (0,i*gap), (WIDTH,i*gap), thickness)
        pygame.draw.line(WIN, LINE_COLOR, (i*gap,0), (i*gap,WIDTH), thickness)

def draw_numbers(board, wrong_cells):
    gap = WIDTH//9
    for i in range(9):
        for j in range(9):
            if board[i][j]!=0:
                color = BUTTON_RED if (i,j) in wrong_cells else BLACK
                text = FONT.render(str(board[i][j]), True, color)
                WIN.blit(text, (j*gap+20,i*gap+10))

def draw_buttons():
    mouse_pos = pygame.mouse.get_pos()
    
    # Solve
    solve_rect = pygame.Rect(50,550,150,40)
    pygame.draw.rect(WIN, BUTTON_BLUE, solve_rect)
    WIN.blit(SMALL_FONT.render("Solve", True, BLACK), (95,560))
    
    # Hint
    hint_rect = pygame.Rect(340,550,150,40)
    pygame.draw.rect(WIN, BUTTON_GREEN, hint_rect)
    WIN.blit(SMALL_FONT.render("Hint", True, BLACK), (390,560))
    
    # Check
    check_rect = pygame.Rect(195,550,150,40)
    pygame.draw.rect(WIN, BUTTON_YELLOW, check_rect)
    WIN.blit(SMALL_FONT.render("Check", True, BLACK), (235,560))

def draw_selection():
    if selected:
        gap = WIDTH//9
        s = pygame.Surface((gap,gap))
        s.set_alpha(100)
        s.fill(SELECT_COLOR)
        WIN.blit(s, (selected[1]*gap, selected[0]*gap))

def draw_timer_score():
    elapsed = int(time.time()-start_time)
    timer_text = SMALL_FONT.render(f"Time: {elapsed}s", True, BLACK)
    score_text = SMALL_FONT.render(f"Score: {score}", True, BLACK)
    WIN.blit(timer_text, (10,650))
    WIN.blit(score_text, (400,650))

# ---------------- GAME FUNCTIONS ----------------
def solve_visual(board):
    empty = find_empty_cell(board)
    if not empty: return True
    row,col = empty
    for num in range(1,10):
        if valid_board(num,(row,col),board):
            board[row][col]=num
            update_window(board)
            pygame.time.delay(50)
            if solve_visual(board): return True
            board[row][col]=0
            update_window(board)
            pygame.time.delay(50)
    return False

def give_hint():
    global score
    empty = find_empty_cell(board)
    if not empty: return
    row,col = empty
    board[row][col]=solution[row][col]
    score-=5

def check_mistakes():
    global wrong_cells, score
    wrong_cells=[]
    for i in range(9):
        for j in range(9):
            if board[i][j]!=0 and board[i][j]!=solution[i][j]:
                wrong_cells.append((i,j))
                score-=2

def check_solved():
    for i in range(9):
        for j in range(9):
            if board[i][j]==0 or board[i][j]!=solution[i][j]: return False
    return True

def update_window(board):
    draw_grid()
    draw_numbers(board, wrong_cells)
    draw_buttons()
    draw_selection()
    draw_timer_score()
    pygame.display.update()

# ---------------- START MENU ----------------
def start_menu():
    running=True
    while running:
        WIN.fill(BG_COLOR)
        title = BIG_FONT.render("AI Sudoku Solver", True, BLACK)
        WIN.blit(title,(40,150))
        mouse_pos = pygame.mouse.get_pos()
        # Easy
        easy_color = BUTTON_GREEN if not(70<=mouse_pos[0]<=470 and 300<=mouse_pos[1]<=360) else (144,238,144)
        pygame.draw.rect(WIN, easy_color, (70,300,400,60))
        WIN.blit(FONT.render("Easy", True, BLACK), (220,310))
        # Medium
        med_color = BUTTON_YELLOW if not(70<=mouse_pos[0]<=470 and 380<=mouse_pos[1]<=440) else (255,250,205)
        pygame.draw.rect(WIN, med_color, (70,380,400,60))
        WIN.blit(FONT.render("Medium", True, BLACK), (180,390))
        # Hard
        hard_color = BUTTON_RED if not(70<=mouse_pos[0]<=470 and 460<=mouse_pos[1]<=520) else (255,99,71)
        pygame.draw.rect(WIN, hard_color, (70,460,400,60))
        WIN.blit(FONT.render("Hard", True, BLACK), (220,470))
        pygame.display.update()
        
        for event in pygame.event.get():
            if event.type==pygame.QUIT:
                pygame.quit(); exit()
            if event.type==pygame.MOUSEBUTTONDOWN:
                x,y=event.pos
                if 70<=x<=470 and 300<=y<=360: return "easy"
                if 70<=x<=470 and 380<=y<=440: return "medium"
                if 70<=x<=470 and 460<=y<=520: return "hard"

# ---------------- MAIN ----------------
difficulty = start_menu()
board, solution = generate_puzzle(difficulty)
start_time = time.time()
score = 100
selected = None
wrong_cells = []

run=True
while run:
    update_window(board)
    if check_solved():
        WIN.fill(BG_COLOR)
        WIN.blit(BIG_FONT.render("YOU WIN!", True, BLACK), (150,300))
        pygame.display.update()
        pygame.time.delay(5000)
        break
    for event in pygame.event.get():
        if event.type==pygame.QUIT:
            run=False
        if event.type==pygame.MOUSEBUTTONDOWN:
            x, y = event.pos
            if y < 540:
                gap = WIDTH // 9
                selected = (y // gap, x // gap)
            # Solve
            if 50 <= x <= 200 and 550 <= y <= 590:
                solve_visual(board)
                wrong_cells=[]
            # Hint
            if 340 <= x <= 490 and 550 <= y <= 590:
                give_hint()
            # Check
            if 195 <= x <= 345 and 550 <= y <= 590:
                check_mistakes()
        if event.type == pygame.KEYDOWN and selected:
            row,col=selected
            if event.key in [pygame.K_1,pygame.K_2,pygame.K_3,pygame.K_4,pygame.K_5,
                             pygame.K_6,pygame.K_7,pygame.K_8,pygame.K_9]:
                board[row][col]=int(event.unicode)
            if event.key in [pygame.K_BACKSPACE,pygame.K_DELETE,pygame.K_0]:
                board[row][col]=0

pygame.quit()
