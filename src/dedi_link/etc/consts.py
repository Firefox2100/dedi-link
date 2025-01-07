"""
This module contains the constants used in the decentralised discovery link.
"""

import logging


MESSAGE_ATTRIBUTES = 'messageAttributes'
MESSAGE_DATA = 'messageData'
MESSAGE_ID_PATH = f'{MESSAGE_ATTRIBUTES}.messageID'
NODE_ID_PATH = 'messageAttributes.nodeID'

AUTH_TYPE_PATH = f'{MESSAGE_ATTRIBUTES}.authType'
STATUS_PATH = f'{MESSAGE_ATTRIBUTES}.status'

LOGGER = logging.getLogger('Decentralised Discovery Link')

PUBLIC_REACHABLE = True
