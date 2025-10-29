# ethereum_wallet_transacts

Python-based Ethereum wallet transaction tracker.

## Overview
Track and summarize wallet transactions across Ethereum accounts.

## Features
- Fetch transaction history for one or multiple wallets
- Summarize sent/received ETH and ERC20 transfers
- Supports mainnet and testnets
- Generates CSV or JSON output for further analysis

## Installation
```bash
git clone <repo-url>
cd ethereum_wallet_transacts
pip install -r requirements.txt
```
Set environment variables (optional):
```
RPC_URL=https://mainnet.infura.io/v3/YOUR_INFURA_KEY
```

## Usage
```bash
python wallet_tracker.py --wallet <wallet_address>
```

## Sample Output
```json
{
  "wallet": "0x...",
  "transactions": [
    {"hash": "0x...", "from": "0x...", "to": "0x...", "value": 0.5, "token": "ETH"}
  ]
}
```

## License
MIT
