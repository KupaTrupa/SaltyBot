import json

import discord

def check_if_in_active_voice_chan(user):
    pass

def reload_config(old_config = None):
    config = {}

    if old_config is not None and "file" in old_config:
        old_config["file"].close()
    config["file"] = open('config.json', 'r+')

    config["json"] = json.load(config["file"])
    return config

def get_role_index(server, role_name):
    role_list = list(map(lambda x: str(x), server.roles))

    role_index = role_list.index(role_name) if role_name in role_list else None
    return role_index

def check_if_authorized(user_roles, authorized_roles):
    is_authorized = False
    for role_id in user_roles:
        if role_id in authorized_roles:
            is_authorized = True
            break
    return is_authorized
