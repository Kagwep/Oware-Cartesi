# Oware: Core Mechanics Implementation and Model Training


## 1. Game Board Representation:

The Oware game board consists of 12 pits, arranged in two rows, with six pits per row. Each player controls the six pits on their side of the board, with a mancala (score pit) located at the end of their row.

We can represent the game state using a data structure such as an array or a matrix. Each element in this structure corresponds to a specific pit on the board.

## 2. Game Logic: Sowing and Capturing

Oware is a turn-based strategy game with the following core mechanics:

### Sowing:

- A player chooses one of their pits with seeds.
- Starting from this pit, seeds are distributed counterclockwise, one by one, into subsequent pits, including the player's own pits and the opponent's pits but not the opponent's mancala.
- The sowing ends when the last seed is placed or when it reaches the player's mancala. 

### Capturing:

- If the last seed sown lands in an empty pit on the player's side and the opponent's pit opposite to it contains seeds 2 or 3, both the last sown seed and the seeds in the opponent's pit are captured and placed into the player's mancala.
- If the last seed sown lands in the player's mancala, they get an additional turn.

## 3. Game Termination and Winning:

The game ends when one player has more than 24 seeds. 

## Game Logic

### Houses Class

#### Description:
- This class represents the houses in the Oware game.
- Each house contains a number of seeds.

#### Attributes:
- `houses_dictionary`: A dictionary containing information about each house, including the seeds it holds and the number of seeds.
- `houses_order`: A list specifying the order of the houses.

#### Methods:
1. `get_houses()`: 
    - Returns the dictionary containing information about each house.

2. `print_houses()`: 
    - Prints the information of all houses in two rows, representing both players' sides.
    - Each house is represented by its name and the number of seeds it holds, highlighted in magenta.

### Player Class

#### Description:
- This class represents a player in the Oware game.
- Each player has a name, houses they control, and captured seeds.

#### Constructor:
- `__init__(name, houses, captured)`: Initializes a Player object with the provided name, houses, and captured seeds.

#### Methods:
1. `player_info()`: 
    - Returns a dictionary containing information about the player, including their name, houses, and captured seeds.
    
2. `get_captured()`: 
    - Returns the number of seeds the player has captured.

### Play Class

#### Description:
- This class represents the play state in the Oware game.
- It extends both the State and Player classes.

#### Constructor:
- `__init__(turn, houses, game_state)`: Initializes a Play object with the provided turn, houses, and game state.

#### Attributes:
- `turn`: The current turn in the game.
- `picked_seeds`: A list to store seeds picked during the current turn.
- `houses_dict`: A dictionary containing information about each house.
- `houses`: An instance of the Houses class containing information about houses.
- `houses_order`: The order of houses in the game.
- `game_state`: The current state of the game.
- `players_turn`: The player whose turn it is.

#### Methods:
1. `scan_opponent_houses(opponent, house_captured)`: 
    - **Description:** Finds whether the opponent is left with seeds after making a move.
    - **Parameters:** `opponent` (Player), `house_captured` (str).
    
2. `check_capture_move(last_house, house, opponent)`: 
    - **Description:** Checks if a capture move is possible.
    - **Parameters:** `last_house` (str), `house` (str), `opponent` (Player).
    
3. `capture_previous_house(current_house, player, opponent)`: 
    - **Description:** Captures seeds from the previous house if a capture move is made.
    - **Parameters:** `current_house` (str), `player` (Player), `opponent` (Player).
   
4. `make_move(house_picked, valid_player, valid_pick, player, opponent, game_state)`: 
    - **Description:** Performs a move in the game.
    - **Parameters:** `house_picked` (str), `valid_player` (bool), `valid_pick` (bool), `player` (Player), `opponent` (Player), `game_state` (State).


### State Class

#### Description:
- This class represents the state of the Oware game.

#### Constructor:
- `__init__(inplay, player_one, player_two, player, board_state)`: Initializes a State object with the provided parameters.

#### Attributes:
- `inplay`: Indicates whether the game is currently in play.
- `player_one`: Information about player one.
- `player_two`: Information about player two.
- `players_turn`: The player whose turn it is.
- `board_state`: The current state of the game board.
- `winner`: The winner of the game (empty string if the game is ongoing).
- `draw`: Indicates if the game ended in a draw.

#### Methods:
1. `get_player_one_info()`: 
    - Returns information about player one.
    
2. `get_player_two_info()`: 
    - Returns information about player two.
    
3. `is_inplay()`: 
    - Returns whether the game is currently in play.
    
4. `state_info()`: 
    - Returns a dictionary containing information about the game state.
    
5. `get_player_turn()`: 
    - Returns the player whose turn it is.

### OwareMoves Class

#### Description:
- This class handles Oware game moves and related functionalities.

#### Constructor:
- `__init__()`:
    - Initializes an OwareMoves object.

#### Attributes:
- `board_numpy_status`: Status of the Oware game board represented as a NumPy array.
- `player_turn`: The player whose turn it is.
- `legal_moves_dict`: A dictionary to store legal moves and their corresponding board states.

#### Methods:
1. `check_for_capture(seeds, in_player_houses)`:
    - Checks if a capture move is possible.
    - Parameters: `seeds` (int), `in_player_houses` (bool).

2. `check_previous(original_path, next_house_to_sow)`:
    - Checks the previous houses for possible captures.
    - Parameters: `original_path` (list), `next_house_to_sow` (str).

3. `is_there_a_capture(original_path, next_house_to_sow)`:
    - Checks if there is a capture move.
    - Parameters: `original_path` (list), `next_house_to_sow` (str).

4. `possible_moves(player_turn, player, original_board)`:
    - Generates possible moves for the current player.
    - Parameters: `player_turn` (str), `player` (Player), `original_board` (list).

5. `legal_moves_generator(game_state, player)`:
    - Generates legal moves based on the current game state.
    - Parameters: `game_state` (State), `player` (Player).

6. `move_selector(model)`:
    - Selects a move based on the provided model.
    - Parameters: `model` (TensorFlow model).

    - Returns: A tuple containing the selected move, new board state, and score.


### Functions Overview - Opponent moves selector

#### 1. `check_next_best_move(legal_moves_dict, player_turn, top_row_seed_numbers, bottom_row_seed_numbers)`

- **Description:** 
    - Checks for the next best move among legal moves.

- **Parameters:** 
    - `legal_moves_dict` (dict): Dictionary containing legal moves and their corresponding board states.
    - `player_turn` (str): The player whose turn it is.
    - `top_row_seed_numbers` (list): Seed numbers in the top row.
    - `bottom_row_seed_numbers` (list): Seed numbers in the bottom row.

#### 2. `capture_move_check(game_state, legal_moves_dict, player_turn, houses_list)`

- **Description:** 
    - Checks for capture moves in the current game state.

- **Parameters:** 
    - `game_state` (State): The current state of the game.
    - `legal_moves_dict` (dict): Dictionary containing legal moves and their corresponding board states.
    - `player_turn` (str): The player whose turn it is.
    - `houses_list` (list): List of houses in the game.

