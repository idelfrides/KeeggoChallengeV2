
# rent_value = valor de aluguel


# ---------------------------------------
# importing modules
# ---------------------------------------
from utils.libs import print_log
from random import randint

class PalyerManager(object):

    def __init__(self, player, money=300):
        self.player = self.define_player(player)
        self.money = money
        self.position = self.get_player_position()


    def get_land_property(self):
        MANX_RENT = 100
        land_property = {}
        land_property['name'] = ''
        land_property['owner'] = self.player
        land_property['sell_value'] =  randint(MANX_RENT, 200)
        land_property['rent_value'] = randint(20, MANX_RENT)
        land_property['position'] = randint(1, 20)

        return  land_property


    def start_game_money(self):
        saldo = 300
        return saldo


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


    def round_completed(self):
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

        property_dict['name'] = 'RUSSIA'
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

            property_dict['name'] = 'UK'
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
            property_dict['name'] = 'USA'
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

        buy = randint(1, 50)

        try:
            player_info = all_player_info[str(player_number)]
        except Exception as err:
            player_info = self.get_player_info()

        if buy == 50:      # 50%
            property_dict = self.get_land_property()

            property_dict['name'] = 'VENEZUELA'
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

        owner_id_list = other_player_property.keys()
        owner_id_list = list(owner_id_list)
        owner_id = owner_id_list[0]

        try:
            player_info = all_player_info[str(player_number)]
        except Exception as err:
            player_info = self.get_player_info()

        balance = player_info['balance']

        # pay for property
        rent_value = (
            other_player_property[owner_id]['current_property']['rent_value']
        )

        pay = balance - rent_value

        other_player_property[owner_id]['current_property']['rent_value'] += (
            rent_value
        )

        player_info['balance'] = pay

        print(other_player_property)
        print(all_player_info)

        return player_info, other_player_property
