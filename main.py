"""
Crappy Game
Yash Trivedi
9-23-26
ICS4U
Simple Python grid game where you try to outrun toilets trying to flush you
"""

# IMPORTS

import os
import random
import sys, termios, tty
from collections import deque


# CONSTANTS AND VARIABLES

game = True
enemy_movement = True
score = 0
char = 0

PLAYER = "💩"
WALL = "🧱"
FILLER = " "
DOOR = "🌀"
ENEMY = "🚽"
HOLE = "🕳️"
STAR = "⭐"

IMPORTANT_TILES = [PLAYER, WALL, DOOR, ENEMY, HOLE, STAR]
IMPORTANT_PATHFINDING_TILES = [WALL, DOOR, ENEMY, HOLE, STAR]

MAP_BASE = 50 # RECOMMENDED: 20
MAP_HEIGHT = 50 # RECOMMENDED: 15
OBSTACLE_NUMBER = 8 # RECOMMENDED: 8
ENEMY_NUMBER = 10 # RECOMMENDED: 2
STAR_NUMBER = 69 # RECOMMENDED: 3
#number of doors should always be 2 cuz they have to be linked

# for pathfinding
MOVES = {
    'u' : (0, -1),
    'd' : (0, 1),
    'l' : (-1, 0),
    'r' : (1, 0)
}

# for key presses
KEY_MOVES = {
    'w' : (0, -1),
    's' : (0, 1),
    'a' : (-1, 0),
    'd' : (1, 0)
}



# FUNCTIONS

# Pasted from CodeHS example, arg for .read() can stay as 1 beacuase I'm using WASD
def getch():
    """
    Not entirely sure how this works
    Args: None
    Returns: ch (string)
    """
    # assining the file descriptor integer (0 for input)  
    fd = sys.stdin.fileno()
    # returns a list containing the attributes for the terminal
    old_settings = termios.tcgetattr(fd)
    try:
        # changes the mode of the file to raw
        tty.setraw(sys.stdin.fileno())
        # essentially calls the input(), it is reading in what is input
        ch = sys.stdin.read(1)
    finally:
        # Returns attribute settings to previous
        termios.tcsetattr(fd, termios.TCSADRAIN, old_settings)
        # Return the ord value (keycode.info is helpful)
    return ch

def create_map():
    """
    Creates the 3D list containing the map
    Returns map (list (3D))
    """
    
    map = []
    for y in range(MAP_HEIGHT):
        map.append([])
        for x in range(MAP_BASE):
            if y == 0 or y == MAP_HEIGHT - 1 or x == 0 or x == MAP_BASE - 1:
                map[y].append(WALL)
            else:
                map[y].append(FILLER)
            
    return map
    
def create_player(map):
    """
    Creates the player by generating random coordinates and appends them to map
    Args: map (3D list)
    Returns: player's coordinates (tuple)
    """
    x = random.randint(1, MAP_BASE-2)
    y = random.randint(1, MAP_HEIGHT-2)
    replace_e(x, y, PLAYER, map)
    return (x, y)
    
# def create_obstacles(map):
#     """
#     Creates 8 obstacles by initializing i to 0, then generating random (non-overlapping) coodinates to append to map. Number is dependant on a constant.
#     Args: map (3D list)
#     Returns: Nothing (None)
#     """
#     i = 0
#     while i < OBSTACLE_NUMBER:
#         x = random.randint(1, MAP_BASE-2)
#         y = random.randint(1, MAP_HEIGHT-2)
        
#         if map[y][x] not in IMPORTANT_TILES:
#             replace_e(x, y, WALL, map)
#             i += 1
            

def replace_e(x, y, new_char, map):
    """
    Replaces an element of the map with coordinates
    Args: x, y: int (the coordinates), new_char: str (what will be appended), map list (3D, what is being mutated)
    Returns: None
    """
    map[y].pop(x)
    map[y].insert(x, new_char)
            
def render(map=[]):
    """
    Prints out the map iteratively
    Args: map (list) (to print)
    """
    for row in map:
        string = ""
        for e in row:
            string += str(e) + " "
        print(string.strip())
        
# def create_enemy(map):
#     """
#     Creates two enemy characters with random non-overlapping coordinates, appends them to list and keeps track of their coordinates in a list
#     Args: map (list) (3D)
#     Returns: enemy_coords (list containing the enemies coordinates (tuples))
#     """
#     i = 0
#     enemy_coords = []
#     while i < ENEMY_NUMBER:
#         x = random.randint(1, MAP_BASE-2)
#         y = random.randint(1, MAP_HEIGHT-2)
        
#         if map[y][x] not in IMPORTANT_TILES:
#             replace_e(x, y, ENEMY, map)
#             i += 1
#             enemy_coords.append((x, y))
            
#     return enemy_coords
    
# def create_star(map):
#     """
#     Creates stars
#     Args: map (list)
#     Returns: Star coordinates (tuple)
#     """
#     star_coords = []
#     i=0
#     while i < STAR_NUMBER:
#         x = random.randint(1, MAP_BASE-2)
#         y = random.randint(1, MAP_HEIGHT-2)
#         if map[y][x] == FILLER:
#             replace_e(x, y, STAR, map)
#             star_coords.append((x, y))
#             i+= 1
            
#     return star_coords
    
# def create_door(map):
#     """
#     Creates doors on map using same method as create enemies
#     Args: map (list)
#     Returns: door_coords (list containing two tuples)
#     """
    
#     door_coords = [] # This was accident but cool I didn't knwo you could unpack a list
#     i=0
#     while i < 2:
        
#         x = random.randint(1, 18)
#         y = random.randint(1, 13)
            
#         if map[y][x] == FILLER:
#             door_coords.append((x, y))
#             replace_e(x, y, DOOR, map)
#             i+=1
        
        
            
            
#     return door_coords
    
# def create_hole(map):
#     """
#     Creates hole that allows player to advance to next level
#     Args: map (list)
#     Returns: player_coords (tuple)
#     """
#     x, y = (0, 0)
#     while map[y][x] != FILLER:
#         x = random.randint(1, MAP_BASE-2)
#         y = random.randint(1, MAP_HEIGHT-2)
        
#     replace_e(x, y, HOLE, map)
#     return (x, y)


def create_elements(map):
    """
    Creates elements for the map like enemies, obstacles, stars, doors, and holes. The number of enemies, obstacles, and stars are dependant on constants.
    Args: map:list (2D)
    Returns: enemy_coords, star_coords, door_coords, hole_coords (all tuples)
    """

    i = 0
    enemy_coords = []
    while i < ENEMY_NUMBER:
        x = random.randint(1, MAP_BASE-2)
        y = random.randint(1, MAP_HEIGHT-2)
        
        if map[y][x] not in IMPORTANT_TILES:
            replace_e(x, y, ENEMY, map)
            i += 1
            enemy_coords.append((x, y))

    i = 0
    while i < OBSTACLE_NUMBER:
        x = random.randint(1, MAP_BASE-2)
        y = random.randint(1, MAP_HEIGHT-2)
        
        if map[y][x] not in IMPORTANT_TILES:
            replace_e(x, y, WALL, map)
            i += 1

    star_coords = []
    i=0
    while i < STAR_NUMBER:
        x = random.randint(1, MAP_BASE-2)
        y = random.randint(1, MAP_HEIGHT-2)
        if map[y][x] == FILLER:
            replace_e(x, y, STAR, map)
            star_coords.append((x, y))
            i+= 1

    door_coords = [] # This was accident but cool I didn't knwo you could unpack a list
    i=0
    while i < 2:
        
        x = random.randint(1, 18)
        y = random.randint(1, 13)
            
        if map[y][x] == FILLER:
            door_coords.append((x, y))
            replace_e(x, y, DOOR, map)
            i+=1

    x, y = (0, 0)
    while map[y][x] != FILLER:
        x = random.randint(1, MAP_BASE-2)
        y = random.randint(1, MAP_HEIGHT-2)
        
    replace_e(x, y, HOLE, map)
    hole_coords = (x, y)

    return enemy_coords, star_coords, door_coords, hole_coords

    
        
def move_player(player_coords, dx, dy, map):
    player_x, player_y = player_coords
    
    if map[player_y+dy][player_x+dx] != WALL:
        replace_e(player_x, player_y, FILLER, map)
        player_x += dx
        player_y += dy
        replace_e(player_x, player_y, PLAYER, map)
        
    player_coords = (player_x, player_y)
    return player_coords
      

  
    
def valid(new_coords, map):
    """
    For pathfinding algorithm, checks if path (passed coords) go over any tiles it shouldn't
    Args: new_coords (tuple), map (list)
    Returns: result (boolean)
    """

    x, y = new_coords
    if map[y][x] not in IMPORTANT_PATHFINDING_TILES:
        result = True
    else:
        result = False
    
    return result

def flushed(score):
    """
    If you lost, what gets printed
    Args: score
    Returns: None
    """
    print("You got flushed by the toilet, you lose!")
    print(f'Your score was: {score}')

def generate_new_map():
    """
    Generates new level/map
    Args: None
    Returns: map (list), player_coords (tuple), enemy_coords (list), hole_coords (tuple), door_coords (list containing tuples)
    """
    
    # Uses BFS

    visited = {(0, 0)} # Just to initialize
   
    # Checking whether or not the path is valid (if the walls block anything off)   
    while len(visited) != MAP_BASE * MAP_HEIGHT - MAP_BASE*2 - (MAP_HEIGHT-2)*2 - OBSTACLE_NUMBER: 
        
        map = create_map()
        player_coords = create_player(map)
        # create_obstacles(map)
        # enemy_coords = create_enemy(map)
        # hole_coords = create_hole(map)
        # door_coords = create_door(map)
        # star_coords = create_star(map)

        enemy_coords, star_coords, door_coords, hole_coords = create_elements(map)

        # print(enemy_coords)
        
        
        visited = {player_coords}
        q = deque() # Initializes queue
        q.append((player_coords))
        
                    
        while q:
            curr_coords = q.popleft()
            
            for m in ['u', 'd', 'l', 'r']: # m for move, up, right, left, down
                x, y = curr_coords
                dx, dy = MOVES[m] # Unpacks the tuple corresponding to the path direction
                new_x = x+dx
                new_y = y+dy
                # Interprets new coordinates based on position and MOVES dictionary
                if map[new_y][new_x] != WALL and (new_x, new_y) not in visited:
                    visited.add((new_x, new_y))
                    q.append((new_x, new_y))
                    
    render(map) # Prints map


    return map, player_coords, enemy_coords, hole_coords, door_coords, star_coords
    

def play(game, score):
    """
    Main function
    Args: game:boolean, score:int
    Returns: None
    """
    
    # Just a welcome message
    print("Use WASD to move, the toilets will follow and flush you, the doors link to each other, collect stars to up your score, and get to the holes for the next level, get the highest score possible!")
    
    # Initializes map
    map, player_coords, enemy_coords, hole_coords, door_coords, star_coords  = generate_new_map()
    
    while game:
    
        print(f'Score: {score}')
    
        key = getch() # For finding what player pressed
    
        if key in ['w', 'a', 's', 'd']:
            dx, dy = KEY_MOVES[key]
            player_coords = move_player(player_coords, dx, dy, map)
            
    
            # # Logic for moving player between doors based on the door coordinates
            # for idx, door in enumerate(door_coords):
            #     if player_coords == door:
            #         door_x, door_y = door_coords[(-idx + 1)]
            #         x, y = player_coords
            #         replace_e(door_x, door_y, PLAYER, map)
            #         replace_e(x, y, DOOR, map)
            #         player_coords = (door_x, door_y)
            #         break
            #     else:
            #         x, y = door
            #         replace_e(x, y, DOOR, map)
    
            
            if player_coords in door_coords:
                door_x, door_y = door_coords[door_coords.index(player_coords) - 1]
                x, y = player_coords
                replace_e(door_x, door_y, PLAYER, map)
                replace_e(x, y, DOOR, map)
                player_coords = (door_x, door_y)
            else:
                for door in door_coords:
                    x, y = door
                    if map[y][x] != DOOR:
                        replace_e(x, y, DOOR, map)
                    
                    
            # If player finds hole
            if player_coords == hole_coords:
                score += 1
                
                os.system('clear')
                map, player_coords, enemy_coords, hole_coords, door_coords, star_coords = generate_new_map()
                continue
    
        
            elif player_coords in enemy_coords: # If you're touching toilet (you get flushed)
    
                flushed(score)
                game = False
                # is_lost = True
                break
            
            elif player_coords in star_coords:
                star_coords.remove(player_coords)
                score+=1
            
            # BFS pathfinding algorithm for enemies to follow player
                    
            enemy_iteration = 0 # Which enemy we're on [0, or 1]
            
            for e in enemy_coords: # Repeats for however many enemies
                
                enemy_x, enemy_y = e
                
                q = deque() # FIFO queue
                visited = {(enemy_x, enemy_y)} # Whats visited and put in queue are the coordinates
                q.append(("", (enemy_x, enemy_y))) # Queue holds the coordinates but the path taken as well
                
                while q:
                    
                    curr_path, curr_coords = q.popleft() # Get the path and coordinates from queue
                    
                    if curr_coords == player_coords:
                        break # cuz that means we found the path, now just refer to curr_path[0] for first move
                    
                    for m in ['u', 'd', 'l', 'r']: # For each possible movement from that position
                        new_path = curr_path + m
                        dx, dy = MOVES[m]
                        new_coords = (curr_coords[0] + dx, curr_coords[1] + dy) # Adds the prev. coords and the movement tuple
                        
                        if valid(new_coords, map) and new_coords not in visited: # Checks if it doesn't run into walls or anything
                            visited.add(new_coords) # Then it adds to visited and queue
                            q.append((new_path, new_coords))
                            
                dx, dy = MOVES[curr_path[0]] # First move of the pathfinding, where enemies should move
                
                replace_e(enemy_x, enemy_y, FILLER, map)
    
                enemy_x += dx
                enemy_y += dy
    
                # Putting the updated coords back into the enemy_coords list
                enemy_coords.pop(enemy_iteration)
                enemy_coords.insert(enemy_iteration, (enemy_x, enemy_y))
    
                replace_e(enemy_x, enemy_y, ENEMY, map)
    
                # Moves onto next enemy
                enemy_iteration += 1
    
                
            
            os.system('clear') # Clears screen
    
            render(map) # Renders map
            # print(f'PLAYER: {player_coords}, ENEMY: {enemy_coords}')
    
            if player_coords in enemy_coords and game: # If you're touching toilet (you get flushed). This is redone if the condition is met after all the enemy movements occur too
                flushed(score)
                game = False
            
            
        elif key == 'q':
            game = False
    
        else:
            print("Invalid option")
            
            
            
# MAIN            
            
play(game, score)
