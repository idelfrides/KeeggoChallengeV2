import os
from datetime import datetime
from random import randint


from IJGeneralUsagePackage.ijfunctions import (
    print_log
)



def show_info(**kwarg):

    info = f"""
    ---------------------------------------------------------
            GAME ROUND : [ {kwarg['round']} ]
            PLAYER PROFILE --> {kwarg['player']}
    ----------------------------------------------------------
    """
    print_log(info)
    return



def define_player_number():
    print_log(f'DEFINING THE PLAYER ORDER ...')
    position = randint(1, 4)

    return position
