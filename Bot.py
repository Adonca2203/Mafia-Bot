import discord
from discord.ext import commands
from PopulateGame import *
from Roles import Mafia
from MainGameLoop import ChangePhase
from bottoken import TOKEN
from MainGameLogic import CacheAllRoles, CacheGameLoop, Subscribe

servers = {}
ongoing_games = {}
mafia_channels = {}
voice_clients = {}
categories = {}
game_active = {}

bot = commands.Bot(command_prefix = "!")

@bot.event
async def on_ready():

    await Subscribe()
    print("Ready")

#Non Bot Commands

async def AddUserToLobby(ctx):

    for key, value in servers.items():

        if ctx.author in value:

            await ctx.send(f"You are already in a lobby {ctx.author.name}")
            raise Exception

    if servers.get(ctx.guild):

        servers[ctx.guild].append(ctx.author)

    else:

        servers[ctx.guild] = [ctx.author]

async def CreateMafiaChannel(ctx, all_roles: dict):

    server = ctx.guild
    channels = ctx.guild.channels
    everyone_overwrite = discord.PermissionOverwrite()
    maf_overwrite = discord.PermissionOverwrite()
    everyone_overwrite.view_channel = False
    maf_overwrite.view_channel = True

    #maf_bot_role = await determine_bot_role(server)

    await ctx.send("Creating the channel for Mafia")
    new_category = await server.create_category("MAFIA GAME")

    maf_channel = await server.create_text_channel("mafia-chat", category=new_category)
    await maf_channel.set_permissions(bot.user, overwrite=maf_overwrite, reason="Mafia Game")
    new_client = await server.create_voice_channel("mafia-game-voice", category=new_category)
    mafia_channels[ctx.guild] = maf_channel
    voice_clients[ctx.guild] = new_client
    categories[ctx.guild] = new_category

    for player, role in all_roles.items():
        if isinstance(role, Mafia):
            await maf_channel.set_permissions(player, overwrite=maf_overwrite, reason="Mafia Game")
        else:
            await maf_channel.set_permissions(player, overwrite=everyone_overwrite, reason="Mafia Game")

async def GameConclude(ctx, team_class: Role, left_alive: dict):

    #will use left_alive later to display all the remaining roles at end of game dont remove

    await ctx.send(f"The game has concluded")
    await ctx.send(f"Congrats to the {type(team_class).__name__} on the win")

#Bot Commands

@bot.command()
async def mafStart(ctx):

    if not servers.get(ctx.guild):
        await AddUserToLobby(ctx)
        await ctx.send(f"Okay, setting up the lobby. I have added {ctx.author.name} to it")
        await ctx.send(f"Anyone else who would like to join, type !join")
        await ctx.send(f"Type !start when everyone is ready (minimum is 8 people)")

    else:

        await join(ctx)

@bot.command()
async def join(ctx):

    if ctx.guild in servers.keys():

        try:

            await AddUserToLobby(ctx)

        except Exception:

            return

        await ctx.send(f"Added {ctx.author.name} to the lobby")
        await ctx.send(f"Have {servers[ctx.guild].count} players currently")

@bot.command()
async def start(ctx):

    # this is set != 8 for testing with less than 8 players
    if servers[ctx.guild].count != 8:

        server_player_role = {}

        selected_roles = TestPopulateGame(servers[ctx.guild])

        server_player_role[ctx.guild] = selected_roles

        await CreateMafiaChannel(ctx, selected_roles)
        await CacheAllRoles(ctx.guild, server_player_role)

        if ctx.guild not in ongoing_games.keys():

            game_active[ctx.guild] = True
            ongoing_games[ctx.guild] = ChangePhase(ctx, servers[ctx.guild], voice_clients[ctx.guild])
            await CacheGameLoop(ctx.guild, ongoing_games)

@bot.command()
async def quitGame(ctx):

    try:
        for player in servers[ctx.guild]:

            await ctx.message.channel.set_permissions(player, overwrite=None)

        #Unload everthing
        ongoing_games[ctx.guild].cog_unload()
        await voice_clients[ctx.guild].delete()
        await mafia_channels[ctx.guild].delete()
        await categories[ctx.guild].delete()

        #Delete relevant keys and values
        del ongoing_games[ctx.guild]
        del servers[ctx.guild]
        del mafia_channels[ctx.guild]
        del voice_clients[ctx.guild]
        del categories[ctx.guild]

    except:
        pass

bot.run(TOKEN)