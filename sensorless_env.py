﻿import pygame
from solve import Solve
from comboBox import ComboBox

class SensorlessEnvironment:
    def __init__(self, start_state, goal_state, screen, width, height, small_grid_size):
        self.start_state = start_state
        self.goal_state = goal_state
        self.screen = screen
        self.width = width
        self.height = height
        self.small_grid_size = 70
        self.solver = Solve(start_state, goal_state)
        
        # Tạo belief state ban đầu
        self.initial_belief_states = {tuple(self.start_state)}
        for neighbor in self.solver.get_neighbors(self.start_state):
            self.initial_belief_states.add(tuple(neighbor))
        
        self.current_belief_state = self.initial_belief_states
        self.actions = None
        self.solution = None
        self.current_step = 0
        self.is_solution_found = False
        self.is_solved = False
        
        # Vị trí và kích thước các thành phần giao diện
        self.SENSORLESS_SOLVE_BUTTON_RECT = pygame.Rect(self.width * 0.3, self.height * 0.05, self.width * 0.1, self.height * 0.06)
        self.BACK_TO_MAIN_BUTTON_RECT = pygame.Rect(self.width * 0.85, self.height * 0.05, self.width * 0.15, self.height * 0.06)
        self.SENSORLESS_NEXT_STEP_BUTTON_RECT = pygame.Rect(self.width * 0.45, self.height * 0.05, self.width * 0.1, self.height * 0.06)
        self.SENSORLESS_BACK_BUTTON_RECT = pygame.Rect(self.width * 0.6, self.height * 0.05, self.width * 0.1, self.height * 0.06)
        
        # Thêm ComboBox cho lựa chọn thuật toán
        self.algo_combo_box = ComboBox(self.width * 0.05, self.height * 0.05, self.width * 0.2, self.height * 0.06,
                                      ["Partially Observable", "No Observation"])

    def draw_small_board(self, state, position, label):
        """Hiển thị một trạng thái dưới dạng lưới 3x3 nhỏ"""
        x_offset, y_offset = position
        font = pygame.font.Font(None, int(self.height * 0.035))
        label_text = font.render(label, True, (0, 0, 0))
        label_rect = label_text.get_rect(center=(x_offset + (3 * self.small_grid_size) // 2, y_offset - self.height * 0.025))
        self.screen.blit(label_text, label_rect)

        background_rect = pygame.Rect(x_offset - self.width * 0.01, y_offset - self.height * 0.01, 
                                     3 * self.small_grid_size + self.width * 0.02, 3 * self.small_grid_size + self.height * 0.02)
        pygame.draw.rect(self.screen, (220, 220, 220), background_rect)
        pygame.draw.rect(self.screen, (0, 0, 0), background_rect, 2)

        for i in range(3):
            for j in range(3):
                idx = i * 3 + j
                value = state[idx]
                rect = pygame.Rect(x_offset + j * self.small_grid_size, y_offset + i * self.small_grid_size, 
                                  self.small_grid_size, self.small_grid_size)
                pygame.draw.rect(self.screen, (128, 128, 128) if value == 0 else (255, 255, 255), rect)
                pygame.draw.rect(self.screen, (0, 0, 0), rect, 2)
                if value != 0:
                    font = pygame.font.Font(None, int(self.height * 0.035))
                    text = font.render(str(value), True, (0, 0, 0))
                    text_rect = text.get_rect(center=rect.center)
                    self.screen.blit(text, text_rect)

    def draw_belief_state(self, belief_state, y_offset):
        """Hiển thị belief state dưới dạng các lưới 3x3 nhỏ"""
        x_offset = self.width * 0.05
        states = list(belief_state)
        font = pygame.font.Font(None, int(self.height * 0.035))
        
        for idx, state in enumerate(states):
            pos_x = x_offset + (idx % 5) * (3 * self.small_grid_size + self.width * 0.05)
            pos_y = y_offset + (idx // 5) * (3 * self.small_grid_size + self.height * 0.05)
            self.draw_small_board(list(state), (pos_x, pos_y), f"State {idx + 1}")

    def draw(self):
        self.screen.fill((255, 255, 255))
        
        # Hiển thị belief state ban đầu
        font = pygame.font.Font(None, int(self.height * 0.045))
        text = font.render("Initial Belief State:", True, (0, 0, 0))
        self.screen.blit(text, (self.width * 0.05, self.height * 0.12))
        self.draw_belief_state(self.initial_belief_states, self.height * 0.2)

        # Hiển thị belief state hiện tại nếu đã giải
        if self.solution:
            current_belief_state = set()
            for state in self.solution[self.current_step]:
                current_belief_state.add(tuple(state))
            text = font.render("Current Belief State:", True, (0, 0, 0))
            self.screen.blit(text, (self.width * 0.05, self.height * 0.52))
            self.draw_belief_state(current_belief_state, self.height * 0.6)

        # Vẽ ComboBox
        self.algo_combo_box.draw(self.screen)

        # Nút "Solve"
        mouse_x, mouse_y = pygame.mouse.get_pos()
        if self.SENSORLESS_SOLVE_BUTTON_RECT.collidepoint((mouse_x, mouse_y)):
            pygame.draw.rect(self.screen, (255, 0, 0), self.SENSORLESS_SOLVE_BUTTON_RECT)
        else:
            pygame.draw.rect(self.screen, (0, 0, 255), self.SENSORLESS_SOLVE_BUTTON_RECT)
        font = pygame.font.Font(None, int(self.height * 0.05))
        text = font.render("Solve", True, (255, 255, 255))
        text_rect = text.get_rect(center=self.SENSORLESS_SOLVE_BUTTON_RECT.center)
        self.screen.blit(text, text_rect)

        # Nút "Next Step"
        if self.solution:
            if self.SENSORLESS_NEXT_STEP_BUTTON_RECT.collidepoint((mouse_x, mouse_y)):
                pygame.draw.rect(self.screen, (255, 0, 0), self.SENSORLESS_NEXT_STEP_BUTTON_RECT)
            else:
                pygame.draw.rect(self.screen, (0, 255, 0), self.SENSORLESS_NEXT_STEP_BUTTON_RECT)
            text = font.render(f"Next ({self.current_step}/{len(self.solution) - 1})", True, (255, 255, 255))
            text_rect = text.get_rect(center=self.SENSORLESS_NEXT_STEP_BUTTON_RECT.center)
            self.screen.blit(text, text_rect)

        # Nút "Back"
        if self.solution and self.current_step > 0:
            if self.SENSORLESS_BACK_BUTTON_RECT.collidepoint((mouse_x, mouse_y)):
                pygame.draw.rect(self.screen, (255, 0, 0), self.SENSORLESS_BACK_BUTTON_RECT)
            else:
                pygame.draw.rect(self.screen, (255, 255, 0), self.SENSORLESS_BACK_BUTTON_RECT)
            text = font.render("Back", True, (0, 0, 0))
            text_rect = text.get_rect(center=self.SENSORLESS_BACK_BUTTON_RECT.center)
            self.screen.blit(text, text_rect)

        # Nút "Back to Main"
        if self.BACK_TO_MAIN_BUTTON_RECT.collidepoint((mouse_x, mouse_y)):
            pygame.draw.rect(self.screen, (255, 0, 0), self.BACK_TO_MAIN_BUTTON_RECT)
        else:
            pygame.draw.rect(self.screen, (0, 0, 255), self.BACK_TO_MAIN_BUTTON_RECT)
        text = font.render("Back to Main", True, (255, 255, 255))
        text_rect = text.get_rect(center=self.BACK_TO_MAIN_BUTTON_RECT.center)
        self.screen.blit(text, text_rect)

        # Hiển thị chuỗi hành động nếu đã giải
        if self.actions:
            font = pygame.font.Font(None, int(self.height * 0.045))
            text = font.render(f"Action Sequence: {self.actions}", True, (0, 0, 0))
            self.screen.blit(text, (self.width * 0.05, self.height * 0.9))

        if not self.is_solution_found and self.is_solved:
                text = font.render("NO SOLUTION FOUND!", True, (255, 0, 0))
                self.screen.blit(text, (self.width * 0.05, self.height * 0.9))

        pygame.display.flip()

    def handle_event(self, event):
        # Xử lý sự kiện của ComboBox
        if self.algo_combo_box.handle_event(event):
            pass  # ComboBox tự xử lý việc chọn tùy chọn

        if event.type == pygame.MOUSEBUTTONDOWN:
            x, y = event.pos

            # Nút "Solve"
            if self.SENSORLESS_SOLVE_BUTTON_RECT.collidepoint(x, y):
                start_time = pygame.time.get_ticks() / 1000.0
                if self.algo_combo_box.selected_option == "Partially Observable":
                    self.actions = self.solver.solve_partially_observable(max_steps=100000)
                elif self.algo_combo_box.selected_option == "No Observation":
                    self.actions = self.solver.solve_no_observation(max_steps=50000)
                end_time = pygame.time.get_ticks() / 1000.0
                execution_time = end_time - start_time

                if self.actions:
                    # Tạo solution: danh sách các belief states qua từng bước
                    self.solution = [list(self.initial_belief_states)]
                    self.is_solved = True
                    temp_belief_state = self.initial_belief_states
                    actual_state = self.start_state  # Để mô phỏng actual_state như trong solve_partially_observable

                    if self.algo_combo_box.selected_option == "No Observation":
                        for action in self.actions:
                            # Áp dụng hành động để tạo belief state mới
                            temp_belief_state = self.solver.apply_action_to_belief_state(temp_belief_state, action)

                            new_belief_state = set()
                            for state in temp_belief_state:
                                new_belief_state.add(tuple(state))
                            temp_belief_state = new_belief_state

                            self.solution.append(list(temp_belief_state))
    
                        # Kiểm tra xem belief state cuối cùng có thỏa mãn điều kiện không
                        final_belief_state = set(temp_belief_state)
                        # Solve No Observation: Belief state cuối cùng phải chỉ chứa goal_state
                        self.is_solution_found = len(final_belief_state) == 1 and list(final_belief_state)[0] == tuple(self.goal_state)
                    else:
                        for action in self.actions:
                            # Áp dụng hành động để tạo belief state mới
                            temp_belief_state = self.solver.apply_action_to_belief_state(temp_belief_state, action)

                            # Mô phỏng actual_state và lấy percept
                            actual_state = self.solver.apply_action(actual_state, action)
                            actual_percept = self.solver.percept(actual_state)

                            # Thu hẹp belief state dựa trên percept (tương tự như update trong solve_partially_observable)
                            new_belief_state = set()
                            for state in temp_belief_state:
                                if self.solver.percept(state) == actual_percept:
                                    new_belief_state.add(tuple(state))
                            temp_belief_state = new_belief_state

                            self.solution.append(list(temp_belief_state))
    
                        # Kiểm tra xem belief state cuối cùng có thỏa mãn điều kiện không
                        final_belief_state = set(temp_belief_state)
                        # Partially Observable: Chỉ cần goal_state nằm trong belief_state
                        self.is_solution_found = tuple(self.goal_state) in final_belief_state

                    print(f"{self.algo_combo_box.selected_option} completed! Action sequence: {self.actions}")
                    print(f"Number of actions: {len(self.actions)}")
                    print(f"Execution Time: {execution_time:.6f} seconds")
                else:
                    self.is_solution_found = False
                    self.solution = None  # Không có giải pháp, không hiển thị các bước
                    self.is_solved = True
                    print(f"No solution found with {self.algo_combo_box.selected_option}!")
                    print(f"Execution Time: {execution_time:.6f} seconds")

                self.current_step = 0

            # Nút "Next Step"
            elif self.solution and self.SENSORLESS_NEXT_STEP_BUTTON_RECT.collidepoint(x, y):
                if self.current_step < len(self.solution) - 1:
                    self.current_step += 1

            # Nút "Back"
            elif self.solution and self.SENSORLESS_BACK_BUTTON_RECT.collidepoint(x, y) and self.current_step > 0:
                self.current_step -= 1

            # Nút "Back to Main"
            elif self.BACK_TO_MAIN_BUTTON_RECT.collidepoint(x, y):
                return False  # Quay lại giao diện chính

        return True  # Tiếp tục ở trang Sensorless Environment