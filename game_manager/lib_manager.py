
# rent_value = valor de aluguel

# ---------------------------------------
# importing modules
# ---------------------------------------

from  IJGeneralUsagePackage.IJGeneralLib import (
    print_log
)

from random import randint
from hold_constants_paths import (
    BOARD_LENGHT,
    MAX_LIMIT,
    PROPERTIES_NAME,
)


# ------------------------------------------------------------------
#                     CLASS BEGIN HERE
# ------------------------------------------------------------------


class PalyerManager(object):

    def __init__(self, player, money, rent_value):
        self.player = self.define_player(player)
        self.position = self.get_player_position()
        self.money = money
        self.rent_value = rent_value


    def get_land_property(self):
        land_property = {}
        land_property['name'] = 'Keeggo'
        land_property['owner'] = self.player

        land_property['position'] = 'BR' # will be updated

        try:   # the same values for all properties
            land_property['sell_value'] = self.rent_value * 2
            land_property['rent_value'] = self.rent_value
        except (TypeError, ValueError) :
            # different values for each property
            rent_value = self.rent_value[self.position]
            land_property['rent_value'] = rent_value
            land_property['sell_value'] = rent_value * 2

        return  land_property


    def get_player_position(self):
        to_walk = randint(1, 6)
        return to_walk


    def get_player_info(self):

        player_info= {
            'name': self.player,
            'current_property': {},
            'balance': self.money,
            'position': self.position
        }

        return player_info


    def board_completed(self):
        return 100


    def define_player(self, player_numer):
        """ 4 types
            1. Player one is impulsive
            2. Player two is demanding
            3. Player three is cautious
            4. Player four is random
        """

        player_dict = {}

        player_dict['1'] = 'Inpulsive Player'
        player_dict['2'] = 'Demanding Player'
        player_dict['3'] = 'Cautious Player'
        player_dict['4'] = 'Random Player'

        return player_dict[str(player_numer)]


    def buy_land_property_inpulsive_player(self, player_number, all_player_info):

        print_log(f'IMPULSIVE PALYER BUYS ANY PROPERTY WHEREVER HE STAND ON')

        property_dict = self.get_land_property()

        property_dict['name'] = PROPERTIES_NAME['impulsive_land_name']
        property_dict['position'] = self.position

        try:
            player_info = all_player_info[str(player_number)]
        except Exception as err:
            player_info = self.get_player_info()

        old_balance = player_info['balance']
        new_balance = old_balance - property_dict['sell_value']

        player_info['current_property'] = property_dict
        player_info['balance'] = new_balance

        player_full_content = {
            str(player_number): player_info
        }

        return player_info, player_full_content


    def buy_land_property_demanding_player(self, player_number, all_player_info):

        print_log(f'DEMANDING PALYER BUYS ANY PROPERTY AS LONG AS ITS RENT IS GREATER THAN 50.')

        property_dict = self.get_land_property()

        try:
            player_info = all_player_info[str(player_number)]
        except Exception as err:
            player_info = self.get_player_info()

        if property_dict['rent_value'] > 50:

            property_dict['name'] = PROPERTIES_NAME['demanding_land_name']
            property_dict['position'] = self.position

            old_balance = player_info['balance']
            new_balance = old_balance - property_dict['sell_value']

            player_info['current_property'] = property_dict
            player_info['balance'] = new_balance

            player_full_content = {
                str(player_number): player_info
            }

        else:
            player_full_content = 0

        return player_info, player_full_content


    def buy_land_property_cautious_player(self, player_number):

        print_log(f'CAUTIOUS PLAYER BUYS ANY PROPERTY AS LONG AS HE HAS A \n   RESERVE OF 80 BALANCE LEFT AFTER THE PURCHASE IS MADE.')

        property_dict = self.get_land_property()
        new_balance = self.money - property_dict['sell_value']

        if new_balance == 80:
            property_dict['name'] = PROPERTIES_NAME['cautious_land_name']
            property_dict['position'] = self.position

            player_info = self.get_player_info()

            player_info['current_property'] = property_dict
            player_info['balance'] = new_balance

            player_full_content = {
                str(player_number): player_info
            }
        else:
            player_info = self.get_player_info()
            player_full_content = 0

        return player_info, player_full_content


    def buy_land_property_random_player(self, player_number, all_player_info):
        print_log(f'RANDOM PLAYER BUYS A PROPERTY HE LANDS ON WITH A 50% OF PROBABILITY')

        buy_probability = randint(1, MAX_LIMIT)

        try:
            player_info = all_player_info[str(player_number)]
        except Exception as err:
            player_info = self.get_player_info()

        if buy_probability == 50:      # 50%
            property_dict = self.get_land_property()

            property_dict['name'] = PROPERTIES_NAME['random_land_name']
            property_dict['position'] = self.position

            old_balance = player_info['balance']
            new_balance = old_balance - property_dict['sell_value']

            player_info['current_property'] = property_dict
            player_info['balance'] = new_balance

            player_full_content = {
                str(player_number): player_info
            }

        else:
            player_full_content = 0

        return player_info, player_full_content


    def pay_rent_for_property(self, player_number, all_player_info, property_board_list):

        other_player_property = property_board_list[self.position-1]

        owner_id_list = list(other_player_property.keys())
        owner_id = owner_id_list[0]

        try:
            player_info = all_player_info[str(player_number)]
        except Exception as err:
            player_info = self.get_player_info()

        current_player_balance = player_info['balance']

        # pay for property
        property_rent_value = (
            other_player_property[owner_id]['current_property']['rent_value']
        )

        pay = current_player_balance - property_rent_value
        player_info['balance'] = pay

        # update curretn property owner balance after made a rent of his property to
        # current player
        other_player_property[owner_id]['balance'] += (
            property_rent_value
        )

        return player_info, other_player_property


    def get_owner(self, property_board_list):
        other_player_property = property_board_list[self.position-1]

        owner_id_list = list(dict(other_player_property).keys())
        owner_id = owner_id_list[0]

        player_name = self.define_player(player_numer=owner_id)

        return player_name


def update_board(property_board_list, player_game_over):

    """ UPDATE BOARD PROPERTY """

    for board_posi, owner_content in enumerate(property_board_list, start=0):

        if owner_content == 'SEM-DONO':
            continue

        player_number = list(dict(owner_content).keys())
        player_number = int(player_number[0])

        if player_number in player_game_over:
            property_board_list[board_posi] = 'SEM-DONO'
        else:
            pass

    return property_board_list


def one_winner_per_simulation(all_player_info_dict):

    winner_player_info = {}
    winner_balance_list = []

    winner_balance_list.append(all_player_info_dict)
    code_winner, _ = calculate_winner(winner_balance_list)

    winner_player_info[str(code_winner)] = (
        all_player_info_dict.get(str(code_winner))
    )

    return winner_player_info


def show_game_over_winner(winner_player):

    info = """
    #############################################################
    #                                                           #
    #               THE GAME IS OVER                            #
    #               WE GOT A PLAYER WINNER                      #
    #               WINNER [ {} ] | NUMBER: {}        #
    #               BALANCE :  {}                             #
    #                                                           #
    #               AN OTHER MATCH WILL BEGIN ...               #
    #                                                           #
    #############################################################
    """.format(
        winner_player['name'],
        str(winner_player['code_']), winner_player['balance']
    )

    print(info)

    return


def prepare_calculate_winner(hold_info_per_simulation_list):

    winner_behavior_list = []
    player_number = []
    winner_behavior_number = []
    game_over_by_timeout = 0
    palyer_info_to_define_winner = []

    for one_simulation_info in hold_info_per_simulation_list:
        winner_behavior_dict = one_simulation_info.get('winner_behavior')

        try:
            check_balance = (
                list(dict(winner_behavior_dict).values())[0].get('balance')
            )
        except Exception as error:
            check_balance = None

        if not check_balance:
            continue

        if check_balance < 0:
            continue

        if one_simulation_info.get('game_over'): # game_over=True | by a winner

            palyer_info_to_define_winner.append(winner_behavior_dict)
            player_number = dict(winner_behavior_dict).keys()
            player_number = int(list(player_number)[0])
            winner_behavior_number.append(player_number)

        else:  # game_over = False | by time out

            winner_behavior_dict = one_simulation_info['winner_behavior']
            game_over_by_timeout += one_simulation_info['time_out']
            palyer_info_to_define_winner.append(winner_behavior_dict)

    real_winner_bahavior, winner_behavior_list = calculate_winner(
        palyer_info_to_define_winner
    )

    return real_winner_bahavior, winner_behavior_list, game_over_by_timeout


def calculate_tiebraeker(player_dict_tiebraeker_list):

    print_log('CALCULATE TIEBRAEKER')

    seen_balance = set()
    balance_round_older = {}
    real_winner_info = {}
    real_winner_info_list = []

    for one_simulation_info in player_dict_tiebraeker_list:

        for balance, winner_info in one_simulation_info.items():
            try:
                balance = int(balance)
            except Exception as error:
                continue

            if balance in seen_balance:

                previous_round = balance_round_older[str(balance)][0]
                current_round = winner_info.get('round_')

                if previous_round <= current_round:
                    previous_code = balance_round_older[str(balance)][1]
                    real_winner_info[str(previous_code)] = winner_info

                elif previous_round > current_round:
                    current_code = winner_info.get('code_')
                    real_winner_info[str(current_code)] = winner_info

                real_winner_info_list.append(real_winner_info)

            else:
                try:
                    balance_round_older[str(balance)] = [
                        winner_info['round_'], winner_info['code_']
                    ]
                except Exception as error:
                    pass

                seen_balance.add(balance)

    return real_winner_info_list


def calculate_winner(hold_info_per_simulation_list):

    greatest_balance = 0
    balance = 0
    winner_behavior_list = []
    balance_dict = {}
    graetest_balance_dict = {}

    for one_player_info in hold_info_per_simulation_list:

        for id_player, info in dict(one_player_info).items():

            if not id_player:
                continue

            greatest_balance = info['balance']

            if balance > greatest_balance:
                hold_balace = greatest_balance
                greatest_balance = balance

                info['code_'] = int(id_player)
                balance_dict[str(balance)] = graetest_balance_dict.get(str(balance))

                try:
                    id_player =  balance_dict[str(balance)].get('code_', id_player)
                except Exception as error:
                    pass

                winner_player_number = int(id_player)

            elif balance < greatest_balance:
                balance = greatest_balance

                info['code_'] = int(id_player)
                graetest_balance_dict[str(greatest_balance)] = info

                winner_player_number = int(id_player)

            elif balance == greatest_balance:
                if balance_dict or graetest_balance_dict:

                    real_winner_dic = calculate_tiebraeker(
                        [balance_dict, graetest_balance_dict]
                    )

                    try:
                        real_winner_dic = real_winner_dic[0]

                        info['code_'] = list(real_winner_dic.values())[0].get('code_')

                        graetest_balance_dict[str(greatest_balance)] = info

                        id_player = info['code_']

                    except Exception as error:
                        info['code_'] = int(id_player)
                        graetest_balance_dict[str(greatest_balance)] = info

                winner_player_number = int(id_player)

            else:
                pass


        winner_behavior_list.append(winner_player_number)

    count_impulsive = winner_behavior_list.count(1)  # impulsive
    count_demanding = winner_behavior_list.count(2)  # demanding
    count_coutious = winner_behavior_list.count(3)   # coutious
    count_random = winner_behavior_list.count(4)     # random

    winner_dict = {
        str(count_impulsive): 1,
        str(count_demanding): 2,
        str(count_coutious): 3,
        str(count_random): 4
    }

    winner_behavior_counter = [
        count_impulsive, count_demanding,
        count_coutious, count_random
    ]

    winner_behavior_list.clear()

    winner_behavior_list = winner_behavior_counter.copy()

    winner_behavior_counter.sort(reverse=True)

    most_winner = winner_behavior_counter[0]

    winner_by_bahavior = winner_dict[str(most_winner)]

    return winner_by_bahavior, winner_behavior_list


def define_player_behavior(player_numer):
    """ 4 types
        1. Player one is impulsive
        2. Player two is demanding
        3. Player three is cautious
        4. Player four is random
    """

    player_dict = {}

    player_dict['1'] = 'JOGADOR INPULSIVO'
    player_dict['2'] = 'JOGADOR EXIGENTE'
    player_dict['3'] = 'JOGADOR CAUTELOSO'
    player_dict['4'] = 'JOGADOR ALEATÓRIO'

    return player_dict[str(player_numer)]


def set_value_each_property():

    property_values_dict = {}
    seen_rent_value = set()

    property_index = 1

    while property_index <= BOARD_LENGHT:

        rent_value = randint(10, 100)

        if rent_value in seen_rent_value:
            continue
        seen_rent_value.add(rent_value)

        property_values_dict[property_index] = rent_value
        property_index += 1

    return property_values_dict
