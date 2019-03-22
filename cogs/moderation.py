import discord
from discord.ext import commands

class Moderation(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command()
    @commands.guild_only()
    @commands.has_permissions(kick_members = True)
    async def delete(self, ctx, amount: int=1):
        """Delete an amount of messages"""
        await ctx.message.delete()
        await ctx.message.channel.purge(limit=amount)
        await ctx.send(f"Deleted {amount} messages.", delete_after=3)

    @commands.command()
    @commands.guild_only()
    @commands.has_permissions(kick_members = True)
    async def kick(self, ctx, member: discord.Member, for_, *, args: str):
        
        if member.dm_channel == None:
            await member.create_dm()

        reason = ''
        for word in args:
            if word.isspace():
                reason += ' '
            else:
                reason += word

        await member.dm_channel.send(f'You were kicked from **{ctx.guild.name}** for {reason}')
        await ctx.send(f'**{member.name}** was kicked for {reason}')
        
        await member.kick()

    @commands.command()
    @commands.guild_only()
    @commands.has_permissions(ban_members = True)
    async def ban(self, ctx, member: discord.Member, for_, *, args: str):
        
        if member.dm_channel == None:
            await member.create_dm()

        reason = ''
        for word in args:
            if word.isspace(): # Some black magic done on 9:30 PM at 23rd February, 2019. 
                reason += ' '
            else:
                reason += word
        
        await member.dm_channel.send(f'You were banned from **{ctx.guild.name}** for **{reason}**.')
        await ctx.send(f'**{member.name}** was banned for **{reason}**.')
        
        await member.ban()


def setup(bot):
    bot.add_cog(Moderation(bot))
