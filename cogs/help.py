"""coding: UTF-8, coding by: discordtag: chaemoong#9454"""
from discord.ext import commands
import discord
from os import listdir
from os.path import isfile, join
import traceback

class Embed(commands.Cog):

    def __init__(self, bot):
        self.bot = bot

    @commands.command(name='help', description='The help command!', aliases=['commands', 'command'])
    async def help_command(self, ctx, cog='all'):
        
        # The third parameter comes into play when
        # only one word argument has to be passed by the user

        # Prepare the embed

        author = ctx.author
        help_embed = discord.Embed(
            title='Help',
            color=author.colour
        )
        help_embed.set_thumbnail(url=self.bot.user.avatar_url)
        if author.avatar_url:
            help_embed.set_footer(text=f'Request By {author}', icon_url=author.avatar_url)
        else:
            help_embed.set_footer(text=f'Request By {author}')

        cogs = [c for c in self.bot.cogs.keys()]
        if cog == 'all':
            for cog in cogs:
                cog_commands = self.bot.get_cog(cog).get_commands()
                commands_list = ''
                for comm in cog_commands:
                    commands_list += f'`{comm.name}`, '             
                if not cog == 'error':
                    help_embed.add_field(
                        name=cog,
                        value=commands_list,
                        inline=False
                    )
                if cog == 'notice':
                    pass
                else:
                    pass
        else:

            # If the cog was specified

            lower_cogs = [c.lower() for c in cogs]

            # If the cog actually exists.
            if cog.lower() in lower_cogs:

                # Get a list of all commands in the specified cog
                commands_list = self.bot.get_cog(cogs[ lower_cogs.index(cog.lower()) ]).get_commands()
                help_text=''

                # Add details of each command to the help text
                # Command Name
                # Description
                # [Aliases]
                #
                # Format
                for command in commands_list:
                    help_text += f'{ctx.prefix}{command.name} - {command.description}\n'

                    # Also add aliases, if there are any
                    if len(command.aliases) > 0:
                        help_text += f'**다른 이름:** `{"`, `".join(command.aliases)}`\n'
                    # Finally the format
                    help_text += f'사용 방법: `{ctx.prefix}{command.name} {command.usage}`\n----------------------------------------------------------------\n'

                help_embed.description = help_text
            else:
                # Notify the user of invalid cog and finish the command
                await ctx.send('Invalid cog specified.\nUse `help` command to list all cogs.')
                return

        await ctx.send(embed=help_embed)
        
        return


def setup(bot):
    bot.remove_command('help')
    bot.add_cog(Embed(bot))
    # Adds the Basic commands to the bot
    # Note: The "setup" function has to be there in every cog file