#!/usr/bin/env python3
# encoding: utf-8

import time
from typing import Counter
from hold_constants_paths import (
    SIMULATIONS, ROUNDS,
    SLEEP_TIME_ZERO, SLEEP_TIME_1
)

from utils.libs import (
    print_log, show_info,
    define_player_number,
)

from game_manager.lib_manager import PalyerManager
from ijfunctions import (
    copy_libs
)

def run_game(round, player_number, player_game_over, property_board_list, all_player_info):

    player = PalyerManager(player=player_number)
    show_info(round=round, player=player.player)

    print_log(f'{player.player} MUST WALK [{player.position}] POSITION')

    try:
        balance = all_player_info[str(player_number)]['balance']
        if balance < 0:
            player_game_over.append(player_number)
    except Exception as excep:
        pass

    if player_number in player_game_over:
        print_log(f'GAME IS OVER FOR [ {player.player} ] | NUMBER {player_number}')
        return

    board_lenght = 20
    min_position = 1

    while True:
        for walk_ in range(min_position, player.position + 1):

            print_log(f'{player.player} IN POSITION [{walk_}]...')

            if walk_ == player.position:

                print_log(
                    f'{player.player} GETS HIS END POSITION [{walk_}]...'
                )

                # find player profile to verify what he going to do
                if player_number == 1:  # implulsive player

                    if property_board_list[player.position-1] == 'SEM-DONO':
                        print_log(f'PROPERTY IN POSITION [ {player.position} ] IS AVAILABLE TO BUY')

                        player_info, player_board_content = player.buy_land_property_inpulsive_player(
                            player_number, all_player_info
                        )

                        all_player_info[str(player_number)] = player_info

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
                            player_number,  all_player_info, property_board_list)
                        )

                        if player_info['balance'] < 0:
                            print_log(f'GAME IS OVER FOR [ {player.player} ]...')
                            player_game_over.append(player_number)
                            all_player_info.pop(str(player_number))
                        else:
                            # on the game
                            all_player_info[str(player_number)] = player_info

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

                        if player_info['balance'] < 0:
                            print_log(f'GAME IS OVER FOR [ {player.player} ]...')
                            player_game_over.append(player_number)
                            all_player_info.pop(str(player_number))
                        else:
                            # on the game
                            all_player_info[str(player_number)] = player_info
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

                        if all_player_info[str(player_number)]['balance'] < 0:
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

                        if player_info['balance'] < 0:
                            print_log(f'GAME IS OVER FOR [ {player.player} ]...')
                            player_game_over.append(player_number)
                            all_player_info.pop(str(player_number))
                        else:
                            # on the game
                            all_player_info[str(player_number)] = player_info
                            property_board_list[player.position-1] = (
                                other_player_property
                            )

                    else:
                        pass

                if player_number == 4:  # random one
                    if property_board_list[player.position-1] == 0:
                        print_log(f'PROPERTY IN POSITION [ {player.position} ] IS AVAILABLE TO BUY')

                        player_info, player_board_content = player.buy_land_property_random_player(player_number,
                            all_player_info
                        )

                        if player_board_content == 0:
                            continue

                        all_player_info[str(player_number)] = player_info

                        if all_player_info[str(player_number)]['balance'] < 0:
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

                        if player_info['balance'] < 0:
                            print_log(f'GAME IS OVER FOR [ {player.player} ]...')
                            player_game_over.append(player_number)
                            all_player_info.pop(str(player_number))
                        else:
                            # on the game
                            all_player_info[str(player_number)] = player_info
                            property_board_list[player.position-1] = (
                                other_player_property
                            )

                    else:
                        pass

        min_position = player.position
        player.position += 1

        if player.position > board_lenght:
            updated_balance = player.round_completed()

            try:
                all_player_info[str(player_number)]['balance'] += updated_balance
            except Exception as err:
                print_log(f'EXCEPTION: {err}')

            break   # exit from while


    return


def calculate_winner(all_player_info):
    greatest_balance = 0
    balance = 0
    winner_behavior_list = []
    winner_dict= {}

    for one_player_info in all_player_info:
        for id_player, info in one_player_info.items():
            greatest_balance = info['balance']

            if balance > greatest_balance:
                hold_balace = greatest_balance
                greatest_balance = balance
                winner_player_number = int(id_player)
            else:
                balance = greatest_balance
                winner_player_number = int(id_player)

        winner_behavior_list.append(winner_player_number)

    count_1 = winner_behavior_list.count(1)
    count_2 = winner_behavior_list.count(2)
    count_3 = winner_behavior_list.count(3)
    count_4 = winner_behavior_list.count(4)

    winner_dict[str(count_1)] = 1
    winner_dict[str(count_2)] = 2
    winner_dict[str(count_3)] = 3
    winner_dict[str(count_4)] = 4

    winner_behavior_counter = [count_1, count_2, count_3, count_4]
    winner_behavior_list.clear()
    winner_behavior_list = [count_1, count_2, count_3, count_4]

    winner_behavior_counter.sort(reverse=True)
    most_win = winner_behavior_counter[0]

    winner_by_bahavior = winner_dict[str(most_win)]

    return winner_by_bahavior, winner_behavior_list


def control_run_game():
    winner_behavior = []
    simulation_counter = 1

    while simulation_counter < SIMULATIONS:

        print_log(f'\n\n\n SIMULATION/PARTIDA --> {SIMULATIONS}\n\n\n')

        player_game_over = []
        round_by_simulation = []
        all_player_info = {}
        players_dict_info = {}
        property_board_list = ['SEM-DONO' for v in range(1, 21)]

        print_log(f'STARTING THE GAME ...\n')
        player_number = define_player_number()
        game_over_by_complete_round = 0

        for round in range(1, ROUNDS + 1):

            if player_number > 4:
                player_number = 1

            run_game(round, player_number, player_game_over,
                property_board_list, all_player_info)

            player_number += 1  # next player
            time.sleep(SLEEP_TIME_ZERO)

        for key, value_ in all_player_info.items():
            players_dict_info[key] = value_

        winner_behavior.append(players_dict_info)

        game_over_by_complete_round += 1
        round_by_simulation.append(round)

        simulation_counter += 1


    winner_by_bahavior, winner_behavior_counter = (
        calculate_winner(winner_behavior)
    )
    wb_counter = winner_behavior_counter

    percentual_vitoria_impulsivo = (wb_counter[0]/SIMULATIONS) *100
    percentual_vitoria_exigente = (wb_counter[1]/SIMULATIONS) *100
    percentual_vitoria_cauteloso = (wb_counter[2]/SIMULATIONS) *100
    percentual_vitoria_aleatorio = (wb_counter[3]/SIMULATIONS) *100

    round_mean = sum(round_by_simulation)/SIMULATIONS

    print('-'*80)
    print(f'GOME OVER BY ROUND {round}')
    print('\n  GAME RESULTS \n')
    print('-'*40)

    print(f'\n PARTIDAS POR TIME OUT: {game_over_by_complete_round}')    # 1
    print(f'\n MÉDIA DE RODADAS POR PARTIDA : {round_mean}')             # 2
    print(f'\nTAXA DE VITORIAS DO IMPULSIVO: {percentual_vitoria_impulsivo}')   # 3
    print(f'\n TAXA DE VITORIAS DO EXIGENTE: {percentual_vitoria_exigente}')
    print(f'\n TAXA DE VITORIAS DO CAUTELOSO: {percentual_vitoria_cauteloso}')
    print(f'\n TAXA DE VITORIAS DO ALEATÓRIO: {percentual_vitoria_aleatorio}')
    print(f'\n COMPORTAMENTO MAIS VENCEDOR: {winner_by_bahavior}')       # 4

    print('-'*80)



if __name__ == '__main__':

    copy_libs()

    menu_options = {
        1: 'run game'
    }

    while True:

        SATART_TIME = time.time()

        menu_option_qtd = len(menu_options.values())

        # TODO: create a show_info function in the libs module

        menu_response = ij_smart_menu(menu_options.values())

        if menu_response == 0:
            break

        if menu_response == -1:
            menu_options.clear()

        if menu_option_qtd < menu_response:
            new_option = input('\n\n INFORME A NEW OPTION -->   ')
            menu_options.update({menu_response: new_option})

        user_action = menu_options.get(menu_response, 'REMOVE OPTIONS')

        control_run_game(stakeholder=user_action)

        make_sound()
        END_TIME = time.time()

        total_run_time = END_TIME - SATART_TIME
        total_run_time /= 60

        total_minutes =  str(total_run_time).split('.')[0]
        total_seconds =  str(total_run_time).split('.')[1]

        make_response(
            total_minutes=total_minutes, total_seconds=total_seconds,fornecedor=user_action
        )
        time.sleep(15)

        SATART_TIME = 0
        END_TIME = 0
