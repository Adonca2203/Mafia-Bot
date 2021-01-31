
from Roles import Innocent, Mafia
from pubsub import pub

all_roles = {}
innocent_roles = {}
mafia_roles = {}
ongoing_games = {}


async def CacheGameLoop(server, server_cog: dict) -> None:

    if server not in ongoing_games.keys():
        ongoing_games[server] = server_cog[server]

async def CacheAllRoles(server, server_player_role_pair: dict) -> None:

    if server not in all_roles.keys():
        all_roles[server] = server_player_role_pair[server]

    for player, role in all_roles[server].items():

        if isinstance(role, Mafia):

            if not mafia_roles.get(server):

                mafia_roles[server] = [role]

            elif mafia_roles.get(server):

                mafia_roles[server].append(role)

        elif isinstance(role, Innocent):

            if not innocent_roles.get(server):

                innocent_roles[server] = [role]

            elif innocent_roles.get(server):

                innocent_roles[server].append(role)

    print(f"{mafia_roles}, {innocent_roles}")

# Function used to kill players, the default reason being suicide (they chose to leave the game)
async def Kill_Player(player_list: list, reason = "Committed Suicide") -> dict:

    dead_dict = {}

    for player in player_list:

        del all_roles[player]

        if isinstance(player, Innocent):

            del innocent_roles[player]

        else:

            del mafia_roles[player]

        dead_dict[player] = reason


    return dead_dict

async def DetermineWin(innocent_list: dict, mafia_list: dict, all_roles: dict) -> dict or None:

    temp = {}

    if len(innocent_list) > len(mafia_list):

        temp[Innocent] = all_roles

        return temp
    
    elif len(mafia_list) > len(innocent_list):

        temp[Mafia] = all_roles

        return temp

    return None

async def RoleOf(user):

    pass