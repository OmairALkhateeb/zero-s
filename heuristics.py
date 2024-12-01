def heuristic(grid, player_pos, player_num):
    # Original heuristic logic from your provided code
    if player_num == 1:
        target_char = 't'
    else:
        target_char = 't2'

    target_pos = find_target(grid, target_char)
    if not target_pos:
        return float('inf')  # High cost if no target is found

    # Manhattan distance heuristic
    distance = abs(player_pos[0] - target_pos[0]) + abs(player_pos[1] - target_pos[1])

    # Penalty for obstacles or opponent's position
    if grid[target_pos[0]][target_pos[1]].content not in ['_', target_char]:
        distance += 10  # Arbitrary large penalty

    return distance

def find_target(grid, target_char):
    for i, row in enumerate(grid):
        for j, cell in enumerate(row):
            if cell.content == target_char:
                return (i, j)
    return None
