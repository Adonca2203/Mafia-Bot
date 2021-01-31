
from Roles import Mafia, Innocent, Role, DayActor
from GameManager import DetermineWin, all_roles, innocent_roles, mafia_roles
from pubsub import pub
import asyncio

vowels = ["A", "E", "I", "O", "U"]

# Day phase function. An event Listener

async def Subscribe():

    pub.subscribe(DayHandler, "Day")
    pub.subscribe(VoteHandler, "Vote")
    pub.subscribe(NightHandler, "Night")

def DayHandler(discord_server):

    async def DayHandlerAsync():

        if await DetermineWin(innocent_roles, mafia_roles, all_roles) is None:
        
            for player, role in all_roles[discord_server].items():

                if isinstance(role, DayActor):

                    if role.status == "Alive":

                        await player.send(f"you are {'an' if [vowel for vowel in vowels if vowel == role.__class__.__name__[0]] else 'a'} {role.__class__.__name__}")

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

            if role.status == "Alive":
                
                await player.send(f"you are {'an' if [vowel for vowel in vowels if vowel == role.__class__.__name__[0]] else 'a'} {role.__class__.__name__}")

    asyncio.create_task(NightHandlerAsync())