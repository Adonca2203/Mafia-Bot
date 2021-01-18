
from Roles import Mafia, Innocent, Role, DayActor
from GameManager import DetermineWin
from pubsub import pub
import asyncio

all_roles = {}
game_loops = {}
mafia_roles = {}
innocent_roles = {}

async def CacheGameLoop(server, server_cog: dict) -> None:

    if server not in game_loops.keys():
        game_loops[server] = server_cog[server]

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

# Day phase function. An event Listener

async def Subscribe():

    pub.subscribe(DayHandler, "Day")
    pub.subscribe(VoteHandler, "Vote")
    pub.subscribe(NightHandler, "Night")

def DayHandler(discord_server):

    async def DayHandlerAsync():

        # Commented out for testing purposes

        #if await DetermineWin(innocent_roles, mafia_roles, all_roles) is None:
        
            for player, role in all_roles[discord_server].items():

                if isinstance(role, DayActor):

                    await player.send("You are a day actor")

    asyncio.create_task(DayHandlerAsync())
  
# Vote phase function. An event Listener
def VoteHandler(discord_server):

    pass

# Night phase function. An event Listener
def NightHandler(discord_server):
    #DM all users with a night ability and instructions on how to use it.

    async def NightHandlerAsync():

        # Commented out for testing purposes

        for player, role in all_roles[discord_server].items():

            await player.send("You are a night actor")

    asyncio.create_task(NightHandlerAsync())