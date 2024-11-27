from cell import Cell
from grid_game import GridGame
from algorithms import GridGameAlgorithms

def create_grid():
    return [
        [Cell(' '), Cell(' '), Cell('*'), Cell('*'), Cell('*'), Cell('*'), Cell('*'), Cell(' '), Cell(' '), Cell(' '), Cell(' ')],
        [Cell('*'), Cell('*'), Cell('*'), Cell('_'), Cell('_'), Cell('_'), Cell('*'), Cell('*'), Cell('*'), Cell('*'), Cell('*')],
        [Cell('*'), Cell('_'), Cell('*'), Cell('_'), Cell('_'), Cell('t'), Cell('*'), Cell('*'), Cell('*'), Cell('*'), Cell('*')],
        [Cell('*'), Cell('_'), Cell('*'), Cell('_'), Cell('_'), Cell('_'), Cell('_'), Cell('*'), Cell('_'), Cell('_'), Cell('*')],
        [Cell('*'), Cell('_'), Cell('*'), Cell('*'), Cell('_'), Cell('*'), Cell('*'), Cell('*'), Cell('_'), Cell('_'), Cell('*')],
        [Cell('*'), Cell('_'), Cell('_'), Cell('_'), Cell('_'), Cell('_'), Cell('_'), Cell('t2'), Cell('_'), Cell('*'), Cell('*')],
        [Cell('*'), Cell('p2'), Cell('_'), Cell('*'), Cell('_'), Cell('p'), Cell('_'), Cell('_'), Cell('_'), Cell('*'), Cell('_')],
        [Cell('*'), Cell('*'), Cell('*'), Cell('*'), Cell('*'), Cell('*'), Cell('*'), Cell('*'), Cell('*'), Cell('*'), Cell('*')]
    ]

def main():
    grid = create_grid()
    game = GridGameAlgorithms(grid)
    
    print("Initial Grid:")
    game.display_grid()
    
    # Test the Depth-First Search algorithm
    print("\nTesting Depth-First Search (DFS):")
    game.re_DFS() 
 
 

if __name__ == "__main__":
    main()
