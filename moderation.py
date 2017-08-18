import asyncio
import re

import discord
import utilities as utils
import errors as err

def temp_ban(server, channel_name, user, ban_duration = 0):
    role_index = utils.get_role_index(message.channel.server, "Kicked from " + channel_name)

    await client.add_roles(member_to_kick, message.channel.server.roles[role_index])

    if ban_duration > 0:
        await client.send_message(message.channel, "{} a été banni du salon pour {} minute{}.".format(member_name), channel_name, "s" if ban_duration > 1 else "")

    await asyncio.sleep(60 * ban_duration)

    role_index = utils.get_role_index(message.channel.server, role_name)
    await client.remove_roles(member_to_kick, message.channel.server.roles[role_index])

async def kick_command(message, config):
    try:
        if utils.check_if_authorized([role.id for role in message.author.roles], config["json"]["moderatorRoles"]):
            raise err.UnauthorizedError("Vous n'êtes pas autorisé à utiliser cette commande")

        args_match = re.match(r"!kick ([\w]+#[0-9]{4}|\"[\w ]+#[0-9]{4}\")$", message.content, re.UNICODE)

        if not args_match:
            raise err.BadCommandSyntaxError("Syntaxe incorrecte : !kick <nomDuBatardAKick>")

        member_to_kick = message.server.get_member_named(args_match.group(1))
        await temp_ban(message.channel.server, str(message.channel), member_to_kick)

    except Exception as e:
        await client.send_message(message.channel, str(e))

async def vote_kick_command(message, config, vote_list):
    try:
        if not utils.check_if_in_active_voice_chan(message.author):
            raise err.NotInActiveVoiceChannelError("Vous n'êtes pas dans un salon vocal actif !")

        args_match = re.match(r"!vkick ([\w]+#[0-9]{4}|\"[\w ]+#[0-9]{4}\")$", message.content, re.UNICODE)

        if not args_match:
            raise err.BadCommandSyntaxError("Syntaxe incorrecte : !vkick <nomDuBatardAKick>")

        member_to_kick = message.server.get_member_named(args_match.group(1))
        if not utils.check_if_in_active_voice_chan(member_to_kick):
            raise err.NotInActiveVoiceChannelError("L'utilisateur ciblé n'est pas dans un salon vocal actif !")

    except Exception as e:
        await client.send_message(message.channel, str(e))

async def vote_yes_kick_command():
    pass

async def vote_no_kick_command():
    pass

async def tempban_command(message, config):
    pass

async def ban_command(message, config):
    pass

async def servban_command(message, config):
    try:
        if not utils.check_if_authorized(message.author, config["json"]["moderatorRoles"]):
            raise err.UnauthorizedError("Vous n'êtes pas autorisé à utiliser cette commande")

        args_match = re.match(r"!servban ([\w]+#[0-9]{4}|\"[\w ]+#[0-9]{4}\")$", message.content, re.UNICODE)

        if not args_match:
            raise err.BadCommandSyntaxError("Syntaxe incorrecte : !servban <nomDuBatardAKick>")

        member_to_kick = message.server.get_member_named(args_match.group(1))

    except Exception as e:
        client.send_message(message.channel, str(e))
