import discord
from discord.ext import commands
from PopulateGame import *
from Roles import Mafia
from MainGameLoop import ChangePhase
from bottoken import TOKEN

servers = {}
ongoing_games = {}

bot = commands.Bot(command_prefix = "!")

@bot.event
async def on_ready():

    print("Ready")


async def AddUserToLobby(ctx):

    for key, value in servers.items():

        if ctx.author in value:

            await ctx.send(f"You are already in a lobby {ctx.author.name}")
            raise Exception

    if ctx.guild in servers.keys():

        servers[ctx.guild].append(ctx.author)

    else:

        servers[ctx.guild] = [ctx.author]

@bot.command()
async def mafStart(ctx):

    await AddUserToLobby(ctx)
    await ctx.send(f"Okay, setting up the lobby. I have added {ctx.author.name} to it")
    await ctx.send(f"Anyone else who would like to join, type !join")
    await ctx.send(f"Type !start when everyone is ready (minimum is 8 people)")

@bot.command()
async def join(ctx):

    if ctx.guild in servers.keys():

        try:

            await AddUserToLobby(ctx)

        except Exception:

            return

        await ctx.send(f"Added {ctx.author.name} to the lobby")

@bot.command()
async def start(ctx):

    if servers[ctx.guild].count != 8:

        await CreateMafiaChannel(ctx, TestPopulateGame(servers[ctx.guild]))

        if ctx.guild not in ongoing_games.keys():

            ongoing_games[ctx.guild] = ChangePhase(ctx)


async def CreateMafiaChannel(ctx, all_roles: dict):

    server = ctx.guild
    channels = ctx.guild.channels
    everyone_overwrite = discord.PermissionOverwrite()
    maf_overwrite = discord.PermissionOverwrite()
    everyone_overwrite.view_channel = False
    maf_overwrite.view_channel = True

    maf_bot_role = await determine_bot_role(server)

    if "mafia-chat" not in channels:
        await ctx.send("Creating the channel for Mafia")
        current_channel = ctx.message.channel.category

        # Not sure what this is for
        global maf_channel

        maf_channel = await server.create_text_channel("mafia-chat", category=current_channel)
        await maf_channel.set_permissions(maf_bot_role, overwrite=maf_overwrite, reason="Mafia Game")

        for player, role in all_roles.items():
            if isinstance(role, Mafia):
                await maf_channel.set_permissions(player, overwrite=maf_overwrite, reason="Mafia Game")

        await maf_channel.set_permissions(server.default_role, overwrite=everyone_overwrite, reason="Mafia Game")
        await ctx.send("Done!")


async def determine_bot_role(server):
    for server_roles in server.roles:
        # TODO: a way to determine MafiaBot's name with more precision?
        if "MafiaBot" == server_roles.name:
            maf_bot_role = server_roles
    if maf_bot_role is None:
        raise Exception("Bot cannot find it's role, likely searching for the wrong username")
    return maf_bot_role


@bot.command()
async def quitGame(ctx):
    try:
        await ctx.message.channel.set_permissions(ctx.guild.default_role, overwrite=None)

    except:
        pass

    try:
        await maf_channel.delete()

    except:
        pass

    ongoing_games[ctx.guild].cog_unload()

bot.run(TOKEN)
