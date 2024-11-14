from datetime import datetime

def verify_property(data, property_name):
    if data is None: return None
    if property_name in data:  # Check if property_name exists in data dictionary
        if data[property_name]:  # Check if property_name value is not None to avoid TypeError
            return data[property_name]
    return None

def build_db_message(data):
    content = verify_property(data, 'content')
    channel_id = verify_property(data, 'channel_id')
    guild_id = verify_property(data, 'guild_id')
    user_id = verify_property(verify_property(data, 'author'), 'id')
    timestamp = verify_property(data, 'timestamp')
    embeds = verify_property(data, 'embeds')
    components = verify_property(data, 'components')
    attachments = verify_property(data, 'attachments')
    mentions = verify_property(verify_property(data, 'mentions'), 'users')
    message_id = verify_property(data, 'id')

    referenced_message_id = None
    referenced_message = verify_property(data, 'referenced_message')
    if referenced_message:
        referenced_message_id = verify_property(referenced_message, 'id')



    #TODO handle timestamp to unix timestamp
    dt = datetime.strptime(timestamp, "%Y-%m-%dT%H:%M:%S.%fZ")
    unix_ts = int(dt.timestamp())
    result = {
        'content': content,
        'channel_id': channel_id,
        'guild_id': guild_id,
        'user_id': user_id,
        'timestamp': unix_ts,
        'embeds': embeds,
        'components': components,
        'attachments': attachments,
        'mentions': mentions,
        'reference': referenced_message_id,
        'id': message_id

    }

    return result


def build_db_guild(data):
    print("Verify this data for building a guild object:")
    print(data)
    guild_id = verify_property(data, 'id')
    name = verify_property(data, 'name')
    icon = verify_property(data, 'icon')
    owner = verify_property(data, 'ownerId')
    region = verify_property(data, 'region')
    member_count = verify_property(data, 'memberCount')
    verification_level = verify_property(data, 'verificationLevel')
    permissions = verify_property(data, 'permissions')
    features = verify_property(data, 'features')

    result = {
        'id': guild_id,
        'name': name,
        'icon': icon,
        'owner': owner,
        'region': region,
        'member_count': member_count,
        'verification_level': verification_level,
        'permissions': permissions,
        'features': features
    }
    return result


def build_db_user(data):
    user_id = verify_property(data, 'id')
    username = verify_property(data, 'username')
    global_name = verify_property(data, 'global_name')
    avatar = verify_property(data, 'avatar')
    flags = verify_property(data, 'flags')
    accent_color = verify_property(data, 'accent_color')
    bot = verify_property(data, 'bot')
    bio = verify_property(data, 'bio')
    pronouns = verify_property(data, 'pronouns')
    banner = verify_property(data, 'banner')
    banner_color = verify_property(data, 'banner_color')
    public_flags = verify_property(data, 'public_flags')
    mutual_friends_count = verify_property(data, 'mutual_friends_count')

    result = {
        'id': user_id,
        'username': username,
        'global_name': global_name,
        'avatar': avatar,
        'flags': flags,
        'accent_color': accent_color,
        'banner': banner,
        'banner_color': banner_color,
        'bot': bot,
        'bio': bio,
        'pronouns': pronouns,
        'public_flags': public_flags,
        'mutual_friends_count': mutual_friends_count,
    }
    return result


def build_db_channel(data):
    channel_id = verify_property(data, 'id')
    name = verify_property(data, 'name')
    type = verify_property(data, 'type')
    topic = verify_property(data, 'topic')
    last_message_id = verify_property(data, 'lastMessageId')
    nsfw = verify_property(data, 'nsfw')

    result = {
        'id': channel_id,
        'name': name,
        'type': type,
        'topic': topic,
        'last_message_id': last_message_id,
        'nsfw': nsfw,
    }
    return result



