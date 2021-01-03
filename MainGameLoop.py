
from discord.ext import tasks, commands
import discord

class ChangePhase(commands.Cog):

    def __init__(self, ctx, players: list, currentPhase = "Day"):

        self.currentPhase = currentPhase
        self.players = players

        if self.currentPhase == "Day":

            self.DayPhase.start()

        elif self.currentPhase == "Vote":

            self.VotePhase.start()

        else:

            self.NightPhase.start()

        self.first_iter = True
        self.ctx = ctx

    def cog_unload(self):
        self.DayPhase.cancel()
        self.VotePhase.cancel()
        self.NightPhase.cancel()
        self.counter.cancel()
        

    @tasks.loop(seconds=15)
    async def DayPhase(self):

        self.currentPhase = "Day"
        everyone_overwrite = discord.PermissionOverwrite()

        for player in self.players:

            await self.ctx.message.channel.set_permissions(player, overwrite=None, reason="Mafia Game")

        if not self.first_iter:

            self.first_iter = True
            self.DayPhase.cancel()
            self.VotePhase.start()
            return
            
        await self.ctx.send(f"It is now Day Time, the chat is open for discussion")
        self.first_iter = False

    @tasks.loop(seconds=10)
    async def VotePhase(self):

        self.currentPhase = "Vote"

        if not self.first_iter:

            self.first_iter = True
            self.VotePhase.cancel()
            self.NightPhase.start()
            return
            
        await self.ctx.send(f"It is now Voting Time, type !vote @user to vote for who you think is guilty")
        self.first_iter = False

    @tasks.loop(seconds=15)
    async def NightPhase(self):

        self.currentPhase = "Night"

        if not self.first_iter:

            self.first_iter = True
            self.NightPhase.cancel()
            self.DayPhase.start()
            return
            
        await self.ctx.send(f"It is now night time, I will lock this chat for typing until day time")
        everyone_overwrite = discord.PermissionOverwrite()
        everyone_overwrite.send_messages = False
        await self.ctx.message.channel.set_permissions(self.ctx.guild.default_role, overwrite=everyone_overwrite, reason="Mafia Game")
        self.first_iter = False
