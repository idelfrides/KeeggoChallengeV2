import os
from datetime import datetime
from random import randint


from IJGeneralUsagePackage.ijfunctions import (
    print_log
)


# ------------------------------------------------------------------
#                     FUNCTIONS BEGIN HERE
# ------------------------------------------------------------------


def show_info(**kwarg):

    if kwarg['type_'] == 'round':

        info = f"""
        ----------------------------------------------------------
                GAME ROUND : [ {kwarg['value_']} ]
                PLAYER PROFILE --> {kwarg['player']}
                PLAYER BALANCE --> {kwarg['balance']}
        ----------------------------------------------------------
        """

    if kwarg['type_'] == 'game_info':

        info = f"""
        ----------------------------------------------------------
                SIMULATION/PARTIDA --> [ {kwarg['value_']} ]
                GAME ROUND --> [ {kwarg['value_round']} ]
                PLAYER PROFILE --> {kwarg['player']}
                PLAYER BALANCE --> {kwarg['balance']}
        ----------------------------------------------------------
        """

    if kwarg['type_'] == 'simulation':

        info = f"""
        ---------------------------------------------------------

                GAME SIMULATION/PARTIDA : [ {kwarg['value_']} ]

        ----------------------------------------------------------
        """

    print(info)

    return


def define_player_number():

    print_log(f'RANDOMIC DEFINING THE PLAYER ORDER ...')

    player_profile_number = randint(1, 4)
    print_log(f'PLAYER PROFILE NUMBER IS --> {player_profile_number}')

    return player_profile_number
