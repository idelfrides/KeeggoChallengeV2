
from random import randint

# -----------------------------------------------------------------

SIMULATIONS = 300     # 300
ROUNDS = 1000         # 1000

MAX_LIMIT = 100
BOARD_LENGHT = 20
DEFAULT_BALANCE = 300

# RENT_VALUE =  70     # randint(20, MAX_LIMIT)  # or use random mode
# RENT_VALUE = randint(20, MAX_LIMIT)  # or use random mode
# SELL_VALUE = RENT_VALUE * 2

PROPERTIES_NAME = {
    "impulsive_land_name": "RUSSIA",
    "demanding_land_name": "UK",
    "cautious_land_name": "USA",
    "random_land_name": "VENEZUELA",
}

# slesp times in minutes
SLEEP_TIME_ZERO = 0
SLEEP_TIME_ONE = 1
SLEEP_TIME_TWO = 2
SLEEP_TIME_THREE = 3
SLEEP_TIME_FOUR = 4
SLEEP_TIME_WALK = 0 # in second . set value 0.7 to see player walking
