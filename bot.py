import discord
from discord.ext import commands
import sys
import traceback
import bot_secrets

# Globala

DESCRIPTION = ""
TOKEN = bot_secrets.TOKEN

bot = commands.Bot(command_prefix="!", description=DESCRIPTION)

# this specifies what extensions to load when the bot starts up
startup_extensions = ["cogs.misc",
                      "cogs.moderation"]

# <------ Events ------>
@bot.event
async def on_ready ():
    print('Logged in.')
    print(bot.user.name)
    print(bot.user.id)
    print('------')


@bot.event
async def on_message(message):
    await bot.process_commands(message)


@bot.event
async def on_command_error(ctx, error):
    """The event triggered when an error is raised while invoking a command.
    ctx   : Context
    error : Exception"""
    # This prevents any commands with local handlers being handled here in on_command_error.
    if hasattr(ctx.command, 'on_error'):
        return

    ignored = (commands.UserInputError, commands.BadArgument)

    # Allows us to check for original exceptions raised and sent to CommandInvokeError.
    # If nothing is found. We keep the exception passed to on_command_error.
    error = getattr(error, 'original', error)

    # Anything in ignored will return and prevent anything happening.
    if isinstance(error, ignored):
        return

    elif isinstance(error, commands.DisabledCommand):
        return await ctx.send(f'{ctx.command} has been disabled.', delete_after=10)

    elif isinstance(error, commands.NoPrivateMessage):
        try:
            return await ctx.author.send(f'Sorry, {ctx.command} can not be used in Private Messages.')
        except:
            pass
    elif isinstance(error, commands.NotOwner):
        return await ctx.send("This command can only be run by Acey#4962. Please ping him if I'm causing trouble!", delete_after=10)
    elif isinstance(error, commands.MissingPermissions):
        return await ctx.send(error.message, delete_after=10)

    # All other Errors not returned come here... And we can just print the default TraceBack.
    print('Ignoring exception in command {}:'.format(ctx.command), file=sys.stderr)
    traceback.print_exception(type(error), error, error.__traceback__, file=sys.stderr)

# <------ Commands ------>
@bot.command()
@commands.is_owner()
async def disconnect():
    """Disconnect"""
    print('Exit command received. Ending process.')
    await bot.logout()
    exit()


@bot.command()
@commands.is_owner()
async def load(ctx, extension_name : str):
    """Loads an extension."""
    try:
        bot.load_extension(extension_name)
    except (AttributeError, ImportError) as e:
        await ctx.send("```py\n{}: {}\n```".format(type(e).__name__, str(e)))
        return
    await ctx.send("{} loaded.".format(extension_name))


@bot.command()
@commands.is_owner()
async def unload(ctx, extension_name : str):
    """Unloads an extension."""
    bot.unload_extension(extension_name)
    await ctx.send("{} unloaded.".format(extension_name))


@bot.command()
@commands.is_owner()
async def reload(ctx, extension_name : str):
    """Reloads an extension."""
    bot.unload_extension(extension_name)
    await ctx.send("Working...")
    try:
        bot.load_extension(extension_name)
    except (AttributeError, ImportError) as e:
        await ctx.send("```py\n{}: {}\n```".format(type(e).__name__, str(e)))
        return
    await ctx.send(f'{extension_name} reloaded successfully.')


if __name__ == "__main__":
    for extension in startup_extensions:
        try:
            bot.load_extension(extension)
        except Exception as e:
            exc = '{}: {}'.format(type(e).__name__, e)
            print('Failed to load extension {}\n{}'.format(extension, exc))

    bot.run(TOKEN)
