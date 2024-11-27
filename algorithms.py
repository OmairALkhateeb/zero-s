import heapq
from collections import deque
from grid_game import GridGame
from queue import Queue

class GridGameAlgorithms(GridGame):
    def bfs_check_visited(self, grid):
        grid_tuple = tuple(tuple(cell.content for cell in row) for row in grid)
        queue = deque(self.moves_history.items())

        while queue:
            key, visited_grid = queue.popleft()
            visited_tuple = tuple(tuple(cell for cell in row) for row in visited_grid)
            
            if grid_tuple == visited_tuple:
                print(f"Grid configuration found in {key}.")
                return True

        print("Grid configuration not found in history.")
        return False
    
    def dfs_check_visited(self, grid):
        grid_tuple = tuple(tuple(cell.content for cell in row) for row in grid)
        stack = list(self.moves_history.items())

        while stack:
            key, visited_grid = stack.pop()
            visited_tuple = tuple(tuple(cell for cell in row) for row in visited_grid)
            
            if grid_tuple == visited_tuple:
                print(f"Grid configuration found in {key}.")
                return True

        print("Grid configuration not found in history.")
        return False

    def re_DFS(self, current_state=None, visited=None, path=None):
        if visited is None:
            visited = []
        if path is None:
            path = []

        if current_state is None:
            current_state = self.grid
            visited.append(current_state)

        self.display_grid_noCommn(current_state, 'DFS')
        x1, y1 = self.player_pos
        x2, y2 = self.player2_pos

        if self.is_target((x1, y1), 1, is_test=False):
            print(f"Player 1 reached the target at ({x1}, {y1}).")
            self.update_grid(x1, y1, 1)
            if self.p2_won:
                print("Both players have won! Ending game...")
                self.win_game((x1, y1), 1)
            return path + [current_state]

        if self.is_target((x2, y2), 2, is_test=False):
            print(f"Player 2 reached the target at ({x2}, {y2}).")
            self.update_grid(x2, y2, 2)
            if self.p1_won:
                print("Both players have won! Ending game...")
                self.win_game((x2, y2), 2)
            return path + [current_state]

        path.append(current_state)
        self.next_state()

        for next_state in self.next_state_list:
            if next_state not in visited:
                print(f"Exploring new state: {next_state}")
                visited.append(next_state)
                result_path = self.re_DFS(next_state, visited, path)
                if result_path:
                    return result_path
            else:
                print(f"State already visited: {next_state}")

        print(f"Backtracking from state: {current_state}")
        path.pop()
        return []

    def BFS(self):
        q = Queue()
        path = []
        visited = []

        q.put(self.grid)
        visited.append(self.grid)

        while not q.empty():
            current_state = q.get()
            self.display_grid_noCommn(current_state, 'BFS')

            x1, y1 = self.player_pos
            x2, y2 = self.player2_pos

            if self.is_target((x1, y1), 1, is_test=False):
                print(f"Player 1 reached the target at ({x1}, {y1}).")
                self.update_grid(x1, y1, 1)
                break

            if self.is_target((x2, y2), 2, is_test=False):
                print(f"Player 2 reached the target at ({x2}, {y2}).")
                self.update_grid(x2, y2, 2)
                break

            self.next_state()
            for next_state in self.next_state_list:
                if next_state not in visited:
                    print(f"Adding new state to queue: {next_state}")
                    next_state.previous = current_state
                    q.put(next_state)
                    visited.append(next_state)

        if self.p1_won or self.p2_won:
            path = []
            while current_state.previous is not None:
                path.append(current_state)
                current_state = current_state.previous
            path.reverse()
            print("Path construction complete.")
            return path

        print("No solution found. Returning empty path.")
        return []

    def DFS(self):
        stack = []
        path = []
        visited = []

        stack.append(self.grid)
        visited.append(self.grid)

        while stack:
            current_state = stack.pop()
            self.display_grid_noCommn(current_state, 'DFS')

            x1, y1 = self.player_pos
            x2, y2 = self.player2_pos

            if self.is_target((x1, y1), 1, is_test=False):
                print(f"Player 1 reached the target at ({x1}, {y1}).")
                self.update_grid(x1, y1, 1)
                break

            if self.is_target((x2, y2), 2, is_test=False):
                print(f"Player 2 reached the target at ({x2}, {y2}).")
                self.update_grid(x2, y2, 2)
                break

            self.next_state()
            for next_state in self.next_state_list:
                if next_state not in visited:
                    print(f"Adding new state to stack: {next_state}")
                    next_state.previous = current_state
                    stack.append(next_state)
                    visited.append(next_state)

        if self.p1_won or self.p2_won:
            path = []
            while current_state.previous is not None:
                path.append(current_state)
                current_state = current_state.previous
            path.reverse()
            print("Path construction complete.")
            return path

        print("No solution found. Returning empty path.")
        return []



    def ucs(self):
        # Priority queue stores tuples: (cost, current_state, path)
        priority_queue = []
        visited = set()

        # Initial state: cost = 0, path = empty list
        heapq.heappush(priority_queue, (0, self.grid, []))
        
        while priority_queue:
            cost, current_state, path = heapq.heappop(priority_queue)

            # Convert grid state to tuple to check if visited
            state_tuple = self.grid_to_tuple(current_state)
            if state_tuple in visited:
                continue
            
            # Mark current state as visited
            visited.add(state_tuple)
            path = path + [current_state]
            self.display_grid_noCommn(current_state, 'UCS')

            # Check if either player has reached the target
            x1, y1 = self.player_pos
            x2, y2 = self.player2_pos
            
            if self.is_target((x1, y1), 1, is_test=False):
                print(f"Player 1 reached the target at ({x1}, {y1}).")
                self.update_grid(x1, y1, 1)
                return path

            if self.is_target((x2, y2), 2, is_test=False):
                print(f"Player 2 reached the target at ({x2}, {y2}).")
                self.update_grid(x2, y2, 2)
                return path

            # Generate and explore next states with updated costs
            self.next_state()
            for next_state in self.next_state_list:
                next_tuple = self.grid_to_tuple(next_state)
                if next_tuple not in visited:
                    new_cost = cost + self.calculate_move_cost(current_state, next_state)
                    heapq.heappush(priority_queue, (new_cost, next_state, path))

        print("No solution found. Returning empty path.")
        return []

    def grid_to_tuple(self, grid):
        return tuple(tuple(cell.content for cell in row) for row in grid)
    
    def calculate_move_cost(self, current_state, next_state):
        # Define the cost between current_state and next_state (e.g., 1 for simple moves)
        return 1