"""
The MIT License (MIT)

Copyright (c) 2021-present ThisIsanAlt

Permission is hereby granted, free of charge, to any person obtaining a
copy of this software and associated documentation files (the 'Software'),
to deal in the Software without restriction, including without limitation
the rights to use, copy, modify, merge, publish, distribute, sublicense,
and/or sell copies of the Software, and to permit persons to whom the
Software is furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in
all copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED 'AS IS', WITHOUT WARRANTY OF ANY KIND, EXPRESS
OR IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING
FROM, OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER
DEALINGS IN THE SOFTWARE.
"""

import requests
from threading import Event
import json
from math import sqrt
from errors import *
from warnings import warn

class HypixelConnection():
    """
    Base class to handle connecting to Hypixel.
    """

    def __init__(self, api_key):
        """:arg api_key: Hypixel API key"""
        self.api_key = api_key
        if len(api_key) != 37:
            raise InvalidAPIKey(f'API key {api_key} is too long '+
            'or too short.')

        self.uuids = {}  # Store UUIDs to stay within Mojang rate limits
        
        # Store values for duels prestige
        self.duelsprestigemode = {
            50:'Rookie',
            60:'Rookie II',
            70:'Rookie III',
            80:'Rookie IV',
            90:'Rookie V',
            100:'Iron',
            120:'Iron II',
            140:'Iron III',
            160:'Iron IV',
            180:'Iron V',
            200:'Gold',
            260:'Gold II',
            320:'Gold III',
            380:'Gold IV',
            440:'Gold V',
            500:'Diamond',
            600:'Diamond II',
            700:'Diamond III',
            800:'Diamond IV',
            900:'Diamond V',
            1000:'Master',
            1200:'Master II',
            1400:'Master III',
            1600:'Master IV',
            1800:'Master V',
            2000:'Legend',
            2600:'Legend II',
            3200:'Legend III',
            3800:'Legend IV',
            4400:'Legend V',
            5000:'Grandmaster',
            6000:'Grandmaster II',
            7000:'Grandmaster III',
            8000:'Grandmaster IV',
            9000:'Grandmaster V',
            10000:'Godlike',
            12000:'Godlike II',
            14000:'Godlike III',
            16000:'Godlike IV',
            18000:'Godlike V',
            20000:'Godlike VI',
            22000:'Godlike VII',
            24000:'Godlike VIII',
            26000:'Godlike IX',
            28000:'Godlike X',
        }
        self.duelsprestigemode = {
            100:'Rookie',
            120:'Rookie II',
            140:'Rookie III',
            160:'Rookie IV',
            180:'Rookie V',
            200:'Iron',
            240:'Iron II',
            280:'Iron III',
            320:'Iron IV',
            360:'Iron V',
            400:'Gold',
            520:'Gold II',
            640:'Gold III',
            760:'Gold IV',
            880:'Gold V',
            1000:'Diamond',
            1200:'Diamond II',
            1400:'Diamond III',
            1600:'Diamond IV',
            1800:'Diamond V',
            2000:'Master',
            2400:'Master II',
            2800:'Master III',
            3200:'Master IV',
            3600:'Master V',
            4000:'Legend',
            5200:'Legend II',
            6400:'Legend III',
            7600:'Legend IV',
            8800:'Legend V',
            10000:'Grandmaster',
            12000:'Grandmaster II',
            14000:'Grandmaster III',
            16000:'Grandmaster IV',
            18000:'Grandmaster V',
            20000:'Godlike',
            24000:'Godlike II',
            28000:'Godlike III',
            32000:'Godlike IV',
            36000:'Godlike V',
            40000:'Godlike VI',
            44000:'Godlike VII',
            48000:'Godlike VIII',
            52000:'Godlike IX',
            56000:'Godlike X',
        }

    def get_player_stats(self, username, uuid):
        """
        Returns the Hypixel API stats for that player, with additions
        such as KDR and WLR. Check the docs for more info about
        changes.

        :kwarg username (optional): The username of the player.
        :kwarg uuid (optional): The uuid of the player.

        Raises InvalidPlayer if the player cannot be found.
        Raises NoResponse if Hypixel cannot respond to requests.
        Raises InvalidAPIKey if the API key is invalid.
        """

        if username is None and uuid is None:
            raise InvalidPlayer('Username or UUID was not provided.')

        # Get UUID from Mojang and cache the result
        if (username is not None) and (username not in self.uuids):
            try:
                uuid = requests.get(f'https://api.mojang.com/users/profiles/minecraft/{username}').json()['id']
            except json.decoder.JSONDecodeError:
                raise InvalidPlayer(f'IGN {username} not found.')
            else:
                self.uuids[username] = uuid

        # Get dict from Hypixel
        try:
            data = requests.get(f'https://api.hypixel.net/player?key={self.api_key}&uuid={uuid}').json()
        except json.decoder.JSONDecodeError:
            raise NoResponse('No response from Hypixel; Is there an API outage?')

        # Check to ensure nothing has gone wrong
        if not data['success']:
            if data['cause'] == 'Key throttle':
                retries = 0
                while retries < 4:
                    Event().wait(.5)
                    data = requests.get(f'https://api.hypixel.net/player?key={self.api_key}&uuid={uuid}').json()
                    if data['success']:
                        break
                    retries += 1
                    continue
                if not data['success']:
                    raise Ratelimited('Max retries exceeded, (3/3)')
            
            # fix
            elif data['cause'] == 'uuid':
                raise InvalidPlayer(f'UUID {uuid} is invalid.')

            elif data['cause'] == 'Invalid API key':
                raise InvalidAPIKey(f'API key {self.api_key} is invalid')
            else:
                raise HypixelException(f'{data["cause"]}')                
        elif data['player'] == 'null':
            if username is not None:
                raise InvalidPlayer(f'IGN {username} has never logged onto Hypixel.')
            else:
                raise InvalidPlayer(f'UUID {uuid} has never logged onto Hypixel.')
        
        data['player']['IGN'] = data['player'].get('display_name', data['player'].get('playername'))
        data['player']['rank'] = data['player']['newPackageRank'] if not data['player']['monthlyPackageRank'] else 'MVP_PLUS_PLUS'
        data['player']['networkLVL'] = round(((sqrt((2 * data['player']['networkExp']) + 30625) / 50) - 2.5), 2)
        data['player']['stats']['Duels']['melee_misses'] = data['player']['stats']['Duels']['melee_swings'] - data['player']['stats']['Duels']['melee_hits']
        data['player']['stats']['Duels']['melee_hit_miss_ratio'] = data['player']['stats']['Duels']['melee_swings'] / data['player']['stats']['Duels']['melee_misses']
        data['player']['stats']['Duels']['win_loss_ratio'] = data['player']['stats']['Duels']['wins'] / ['player']['stats']['Duels']['losses']
        data['player']['stats']['Duels']['kill_death_ratio'] = ['player']['stats']['Duels']['kills'] / ['player']['stats']['Duels']['deaths']
        return data

class Player(HypixelConnection):
    """
    Gets stats for a player using functions. Useful if you wish to
    avoid dicts.
    """

    def __init__(self, cls, username=None, uuid=None):
        """
        :arg cls: A HypixelConnection instance.
        :arg username: The username of the player.
        :arg uuid: The uuid of the player.
        """
        self.cls = cls
        self.api_key = cls.api_key
        self.username = username
        self.uuid = uuid

        if username is not None:
            try:
                uuid = requests.get(f'https://api.mojang.com/users/profiles/minecraft/{username}').json()['id']
            except json.decoder.JSONDecodeError:
                raise InvalidPlayer(f'IGN {username} not found.')
            else:
                self.uuid = uuid
        
        try:
            self.data = requests.get(f'https://api.hypixel.net/player?key={self.api_key}&uuid={uuid}').json()
        except json.decoder.JSONDecodeError:
            raise NoResponse('No response from Hypixel; Is there an API outage?')

        if not self.data['success']:
            if self.data['cause'] == 'Key throttle':
                retries = 0
                while retries < 4:
                    Event().wait(.5)
                    data = requests.get(f'https://api.hypixel.net/player?key={self.api_key}&uuid={uuid}').json()
                    if data['success']:
                        break
                    retries += 1
                    continue
                if not data['success']:
                    raise
            elif self.data['cause'] == 'Invalid API key':
                raise InvalidAPIKey(f'API key {self.api_key} is invalid')
            else:
                raise HypixelException(f'{self.data["cause"]}')
        elif self.data['player'] == 'null':
            raise InvalidPlayer(f'IGN {username} has never logged onto Hypixel.')
