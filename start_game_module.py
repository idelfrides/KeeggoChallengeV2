#!/usr/bin/env python3
# encoding: utf-8

import sys
import time

from hold_constants_paths import (
    DEFAULT_BALANCE, SIMULATIONS,
    ROUNDS,
    SLEEP_TIME_WALK, SLEEP_TIME_ZERO,
    BOARD_LENGHT,
)
from utils.lib_functions import (
    show_info,
    define_player_number,
)
from IJGeneralUsagePackage.ijfunctions import (
    build_line,
    convert_minutes_to_second,
    ij_smart_menu,
    make_sound, print_log
)
from game_manager.lib_manager import (
    PalyerManager,
    calculate_winner_v2,
    define_player_behavior,
    one_winner_per_simulation,
    show_game_over_winner,
    update_board
)


# ------------------------------------------------------------------
#                     RUN GAME FUNCTION BEGIN HERE
# ------------------------------------------------------------------


def run_game(round_, simulation_, player_number, player_game_over, property_board_list, all_player_info, current_balance):

    player = PalyerManager(player=player_number, money=current_balance)

    if player_number in player_game_over:
        print_log(f'GAME IS OVER FOR [ {player.player} ] | NUMBER:    {player_number}')
        return

    show_info(
        type_='game_info', balance=player.money,
        value_=simulation_, value_round=round_,
        player=player.player
    )
    time.sleep(0)

    to_walk_on_board = player.position

    try:

        balance = all_player_info[str(player_number)]['balance']
        current_position = all_player_info[str(player_number)]['position']

        player.position += current_position

        if balance < 0:
            player_game_over.append(player_number)

    except Exception as excep:
        current_position = 1


    game_info = """
    ---------------------------------------------------------------------
        [ {} ]  MUST WALK [ {} ] POSITION(S) ON THE BOARD
        FROM CURRENT POSITION {}
    ---------------------------------------------------------------------
    """.format(player.player, to_walk_on_board, current_position)

    print(game_info)

    if player.position > BOARD_LENGHT:
        player.position = BOARD_LENGHT


    while True:
        for walk_ in range(current_position, player.position + 1):

            print_log(f'{player.player} IN POSITION [ {walk_} ] ...')
            time.sleep(SLEEP_TIME_WALK)

            if walk_ == player.position:

                print_log(
                    f'{player.player} GETS HIS END POSITION [ {walk_} ]...'
                )

                # find player profile to verify what he going to do
                if player_number == 1:  # implulsive player

                    if property_board_list[player.position-1] == 'SEM-DONO':
                        print_log(f'PROPERTY IN POSITION [ {player.position} ] IS AVAILABLE TO BUY')

                        player_info, player_board_content = player.buy_land_property_inpulsive_player(
                            player_number, all_player_info
                        )

                        all_player_info[str(player_number)] = player_info

                        if player_info['balance'] < 0:
                            print_log(f'GAME IS OVER FOR [ {player.player} ]...')
                            player_game_over.append(player_number)
                            all_player_info.pop(str(player_number))
                        else:
                            property_board_list[player.position-1] = (
                                player_board_content
                            )

                    # property belong to other plyer
                    elif not property_board_list[player.position-1].get(str(player_number)):
                        print_log(f'PROPERTY IN POSITION [ {player.position} ] HAS AN OWNER')

                        player_info, other_player_property = (
                            player.pay_rent_for_property(
                            player_number,  all_player_info, property_board_list)
                        )

                        all_player_info[str(player_number)] = player_info

                        if player_info['balance'] < 0:
                            print_log(f'GAME IS OVER FOR [ {player.player} ]...')
                            player_game_over.append(player_number)
                            all_player_info.pop(str(player_number))
                        else:
                            # on the game
                            property_board_list[player.position-1] = (
                                other_player_property
                            )

                    else:
                        # property belong to this player
                        pass

                if player_number == 2:  # demanding  player

                    if property_board_list[player.position-1] == 'SEM-DONO':
                        print_log(f'PROPERTY IN POSITION [ {player.position} ] IS AVAILABLE TO BUY')

                        player_info, player_board_content = player.buy_land_property_demanding_player(
                            player_number, all_player_info
                        )

                        if player_board_content == 0:
                            break

                        all_player_info[str(player_number)] = player_info

                        print_log(f'{player_board_content}')

                        if all_player_info[str(player_number)]['balance'] < 0:
                            print_log(f'GAME IS OVER FOR [ {player.player} ]...')
                            player_game_over.append(player_number)
                            all_player_info.pop(str(player_number))
                        else:
                            property_board_list[player.position-1] = (
                                player_board_content
                            )

                    # property belong to other plyer
                    elif not property_board_list[player.position-1].get(str(player_number)):
                        print_log(f'PROPERTY IN POSITION [ {player.position} ] HAS AN OWNER')

                        player_info, other_player_property = (
                            player.pay_rent_for_property(
                            player_number, all_player_info, property_board_list)
                        )

                        all_player_info[str(player_number)] = player_info

                        if player_info['balance'] < 0:
                            print_log(f'GAME IS OVER FOR [ {player.player} ]...')
                            player_game_over.append(player_number)
                            all_player_info.pop(str(player_number))
                        else:
                            # on the game
                            property_board_list[player.position-1] = (
                                other_player_property
                            )

                    else:
                        # property belong to this player
                        pass

                if player_number == 3:  # cautious one

                    try:
                        player.money = all_player_info[str(player_number)]['balance']
                    except Exception as err:
                        print_log(f'EXCEPTION: {err}')

                    if property_board_list[player.position-1] == 'SEM-DONO':
                        print_log(f'PROPERTY IN POSITION [ {player.position} ] IS AVAILABLE TO BUY')

                        player_info, player_board_content = player.buy_land_property_cautious_player(
                            player_number)

                        if player_board_content == 0:   # não comprou
                            continue

                        all_player_info[str(player_number)] = player_info

                        if player_info['balance'] < 0:
                            print_log(f'GAME IS OVER FOR [ {player.player} ]...')
                            player_game_over.append(player_number)
                            all_player_info.pop(str(player_number))
                        else:
                            # on the game
                            property_board_list[player.position-1] = (
                                player_board_content
                            )

                    # property belong to other plyer
                    elif not property_board_list[player.position-1].get(str(player_number)):
                        print_log(f'PROPERTY IN POSITION [ {player.position} ] HAS AN OWNER')

                        player_info, other_player_property = (
                            player.pay_rent_for_property(
                            player_number, all_player_info, property_board_list)
                        )

                        all_player_info[str(player_number)] = player_info

                        if player_info['balance'] < 0:
                            print_log(f'GAME IS OVER FOR [ {player.player} ]...')
                            player_game_over.append(player_number)
                            # all_player_info.pop(str(player_number))
                        else:
                            # on the game
                            property_board_list[player.position-1] = (
                                other_player_property
                            )

                    else:
                        pass

                if player_number == 4:  # random one
                    if property_board_list[player.position-1] == 'SEM-DONO':
                        print_log(f'PROPERTY IN POSITION [ {player.position} ] IS AVAILABLE TO BUY')

                        player_info, player_board_content = player.buy_land_property_random_player(player_number,
                            all_player_info
                        )

                        if player_board_content == 0:
                            continue

                        all_player_info[str(player_number)] = player_info

                        if player_info['balance'] < 0:
                            print_log(f'GAME IS OVER FOR [ {player.player} ]...')
                            player_game_over.append(player_number)
                            all_player_info.pop(str(player_number))
                        else:
                            property_board_list[player.position-1] = (
                                player_board_content
                            )

                    # property belong to other player
                    elif not property_board_list[player.position-1].get(str(player_number)):
                        print_log(f'PROPERTY IN POSITION [ {player.position} ] HAS AN OWNER')

                        player_info, other_player_property = (
                            player.pay_rent_for_property(
                            player_number, all_player_info, property_board_list)
                        )

                        all_player_info[str(player_number)] = player_info

                        if player_info['balance'] < 0:
                            print_log(f'GAME IS OVER FOR [ {player.player} ]...')
                            player_game_over.append(player_number)
                            all_player_info.pop(str(player_number))
                        else:
                            # on the game
                            property_board_list[player.position-1] = (
                                other_player_property
                            )
                    else:
                        pass
                else:   # END if player_number == 4:  # random one
                    pass

            # END if walk_ == player.position
        # END for walk_ in range(min_position, player.position + 1)

        current_position = player.position
        player.position += 1

        try:
            player_info_value = all_player_info[str(player_number)]
            player_info_value['round_'] = round_

            player_info_value['position'] = current_position
            all_player_info[str(player_number)] = player_info_value
        except Exception as error:
            pass

        if player.position > BOARD_LENGHT:
            updated_balance = player.board_completed()
            print_log(f' UPDATE BALANCE FOR PLAYER [ {player.player} ].')

            try:
                all_player_info[str(player_number)]['balance'] += (
                    updated_balance
                )

                all_player_info[str(player_number)]['position'] = 1

            except Exception as err:
                print_log(f'EXCEPTION: {err}')

            break  # exit from while
        else:
            break  # exit from while for one player

    # END while True:

    return


def control_run_game():

    simulation_counter = 1
    hold_info_per_simulation_list = []
    round_by_simulation = []
    game_over = False

    # SIMULATIONS is the same as PARTIDAS
    while simulation_counter <= SIMULATIONS:

        build_line('-', 80)
        print(f'\t\t\t THE GAME IS ONGOING ...')

        hold_info_per_simulation_dict = {}
        player_game_over = []
        all_player_info = {}
        winner_dict_info = {}
        winner_dict_info_help = {}

        property_board_list = ['SEM-DONO' for v in range(1, 21)]

        player_number = define_player_number()

        game_over_by_time_out = 0
        game_over_by_player_winner = 0
        game_over = False

        for round in range(1, ROUNDS + 1):

            if player_number > 4:
                player_number = 1

            try:
                current_balance = (
                    all_player_info.get(str(player_number), DEFAULT_BALANCE)['balance']
                )
            except Exception as error:
                print_log(f'\n\n EXCEPTION --> {error}')
                current_balance = DEFAULT_BALANCE

            run_game(
                simulation_=simulation_counter,
                round_=round,
                player_number=player_number,
                player_game_over=player_game_over,
                property_board_list=property_board_list,
                all_player_info=all_player_info,
                current_balance=current_balance
            )

            # print(f'\n\n\t\t PROPERTY_BOARD_LIST \n\n\t {property_board_list}')

            player_key = list(all_player_info.keys())

            if len(player_game_over) == 3 and player_key:

                player_key = player_key[0]

                if str(player_key).isnumeric() and int(player_key) not in player_game_over:
                    game_over = True
                    break

            property_board_list = update_board(
                property_board_list=property_board_list, player_game_over=player_game_over
            )

            time.sleep(convert_minutes_to_second(SLEEP_TIME_ZERO))

            player_number += 1 # next  = NEXT ROUND

        # END for round in range(1, ROUNDS + 1):

        if game_over:
            winner_dict = {}
            winner_dict['code'] = player_key
            winner_dict['name'] = all_player_info[str(player_key)]['name']
            winner_dict['balance'] = all_player_info[str(player_key)]['balance']
            winner_dict['simulation'] = simulation_counter

            show_game_over_winner(winner_dict)
            # real_winner_bahavior_info.add(player_key)
            winner_dict_info[str(player_key)] = winner_dict

            game_over = False

            # break
            # return

        if not game_over:
            if len(all_player_info) > 1:
                all_player_info = one_winner_per_simulation(all_player_info)

            for number_, player_info in all_player_info.items():
                winner_dict_info_help['name'] = player_info['name']
                winner_dict_info_help['balance'] = player_info['balance']
                winner_dict_info_help['simulation'] = simulation_counter

                winner_dict_info[number_] = winner_dict_info_help

            if round == ROUNDS:
                game_over_by_time_out += 1
            else:
                game_over_by_player_winner += 1

            round_by_simulation.append(round)

        hold_info_per_simulation_dict['winner_behavior'] = winner_dict_info

        hold_info_per_simulation_dict['time_out'] = (
            game_over_by_time_out
        )

        hold_info_per_simulation_dict['player_winner'] = (
            game_over_by_player_winner
        )

        hold_info_per_simulation_list.append(hold_info_per_simulation_dict)

        simulation_counter += 1

    # END while simulation_counter <= SIMULATIONS

    real_winner_bahavior, wb_counter, game_over_by_time_out = (
        calculate_winner_v2(hold_info_per_simulation_list)
    )

    percentual_wins_impulsive = (wb_counter[0]/SIMULATIONS)*100
    percentual_wins_demanding = (wb_counter[1]/SIMULATIONS)*100
    percentual_wins_cautious = (wb_counter[2]/SIMULATIONS)*100
    percentual_wins_random = (wb_counter[3]/SIMULATIONS)*100

    mean_round_per_simulation = sum(round_by_simulation)/SIMULATIONS

    build_line('#', 100)
    print(f'\t\t GAME OVER BY ROUND')
    print('\n\t\t FINAL RESULTS')
    build_line('-', 60)

    print(f'\n\tPARTIDAS POR TIME OUT: {game_over_by_time_out}')            # 1
    print(f'\n\tMÉDIA DE RODADAS POR PARTIDA: {mean_round_per_simulation}') # 2
    print(f'\n\t% DE VITORIAS DO IMPULSIVO: {percentual_wins_impulsive}')   # 3
    print(f'\n\t% DE VITORIAS DO EXIGENTE: {percentual_wins_demanding}')    # 3
    print(f'\n\t% DE VITORIAS DO CAUTELOSO: {percentual_wins_cautious}')    # 3
    print(f'\n\t% DE VITORIAS DO ALEATÓRIO: {percentual_wins_random}')      # 3

    winner_bahavior = define_player_behavior(real_winner_bahavior)
    print(f'\n\tCOMPORTAMENTO MAIS VENCEDOR: [ {winner_bahavior} ]')           # 4

    build_line('#', 100)

    return


if __name__ == '__main__':

    menu_options = {
        1: 'run game'
    }

    while True:

        SATART_TIME = time.time()

        menu_option_qtd = len(menu_options.values())

        menu_response = ij_smart_menu(menu_options.values())

        if menu_response == 0:
            break

        if menu_response == -1:
            menu_options.clear()

        if menu_option_qtd < menu_response:
            new_option = input('\n\n INFORME A NEW OPTION -->   ')
            menu_options.update({menu_response: new_option})

        user_action = menu_options.get(menu_response, 'REMOVE OPTIONS')

        control_run_game()

        END_TIME = time.time()

        total_run_time = END_TIME - SATART_TIME
        total_run_time /= 60

        total_minutes =  str(total_run_time).split('.')[0]
        total_seconds =  str(total_run_time).split('.')[1]

        # make_response(
        #     total_minutes=total_minutes,
        #     total_seconds=total_seconds,
        #     source_data=user_action
        # )

        make_sound()
        time.sleep(convert_minutes_to_second(SLEEP_TIME_ZERO))
        SATART_TIME = 0
        END_TIME = 0
