import pygame
import random
import pickle
import numpy as np
from collections import defaultdict

# Khởi tạo Pygame
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
GOAL_GRID_X = WIDTH * 0.75
GOAL_GRID_Y = HEIGHT * 0.1
INFO_X = WIDTH * 0.05
INFO_Y = HEIGHT * 0.6

# Khởi tạo màn hình
screen = pygame.display.set_mode((WIDTH, HEIGHT), pygame.RESIZABLE)
pygame.display.set_caption("Q-Learning Training - Sliding Puzzle")

# Màu sắc
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
GRAY = (128, 128, 128)
RED = (255, 0, 0)
BLUE = (0, 0, 255)
GREEN = (0, 255, 0)
LIGHT_GRAY = (200, 200, 200)

# Lớp môi trường Sliding Puzzle
class SlidingPuzzleEnv:
    def __init__(self, goal_state, size=3):
        self.goal_state = goal_state
        self.size = size
        self.actions = ["up", "down", "left", "right"]
        self.reset()

    def reset(self, random_state=True):
        if random_state:
            self.state = list(self.goal_state)
            random.shuffle(self.state)
            while not self.is_solvable(self.state):
                random.shuffle(self.state)
        else:
            self.state = list(self.goal_state)
        return self.state

    def is_solvable(self, state):
        inversions = 0
        state_no_zero = [x for x in state if x != 0]
        for i in range(len(state_no_zero)):
            for j in range(i + 1, len(state_no_zero)):
                if state_no_zero[i] > state_no_zero[j]:
                    inversions += 1
        return inversions % 2 == 0

    def step(self, action):
        empty_idx = self.state.index(0)
        row, col = divmod(empty_idx, self.size)
        new_row, new_col = row, col

        if action == "up" and row > 0:
            new_row -= 1
        elif action == "down" and row < self.size - 1:
            new_row += 1
        elif action == "left" and col > 0:
            new_col -= 1
        elif action == "right" and col < self.size - 1:
            new_col += 1
        else:
            return self.state, -10, False

        new_idx = new_row * self.size + new_col
        new_state = list(self.state)
        new_state[empty_idx], new_state[new_idx] = new_state[new_idx], new_state[empty_idx]

        reward = -self.manhattan_distance(new_state, self.goal_state)
        if new_state == self.goal_state:
            reward += 100

        self.state = new_state
        done = new_state == self.goal_state
        return new_state, reward, done

    def manhattan_distance(self, state, goal_state):
        total_distance = 0
        for value in range(1, self.size * self.size):
            current_idx = state.index(value)
            goal_idx = goal_state.index(value)
            curr_row, curr_col = divmod(current_idx, self.size)
            goal_row, goal_col = divmod(goal_idx, self.size)
            total_distance += abs(curr_row - goal_row) + abs(curr_col - goal_col)
        return total_distance

# Lớp quản lý Q-Learning và giao diện
class QLearningTrainer:
    def __init__(self, goal_state):
        self.env = SlidingPuzzleEnv(goal_state)
        self.Q = defaultdict(lambda: {action: 0 for action in self.env.actions})
        self.goal_state = goal_state
        self.current_state = self.env.reset()
        self.episode = 0
        self.step = 0
        self.total_reward = 0
        self.is_training = False
        self.is_paused = False
        self.epsilon = 1.0
        self.episodes = 100
        self.alpha = 0.1
        self.gamma = 0.9
        self.epsilon_start = 1.0
        self.epsilon_end = 0.1
        self.epsilon_decay = 0.995
        self.max_steps = 100

        # Nút điều khiển
        self.BUTTON_WIDTH = WIDTH * 0.1
        self.BUTTON_HEIGHT = HEIGHT * 0.06
        self.PAUSE_BUTTON_RECT = pygame.Rect(WIDTH * 0.05, HEIGHT * 0.85, self.BUTTON_WIDTH, self.BUTTON_HEIGHT)
        self.SAVE_BUTTON_RECT = pygame.Rect(WIDTH * 0.2, HEIGHT * 0.85, self.BUTTON_WIDTH, self.BUTTON_HEIGHT)

    def update_layout(self):
        global WIDTH, HEIGHT, TILE_SIZE, SMALL_GRID_SIZE, MAIN_GRID_X, MAIN_GRID_Y, GOAL_GRID_X, GOAL_GRID_Y, INFO_X, INFO_Y
        WIDTH, HEIGHT = screen.get_size()
        TILE_SIZE = min(WIDTH // 5, HEIGHT // 5)
        SMALL_GRID_SIZE = TILE_SIZE // 2
        MAIN_GRID_X = WIDTH * 0.05
        MAIN_GRID_Y = HEIGHT * 0.2
        GOAL_GRID_X = WIDTH * 0.75
        GOAL_GRID_Y = HEIGHT * 0.1
        INFO_X = WIDTH * 0.05
        INFO_Y = HEIGHT * 0.6
        self.BUTTON_WIDTH = WIDTH * 0.1
        self.BUTTON_HEIGHT = HEIGHT * 0.06
        self.PAUSE_BUTTON_RECT = pygame.Rect(WIDTH * 0.05, HEIGHT * 0.85, self.BUTTON_WIDTH, self.BUTTON_HEIGHT)
        self.SAVE_BUTTON_RECT = pygame.Rect(WIDTH * 0.2, HEIGHT * 0.85, self.BUTTON_WIDTH, self.BUTTON_HEIGHT)

    def get_action(self, state):
        state_tuple = tuple(state)
        if random.random() < self.epsilon:
            return random.choice(self.env.actions)
        return max(self.Q[state_tuple], key=self.Q[state_tuple].get)

    def train_step(self):
        if self.is_training and not self.is_paused and self.episode < self.episodes:
            state_tuple = tuple(self.current_state)
            action = self.get_action(self.current_state)
            new_state, reward, done = self.env.step(action)

            # Cập nhật Q-value
            new_state_tuple = tuple(new_state)
            old_q = self.Q[state_tuple][action]
            future_q = max(self.Q[new_state_tuple].values())
            self.Q[state_tuple][action] = (1 - self.alpha) * old_q + self.alpha * (reward + self.gamma * future_q)

            self.current_state = new_state
            self.total_reward += reward
            self.step += 1

            if done or self.step >= self.max_steps:
                self.episode += 1
                self.step = 0
                self.total_reward = 0
                self.current_state = self.env.reset(random_state=True)
                self.epsilon = max(self.epsilon_end, self.epsilon * self.epsilon_decay)

            return True
        return False

    def save_q_table(self, filename="q_table.pkl"):
        with open(filename, 'wb') as f:
            pickle.dump(dict(self.Q), f)

    def draw_board(self, state, position, label):
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
                    text = font.render(str(value), True, BLACK)
                    text_rect = text.get_rect(center=rect.center)
                    screen.blit(text, text_rect)

    def draw(self):
        screen.fill(WHITE)

        # Vẽ bảng hiện tại (lớn)
        for i in range(3):
            for j in range(3):
                idx = i * 3 + j
                value = self.current_state[idx]
                rect = pygame.Rect(MAIN_GRID_X + j * TILE_SIZE, MAIN_GRID_Y + i * TILE_SIZE, TILE_SIZE, TILE_SIZE)
                pygame.draw.rect(screen, GRAY if value == 0 else WHITE, rect)
                pygame.draw.rect(screen, BLACK, rect, 2)
                if value != 0:
                    font = pygame.font.Font(None, int(TILE_SIZE * 0.5))
                    text = font.render(str(value), True, BLACK)
                    text_rect = text.get_rect(center=rect.center)
                    screen.blit(text, text_rect)

        # Vẽ bảng mục tiêu
        self.draw_board(self.goal_state, (GOAL_GRID_X, GOAL_GRID_Y), "Goal State")

        # Vẽ thông tin huấn luyện
        font = pygame.font.Font(None, int(HEIGHT * 0.035))
        info_texts = [
            f"Episode: {self.episode}/{self.episodes}",
            f"Step: {self.step}/{self.max_steps}",
            f"Epsilon: {self.epsilon:.4f}",
            f"Total Reward: {self.total_reward:.2f}",
            f"Training: {'Running' if self.is_training and not self.is_paused else 'Paused' if self.is_training else 'Stopped'}"
        ]
        for i, text in enumerate(info_texts):
            text_surface = font.render(text, True, BLACK)
            screen.blit(text_surface, (INFO_X * 10, INFO_Y + i * HEIGHT * 0.05))

        # Vẽ nút Pause/Resume
        mouse_x, mouse_y = pygame.mouse.get_pos()
        if self.PAUSE_BUTTON_RECT.collidepoint((mouse_x, mouse_y)):
            pygame.draw.rect(screen, RED, self.PAUSE_BUTTON_RECT)
        else:
            pygame.draw.rect(screen, GREEN if self.is_paused else BLUE, self.PAUSE_BUTTON_RECT)
        text = font.render("Pause" if not self.is_paused else "Resume", True, WHITE)
        text_rect = text.get_rect(center=self.PAUSE_BUTTON_RECT.center)
        screen.blit(text, text_rect)

        # Vẽ nút Save Q-Table
        if self.SAVE_BUTTON_RECT.collidepoint((mouse_x, mouse_y)):
            pygame.draw.rect(screen, RED, self.SAVE_BUTTON_RECT)
        else:
            pygame.draw.rect(screen, BLUE, self.SAVE_BUTTON_RECT)
        text = font.render("Save Q-Table", True, WHITE)
        text_rect = text.get_rect(center=self.SAVE_BUTTON_RECT.center)
        screen.blit(text, text_rect)

        pygame.display.flip()

    def handle_event(self, event):
        if event.type == pygame.QUIT:
            return False
        if event.type == pygame.VIDEORESIZE:
            screen = pygame.display.set_mode((event.w, event.h), pygame.RESIZABLE)
            self.update_layout()
        if event.type == pygame.MOUSEBUTTONDOWN:
            x, y = event.pos
            if self.PAUSE_BUTTON_RECT.collidepoint(x, y):
                if not self.is_training:
                    self.is_training = True
                    self.is_paused = False
                else:
                    self.is_paused = not self.is_paused
            elif self.SAVE_BUTTON_RECT.collidepoint(x, y):
                self.save_q_table()
                print("Q-Table saved to q_table.pkl")
        return True

if __name__ == "__main__":
    # Chỉ chạy code này khi file được execute trực tiếp
    GOAL_STATE = [1, 2, 3, 4, 5, 6, 7, 8, 0]
    trainer = QLearningTrainer(GOAL_STATE)

    # Vòng lặp chính
    clock = pygame.time.Clock()
    running = True

    while running:
        for event in pygame.event.get():
            running = trainer.handle_event(event)

        # Thực hiện một bước huấn luyện
        trainer.train_step()

        # Vẽ giao diện
        trainer.draw()

        # Giới hạn tốc độ khung hình
        clock.tick(30)  # Giảm tốc độ để dễ quan sát

    pygame.quit()