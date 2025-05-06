import pygame
import copy
from comboBox import ComboBox
from solve import Solve
import time
import numpy as np
from sensorless_env import SensorlessEnvironment

pygame.init()

# Lấy kích thước màn hình thực tế
info = pygame.display.Info()
SCREEN_WIDTH = info.current_w
SCREEN_HEIGHT = info.current_h

# Đặt kích thước mặc định nếu không lấy được thông tin màn hình
DEFAULT_WIDTH = 1200
DEFAULT_HEIGHT = 800
WIDTH = min(SCREEN_WIDTH, DEFAULT_WIDTH) if SCREEN_WIDTH > 0 else DEFAULT_WIDTH
HEIGHT = min(SCREEN_HEIGHT, DEFAULT_HEIGHT) if SCREEN_HEIGHT > 0 else DEFAULT_HEIGHT

# Tính toán các tỷ lệ dựa trên kích thước màn hình
TILE_SIZE = min(WIDTH // 5, HEIGHT // 5)
SMALL_GRID_SIZE = TILE_SIZE // 2

# Tính toán vị trí dựa trên tỷ lệ
MAIN_GRID_X = WIDTH * 0.05
MAIN_GRID_Y = HEIGHT * 0.2
START_GRID_X = WIDTH * 0.5
START_GRID_Y = HEIGHT * 0.1
GOAL_GRID_X = WIDTH * 0.75
GOAL_GRID_Y = HEIGHT * 0.1

# Khởi tạo màn hình
screen = pygame.display.set_mode((WIDTH, HEIGHT), pygame.RESIZABLE)
pygame.display.set_caption("Sliding Puzzle - Nguyễn Trí Lâm")

WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
GRAY = (128, 128, 128)
RED = (255, 0, 0)
BLUE = (0, 0, 255)
GREEN = (0, 255, 0)
YELLOW = (255, 255, 0)
LIGHT_GRAY = (220, 220, 220)

DEFAULT_INITIAL_STATE = [2, 6, 5, 0, 8, 7, 4, 3, 1]
INITIAL_STATE = copy.deepcopy(DEFAULT_INITIAL_STATE)
GOAL_STATE = [1, 2, 3, 4, 5, 6, 7, 8, 0]

# Hàm cập nhật các thành phần giao diện dựa trên kích thước màn hình
def update_layout():
    global WIDTH, HEIGHT, TILE_SIZE, SMALL_GRID_SIZE, MAIN_GRID_X, MAIN_GRID_Y, START_GRID_X, START_GRID_Y, GOAL_GRID_X, GOAL_GRID_Y
    global SOLVE_BUTTON_RECT, NEXT_STEP_BUTTON_RECT, BACK_BUTTON_RECT, RESET_BUTTON_RECT, SET_INITIAL_BUTTON_RECT
    global SENSORLESS_ENV_BUTTON_RECT, POPUP_WIDTH, POPUP_HEIGHT, POPUP_X, POPUP_Y, YES_BUTTON_RECT, NO_BUTTON_RECT, combo_box

    WIDTH, HEIGHT = screen.get_size()
    TILE_SIZE = min(WIDTH // 5, HEIGHT // 5)
    SMALL_GRID_SIZE = TILE_SIZE // 2

    MAIN_GRID_X = WIDTH * 0.05
    MAIN_GRID_Y = HEIGHT * 0.2
    START_GRID_X = WIDTH * 0.5
    START_GRID_Y = HEIGHT * 0.1
    GOAL_GRID_X = WIDTH * 0.75
    GOAL_GRID_Y = HEIGHT * 0.1

    BUTTON_WIDTH = WIDTH * 0.1
    BUTTON_HEIGHT = HEIGHT * 0.06
    BUTTON_Y = HEIGHT * 0.9
    SOLVE_BUTTON_RECT = pygame.Rect(WIDTH * 0.05, BUTTON_Y, BUTTON_WIDTH, BUTTON_HEIGHT)
    NEXT_STEP_BUTTON_RECT = pygame.Rect(WIDTH * 0.2, BUTTON_Y, BUTTON_WIDTH, BUTTON_HEIGHT)
    BACK_BUTTON_RECT = pygame.Rect(WIDTH * 0.35, BUTTON_Y, BUTTON_WIDTH * 0.6, BUTTON_HEIGHT)
    RESET_BUTTON_RECT = pygame.Rect(WIDTH * 0.5, BUTTON_Y, BUTTON_WIDTH, BUTTON_HEIGHT)
    SET_INITIAL_BUTTON_RECT = pygame.Rect(WIDTH * 0.65, BUTTON_Y, BUTTON_WIDTH * 1.5, BUTTON_HEIGHT)
    SENSORLESS_ENV_BUTTON_RECT = pygame.Rect(WIDTH * 0.85, BUTTON_Y, BUTTON_WIDTH * 1.5, BUTTON_HEIGHT)

    POPUP_WIDTH = WIDTH * 0.3
    POPUP_HEIGHT = HEIGHT * 0.25
    POPUP_X = (WIDTH - POPUP_WIDTH) // 2
    POPUP_Y = (HEIGHT - POPUP_HEIGHT) // 2
    YES_BUTTON_RECT = pygame.Rect(POPUP_X + POPUP_WIDTH * 0.25, POPUP_Y + POPUP_HEIGHT * 0.5, POPUP_WIDTH * 0.2, POPUP_HEIGHT * 0.2)
    NO_BUTTON_RECT = pygame.Rect(POPUP_X + POPUP_WIDTH * 0.55, POPUP_Y + POPUP_HEIGHT * 0.5, POPUP_WIDTH * 0.2, POPUP_HEIGHT * 0.2)

    combo_box.update_layout(
        x=WIDTH * 0.05,
        y=HEIGHT * 0.05,
        width=WIDTH * 0.2,
        height=HEIGHT * 0.05
    )

# Khởi tạo ComboBox
combo_box = ComboBox(WIDTH * 0.05, HEIGHT * 0.05, WIDTH * 0.2, HEIGHT * 0.05, 
                     ["BFS", "DFS", "UCS", "IDS", "Greedy", "A*", "IDA*", "Hill Climbing", 
                      "SA Hill Climbing", "Stochastic Hill Climbing", "Beam Search", "Annealing", 
                      "Genetic Algorithm", "AND-OR Graph"])

execution_history = []

def find_empty(state):
    return state.index(0)

def draw_small_board(state, position, label):
    x_offset, y_offset = position
    font = pygame.font.Font(None, int(HEIGHT * 0.035))
    label_text = font.render(label, True, BLACK)
    label_rect = label_text.get_rect(center=(x_offset + (3 * SMALL_GRID_SIZE) // 2, y_offset - HEIGHT * 0.025))
    screen.blit(label_text, label_rect)

    background_rect = pygame.Rect(x_offset - WIDTH * 0.01, y_offset - HEIGHT * 0.01, 
                                 3 * SMALL_GRID_SIZE + WIDTH * 0.02, 3 * SMALL_GRID_SIZE + HEIGHT * 0.02)
    pygame.draw.rect(screen, LIGHT_GRAY, background_rect)
    pygame.draw.rect(screen, BLACK, background_rect, 2)

    for i in range(3):
        for j in range(3):
            idx = i * 3 + j
            value = state[idx]
            rect = pygame.Rect(x_offset + j * SMALL_GRID_SIZE, y_offset + i * SMALL_GRID_SIZE, 
                              SMALL_GRID_SIZE, SMALL_GRID_SIZE)
            pygame.draw.rect(screen, GRAY if value == 0 else WHITE, rect)
            pygame.draw.rect(screen, BLACK, rect, 2)
            if value != 0:
                font = pygame.font.Font(None, int(HEIGHT * 0.035))
                text = font.render(str(value), True, BLACK)
                text_rect = text.get_rect(center=rect.center)
                screen.blit(text, text_rect)

def draw_board(state, solution=None, current_step=0, show_popup=False, selected_algorithm=None, 
               combo_box=None, is_customizing=False, is_solution_found=False):
    screen.fill(WHITE)

    for i in range(3):
        for j in range(3):
            idx = i * 3 + j
            value = state[idx]
            rect = pygame.Rect(MAIN_GRID_X + j * TILE_SIZE, MAIN_GRID_Y + i * TILE_SIZE, TILE_SIZE, TILE_SIZE)
            pygame.draw.rect(screen, GRAY if value == 0 else WHITE, rect)
            pygame.draw.rect(screen, BLACK, rect, 2)
            if value != 0:
                font = pygame.font.Font(None, int(TILE_SIZE * 0.5))
                text = font.render(str(value), True, BLACK)
                text_rect = text.get_rect(center=rect.center)
                screen.blit(text, text_rect)

    draw_small_board(INITIAL_STATE, (START_GRID_X, START_GRID_Y), "Start State")
    draw_small_board(GOAL_STATE, (GOAL_GRID_X, GOAL_GRID_Y), "Goal State")

    mouse_x, mouse_y = pygame.mouse.get_pos()
    if combo_box:
        combo_box.draw(screen)

    if SOLVE_BUTTON_RECT.collidepoint((mouse_x, mouse_y)):
        pygame.draw.rect(screen, RED, SOLVE_BUTTON_RECT)
    else:
        pygame.draw.rect(screen, BLUE, SOLVE_BUTTON_RECT)
    
    font = pygame.font.Font(None, int(HEIGHT * 0.05))
    text = font.render("Solve", True, WHITE)
    text_rect = text.get_rect(center=SOLVE_BUTTON_RECT.center)
    screen.blit(text, text_rect)

    if solution:
        if NEXT_STEP_BUTTON_RECT.collidepoint((mouse_x, mouse_y)):
            pygame.draw.rect(screen, RED, NEXT_STEP_BUTTON_RECT)
        else:
            pygame.draw.rect(screen, GREEN, NEXT_STEP_BUTTON_RECT)
        
        text = font.render(f"Next ({current_step}/{len(solution) - 1})", True, WHITE)
        text_rect = text.get_rect(center=NEXT_STEP_BUTTON_RECT.center)
        screen.blit(text, text_rect)

    if solution and current_step > 0:
        if BACK_BUTTON_RECT.collidepoint((mouse_x, mouse_y)):
            pygame.draw.rect(screen, RED, BACK_BUTTON_RECT)
        else:
            pygame.draw.rect(screen, YELLOW, BACK_BUTTON_RECT)
        
        text = font.render("Back", True, BLACK)
        text_rect = text.get_rect(center=BACK_BUTTON_RECT.center)
        screen.blit(text, text_rect)

    if RESET_BUTTON_RECT.collidepoint((mouse_x, mouse_y)):
        pygame.draw.rect(screen, RED, RESET_BUTTON_RECT)
    else:
        pygame.draw.rect(screen, (100, 100, 255), RESET_BUTTON_RECT)
    
    text = font.render("Reset", True, WHITE)
    text_rect = text.get_rect(center=RESET_BUTTON_RECT.center)
    screen.blit(text, text_rect)

    if is_customizing:
        pygame.draw.rect(screen, GREEN, SET_INITIAL_BUTTON_RECT)
        text = font.render("Save Initial", True, WHITE)
    else:
        if SET_INITIAL_BUTTON_RECT.collidepoint((mouse_x, mouse_y)):
            pygame.draw.rect(screen, RED, SET_INITIAL_BUTTON_RECT)
        else:
            pygame.draw.rect(screen, (100, 200, 100), SET_INITIAL_BUTTON_RECT)
        text = font.render("Customize Initial", True, WHITE)
    
    text_rect = text.get_rect(center=SET_INITIAL_BUTTON_RECT.center)
    screen.blit(text, text_rect)

    if SENSORLESS_ENV_BUTTON_RECT.collidepoint((mouse_x, mouse_y)):
        pygame.draw.rect(screen, RED, SENSORLESS_ENV_BUTTON_RECT)
    else:
        pygame.draw.rect(screen, (150, 150, 255), SENSORLESS_ENV_BUTTON_RECT)
    
    text = font.render("Sensorless Env", True, WHITE)
    text_rect = text.get_rect(center=SENSORLESS_ENV_BUTTON_RECT.center)
    screen.blit(text, text_rect)

    if is_customizing:
        font = pygame.font.Font(None, int(HEIGHT * 0.045))
        text = font.render("CUSTOMIZING INITIAL STATE", True, RED)
        screen.blit(text, (MAIN_GRID_X, MAIN_GRID_Y + 3 * TILE_SIZE + HEIGHT * 0.05))

    if solution and not is_solution_found:
        font = pygame.font.Font(None, int(HEIGHT * 0.045))
        text = font.render("NO SOLUTION FOUND! Showing best state reached.", True, RED)
        screen.blit(text, (MAIN_GRID_X, MAIN_GRID_Y + 3 * TILE_SIZE + HEIGHT * 0.05))

    font = pygame.font.Font(None, int(HEIGHT * 0.035))
    y_offset = START_GRID_Y + 3 * SMALL_GRID_SIZE + HEIGHT * 0.05
    text = font.render("Execution History:", True, BLACK)
    screen.blit(text, (START_GRID_X, y_offset))

    for i, (algo, time_taken, is_solved) in enumerate(execution_history[-5:]):
        status = "Solved" if is_solved else "Best State"
        text = font.render(f"{algo}: {time_taken:.6f}s ({status})", True, BLACK)
        screen.blit(text, (START_GRID_X, y_offset + (i + 1) * HEIGHT * 0.035))

    if show_popup:
        pygame.draw.rect(screen, (200, 200, 200), (POPUP_X, POPUP_Y, POPUP_WIDTH, POPUP_HEIGHT))
        font = pygame.font.Font(None, int(HEIGHT * 0.035))
        text = font.render("Do you want to view step by step?", True, BLACK)
        text_rect = text.get_rect(center=(POPUP_X + POPUP_WIDTH // 2, POPUP_Y + POPUP_HEIGHT * 0.3))
        screen.blit(text, text_rect)

        if YES_BUTTON_RECT.collidepoint((mouse_x, mouse_y)):
            pygame.draw.rect(screen, RED, YES_BUTTON_RECT)
        else:
            pygame.draw.rect(screen, GREEN, YES_BUTTON_RECT)
        text = font.render("Yes", True, WHITE)
        text_rect = text.get_rect(center=YES_BUTTON_RECT.center)
        screen.blit(text, text_rect)

        if NO_BUTTON_RECT.collidepoint((mouse_x, mouse_y)):
            pygame.draw.rect(screen, RED, NO_BUTTON_RECT)
        else:
            pygame.draw.rect(screen, BLUE, NO_BUTTON_RECT)
        text = font.render("No", True, WHITE)
        text_rect = text.get_rect(center=NO_BUTTON_RECT.center)
        screen.blit(text, text_rect)

    pygame.display.flip()

def move_tile(state, direction):
    empty_idx = find_empty(state)
    row, col = divmod(empty_idx, 3)
    new_row, new_col = row, col

    if direction == "up" and row > 0:
        new_row -= 1
    elif direction == "down" and row < 2:
        new_row += 1
    elif direction == "left" and col > 0:
        new_col -= 1
    elif direction == "right" and col < 2:
        new_col += 1
    else:
        return state
    
    new_idx = new_row * 3 + new_col
    new_state = copy.deepcopy(state)
    new_state[empty_idx], new_state[new_idx] = new_state[new_idx], new_state[empty_idx]
    return new_state

# Khởi tạo trạng thái ban đầu
current_state = copy.deepcopy(INITIAL_STATE)
clock = pygame.time.Clock()
running = True
solution = None
current_step = 0
show_popup = False
selected_algorithm = "BFS"
is_customizing = False
is_solution_found = False

update_layout()

# Biến để theo dõi trạng thái giao diện
in_sensorless_env = False
sensorless_env = None

while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

        if event.type == pygame.VIDEORESIZE:
            screen = pygame.display.set_mode((event.w, event.h), pygame.RESIZABLE)
            update_layout()

        if not in_sensorless_env:
            # Xử lý giao diện chính
            combo_box.handle_event(event)

            if event.type == pygame.MOUSEBUTTONDOWN:
                x, y = event.pos

                if SOLVE_BUTTON_RECT.collidepoint(x, y) and not is_customizing:
                    selected_algorithm = combo_box.selected_option
                    solve = Solve(current_state, GOAL_STATE)
                    
                    start_time = time.time()
                    
                    if selected_algorithm == "BFS":
                        solution = solve.solve_with_bfs()
                    elif selected_algorithm == "DFS":
                        solution = solve.solve_with_dfs()
                    elif selected_algorithm == "UCS":
                        solution = solve.solve_with_ucs()
                    elif selected_algorithm == "IDS":
                        solution = solve.solve_with_ids()
                    elif selected_algorithm == "Greedy":
                        solution = solve.solve_with_greedy()
                    elif selected_algorithm == "A*":
                        solution = solve.solve_with_astar()
                    elif selected_algorithm == "IDA*":
                        solution = solve.solve_with_idastar()
                    elif selected_algorithm == "Hill Climbing":
                        solution = solve.solve_hill_climbing()
                    elif selected_algorithm == "SA Hill Climbing":
                        solution = solve.solve_steepest_ascent_hill_climbing()
                    elif selected_algorithm == "Stochastic Hill Climbing":
                        solution = solve.solve_stochastic_hill_climbing()
                    elif selected_algorithm == "Beam Search":
                        solution = solve.solve_with_beam_search()
                    elif selected_algorithm == "Annealing":
                        solution = solve.solve_with_annealing()
                    elif selected_algorithm == "Genetic Algorithm":
                        solution = solve.solve_with_genetic_algorithm(
                            pop_size=50, 
                            max_moves=20, 
                            generations=100, 
                            tournament_size=3, 
                            crossover_rate=0.8, 
                            mutation_rate=0.1
                        )
                    elif selected_algorithm == "AND-OR Graph":
                        solution = solve.solve_with_and_or_graph()

                    end_time = time.time()
                    execution_time = end_time - start_time

                    if solution and solution[-1] == GOAL_STATE:
                        is_solution_found = True
                        execution_history.append((selected_algorithm, execution_time, True))
                        print(f"Solution found with {selected_algorithm}! Steps: {len(solution) - 1}")
                        print(f"Execution Time: {execution_time:.6f} seconds")
                        show_popup = True
                    else:
                        is_solution_found = False
                        execution_history.append((selected_algorithm, execution_time, False))
                        print(f"No solution found with {selected_algorithm}! Showing best state reached.")
                        print(f"Execution Time: {execution_time:.6f} seconds")
                        show_popup = True

                    current_step = 0
                    if solution:
                        for state in solution:
                            np_array = np.array(state)
                            np_array = np_array.reshape(3, 3)
                            print(np_array)
                            print("-------------------")

                elif solution and NEXT_STEP_BUTTON_RECT.collidepoint(x, y) and not is_customizing:
                    if current_step < len(solution) - 1:
                        current_step += 1
                        current_state = solution[current_step]

                elif solution and BACK_BUTTON_RECT.collidepoint(x, y) and current_step > 0 and not is_customizing:
                    current_step -= 1
                    current_state = solution[current_step]
                    print(f"Back to step {current_step}")
                    
                elif RESET_BUTTON_RECT.collidepoint(x, y):
                    current_state = copy.deepcopy(INITIAL_STATE)
                    solution = None
                    current_step = 0
                    show_popup = False
                    is_solution_found = False
                    print("Reset to initial state")
                    
                elif SET_INITIAL_BUTTON_RECT.collidepoint(x, y):
                    if is_customizing:
                        INITIAL_STATE = copy.deepcopy(current_state)
                        is_customizing = False
                        print("Saved new initial state")
                    else:
                        is_customizing = True
                        print("Now customizing initial state")

                elif SENSORLESS_ENV_BUTTON_RECT.collidepoint(x, y):
                    in_sensorless_env = True
                    sensorless_env = SensorlessEnvironment(current_state, GOAL_STATE, screen, WIDTH, HEIGHT, SMALL_GRID_SIZE)

                elif show_popup:
                    if YES_BUTTON_RECT.collidepoint(x, y):
                        show_popup = False
                    elif NO_BUTTON_RECT.collidepoint(x, y):
                        show_popup = False
                        if solution:
                            print("Running solution automatically...")
                            for state in solution:
                                current_state = state
                                draw_board(current_state, solution, current_step, show_popup, selected_algorithm, 
                                          combo_box, is_customizing, is_solution_found)
                                pygame.time.wait(100)
                            current_step = len(solution) - 1
                            show_popup = False
                    else:
                        row = int((y - MAIN_GRID_Y) // TILE_SIZE)
                        col = int((x - MAIN_GRID_X) // TILE_SIZE)
                        if 0 <= row < 3 and 0 <= col < 3:
                            idx = row * 3 + col
                            empty_idx = find_empty(current_state)
                            current_state[idx], current_state[empty_idx] = current_state[empty_idx], current_state[idx]
                            solution = None
                            current_step = 0
                            show_popup = False
                            is_solution_found = False

                else:
                    row = int((y - MAIN_GRID_Y) // TILE_SIZE)
                    col = int((x - MAIN_GRID_X) // TILE_SIZE)
                    if 0 <= row < 3 and 0 <= col < 3:
                        idx = row * 3 + col
                        empty_idx = find_empty(current_state)
                        current_state[idx], current_state[empty_idx] = current_state[empty_idx], current_state[idx]
                        if not is_customizing:
                            solution = None
                            current_step = 0
                            is_solution_found = False

            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_UP:
                    current_state = move_tile(current_state, "up")
                    if not is_customizing:
                        solution = None
                        current_step = 0
                        is_solution_found = False
                elif event.key == pygame.K_DOWN:
                    current_state = move_tile(current_state, "down")
                    if not is_customizing:
                        solution = None
                        current_step = 0
                        is_solution_found = False
                elif event.key == pygame.K_LEFT:
                    current_state = move_tile(current_state, "left")
                    if not is_customizing:
                        solution = None
                        current_step = 0
                        is_solution_found = False
                elif event.key == pygame.K_RIGHT:
                    current_state = move_tile(current_state, "right")
                    if not is_customizing:
                        solution = None
                        current_step = 0
                        is_solution_found = False

        else:
            # Xử lý trang Sensorless Environment
            if not sensorless_env.handle_event(event):
                in_sensorless_env = False
                sensorless_env = None

    if not in_sensorless_env:
        draw_board(current_state, solution, current_step, show_popup, selected_algorithm, combo_box, 
                   is_customizing, is_solution_found)
    else:
        sensorless_env.draw()

    clock.tick(60)

pygame.quit()