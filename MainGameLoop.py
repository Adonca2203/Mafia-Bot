
from discord.ext import tasks, commands
import discord
from pubsub import pub

async def AlertListeners(currentPhase, server):
    
    pub.sendMessage(currentPhase, discord_server=server)

class ChangePhase(commands.Cog):

    def __init__(self, ctx, players: list, voice_channel, currentPhase = "Day"):

        self.currentPhase = currentPhase
        self.players = players
        self.voice_channel = voice_channel
        self.first_iter = True
        self.ctx = ctx
        self.DayPhase.start()

    def cog_unload(self):
        self.DayPhase.cancel()
        self.VotePhase.cancel()
        self.NightPhase.cancel()

    @tasks.loop(seconds=15)
    async def DayPhase(self):

        if not self.first_iter:

            self.first_iter = True
            self.DayPhase.cancel()
            self.VotePhase.start()
            return

        self.currentPhase = "Day"
        players_to_msg = await AlertListeners(self.currentPhase, self.ctx.guild)

        for player in self.players:

            await self.ctx.message.channel.set_permissions(player, overwrite=None, reason="Mafia Game")
        
        for player in self.voice_channel.members:

            await player.edit(mute=False)
            
        await self.ctx.send(f"It is now Day Time, the chat is open for discussion")
        self.first_iter = False

    @tasks.loop(seconds=10)
    async def VotePhase(self):

        if not self.first_iter:

            self.first_iter = True
            self.VotePhase.cancel()
            self.NightPhase.start()
            return

        self.currentPhase = "Vote"
        await AlertListeners(self.currentPhase, self.ctx.guild)
            
        await self.ctx.send(f"It is now Voting Time, type !vote @user to vote for who you think is guilty")
        self.first_iter = False

    @tasks.loop(seconds=15)
    async def NightPhase(self):

        if not self.first_iter:

            self.first_iter = True
            self.NightPhase.cancel()
            self.DayPhase.start()
            return

        self.currentPhase = "Night"
        await AlertListeners(self.currentPhase, self.ctx.guild)
            
        await self.ctx.send(f"It is now night time, I will lock this chat for typing until day time")
        everyone_overwrite = discord.PermissionOverwrite()
        everyone_overwrite.send_messages = False

        for player in self.players:

            await self.ctx.message.channel.set_permissions(player, overwrite=everyone_overwrite, reason="Mafia Game")
            await self.voice_channel.set_permissions(player, overwrite=everyone_overwrite, reason="Mafia Game")

        for player in self.voice_channel.members:

            await player.edit(mute=True)

        self.first_iter = False