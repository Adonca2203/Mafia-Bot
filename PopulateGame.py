
from Roles import *
import random

#Default game mode will be:
# Doctor (Support)
# Investigator, Sheriff (Inno Invest)
# Godfather, Mafioso (Mafia)
# Serial Killer (Neutral Killer)
# Vigilante and Jailor (Inno Killing)

_testlist = ["Toshi"]

all_roles = [Doctor, Investigator, Sheriff, Mafioso, Godfather, SerialKiller, Vigilante, Jailor]

_test_all_roles = [Mafioso]

roles_dict = {}

def PopulateGame(players: list) -> dict:

    choose_pool = all_roles

    for player in players:

        _retrole = random.choice(choose_pool)

        playerchoice = _retrole(player)

        choose_pool.remove(_retrole)

        roles_dict[player] = playerchoice

    print(roles_dict)
    print(all_roles)

    return roles_dict

def TestPopulateGame(players: list) -> dict:

    for player in players:

        _retrole = random.choice(_test_all_roles)

        playerchoice = _retrole(player)

        _test_all_roles.remove(_retrole)

        roles_dict[player] = playerchoice

    return roles_dict