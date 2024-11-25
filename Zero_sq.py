# from queue import Queue
from collections import deque
import queue
from queue import Queue



class Cell:
    def __init__(self, content):
        self.content = content

    def __repr__(self):
        return self.content


class GridGame:
   
    def __init__(self, grid):
        self.grid = grid   
        self.sec_grid = [row[:] for row in grid] 
        self.player_pos = self.find_player('p')  # Find player 1 (p)
        self.player2_pos = self.find_player('p2')  # Find player 2 (p2)
        self.moves = []  
        self.next_state_list = {}  
        self.moves_history = {}   
        self.next_state_history = {}   
        self.p1_won = False  # Player 1's win flag
        self.p2_won = False  # Player 2's win flag
        self.stack = []
        self.visited_grids = []
        self.father = None
 
  
    @property
    def my_map(self):
        return self.moves_history
    @property
    def nextstate_list(self):
        return self.next_state_list
    

          

        #####################################################################
        #####################################################################
        #########################[ALGorathem]################################
        #####################################################################
        #####################################################################
 


    def bfs_check_visited(self, grid):
        # Convert the grid into a comparable form (tuple of tuples).
        grid_tuple = tuple(tuple(cell.content for cell in row) for row in grid)

        queue = deque(self.moves_history.items())

        while queue:
            key, visited_grid = queue.popleft()

        # Convert the visited grid into tuple form for comparison.
            visited_tuple = tuple(tuple(cell for cell in row) for row in visited_grid)
        
            if grid_tuple == visited_tuple:
                print(f"Grid configuration found in {key}.")
                return True

        print("Grid configuration not found in history.")
        return False
    
    
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

        # Check if the game ends
            if self.is_target((x1, y1), 1, is_test=False):
                print(f"Player 1 reached the target at ({x1}, {y1}).")
                self.update_grid(x1, y1, 1)
                self.p1_won = True
                if self.p2_won:
                    print("Both players have won! Ending game...")
                    self.win_game((x1, y1), 1)
                break

            if self.is_target((x2, y2), 2, is_test=False):
                print(f"Player 2 reached the target at ({x2}, {y2}).")
                self.update_grid(x2, y2, 2)
                self.p2_won = True
                if self.p1_won:
                    print("Both players have won! Ending game...")
                    self.win_game((x2, y2), 2)
                break

        # next states to the queue
            self.next_state()   
            for next_state in self.next_state_list:
                if next_state not in visited:
                    print(f"Adding new state to queue: {next_state}")
                    next_state.previous = current_state   
                    q.put(next_state)
                    visited.append(next_state)   
                else:
                    print(f"State already visited: {next_state}")

        # Construct the path if the target is reached
            if self.p1_won or self.p2_won:
                path = []
                while current_state.previous is not None:
                    path.append(current_state)
                    current_state = current_state.previous
                path.reverse()
                print("Path construction complete.")
                return path

        print("No solution found. Returning empty path.")
        return path   


    def dfs_check_visited(self, grid):
        """
        Performs a DFS-like check to see if the given grid configuration has been visited.
        """
        # Convert the grid into a comparable form (tuple of tuples).
        grid_tuple = tuple(tuple(cell.content for cell in row) for row in grid)

        # Use a stack to iterate over move history for DFS.
        stack = [self.moves_history.items()]  # Use list as stack for DFS

        while stack:
            key, visited_grid = stack.pop()  # DFS - pop from the stack

            # Convert the visited grid into tuple form for comparison.
            visited_tuple = tuple(tuple(cell for cell in row) for row in visited_grid)
        
            if grid_tuple == visited_tuple:
                print(f"Grid configuration found in {key}.")
                return True

        print("Grid configuration not found in history.")
        return False

    #### [DFS] ###

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

            # Check if the game ends
            if self.is_target((x1, y1), 1, is_test=False):
                print(f"Player 1 reached the target at ({x1}, {y1}).")
                self.update_grid(x1, y1, 1)
                self.p1_won = True
                if self.p2_won:
                    print("Both players have won! Ending game...")
                    self.win_game((x1, y1), 1)
                break

            if self.is_target((x2, y2), 2, is_test=False):
                print(f"Player 2 reached the target at ({x2}, {y2}).")
                self.update_grid(x2, y2, 2)
                self.p2_won = True
                if self.p1_won:
                    print("Both players have won! Ending game...")
                    self.win_game((x2, y2), 2)
                break

        # Add next states to the stack
            self.next_state()
            for next_state in self.next_state_list:
                if next_state not in visited:
                    print(f"Adding new state to stack: {next_state}")
                    next_state.previous = current_state
                    stack.append(next_state)   
                    visited.append(next_state)  
                else:
                    print(f"State already visited: {next_state}")

             
            if self.p1_won or self.p2_won:
                path = []
                while current_state.previous is not None:
                    path.append(current_state)
                    current_state = current_state.previous
                path.reverse()   
                print("Path construction complete.")
                return path

        print("No solution found. Returning empty path.")
        return path



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

    # Checking

        if self.is_target((x1, y1), 1, is_test=False):
            print(f"Player 1 reached the target at ({x1}, {y1}).")
            self.update_grid(x1, y1, 1)
            self.p1_won = True
            if self.p2_won:
                print("Both players have won! Ending game...")
                self.win_game((x1, y1), 1)
            return path + [current_state]

        if self.is_target((x2, y2), 2, is_test=False):
            print(f"Player 2 reached the target at ({x2}, {y2}).")
            self.update_grid(x2, y2, 2)
            self.p2_won = True
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
                result_path = self.DFS(next_state, visited, path)
                if result_path:  
                    return result_path
            else:
                print(f"State already visited: {next_state}")

        print(f"Backtracking from state: {current_state}")
        path.pop()
        return []


        #####################################################################
        #####################################################################
        #####################################################################
        #####################################################################
        #####################################################################


    def find_player(self, player_char):
        for i, row in enumerate(self.grid):
            for j, cell in enumerate(row):
                if cell.content == player_char:
                    return (i, j)   
        return None   

    def display_grid_from_state(self, grid):
        print("Grid from state by index")
        for row in grid:
            print(" ".join(str(cell) for cell in row))   
        print()

    def display_all_grids(self, grid_map):
        print("YOUr MOVEs HISTORy")
        for key, value in grid_map.items():
            self.display_grid_noCommn(value, '')  # Call the display method with the value
        print()  # Add a newline for better readability



    def display_nextstate_list(self):
        print("Next state by index")
        for key, value in self.next_state_list.items():
            self.display_grid_noCommn(value , 'next state item')  # Call the display method with the value
        print()  # Add a newline for better readability


    def take_index_of_state_to_print(self, index):
        key = f"move number {index}"
        grid_state = self.moves_history.get(key)
        if grid_state:
            self.display_grid_from_state(grid_state)
        else:
            print("Index out of range. Available indices:", list(self.moves_history.keys()))

    def display_grid(self):
        print("Current Grid:")
        for row in self.grid:
            print(" ".join(str(cell) for cell in row))   
        print()
    
    def display_griddddddddd(self, passgrid):
        print("P:M")
        # self.add_grid_to_nextstate_list(passgrid)
        for row in passgrid:
            print(" ".join(str(cell) for cell in row))   
        print()

    def display_sec_grid(self):
        print("seccccccccccccc Grid:")
        for row in self.sec_grid:
            print(" ".join(str(cell) for cell in row))   
        print()        

    def display_grid_noCommn(self, grid , dis):
        print(dis)
        for row in grid:
            print(" ".join(str(cell) for cell in row))   
        print()

    def next_state(self):
        self.potential_moves('w' , 's' , False)
        self.potential_moves('s' , 'w' , False)
        self.potential_moves('a' , 'd' , False)
        self.potential_moves('d' , 'a' , False)
        # self.display_nextstate_list()


   

    def potential_moves(self, direction , charback , isback):
    # Get current positions of both players
        # self.display_sec_grid()
        x1, y1 = self.player_pos   
        x2, y2 = self.player2_pos
        old_x1, old_y1 = self.player_pos   
        old_x2, old_y2 = self.player2_pos    

        moved_player1 = False   
        moved_player2 = False  





        direction_map = {
            'w': (-1, 0),   
            's': (1, 0),    
            'a': (0, -1),   
            'd': (0, 1)       
        }




        if direction in direction_map:   
            dx, dy = direction_map[direction]   

        # Move player 1 continuously while the move is valid and they haven't won
            while not self.p1_won and self.is_valid_move_for_player1((x1 + dx, y1 + dy)):
                x1 += dx   
                y1 += dy   
                moved_player1 = True   
                if self.is_target((x1, y1), 1 , is_test=True):
                    self.update_grid(x1, y1, 1)
                    # self.p1_won = True 
                    # if self.p2_won:
                        # self.win_game((x1, y1), 1)
                

                    return self.get_state()  

        # Move player 2 continuously while the move is valid and they haven't won
            while not self.p2_won and self.is_valid_move_for_player2((x2 + dx, y2 + dy)):
                x2 += dx   
                y2 += dy   
                moved_player2 = True   
                if self.is_target((x2, y2), 2 , is_test=True):
                    self.update_grid(x2, y2, 2)
                    # self.p2_won = True 
                    # if self.p1_won:
                        # self.win_game((x2, y2), 2)
                    # return self.get_state()  # Return the state after winning

            # Only update grid if either player moved
            if moved_player1 or moved_player2:
                self.update_grid(x2, y2, 2)
                self.update_grid(x1, y1, 1)
                self.add_grid_to_nextstate_list(self.grid)  # Store the grid state after a valid move
                self.update_grid(old_x2, old_y2, 2)
                self.update_grid(old_x1, old_y1, 1)
                # self.potential_moves(charback , '' , False)
                # if not isback:
                # print(f"list of potntial moves for 1 th move")

                # print(charback)
                
                self.next_state_list
            # self.next_state_list.clear()
            return self.get_state()  # Return the state after a valid move
        else:
            print("Invalid direction! Use 'w', 'a', 's', 'd'.")
            return None   



    def move_players(self, direction):
    # Get current positions of both players
        # self.next_state()
        # self.display_sec_grid()
        x1, y1 = self.player_pos   
        x2, y2 = self.player2_pos   
        moved_player1 = False   
        moved_player2 = False   

        direction_map = {
            'w': (-1, 0),   
            's': (1, 0),    
            'a': (0, -1),   
            'd': (0, 1)       
        }

        if direction in direction_map:   
            dx, dy = direction_map[direction]   

        # Move player 1 continuously while the move is valid and they haven't won
            while not self.p1_won and self.is_valid_move_for_player1((x1 + dx, y1 + dy)):
                x1 += dx   
                y1 += dy   
                moved_player1 = True   
                if self.is_target((x1, y1), 1  ,is_test=False):
                    self.update_grid(x1, y1, 1)
                    self.p1_won = True 
                    if self.p2_won:
                        self.win_game((x1, y1), 1)   
                    return self.get_state()  

        # Move player 2 continuously while the move is valid and they haven't won
            while not self.p2_won and self.is_valid_move_for_player2((x2 + dx, y2 + dy)):
                x2 += dx   
                y2 += dy   
                moved_player2 = True   
                if self.is_target((x2, y2), 2  ,is_test=False):
                    self.update_grid(x2, y2, 2)
                    self.p2_won = True 
                    if self.p1_won:
                        self.win_game((x2, y2), 2)
                    return self.get_state()  # Return the state after winning

            # Only update grid if either player moved
            if moved_player1 or moved_player2:
                self.update_grid(x2, y2, 2)
                self.update_grid(x1, y1, 1)
                self.dfs_check_visited(self.grid)
                self.add_grid_to_history_map(self.grid)  # Store the grid state after a valid move
            return self.get_state()  # Return the state after a valid move
        else:
            print("Invalid direction! Use 'w', 'a', 's', 'd'.")
            return None   

    def get_state(self):
        return {
            'player1_position': self.player_pos,
            'player2_position': self.player2_pos,
            'grid': self.grid,
            'sec_grid': self.sec_grid,
            'p1_won': self.p1_won,
            'p2_won': self.p2_won
        }



    def update_grid(self, x, y, player_num):
        if player_num == 1:
            self.grid[self.player_pos[0]][self.player_pos[1]].content = '_'
            self.player_pos = (x, y)   
            self.grid[x][y].content = 'p'   
        else:
            self.grid[self.player2_pos[0]][self.player2_pos[1]].content = '_'
            self.player2_pos = (x, y)   
            self.grid[x][y].content = 'p2'   
        
        self.moves.append((player_num, (x, y)))


    def update_sec_grid(self, x, y, player_num):
        if player_num == 1:
            self.sec_grid[self.player_pos[0]][self.player_pos[1]].content = '_'
            self.player_pos = (x, y)   
            self.sec_grid[x][y].content = 'p'   
        else:
            self.sec_grid[self.player2_pos[0]][self.player2_pos[1]].content = '_'
            self.player2_pos = (x, y)   
            self.sec_grid[x][y].content = 'p2'   
        
        self.moves.append((player_num, (x, y))) 

    def is_valid_move_for_player1(self, new_pos):
        x, y = new_pos   
        return (0 <= x < len(self.grid) and 
                0 <= y < len(self.grid[0]) and 
                (self.grid[x][y].content == '_' or self.grid[x][y].content == 't') or self.grid[x][y].content == 't2' )  # Fixed this condition
    
    def is_valid_move_for_player2(self, new_pos):
        x, y = new_pos   
        return (0 <= x < len(self.grid) and 
                0 <= y < len(self.grid[0]) and 
                (self.grid[x][y].content == '_' or self.grid[x][y].content == 't2') or self.grid[x][y].content == 't')  # Fixed this condition

    def is_target(self, pos, player_num , is_test):
        if player_num == 1:
        # Check if player 1 has reached their target
            if self.grid[pos[0]][pos[1]].content == 't' or self.grid[pos[0]][pos[1]].content == 'T':
                if is_test == True:
                # Replace "p" with "_" and "t" with "w1" at the target position
                    self.grid[self.player_pos[0]][self.player_pos[1]].content = '_'  # Clear player 1's previous position
                    self.grid[pos[0]][pos[1]].content = 't'  # Mark the target as reached
                    # return True
                else:
                    self.grid[self.player_pos[0]][self.player_pos[1]].content = '_'  # Clear player 1's previous position
                    self.grid[pos[0]][pos[1]].content = 'w1'  # Mark the target as reached
                    return True
        else:
        # Check if player 2 has reached their target
            if self.grid[pos[0]][pos[1]].content == 't2' or self.grid[pos[0]][pos[1]].content == 'T2':
                if  is_test == True:
            # Replace "p2" with "_" and "t2" with "w2" at the target position
                    self.grid[self.player2_pos[0]][self.player2_pos[1]].content = '_'  # Clear player 2's previous position
                    self.grid[pos[0]][pos[1]].content = 't2'  # Mark the target as reached
                # return True
                else :
                    self.grid[self.player2_pos[0]][self.player2_pos[1]].content = '_'  # Clear player 2's previous position
                    self.grid[pos[0]][pos[1]].content = 'w2'  # Mark the target as reached
                    return True
        return False
   

    def win_game(self, target_pos, player_num):
        x, y = target_pos   
        # if player_num == 1:
        #     self.grid[x][y].content = 'W'  # Mark the target of player 1
        # else:
        #     self.grid[x][y].content = 'W2'  # Mark the target of player 2

        if self.moves:   
            last_move = self.moves[-1]   
            player_num_last, last_pos = last_move
            if player_num_last == 1:
                self.grid[last_pos[0]][last_pos[1]].content = '_'   
            else:
                self.grid[last_pos[0]][last_pos[1]].content = '_'

        if player_num == 1:
            self.grid[x][y].content = 'p'   
        else:
            self.grid[x][y].content = 'p2'   

        print(f"Congratulations! Player {player_num} has reached the target and won the game!")
        self.display_grid()
        print("Thanks for playing!") 
        view_state = input("Would you like to see the matrix state by index? (y/n): ")
        if view_state.lower() == 'y':
                user_input = input("Please enter the Grid index to print it from: ")
                try:
                    index = int(user_input)
                    self.take_index_of_state_to_print(index)
                except ValueError:
                    print("Invalid input. Please enter a valid number.")  
        # self.display_all_grids(self.moves_history)   
    
        exit()  


    def add_grid_to_history_map(self, matrix):
        if isinstance(matrix, list) and all(isinstance(row, list) for row in matrix):
            new_index = len(self.my_map) + 1  # Start indexing from 1
            key = f"move number {new_index}"
            self.my_map[key] = [[cell.content for cell in row] for row in matrix]
            print(f"Grid history updated with {key}.")
        else:
            raise ValueError("The matrix must be a 2D list.")

# 
    def add_grid_to_nextstate_list(self, matrix):
        print('potintial move number')
        print(len(self.next_state_list))    
        if isinstance(matrix, list) and all(isinstance(row, list) for row in matrix):
            new_index = len(self.next_state_list) + 1  # Start indexing from 1
            key = f"{new_index}"
            self.next_state_list[key] = [[cell.content for cell in row] for row in matrix]
            self.display_griddddddddd(matrix)
        else:
            raise ValueError("The matrix must be a 2D list.")
  

    def play(self):
        self.BFS()
        # self.DFS()
        # self.add_grid_to_history_map(self.grid)
        # print('fff')
        # while True: 
        #     print('next state length :')
        #     print(len(self.next_state_list)) 
        #     self.next_state()
        #     self.display_grid()    
        #     move = input("Enter your move (w/a/s/d) for both players or 'quit' to exit: ")
        #     self.next_state_list.clear()
            
        #     if move.lower() == 'quit':
        #         # self.display_all_grids(self.moves_history)   
        #         print("Thanks for playing!")   
        #         break   
            
        #     self.move_players(move)

# Create the grid with two players and two targets
new_cells = [
    [Cell(' '), Cell(' '), Cell('*'), Cell('*'), Cell('*'), Cell('*'), Cell('*'), Cell(' '), Cell(' '), Cell(' '), Cell(' ')],
    [Cell('*'), Cell('*'), Cell('*'), Cell('_'), Cell('_'), Cell('_'), Cell('*'), Cell('*'), Cell('*'), Cell('*'), Cell('*')],
    [Cell('*'), Cell('_'), Cell('*'), Cell('_'), Cell('_'), Cell('t'), Cell('*'), Cell('*'), Cell('*'), Cell('*'), Cell('*')],
    [Cell('*'), Cell('_'), Cell('*'), Cell('_'), Cell('_'), Cell('_'), Cell('_'), Cell('*'), Cell('_'), Cell('_'), Cell('*')],
    [Cell('*'), Cell('_'), Cell('*'), Cell('*'), Cell('_'), Cell('*'), Cell('*'), Cell('*'), Cell('_'), Cell('_'), Cell('*')],
    [Cell('*'), Cell('_'), Cell('_'), Cell('_'), Cell('_'), Cell('_'), Cell('_'), Cell('t2'), Cell('_'), Cell('*'), Cell('*')],
    [Cell('*'), Cell('p2'), Cell('_'), Cell('*'), Cell('_'), Cell('p'), Cell('_'), Cell('_'), Cell('_'), Cell('*'), Cell('_')],
    [Cell('*'), Cell('*'), Cell('*'), Cell('*'), Cell('*'), Cell('*'), Cell('*'), Cell('*'), Cell('*'), Cell('*'), Cell('*')]
]
game = GridGame(new_cells)
game.play()
