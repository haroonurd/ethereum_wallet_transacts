import os
import requests
from decimal import Decimal
from dotenv import load_dotenv

load_dotenv()
ETHERSCAN_API_KEY = os.getenv('ETHERSCAN_API_KEY')
ETHERSCAN_BASE = 'https://api.etherscan.io/api'

def etherscan_get(params: dict):
    params = params.copy()
    params['apikey'] = ETHERSCAN_API_KEY
    r = requests.get(ETHERSCAN_BASE, params=params, timeout=20)
    r.raise_for_status()
    resp = r.json()
    if resp.get('status') not in ("1", 1):
        return resp
    return resp

def get_eth_balance(address: str) -> Decimal:
    params = {
        'module': 'account',
        'action': 'balance',
        'address': address,
        'tag': 'latest'
    }
    resp = etherscan_get(params)
    wei = int(resp.get('result', 0))
    return Decimal(wei) / Decimal(10**18)

def get_normal_txs(address: str, startblock: int = 0, endblock: int = 99999999, sort: str = 'asc'):
    params = {
        'module': 'account',
        'action': 'txlist',
        'address': address,
        'startblock': startblock,
        'endblock': endblock,
        'sort': sort
    }
    return etherscan_get(params)

def get_token_txs(address: str, startblock: int = 0, endblock: int = 99999999, sort: str = 'asc'):
    params = {
        'module': 'account',
        'action': 'tokentx',
        'address': address,
        'startblock': startblock,
        'endblock': endblock,
        'sort': sort
    }
    return etherscan_get(params)
