# Ethereum Wallet Checker

Small script to query an Ethereum address and report balances, number of transactions, and volume traded.

## Requirements
- Python 3.9+
- An Etherscan API key (free tier available)

## Setup
1. Copy `.env.example` to `.env` and fill your `ETHERSCAN_API_KEY`.
2. (Optional) If you want to use an RPC provider for token balance verification you can set `WEB3_RPC_URL`.
3. Install dependencies:

```bash
python -m venv venv
source venv/bin/activate  # or venv\Scripts\activate on Windows
pip install -r requirements.txt
```

## Usage

```bash
python main.py --address 0x...        # check a single address
python main.py --address-file addresses.txt   # check addresses from a file (one per line)
```

The script prints a human-readable report and writes a CSV (`report_<address>.csv`) containing basic metrics.

## Notes
- Uses Etherscan API (rate limits and historical coverage apply).
- For accurate ERC-20 balances, you may want to query a full node or a provider (Alchemy/Infura/Covalent) depending on needs.
