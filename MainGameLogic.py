
from Roles import Mafia, Innocent, Role

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
async def Kill_Player(player_role: dict, reason = "Committed Suicide") -> Role:

    #TODO: Implement
    # Remove the player and role instance from any of the dict caches they may belong to, if array is empty delete the key (that game is over)

    pass

# Day phase function called from game loop on begin day phase

async def PhaseHandler(discord_server):

    #DM all users with a day ability and instructions on how to use it.
    
    # Will use cog to keep running game loop for phase
    while(game_loops[discord_server].currentPhase == "Day"):

        pass

    # Vote Phase function called from game loop on begin vote phase

    while(game_loops[discord_server].currentPhase == "Vote"):

        pass

    #DM all users with a night ability and instructions on how to use it.

    # Will use cog to keep running game loop for phase
    while(game_loops[discord_server].currentPhase == "Night"):

        pass
