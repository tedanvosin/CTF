#!/usr/bin/env python3
from pwn import process, context
import time
context.log_level = 'error'

VALID = []
grid = [['.' for _ in range(31)] for _ in range(31)]

# single-character bytes for convenience
MOVES = [b'R', b'L', b'U', b'D']
ANTI_MOVES = {b'L':b'R', b'U':b'D', b'D':b'U', b'R':b'L'}
SHIFT = {b'L':[-1,0], b'R':[1,0], b'U':[0,-1], b'D':[0,1]}

def move(position, move_byte):
    dx, dy = SHIFT[move_byte]
    return [position[0] + dx, position[1] + dy]

def mark_position(position, symbol):
    grid[position[1]][position[0]] = symbol

def print_grid():
    print("\033c", end="")  # Clear the screen for better visualization
    print("Maze visualization:")
    for row in grid:
        print(''.join(row))
    time.sleep(0.1)  # Add a small delay to make changes visible

def try_path(path, position):
    # Convert position to tuple for hashing
    pos_tuple = tuple(position)
    
    # If we've already visited this position, don't explore it again
    if pos_tuple in visited:
        return False
    
    # Mark position as visited
    visited.add(pos_tuple)
    
    # Test the current path
    p = process('./labyrinth')
    p.sendline(path)
    out = p.recvall(timeout=0.2)
    p.close()
    
    # Mark the current position as valid path
    mark_position(position, 'O')
    print_grid()
    
    # If we reach success, print it
    if b'Success' in out:
        print("Valid path found:", path.decode())
        VALID.append(path)
        return True
    
    # If we have reached the maximum length without success
    if len(path) >= 32:
        return False
    
    # Try each possible move
    valid_extension = False
    for m in MOVES:
        # Don't immediately undo your last move (avoid backtracking)
        if path and m == ANTI_MOVES[path[-1:].upper()]:
            continue
        
        # Calculate the new position
        new_position = move(position, m)
        new_pos_tuple = tuple(new_position)
        
        # Skip if already visited
        if 
        
        # Check bounds (optional, to prevent indexing errors)
        if (new_position[0] < 0 or new_position[0] >= 31 or 
            new_position[1] < 0 or new_position[1] >= 31):
            continue
            
        # Try the new path
        p = process('./labyrinth')
        p.sendline(path + m)
        out = p.recvall(timeout=0.1)
        p.close()
        
        # If valid, continue exploring
        if b'Fail' not in out:
            extended_valid = try_path(path + m, new_position)
            valid_extension = valid_extension or extended_valid
        else:
            # Mark as wall if it leads to failure
            mark_position(new_position, 'X')
            print_grid()  # Print grid when wall is found
    
    # If no valid extension was found, and this isn't the final path, mark this as uncertain
    if not valid_extension and not (b'Success' in out):
        mark_position(position, '.')
        print_grid()  # Print grid when marking as uncertain
        
    return valid_extension

# Start from the center
start_position = [15, 15]
mark_position(start_position, 'S')  # Mark start with 'S'
print_grid()  # Show initial grid with start position

# Try each initial direction
for m in MOVES:
    new_position = move(start_position, m)
    new_pos_tuple = tuple(new_position)
    
    # Skip if already visited
    if grid[new_position[0]][new_position[1]] != '.':
        continue
    
    p = process('./labyrinth')
    p.sendline(m)
    out = p.recvall(timeout=0.1)
    p.close()
    
    if b'Fail' not in out:
        try_path(m, new_position)
    else:
        mark_position(new_position, 'X')
        visited.add(new_pos_tuple)  # Mark as visited
        print_grid()  # Print grid when initial wall is found

# Print the final grid
print("\nFinal maze visualization:")
print_grid()

# Print the valid paths found
print("\nValid paths found:")
for path in VALID:
    print(path.decode())