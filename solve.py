import heapq
from collections import deque
import copy
import random
import math
import pickle
from collections import defaultdict
from Qlearning import SlidingPuzzleEnv
import numpy as np

class Solve:
    def __init__(self, start_state, goal_state):
        self.start_state = start_state
        self.goal_state = goal_state

    def is_valid_state(self, state):
        return len(state) == 9 and all(0 <= x <= 8 for x in state)

    def find_empty(self, state):
        return state.index(0)

    def get_neighbors(self, state):
        if not self.is_valid_state(state):
            return []
        
        neighbors = []
        empty_idx = state.index(0)
        row, col = divmod(empty_idx, 3)

        directions = [(-1, 0), (1, 0), (0, -1), (0, 1)]
        for dx, dy in directions:
            new_row, new_col = row + dx, col + dy
            if 0 <= new_row < 3 and 0 <= new_col < 3:
                new_idx = new_row * 3 + new_col
                new_state = list(state)
                new_state[empty_idx], new_state[new_idx] = new_state[new_idx], new_state[empty_idx]
                neighbors.append(new_state)
        return neighbors

    def solve_with_bfs(self):
        if not self.is_valid_state(self.start_state) or not self.is_valid_state(self.goal_state):
            return None

        queue = deque()
        queue.append((self.start_state, [self.start_state]))

        visited = {tuple(self.start_state)}

        # Theo dõi đường đi tốt nhất (dựa trên khoảng cách Manhattan nhỏ nhất)
        best_path = [self.start_state]
        best_distance = self.manhattan_distance(self.start_state, self.goal_state)

        while queue:
            current_state, path = queue.popleft()

            # Cập nhật đường đi tốt nhất
            current_distance = self.manhattan_distance(current_state, self.goal_state)
            if current_distance < best_distance:
                best_distance = current_distance
                best_path = path

            if current_state == self.goal_state:
                return path
    
            for next_state in self.get_neighbors(current_state):
                if tuple(next_state) not in visited:
                    visited.add(tuple(next_state))
                    new_path = path + [next_state]
                    queue.append((next_state, new_path))

        # Nếu không tìm thấy giải pháp, trả về đường đi tốt nhất
        return best_path

    def solve_with_dfs(self):
        if not self.is_valid_state(self.start_state) or not self.is_valid_state(self.goal_state):
            return None

        stack = deque()
        stack.append((self.start_state, [self.start_state]))

        visited = {tuple(self.start_state)}

        # Theo dõi đường đi tốt nhất (dựa trên khoảng cách Manhattan nhỏ nhất)
        best_path = [self.start_state]
        best_distance = self.manhattan_distance(self.start_state, self.goal_state)

        while stack:
            current_state, path = stack.pop()

            # Cập nhật đường đi tốt nhất
            current_distance = self.manhattan_distance(current_state, self.goal_state)
            if current_distance < best_distance:
                best_distance = current_distance
                best_path = path

            if current_state == self.goal_state:
                return path
    
            for next_state in self.get_neighbors(current_state):
                if tuple(next_state) not in visited:
                    visited.add(tuple(next_state))
                    new_path = path + [next_state]
                    stack.append((next_state, new_path))

        # Nếu không tìm thấy giải pháp, trả về đường đi tốt nhất
        return best_path

    def solve_with_ucs(self):
        if not self.is_valid_state(self.start_state) or not self.is_valid_state(self.goal_state):
            return None

        # Sử dụng heapq cho hàng đợi ưu tiên
        pq = []
        heapq.heappush(pq, (0, self.start_state, [self.start_state]))  # (chi phí, trạng thái, đường đi)
        visited = set()

        # Theo dõi đường đi tốt nhất (dựa trên khoảng cách Manhattan nhỏ nhất)
        best_path = [self.start_state]
        best_distance = self.manhattan_distance(self.start_state, self.goal_state)

        while pq:
            cost, current_state, path = heapq.heappop(pq)

            if tuple(current_state) in visited:
                continue
            visited.add(tuple(current_state))

            # Cập nhật đường đi tốt nhất
            current_distance = self.manhattan_distance(current_state, self.goal_state)
            if current_distance < best_distance:
                best_distance = current_distance
                best_path = path

            if current_state == self.goal_state:
                return path

            for next_state in self.get_neighbors(current_state):
                if tuple(next_state) not in visited:
                    new_cost = cost + 1  # Mỗi bước di chuyển có chi phí 1
                    new_path = path + [next_state]
                    heapq.heappush(pq, (new_cost, next_state, new_path))

        # Nếu không tìm thấy giải pháp, trả về đường đi tốt nhất
        return best_path

    def depth_limited_search(self, state, goal_state, depth_limit, visited, best_info):
        """
        best_info là một dictionary để theo dõi đường đi tốt nhất:
        - best_info['path']: Đường đi tốt nhất
        - best_info['distance']: Khoảng cách Manhattan nhỏ nhất
        """
        if state == goal_state:
            return [state]
        if depth_limit == 0:
            return None

        # Cập nhật đường đi tốt nhất
        current_distance = self.manhattan_distance(state, goal_state)
        if current_distance < best_info['distance']:
            best_info['distance'] = current_distance
            best_info['path'] = best_info.get('path', [])[:-1] + [state]

        visited.add(tuple(state))
        for next_state in self.get_neighbors(state):
            if tuple(next_state) not in visited:
                path = self.depth_limited_search(next_state, goal_state, depth_limit - 1, visited, best_info)
                if path is not None:
                    return [state] + path
        return None

    def solve_with_ids(self):
        if not self.is_valid_state(self.start_state) or not self.is_valid_state(self.goal_state):
            return None

        depth_limit = 0

        # Theo dõi đường đi tốt nhất qua best_info
        best_info = {
            'path': [self.start_state],
            'distance': self.manhattan_distance(self.start_state, self.goal_state)
        }

        while True:
            visited = set()
            result = self.depth_limited_search(self.start_state, self.goal_state, depth_limit, visited, best_info)
            if result is not None:
                return result
            depth_limit += 1
            # Nếu depth_limit vượt quá một ngưỡng lớn (ví dụ: 100), trả về đường đi tốt nhất
            if depth_limit > 100:  # Ngưỡng tùy chọn để tránh vòng lặp vô hạn
                return best_info['path']

    def manhattan_distance(self, state, goal_state):
        total_distance = 0
        for value in range(1, 9):
            current_index = state.index(value)
            current_row, current_col = divmod(current_index, 3)

            goal_index = goal_state.index(value) 
            goal_row, goal_col = divmod(goal_index, 3)

            distance = abs(current_row - goal_row) + abs(current_col - goal_col)
            total_distance += distance

        return total_distance

    def solve_with_greedy(self):
        if not self.is_valid_state(self.start_state) or not self.is_valid_state(self.goal_state):
            return None

        # Sử dụng heapq cho hàng đợi ưu tiên
        pq = []
        cost = self.manhattan_distance(self.start_state, self.goal_state)
        heapq.heappush(pq, (cost, self.start_state, [self.start_state]))
        visited = set()

        # Theo dõi đường đi tốt nhất (dựa trên khoảng cách Manhattan nhỏ nhất)
        best_path = [self.start_state]
        best_distance = self.manhattan_distance(self.start_state, self.goal_state)

        while pq:
            cost, current_state, path = heapq.heappop(pq)

            if tuple(current_state) in visited:
                continue
            visited.add(tuple(current_state))

            # Cập nhật đường đi tốt nhất
            current_distance = self.manhattan_distance(current_state, self.goal_state)
            if current_distance < best_distance:
                best_distance = current_distance
                best_path = path

            if current_state == self.goal_state:
                return path

            for next_state in self.get_neighbors(current_state):
                if tuple(next_state) not in visited:
                    new_cost = self.manhattan_distance(next_state, self.goal_state)
                    new_path = path + [next_state]
                    heapq.heappush(pq, (new_cost, next_state, new_path))

        # Nếu không tìm thấy giải pháp, trả về đường đi tốt nhất
        return best_path

    def solve_with_astar(self):
        if not self.is_valid_state(self.start_state) or not self.is_valid_state(self.goal_state):
            return None

        # Sử dụng heapq cho hàng đợi ưu tiên
        pq = []
        h_cost = self.manhattan_distance(self.start_state, self.goal_state)
        g_cost = 0
        heapq.heappush(pq, (h_cost + g_cost, g_cost, self.start_state, [self.start_state]))
        visited = set()

        # Theo dõi đường đi tốt nhất (dựa trên khoảng cách Manhattan nhỏ nhất)
        best_path = [self.start_state]
        best_distance = self.manhattan_distance(self.start_state, self.goal_state)

        while pq:
            cost, g_cost, current_state, path = heapq.heappop(pq)

            if tuple(current_state) in visited:
                continue
            visited.add(tuple(current_state))

            # Cập nhật đường đi tốt nhất
            current_distance = self.manhattan_distance(current_state, self.goal_state)
            if current_distance < best_distance:
                best_distance = current_distance
                best_path = path

            if current_state == self.goal_state:
                return path

            for next_state in self.get_neighbors(current_state):
                if tuple(next_state) not in visited:
                    new_g_cost = g_cost + 1
                    new_h_cost = self.manhattan_distance(next_state, self.goal_state)
                    new_cost = new_h_cost + new_g_cost
                    new_path = path + [next_state]
                    heapq.heappush(pq, (new_cost, new_g_cost, next_state, new_path))

        # Nếu không tìm thấy giải pháp, trả về đường đi tốt nhất
        return best_path

    def depth_limited_search_astar(self, state, goal_state, f_limit, g_cost, best_info):
        """
        best_info là một dictionary để theo dõi đường đi tốt nhất:
        - best_info['path']: Đường đi tốt nhất
        - best_info['distance']: Khoảng cách Manhattan nhỏ nhất
        """
        f_cost = g_cost + self.manhattan_distance(state, goal_state)
        if f_cost > f_limit:
            return f_cost

        # Cập nhật đường đi tốt nhất
        current_distance = self.manhattan_distance(state, goal_state)
        if current_distance < best_info['distance']:
            best_info['distance'] = current_distance
            best_info['path'] = best_info.get('path', [])[:-1] + [state]

        if state == goal_state:
            return [state]

        min_threshold = float('inf')
        for next_state in self.get_neighbors(state):
            # Truyền best_info để tiếp tục cập nhật trong các lần gọi đệ quy
            path = self.depth_limited_search_astar(next_state, goal_state, f_limit, g_cost + 1, best_info)
        
            if isinstance(path, list):
                return [state] + path

            min_threshold = min(min_threshold, path)

        return min_threshold

    def solve_with_idastar(self):
        if not self.is_valid_state(self.start_state) or not self.is_valid_state(self.goal_state):
            return None

        f_limit = self.manhattan_distance(self.start_state, self.goal_state)

        # Theo dõi đường đi tốt nhất qua best_info
        best_info = {
            'path': [self.start_state],
            'distance': self.manhattan_distance(self.start_state, self.goal_state)
        }

        while True:
            result = self.depth_limited_search_astar(self.start_state, self.goal_state, f_limit, 0, best_info)
        
            if isinstance(result, list):
                return result
            elif result == float('inf'):
                return best_info['path']  # Trả về đường đi tốt nhất thay vì None
            else:
                f_limit = result

    def solve_hill_climbing(self):
        if not self.is_valid_state(self.start_state) or not self.is_valid_state(self.goal_state):
            return None

        current_state = self.start_state
        path = [current_state]

        # Theo dõi đường đi tốt nhất (dựa trên khoảng cách Manhattan nhỏ nhất)
        best_path = [self.start_state]
        best_distance = self.manhattan_distance(self.start_state, self.goal_state)

        while True:
            neighbors = self.get_neighbors(current_state)
            best_neighbor = None
            best_cost = self.manhattan_distance(current_state, self.goal_state)

            for neighbor in neighbors:
                cost = self.manhattan_distance(neighbor, self.goal_state)
                # Cập nhật đường đi tốt nhất nếu tìm thấy trạng thái có khoảng cách nhỏ hơn
                if cost < best_distance:
                    best_distance = cost
                    best_path = path + [neighbor]
                if cost < best_cost:
                    best_cost = cost
                    best_neighbor = neighbor

            if best_neighbor is None:
                return best_path  # Trả về đường đi tốt nhất thay vì None

            current_state = best_neighbor
            path.append(current_state)

            if current_state == self.goal_state:
                return path

    def solve_steepest_ascent_hill_climbing(self):
        if not self.is_valid_state(self.start_state) or not self.is_valid_state(self.goal_state):
            return None

        current_state = self.start_state
        path = [current_state]

        # Theo dõi đường đi tốt nhất (dựa trên khoảng cách Manhattan nhỏ nhất)
        best_path = [self.start_state]
        best_distance = self.manhattan_distance(self.start_state, self.goal_state)

        while True:
            neighbors = self.get_neighbors(current_state)
            best_neighbor = None
            best_cost = self.manhattan_distance(current_state, self.goal_state)

            for neighbor in neighbors:
                cost = self.manhattan_distance(neighbor, self.goal_state)
                # Cập nhật đường đi tốt nhất nếu tìm thấy trạng thái có khoảng cách nhỏ hơn
                if cost < best_distance:
                    best_distance = cost
                    best_path = path + [neighbor]
                if cost < best_cost:  # Sửa từ "cost > best_cost" thành "cost < best_cost" để tối thiểu hóa
                    best_cost = cost
                    best_neighbor = neighbor

            if best_neighbor is None:
                return best_path  # Trả về đường đi tốt nhất thay vì None

            current_state = best_neighbor
            path.append(current_state)

            if current_state == self.goal_state:
                return path

    def solve_stochastic_hill_climbing(self):
        if not self.is_valid_state(self.start_state) or not self.is_valid_state(self.goal_state):
            return None

        current_state = self.start_state
        path = [current_state]

        # Theo dõi đường đi tốt nhất (dựa trên khoảng cách Manhattan nhỏ nhất)
        best_path = [self.start_state]
        best_distance = self.manhattan_distance(self.start_state, self.goal_state)

        while True:
            neighbors = self.get_neighbors(current_state)
            current_cost = self.manhattan_distance(current_state, self.goal_state)

            # Cập nhật đường đi tốt nhất dựa trên các neighbor
            for neighbor in neighbors:
                cost = self.manhattan_distance(neighbor, self.goal_state)
                if cost < best_distance:
                    best_distance = cost
                    best_path = path + [neighbor]

            better_neighbors = [
                neighbor for neighbor in neighbors
                if self.manhattan_distance(neighbor, self.goal_state) < current_cost
            ]

            if not better_neighbors:
                return best_path  # Trả về đường đi tốt nhất thay vì None

            current_state = random.choice(better_neighbors)
            path.append(current_state)

            if current_state == self.goal_state:
                return path

    def solve_with_beam_search(self, beam_width=3):
        if not self.is_valid_state(self.start_state) or not self.is_valid_state(self.goal_state):
            return None

        # Beam là danh sách các trạng thái: (state, path)
        beam = [(self.start_state, [self.start_state])]
        visited = {tuple(self.start_state)}

        # Theo dõi đường đi tốt nhất (dựa trên khoảng cách Manhattan nhỏ nhất)
        best_path = [self.start_state]
        best_distance = self.manhattan_distance(self.start_state, self.goal_state)

        while beam:
            candidates = []

            for state, path in beam:
                for neighbor in self.get_neighbors(state):
                    neighbor_tuple = tuple(neighbor)
                    if neighbor_tuple in visited:
                        continue
                    visited.add(neighbor_tuple)
                    new_path = path + [neighbor]
                    if neighbor == self.goal_state:
                        return new_path

                    # Tính khoảng cách Manhattan và cập nhật đường đi tốt nhất
                    cost = self.manhattan_distance(neighbor, self.goal_state)
                    if cost < best_distance:
                        best_distance = cost
                        best_path = new_path
                    candidates.append((cost, neighbor, new_path))

            if not candidates:
                break

            # Chọn beam_width trạng thái tốt nhất theo heuristic
            candidates.sort(key=lambda x: x[0])
            beam = [(state, path) for (_, state, path) in candidates[:beam_width]]

        # Nếu không tìm thấy giải pháp, trả về đường đi tốt nhất
        return best_path

    def solve_with_annealing(self, initial_temperature=1000, cooling_rate=0.99, min_temperature=0.1):
        if not self.is_valid_state(self.start_state) or not self.is_valid_state(self.goal_state):
            return None

        current_state = self.start_state
        current_path = [self.start_state]
        temperature = initial_temperature

        # Theo dõi đường đi tốt nhất (dựa trên khoảng cách Manhattan nhỏ nhất)
        best_path = [self.start_state]
        best_distance = self.manhattan_distance(self.start_state, self.goal_state)

        while temperature > min_temperature:
            neighbors = self.get_neighbors(current_state)
            if not neighbors:
                break

            next_state = random.choice(neighbors)
            current_cost = self.manhattan_distance(current_state, self.goal_state)
            next_cost = self.manhattan_distance(next_state, self.goal_state)

            # Cập nhật đường đi tốt nhất
            if next_cost < best_distance:
                best_distance = next_cost
                best_path = current_path + [next_state]

            delta = next_cost - current_cost

            # Quyết định chấp nhận
            if delta < 0 or random.random() < math.exp(-delta / temperature):
                current_state = next_state
                current_path.append(current_state)

                if current_state == self.goal_state:
                    return current_path

            # Giảm nhiệt độ
            temperature *= cooling_rate

        # Nếu không tìm thấy giải pháp, trả về đường đi tốt nhất
        return best_path

    def solve_with_genetic_algorithm(self, pop_size=50, max_moves=30, generations=200, 
                                tournament_size=3, crossover_rate=0.8, mutation_rate=0.1):

        if not self.is_valid_state(self.start_state) or not self.is_valid_state(self.goal_state):
            return None
    
        # Define possible moves (up, down, left, right for the empty space)
        directions = ["up", "down", "left", "right"]
    
        def initialize_population(pop_size, max_moves):
            """Initialize a population of random move sequences"""
            population = []
            for _ in range(pop_size):
                # Create random move sequences of variable length
                num_moves = random.randint(1, max_moves)
                moves = [random.choice(directions) for _ in range(num_moves)]
                population.append(moves)
            return population
    
        def apply_moves(state, moves):
            """Apply a sequence of moves to a state"""
            current_state = list(state)
            path = [current_state.copy()]  # Start with initial state
        
            for move in moves:
                empty_idx = current_state.index(0)
                row, col = divmod(empty_idx, 3)
                new_row, new_col = row, col
            
                if move == "up" and row > 0:
                    new_row -= 1
                elif move == "down" and row < 2:
                    new_row += 1
                elif move == "left" and col > 0:
                    new_col -= 1
                elif move == "right" and col < 2:
                    new_col += 1
                else:
                    continue  # Skip invalid moves
                
                new_idx = new_row * 3 + new_col
                current_state[empty_idx], current_state[new_idx] = current_state[new_idx], current_state[empty_idx]
                path.append(current_state.copy())  # Record each new state
            
            return path
    
        def fitness(individual):
            """Calculate fitness of an individual (sequence of moves)"""
            path = apply_moves(self.start_state, individual)
            final_state = path[-1]
        
            # Primary objective: how close we are to the goal state
            # Use Manhattan distance as a heuristic
            distance = self.manhattan_distance(final_state, self.goal_state)
        
            # Penalize longer sequences slightly to favor shorter solutions
            length_penalty = len(individual) * 0.1
        
            # Higher fitness is better, so we negate the distance
            return -distance - length_penalty
    
        def tournament_selection(population, fitness_values, tournament_size):
            """Select individuals using tournament selection"""
            selected = []
            for _ in range(len(population)):
                # Select tournament_size individuals randomly
                candidates = random.sample(range(len(population)), tournament_size)
                # Find the best individual among them
                winner_idx = max(candidates, key=lambda idx: fitness_values[idx])
                selected.append(population[winner_idx])
            return selected
    
        def crossover(parent1, parent2):
            """Perform one-point crossover between two parents"""
            if len(parent1) < 2 or len(parent2) < 2:
                return parent1.copy(), parent2.copy()
            
            # Choose a random crossover point
            point1 = random.randint(1, len(parent1) - 1)
            point2 = random.randint(1, len(parent2) - 1)
        
            # Create children by swapping parts of parents
            child1 = parent1[:point1] + parent2[point2:]
            child2 = parent2[:point2] + parent1[point1:]
        
            return child1, child2
    
        def mutate(individual):
            """Mutate an individual by randomly changing some moves"""
            mutated = individual.copy()
            for i in range(len(mutated)):
                if random.random() < mutation_rate:
                    mutated[i] = random.choice(directions)
        
            # Sometimes add or remove a move
            if random.random() < mutation_rate and len(mutated) > 1:
                if random.random() < 0.5 and len(mutated) < max_moves:
                    # Add a random move
                    mutated.append(random.choice(directions))
                else:
                    # Remove a random move
                    del mutated[random.randint(0, len(mutated) - 1)]
                
            return mutated
    
        # Main genetic algorithm loop
        population = initialize_population(pop_size, max_moves)
        best_solution = None
        best_fitness = float('-inf')
    
        for generation in range(generations):
            # Calculate fitness for each individual
            fitness_values = [fitness(individual) for individual in population]
        
            # Check if we've found a solution
            for i, individual in enumerate(population):
                path = apply_moves(self.start_state, individual)
                final_state = path[-1]
            
                if final_state == self.goal_state:
                    # Found a solution!
                    return path
        
            # Find current best individual
            current_best_idx = fitness_values.index(max(fitness_values))
            current_best_individual = population[current_best_idx]
            current_best_fitness = fitness_values[current_best_idx]
        
            # Update overall best if this generation is better
            if current_best_fitness > best_fitness:
                best_fitness = current_best_fitness
                best_solution = current_best_individual
        
            # Select individuals for reproduction
            selected = tournament_selection(population, fitness_values, tournament_size)
        
            # Create new population
            new_population = []
        
            # Elitism: keep the best individual
            new_population.append(current_best_individual)
        
            # Fill the rest of the new population with offspring
            while len(new_population) < pop_size:
                # Select two parents
                parent1, parent2 = random.sample(selected, 2)
            
                # Perform crossover with probability crossover_rate
                if random.random() < crossover_rate:
                    child1, child2 = crossover(parent1, parent2)
                else:
                    child1, child2 = parent1.copy(), parent2.copy()
            
                # Mutate children
                child1 = mutate(child1)
                child2 = mutate(child2)
            
                # Add to new population
                new_population.append(child1)
                if len(new_population) < pop_size:
                    new_population.append(child2)
        
            # Replace old population with new population
            population = new_population
    
        # Nếu chúng ta đã đạt đến đây, chúng ta đã sử dụng hết tất cả các thế hệ mà không tìm thấy giải pháp
        # Trả về đường đi của giải pháp tốt nhất tìm thấy cho đến nay
        if best_solution is not None:
            return apply_moves(self.start_state, best_solution)
    
        return None

    class Node:
        def __init__(self, state, is_and=False, parent=None):
            self.state = state
            self.is_and = is_and  # True nếu là nút AND, False nếu là nút OR
            self.parent = parent
            self.children = []  # Danh sách các nút con
            self.path = []  # Đường đi từ nút gốc đến nút này

    def get_opponent_moves(self, state):
        # Mô phỏng các di chuyển của "đối thủ" (ngẫu nhiên)
        neighbors = self.get_neighbors(state)
        if not neighbors:
            return [state]
        return neighbors  # Trả về tất cả các trạng thái có thể do đối thủ tạo ra

    def solve_with_and_or_graph(self):
        if not self.is_valid_state(self.start_state) or not self.is_valid_state(self.goal_state):
            return None

        # Danh sách các nút đã thăm để tránh lặp
        visited = set()
        # Theo dõi đường đi tốt nhất (dựa trên khoảng cách Manhattan nhỏ nhất)
        best_path = [self.start_state]
        best_distance = self.manhattan_distance(self.start_state, self.goal_state)

        def search(node):
            nonlocal best_path, best_distance

            state_tuple = tuple(node.state)
            if state_tuple in visited:
                return None  # Tránh lặp
            visited.add(state_tuple)

            # Cập nhật đường đi tốt nhất
            current_distance = self.manhattan_distance(node.state, self.goal_state)
            if current_distance < best_distance:
                best_distance = current_distance
                best_path = node.path + [node.state]

            # Nếu trạng thái là goal_state, trả về đường đi
            if node.state == self.goal_state:
                return node.path + [node.state]

            # Nếu là nút OR (lượt của người chơi)
            if not node.is_and:
                children_states = self.get_neighbors(node.state)
                node.children = [self.Node(child_state, is_and=True, parent=node) for child_state in children_states]

                # Tại nút OR, chỉ cần một nhánh con thành công
                for child in node.children:
                    child.path = node.path + [node.state]
                    sub_solution = search(child)
                    if sub_solution is not None:
                        return sub_solution
                return None

            # Nếu là nút AND (lượt của "đối thủ")
            else:
                opponent_states = self.get_opponent_moves(node.state)
                node.children = [self.Node(child_state, is_and=False, parent=node) for child_state in opponent_states]

                # Tại nút AND, tất cả nhánh con phải thành công
                sub_solutions = []
                for child in node.children:
                    child.path = node.path + [node.state]
                    sub_solution = search(child)
                    if sub_solution is None:
                        return None  # Nếu một nhánh thất bại, nút AND thất bại
                    sub_solutions.append(sub_solution)

                # Nếu tất cả nhánh con thành công, chọn nhánh đầu tiên
                return sub_solutions[0] if sub_solutions else None

        # Bắt đầu tìm kiếm từ nút gốc (lượt của người chơi, nên là nút OR)
        root = self.Node(self.start_state, is_and=False)
        root.path = []
        solution = search(root)

        # Nếu tìm thấy giải pháp, trả về giải pháp
        if solution is not None:
            return solution
        # Nếu không tìm thấy giải pháp, trả về đường đi tốt nhất (dựa trên khoảng cách Manhattan nhỏ nhất)
        return best_path

    def apply_action(self, state, action):
        """
        Áp dụng một hành động (up, down, left, right) cho trạng thái.
        Nếu hành động không hợp lệ, trả về trạng thái hiện tại.
        """
        empty_idx = self.find_empty(state)
        row, col = divmod(empty_idx, 3)
        new_row, new_col = row, col

        if action == "up" and row > 0:
            new_row -= 1
        elif action == "down" and row < 2:
            new_row += 1
        elif action == "left" and col > 0:
            new_col -= 1
        elif action == "right" and col < 2:
            new_col += 1
        else:
            return state

        new_idx = new_row * 3 + new_col
        new_state = copy.deepcopy(state)
        new_state[empty_idx], new_state[new_idx] = new_state[new_idx], new_state[empty_idx]
        return new_state

    def apply_action_to_belief_state(self, belief_state, action):
        """
        Áp dụng một hành động cho toàn bộ belief state.
        Trả về belief state mới.
        """
        new_belief_state = set()
        for state in belief_state:
            new_state = tuple(self.apply_action(list(state), action))
            new_belief_state.add(new_state)
        return new_belief_state

    def solve_no_observation(self, max_steps=50):
        """
        Giải bài toán Sensorless Sliding Puzzle bằng BFS trong không gian belief state.
        - max_steps: Giới hạn số bước để tránh tìm kiếm quá lâu.
        Trả về chuỗi hành động dẫn đến trạng thái mục tiêu, hoặc None nếu không tìm thấy.
        """
        if not self.is_valid_state(self.start_state) or not self.is_valid_state(self.goal_state):
            return None

        # Belief state ban đầu: Để đơn giản, giả sử tập hợp trạng thái ban đầu là tất cả các trạng thái
        # có thể đạt được từ start_state qua 1 bước di chuyển
        initial_belief_states = {tuple(self.start_state)}
        for neighbor in self.get_neighbors(self.start_state):
            initial_belief_states.add(tuple(neighbor))

        initial_belief_state = frozenset(initial_belief_states)
        actions = ["up", "down", "left", "right"]

        # Hàng đợi cho BFS: (belief_state, actions)
        queue = deque([(initial_belief_state, [])])
        visited = {initial_belief_state}

        step = 0
        while queue and step < max_steps:
            belief_state, actions_taken = queue.popleft()
            step += 1

            # Kiểm tra xem belief state có chỉ chứa trạng thái mục tiêu không
            belief_state_set = set(belief_state)
            if len(belief_state_set) == 1 and list(belief_state_set)[0] == tuple(self.goal_state):
                return actions_taken

            # Thử tất cả các hành động
            for action in actions:
                new_belief_state = self.apply_action_to_belief_state(belief_state, action)
                new_belief_state_frozen = frozenset(new_belief_state)

                if new_belief_state_frozen not in visited:
                    visited.add(new_belief_state_frozen)
                    new_actions = actions_taken + [action]
                    queue.append((new_belief_state, new_actions))

        return None

    def percept(self, state):
        """
        Hàm PERCEPT: Trả về thông tin quan sát được từ trạng thái.
        Giả định: Chỉ nhìn thấy giá trị ở góc trên cùng bên trái (vị trí 0).
        """
        return state[0]

    def predict(self, belief_state, action):
        """
        Giai đoạn Prediction: Tính predicted belief state sau khi thực hiện hành động.
        """
        return self.apply_action_to_belief_state(belief_state, action)

    def possible_percepts(self, belief_state):
        """
        Giai đoạn Possible Percepts: Tính tập hợp các percept có thể nhận được.
        """
        percepts = set()
        for state in belief_state:
            percept = self.percept(state)
            percepts.add(percept)
        return percepts

    def update(self, belief_state, percept):
        """
        Giai đoạn Update: Cập nhật belief state dựa trên percept.
        """
        new_belief_state = set()
        for state in belief_state:
            if self.percept(state) == percept:
                new_belief_state.add(state)
        return new_belief_state

    def results(self, belief_state, action):
        """
        Tính tập hợp các belief states mới sau khi thực hiện hành động và nhận percept.
        """
        predicted_belief_state = self.predict(belief_state, action)
        possible_percepts = self.possible_percepts(predicted_belief_state)
        results = {}
        for percept in possible_percepts:
            updated_belief_state = self.update(predicted_belief_state, percept)
            results[percept] = updated_belief_state
        return results

    def solve_partially_observable(self, max_steps=50):
        """
        Giải bài toán Sliding Puzzle trong môi trường quan sát một phần bằng BFS.
        - max_steps: Giới hạn số bước để tránh tìm kiếm quá lâu.
        Trả về một chuỗi hành động dẫn đến trạng thái mục tiêu, hoặc None nếu không tìm thấy.
        Lưu ý: Chỉ cần goal_state nằm trong belief_state cuối cùng.
        """
        if not self.is_valid_state(self.start_state) or not self.is_valid_state(self.goal_state):
            return None

        # Khởi tạo belief state ban đầu với start_state và các trạng thái lân cận
        initial_belief_states = {tuple(self.start_state)}
        for neighbor in self.get_neighbors(self.start_state):
            initial_belief_states.add(tuple(neighbor))
        initial_belief_state = frozenset(initial_belief_states)

        actions = ["up", "down", "left", "right"]

        # Hàng đợi cho BFS: (belief_state, actions_taken, actual_state)
        queue = deque([(initial_belief_state, [], self.start_state)])
        visited = {initial_belief_state}  # Belief states đã thăm

        step = 0
        while queue:
            belief_state, actions_taken, actual_state = queue.popleft()
            step += 1

            # Kiểm tra xem goal_state có nằm trong belief_state không
            belief_state_set = set(belief_state)
            if tuple(self.goal_state) in belief_state_set:
                return actions_taken

            # Thử tất cả các hành động
            for action in actions:
                # Tính các belief states mới sau hành động
                results = self.results(belief_state, action)
                if not results:
                    continue

                # Mô phỏng trạng thái thực tế sau khi thực hiện hành động
                new_actual_state = self.apply_action(actual_state, action)

                # Lấy percept thực tế từ trạng thái thực tế
                actual_percept = self.percept(new_actual_state)

                # Chọn nhánh tương ứng với percept thực tế
                if actual_percept not in results:
                    continue  # Nếu percept thực tế không khớp, bỏ qua nhánh này

                new_belief_state = results[actual_percept]
                new_belief_state_frozen = frozenset(new_belief_state)

                if new_belief_state_frozen not in visited:
                    visited.add(new_belief_state_frozen)
                    new_actions = actions_taken + [action]
                    queue.append((new_belief_state, new_actions, new_actual_state))

        # Nếu không tìm thấy giải pháp trong max_steps, trả về None
        return None

    def solve_with_backtracking(self, max_depth=50):
        """Solve the sliding puzzle using recursive backtracking from an all-zero state."""
        if not self.is_valid_state(self.start_state) or not self.is_valid_state(self.goal_state):
            return None

        # Validate start_state is all zeros
        if self.start_state != [0, 0, 0, 0, 0, 0, 0, 0, 0]:
            print("Warning: Expected start_state to be all zeros")
            return None

        # Initialize metrics
        self.visited_count = 0
        self.max_memory = 0

        # Initialize state and storage for all states
        state = [0] * 9  # Start with all zeros
        all_states = []

        def is_consistent(state, position, value):
            """Check if assigning 'value' at 'position' is consistent (unique in state)."""
            count = state.count(value)
            if position < len(state) and state[position] == value:
                count -= 1
            return count == 0

        def is_complete(state):
            """Check if state is complete and matches goal_state."""
            return state == self.goal_state and self.is_valid_state(state)

        def recursive_backtracking(state, depth, position=0):
            """Recursive backtracking to assign values to cells."""
            if depth >= max_depth:
                return False

            if is_complete(state):
                all_states.append(state[:])
                self.visited_count += 1
                self.max_memory = max(self.max_memory, len(all_states))
                return True

            if position >= 9:
                return False

            values = list(range(9))  # Values from 0 to 8
            random.shuffle(values)
            for value in values:
                if is_consistent(state, position, value):
                    old_value = state[position]
                    state[position] = value
                    all_states.append(state[:])
                    self.visited_count += 1
                    self.max_memory = max(self.max_memory, len(all_states))

                    if recursive_backtracking(state[:], depth + 1, position + 1):
                        return True

                    state[position] = old_value
                    all_states.append(state[:])
                    self.visited_count += 1

            return False

        # Start backtracking with consistent randomization
        random.seed(0)
        success = recursive_backtracking(state, 0)

        return all_states if success and all_states else None

    def reset_metrics(self):
        """Reset metrics for tracking visited states and memory usage."""
        self.visited_count = 0
        self.max_memory = 0

    def calculate_constraints(self):
        """Calculate the order of positions to assign values, prioritizing center."""
        # Order positions to assign values, starting with center (1,1), then others, excluding (2,2)
        order = [(1, 1)]  # Start with center
        for row in range(3):
            for col in range(3):
                if (row, col) != (1, 1) and (row, col) != (2, 2):
                    order.append((row, col))
        return order

    def check_constraints(self, state, row, col, value):
        """Check if assigning 'value' at (row, col) is consistent (unique in state)."""
        # Check if value is already present in the state
        for i in range(3):
            for j in range(3):
                if state[i][j] is not None and state[i][j] == value:
                    return False
        return True

    def solve_with_generate_and_test(self, max_depth=50):
        """Solve the sliding puzzle using generate-and-test with backtracking from an all-zero state."""
        if not self.is_valid_state(self.start_state) or not self.is_valid_state(self.goal_state):
            return None

        # Validate start_state is all zeros
        if self.start_state != [0, 0, 0, 0, 0, 0, 0, 0, 0]:
            print("Warning: Expected start_state to be all zeros for generate-and-test")
            return None

        # Initialize metrics
        self.reset_metrics()

        # Initialize state as 2D list
        state = [[None for _ in range(3)] for _ in range(3)]
        all_states = []
        state_count = [0]

        # Calculate order of positions and other positions
        order = self.calculate_constraints()
        other_positions = [pos for pos in order if pos != (1, 1) and pos != (2, 2)]
        center_values = random.sample(range(1, 9), 8)  # Values for center (1,1)

        def is_complete(state):
            """Check if state is complete and matches goal_state."""
            # Convert 2D state to 1D
            flat_state = []
            for i in range(3):
                for j in range(3):
                    flat_state.append(0 if state[i][j] is None else state[i][j])
            return flat_state == self.goal_state and self.is_valid_state(flat_state)

        def backtrack(index, depth=0):
            """Backtrack to assign values to cells."""
            if depth >= max_depth:
                return False

            # Convert current 2D state to 1D for storage
            flat_state = []
            for i in range(3):
                for j in range(3):
                    flat_state.append(0 if state[i][j] is None else state[i][j])
            all_states.append(flat_state)
            state_count[0] += 1
            self.visited_count += 1
            self.max_memory = max(self.max_memory, state_count[0])

            if index == len(other_positions) + 1:
                state[2][2] = 0  # Assign 0 to (2,2) as empty tile
                flat_state = []
                for i in range(3):
                    for j in range(3):
                        flat_state.append(0 if state[i][j] is None else state[i][j])
                all_states.append(flat_state)
                state_count[0] += 1
                self.visited_count += 1
                if is_complete(state):
                    return True
                state[2][2] = None
                return False

            if index == 0:
                row, col = (1, 1)  # Start with center
                values = center_values
            else:
                row, col = other_positions[index - 1]
                # Available values are those not yet used
                used_values = [state[i][j] for i in range(3) for j in range(3) if state[i][j] is not None]
                values = [v for v in range(1, 9) if v not in used_values]

            for value in values:
                if self.check_constraints(state, row, col, value):
                    state[row][col] = value
                    if backtrack(index + 1, depth + 1):
                        return True
                    state[row][col] = None

            return False

        # Start backtracking with consistent randomization
        random.seed(0)
        success = backtrack(0)

        return all_states if success and all_states else None

    def solve_with_ac3(self, max_depth=50):
        """Solve the sliding puzzle using AC-3 for arc consistency followed by backtracking."""
        if not self.is_valid_state(self.start_state) or not self.is_valid_state(self.goal_state):
            return None

        # Validate start_state is all zeros for backtracking
        if self.start_state != [0, 0, 0, 0, 0, 0, 0, 0, 0]:
            print("Warning: Expected start_state to be all zeros for AC-3 and backtracking")
            return None

        # Initialize metrics
        self.visited_count = 0
        self.max_memory = 0

        # Initialize state as 2D array
        state = np.zeros((3, 3), dtype=int)
        DOMAIN = list(range(9))  # Values from 0 to 8 (0 represents empty tile)
        all_states = []

        def is_consistent(state, row, col, value):
            """Check if assigning 'value' at (row, col) is consistent (unique in state)."""
            flat_state = state.flatten()
            count = list(flat_state).count(value)
            return count == 0

        def is_complete(state):
            """Check if state is complete and matches goal_state."""
            flat_state = state.flatten().tolist()
            return flat_state == self.goal_state and self.is_valid_state(flat_state)

        def find_unassigned(state):
            """Find the next unassigned cell (row, col)."""
            for row in range(3):
                for col in range(3):
                    if state[row, col] == 0:
                        return row, col
            return None, None

        def revise(domains, xi, xj):
            """Revise domains[xi] based on domains[xj] to enforce arc consistency."""
            revised = False
            xi_row, xi_col = divmod(xi, 3)
            xj_row, xj_col = divmod(xj, 3)
            for x in domains[xi][:]:
                # Check if there exists a value y in domains[xj] that satisfies the constraint
                # Constraint: xi and xj must have different values
                conflict = all(x == y for y in domains[xj])
                if conflict:
                    domains[xi].remove(x)
                    revised = True
            return revised

        def ac3_algorithm(domains, variables, neighbors):
            """Run AC-3 to enforce arc consistency."""
            queue = deque((xi, xj) for xi in variables for xj in neighbors[xi])
            while queue:
                xi, xj = queue.popleft()
                if revise(domains, xi, xj):
                    if not domains[xi]:
                        return False
                    for xk in neighbors[xi]:
                        if xk != xj:
                            queue.append((xk, xi))
            return True

        def backtracking_with_ac3(state, domains, all_states, depth=0):
            """Backtracking with AC-3 preprocessed domains."""
            if depth >= max_depth:
                return False

            if is_complete(state):
                all_states.append(state.flatten().tolist())
                self.visited_count += 1
                self.max_memory = max(self.max_memory, len(all_states))
                return True

            row, col = find_unassigned(state)
            if row is None:
                return False

            # Convert (row, col) to variable index
            xi = row * 3 + col
            values = domains[xi].copy()
            np.random.shuffle(values)

            for value in values:
                if is_consistent(state, row, col, value):
                    old_value = state[row, col]
                    state[row, col] = value
                    all_states.append(state.flatten().tolist())
                    self.visited_count += 1
                    self.max_memory = max(self.max_memory, len(all_states))

                    # Create a copy of domains to restore after recursion
                    domains_copy = {k: v.copy() for k, v in domains.items()}
                    if backtracking_with_ac3(state.copy(), domains_copy, all_states, depth + 1):
                        return True

                    state[row, col] = old_value
                    all_states.append(state.flatten().tolist())
                    self.visited_count += 1

            return False

        # Initialize variables and neighbors for AC-3
        variables = list(range(9))  # Variables are cell indices 0 to 8
        neighbors = {i: [] for i in range(9)}
        for i in range(9):
            for j in range(9):
                if i != j:
                    neighbors[i].append(j)  # All pairs of distinct cells have a uniqueness constraint

        # Initialize domains
        domains = {i: DOMAIN.copy() for i in range(9)}

        # Run AC-3 to enforce arc consistency
        np.random.seed(0)
        ac3_result = ac3_algorithm(domains, variables, neighbors)
        if not ac3_result:
            return None  # No solution possible

        # Run backtracking with AC-3 preprocessed domains
        success = backtracking_with_ac3(state, domains, all_states)

        return all_states if success and all_states else None

    def save_q_table(self, Q, filename="q_table.pkl"):
        with open(filename, 'wb') as f:
            pickle.dump(Q, f)

    def load_q_table(self, filename="q_table.pkl"):
        try:
            with open(filename, 'rb') as f:
                return pickle.load(f)
        except FileNotFoundError:
            return defaultdict(lambda: {action: 0 for action in ["up", "down", "left", "right"]})

    def train_q_learning(self, env, episodes=50000, alpha=0.1, gamma=0.9, epsilon_start=1.0, epsilon_end=0.1, epsilon_decay=0.995, max_steps=100, q_table_file="q_table.pkl"):
        Q = self.load_q_table(q_table_file)
        actions = ["up", "down", "left", "right"]

        epsilon = epsilon_start
        for episode in range(episodes):
            state = env.reset(random_state=True)
            step = 0

            while step < max_steps:
                state_tuple = tuple(state)
                if state_tuple not in Q:
                    Q[state_tuple] = {action: 0 for action in actions}

                if random.random() < epsilon:
                    action = random.choice(actions)
                else:
                    action = max(Q[state_tuple], key=Q[state_tuple].get)

                new_state, reward, done = env.step(action)
                new_state_tuple = tuple(new_state)
                if new_state_tuple not in Q:
                    Q[new_state_tuple] = {action: 0 for action in actions}

                old_q = Q[state_tuple][action]
                future_q = max(Q[new_state_tuple].values())
                Q[state_tuple][action] = (1 - alpha) * old_q + alpha * (reward + gamma * future_q)

                state = new_state
                step += 1

                if done:
                    break

            epsilon = max(epsilon_end, epsilon * epsilon_decay)

        self.save_q_table(Q, q_table_file)
        return Q

    def solve_with_trained_q(self, Q, max_steps=100):
        best_path = [self.start_state]
        best_distance = self.manhattan_distance(self.start_state, self.goal_state)

        current_state = list(self.start_state)
        path = [current_state]
        visited = {tuple(current_state)}
        step = 0
        actions = ["up", "down", "left", "right"]

        while step < max_steps:
            state_tuple = tuple(current_state)
            if state_tuple not in Q:
                break
            action = max(Q[state_tuple], key=Q[state_tuple].get)
            next_states = self.get_neighbors(current_state)
            valid_action = False
            for next_state in next_states:
                if self.get_action_from_state(current_state, next_state) == action:
                    valid_action = True
                    new_state = next_state
                    break

            if not valid_action:
                break

            current_distance = self.manhattan_distance(new_state, self.goal_state)
            if current_distance < best_distance:
                best_distance = current_distance
                best_path = path + [new_state]

            current_state = new_state
            if tuple(current_state) in visited:
                break
            visited.add(tuple(current_state))
            path.append(current_state)
            step += 1

            if current_state == self.goal_state:
                return path

        return best_path

    def solve_with_q_learning(self, episodes=50000, alpha=0.1, gamma=0.9, epsilon_start=1.0, epsilon_end=0.1, epsilon_decay=0.995, max_steps=100):
        if not self.is_valid_state(self.start_state) or not self.is_valid_state(self.goal_state):
            return None

        # Thử tải Q-table đã huấn luyện
        Q = self.load_q_table("q_table.pkl")
        if Q and any(Q.values()):  # Kiểm tra xem Q-table có dữ liệu không
            print("Using pre-trained Q-table")
            return self.solve_with_trained_q(Q, max_steps)
        else:
            print("No pre-trained Q-table found or Q-table is empty, training new one")
            env = SlidingPuzzleEnv(self.goal_state)
            Q = self.train_q_learning(env, episodes, alpha, gamma, epsilon_start, epsilon_end, epsilon_decay, max_steps)
            return self.solve_with_trained_q(Q, max_steps)