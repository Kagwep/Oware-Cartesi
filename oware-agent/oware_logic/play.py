
from state import State
from player import Player

from colorama import init as colorama_init
from colorama import Fore,Back
from colorama import Style

colorama_init()

class Play(State,Player):



    def __init__(self,turn,houses,game_state):
        self.turn = turn
        self.picked_seeds = []
        self.houses_dict = houses.houses_dictionary
        self.houses = houses
        self.houses_order = houses.houses_order
        self.game_state = game_state
        self.players_turn = game_state.players_turn

    # find whether opponent is left with seeds after making this move.
    def scan_opponent_houses(self,opponent,house_captured):
        opponent_houses = opponent.houses
        houses_list = self.houses_order[::-1]
        house = self.houses_dict[house_captured]

        



    def check_capture_move(self,last_house,house,opponent):

        if (last_house['seeds_number'] == 3 or last_house['seeds_number'] == 2) and house in opponent.houses:
            return True
        else:
            return False
        
    def capture_previous_house(self,current_house,player,opponent):
        previous_house =  current_house - 1

        check_house = self.houses_order[::-1][previous_house]

        check_house_name = check_house

        check_house = self.houses_dict[check_house]

        check = self.check_capture_move(check_house,check_house_name,opponent)

        if check:

            house_captured = self.houses_dict[check_house_name]

            player.captured += house_captured['seeds_number']

            house_captured['seeds'] = []
            house_captured['seeds_number'] = 0

            self.houses_dict[check_house_name] = house_captured


            self.capture_previous_house(previous_house,player,opponent)

        
        

    def make_move(self,house_picked,valid_player,valid_pick,player,opponent,game_state):

        house = house_picked
        house_name = house_picked
        house = self.houses_dict[house]

       

        if valid_player and valid_pick :
            self.picked_seeds = house['seeds']
            house['seeds'] = []
            house['seeds_number'] = 0
            self.houses_dict[house_name] = house

        houses_list = self.houses_order[::-1]

        houses_to_play  = houses_list.index(house_name)
        
        num_elements = len(self.picked_seeds)

        sliced_houses = []

        houses_ordered_list = houses_list.copy()

        for i in range(num_elements):

            houses_to_play= (houses_to_play + 1) % len(houses_ordered_list)
            new_house = houses_list[houses_to_play]
            sliced_houses.append(new_house)

            # sum_plus_index = houses_to_play + i
            # if sum_plus_index > 12:
            #     new_index = sum_plus_index - 12
            #     new_house = houses_list[new_index]
            #     sliced_houses.append(new_house)


            # elif sum_plus_index == 12:
            #     new_house = houses_list[0]
            #     sliced_houses.append(new_house)

            # else:
            #     new_house =houses_list[i+houses_to_play]
            #     sliced_houses.append(new_house)
        

        seed_index = 0
        seeds_captured = 0

        for sliced_house in sliced_houses:


            house_new = self.houses_dict[sliced_house]

            seed = self.picked_seeds[seed_index]

            seeds = house_new.get('seeds')

            seeds = seeds + [seed]


            house_new['seeds'] = seeds if sliced_house is not house_picked else []


            house_new['seeds_number'] += 1 if sliced_house is not house_picked else 0

            self.houses_dict[sliced_house] = house_new
            capture = False

            if seed_index == (len(sliced_houses)-1) and sliced_house in opponent.houses:
                capture = self.check_capture_move(house_new,sliced_house,opponent)


            if capture:
                print(f"{Back.GREEN}Capture!{Style.RESET_ALL}")
                house_captured = self.houses_dict[sliced_house]

                seeds_captured = house_captured['seeds_number']

                house_captured['seeds'] = []
                house_captured['seeds_number'] = 0

                self.houses_dict[sliced_house] = house_captured

                self.capture_previous_house(houses_list.index(sliced_house),player,opponent)

            seed_index += 1



        player.captured += seeds_captured
        self.game_state = self.houses_dict


        if player.captured > 24:
            return player.name
        
        elif player.captured == opponent.captured == 24:
            return 'draw'
        
        else:
            print(game_state.state_info())
            print(player.name)
            if game_state.player_one.name == player.name:
                game_state.players_turn =  game_state.player_two.name
            else:
                game_state.players_turn =  game_state.player_one.name
            
            return 'game_on'


                







            





