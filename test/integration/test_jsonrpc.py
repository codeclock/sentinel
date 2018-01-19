import pytest
import sys
import os
import re
os.environ['SENTINEL_ENV'] = 'test'
os.environ['SENTINEL_CONFIG'] = os.path.normpath(os.path.join(os.path.dirname(__file__), '../test_sentinel.conf'))
sys.path.append(os.path.join(os.path.dirname(__file__), '..', '..', 'lib'))
sys.path.append(os.path.join(os.path.dirname(__file__), '..', '..'))
import config

from suppod import SuppoDaemon
from suppo_config import SuppoConfig


def test_suppod():
    config_text = SuppoConfig.slurp_config_file(config.suppo_conf)
    network = 'mainnet'
    is_testnet = False
    genesis_hash = u'000001618879078e4db50cd72d7ade5c6035b60fc63de0db013bd41e2dfea05e'
    for line in config_text.split("\n"):
        if line.startswith('testnet=1'):
            network = 'testnet'
            is_testnet = True
            genesis_hash = u'00000f90bc98b16e5635ac46ef972eeaee9ff2381f15c4869f8613a5cb7f2b61'

    creds = SuppoConfig.get_rpc_creds(config_text, network)
    suppod = SuppoDaemon(**creds)
    assert suppod.rpc_command is not None

    assert hasattr(suppod, 'rpc_connection')

    # Suppo testnet block 0 hash == 00000f90bc98b16e5635ac46ef972eeaee9ff2381f15c4869f8613a5cb7f2b61
    # test commands without arguments
    info = suppod.rpc_command('getinfo')
    info_keys = [
        'blocks',
        'connections',
        'difficulty',
        'errors',
        'protocolversion',
        'proxy',
        'testnet',
        'timeoffset',
        'version',
    ]
    for key in info_keys:
        assert key in info
    assert info['testnet'] is is_testnet

    # test commands with args
    assert suppod.rpc_command('getblockhash', 0) == genesis_hash
