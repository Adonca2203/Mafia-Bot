
from Roles import Innocent, Mafia

async def DetermineWin(innocent_list: list, mafia_list: list, all_roles: dict) -> dict or None:

    temp = {}

    if innocent_list.count > mafia_list.count:

        temp[Innocent] = all_roles

        return temp
    
    elif mafia_list.count > innocent_list.count:

        temp[Mafia] = all_roles

        return temp

    return None