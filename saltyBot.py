#! /usr/bin/env python3
# coding: utf-8

import asyncio
import datetime
import re
import json
import discord

class BadCommandSyntaxError(Exception):
    pass


class IncorrectArgumentTypeError(Exception):
    pass


class UnauthorizedError(Exception):
    pass


config_file = open('config.json', 'r+')
config_json = json.load(config_file)

client = discord.Client()

def get_role_index(server, role_name):
    role_list = list(map(lambda x: str(x), server.roles))

    role_index = role_list.index(role_name) if role_name in role_list else None
    return role_index

async def kick_member(message):
    try:
        is_authorized = False
        for role_id in list(map(lambda x: x.id, message.author.roles)):
            if role_id in config_json["moderatorRanks"]:
                is_authorized = True
                break

        if not is_authorized:
            raise UnauthorizedError("Not authorized (Kick command)")
        
        args_match = re.match(r"!kick ([\w]+#[0-9]{4}|\"[\w ]+#[0-9]{4}\")( *[0-9]*)$",
                              message.content, re.UNICODE)

        if not args_match:
            raise BadCommandSyntaxError("Bad command syntax !")

        if len(args_match.group(2)) == 0:
            kick_duration = 5
        else:
            try:
                kick_duration = int(args_match.group(2))
                assert kick_duration > 0
            except:
                raise IncorrectArgumentTypeError("Bad kick duration")

        # Clean nom membre (on enlève les guillemets)
        member_name = args_match.group(1).replace('"', '')
        member_to_kick = message.server.get_member_named(member_name)

        role_name = "Kicked from " + str(message.channel)

        role_index = get_role_index(message.channel.server, role_name)

        if role_index is None:
            await client.create_role(message.channel.server, name=role_name,
                                     colour=discord.Colour.dark_red())

        # On ajoute le rôle de kické du chan au batar

        await client.add_roles(member_to_kick, message.channel.server.roles[role_index])
        await client.send_message(message.channel, member_name + " a été kick du salon pour " +
                                  str(kick_duration) + " minute(s).")
        
        print("[" + datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S") + "] Kick : " +
              member_name + " (" + str(kick_duration) + " minute(s))")

        # Attente fin kick & on enlève le rôle au kické

        await asyncio.sleep(60 * kick_duration)

        role_index = get_role_index(message.channel.server, role_name)
        await client.remove_roles(member_to_kick, message.channel.server.roles[role_index])
    except UnauthorizedError:
        await client.send_message(message.channel, "Vous n'êtes pas autorisé à utiliser cette commande")
    except BadCommandSyntaxError:
        await client.send_message(message.channel,
                                  "Syntaxe incorrecte : !kick <nomDuBatardAKick> [<kickDuration>]")
    except IncorrectArgumentTypeError:
        await client.send_message(message.channel, "Le temps d'exclusion doit être un entier positif")

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
            role_name = 'Kicked from ' + str(channel)
            role_index = get_role_index(channel.server, role_name)
            
            if role_index is None:
                await client.create_role(channel.server, name=role_name,
                                         colour=discord.Colour.dark_red())

            chan_perms = channel.overwrites_for(channel.server.roles[role_index])
            chan_perms.update(connect=False)
        else:
            role_name = 'Kicked from ' + str(channel)
            role_index = get_role_index(channel.server, role_name)
            
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
        await kick_member(message)
    elif message.content.startswith('!close'):
        await client.close()

client.run(config_json["apiKey"])
