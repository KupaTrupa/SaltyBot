#! /usr/bin/env python3
# coding: utf-8

import asyncio
import datetime
import re
import discord

import errors as err
import utilities as utils
import moderation as mod

config = utils.reload_config()
client = discord.Client()
vote_list = {}

@client.event
async def on_ready():
    channels = client.get_all_channels()
    roles_list = {}

    for channel in channels:
        try:
            roles_list[channel.server.id]
        except:
            for role in channel.server.roles:
                roles_list[role.id] = str(role)

        if str(channel.type) == 'voice':
            role_name = 'Kicked from {}'.format(str(channel))
            role_index = utils.get_role_index(channel.server, role_name)

            if role_index is None:
                await client.create_role(channel.server, name=role_name,
                                         colour=discord.Colour.dark_red())

            chan_perms = channel.overwrites_for(channel.server.roles[role_index])
            chan_perms.update(connect=False)
        else:
            role_name = 'Kicked from {}'.format(str(channel))
            role_index = utils.get_role_index(channel.server, role_name)

            if role_index is None:
                role = await client.create_role(channel.server, name=role_name,
                                                colour=discord.Colour.dark_red())
            else:
                role = channel.server.roles[role_index]

            chan_perms = channel.overwrites_for(role)
            chan_perms.update(send_messages=False, send_tts_messages=False)

    print("System primed !")
    print(roles_list)

@client.event
async def on_message(message):
    if message.content.startswith('!ping'):
        await client.send_message(message.channel, 'PONG !')
    elif message.content.startswith('!kick'):
        await mod.kick_command(message)
    elif message.content.startswith("!reload"):
        try:
            global config
            if not utils.check_if_authorized([role.id for role in message.author.roles], config["json"]["moderatorRoles"]):
                raise err.UnauthorizedError("Not authorized (Kick command)")

            config = reload_config(config)
        except err.UnauthorizedError:
            await client.send_message(message.channel, "Vous n'êtes pas autorisé à utiliser cette commande")
    elif message.content.startswith('!close'):
        await client.close()

client.run(config["json"]["apiKey"])
