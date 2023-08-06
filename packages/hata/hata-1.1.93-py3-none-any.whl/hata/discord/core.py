﻿__all__ = ('APPLICATIONS', 'APPLICATION_COMMANDS', 'CHANNELS', 'CLIENTS', 'DISCOVERY_CATEGORIES', 'EMOJIS', 'EULAS',
    'GUILDS', 'INTEGRATIONS', 'INVITES', 'KOKORO', 'MESSAGES', 'ROLES', 'SCHEDULED_EVENTS', 'STAGES', 'STICKERS',
    'STICKER_PACKS', 'TEAMS', 'USERS')

import sys, gc

from ..backend.utils import WeakValueDictionary, WeakKeyDictionary
from ..backend.event_loop import EventThread

CHANNELS = WeakValueDictionary()
CLIENTS = {}
EMOJIS = WeakValueDictionary()
GUILDS = WeakValueDictionary()
INTEGRATIONS = WeakValueDictionary()
MESSAGES = WeakValueDictionary()
ROLES = WeakValueDictionary()
TEAMS = WeakValueDictionary()
USERS = WeakValueDictionary()
DISCOVERY_CATEGORIES = WeakValueDictionary()
EULAS = WeakValueDictionary()
APPLICATIONS = WeakValueDictionary()
INVITES = WeakValueDictionary()
APPLICATION_COMMANDS = WeakValueDictionary()
INTERACTION_EVENT_RESPONSE_WAITERS = WeakValueDictionary()
INTERACTION_EVENT_MESSAGE_WAITERS = WeakKeyDictionary()
APPLICATION_ID_TO_CLIENT = {}
STAGES = WeakValueDictionary()
STICKERS = WeakValueDictionary()
STICKER_PACKS = WeakValueDictionary()
SCHEDULED_EVENTS = WeakValueDictionary()

KOKORO = EventThread(daemon=False, name='KOKORO')
