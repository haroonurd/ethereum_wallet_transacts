#!/usr/bin/env python3
import argparse
import csv 
from decimal import Decimal
from helpers import get_eth_balance, get_normal_txs, get_token_txs
from dotenv import load_dotenv

load_dotenv() 

ETH_DECIMALS = Decimal(10**18)

def summarize_address(address: str) -> dict:
    address = address.strip()
    print(f"\n=== Address: {address} ===")

    balance = get_eth_balance(address)
    txs_resp = get_normal_txs(address)
    txs = txs_resp.get('result') if isinstance(txs_resp, dict) else []
    total_txs = len(txs)
    total_sent = Decimal(0)
    total_received = Decimal(0)

    for tx in txs:
        value_wei = Decimal(int(tx.get('value', 0)))
        value_eth = value_wei / ETH_DECIMALS
        if tx.get('from', '').lower() == address.lower():
            total_sent += value_eth
        if tx.get('to', '').lower() == address.lower():
            total_received += value_eth

    tok_resp = get_token_txs(address)
    token_transfers = tok_resp.get('result') if isinstance(tok_resp, dict) else []

    token_balances = {}
    for t in token_transfers:
        contract = t.get('contractAddress')
        token_symbol = t.get('tokenSymbol') or 'UNKNOWN'
        token_decimals = int(t.get('tokenDecimal') or 0)
        val = Decimal(int(t.get('value') or 0)) / (Decimal(10) ** token_decimals)
        if contract not in token_balances:
            token_balances[contract] = {'symbol': token_symbol, 'balance': Decimal(0)}
        if t.get('from', '').lower() == address.lower():
            token_balances[contract]['balance'] -= val
        if t.get('to', '').lower() == address.lower():
            token_balances[contract]['balance'] += val

    summary = {
        'address': address,
        'eth_balance': balance,
        'total_txs': total_txs,
        'total_sent_eth': total_sent,
        'total_received_eth': total_received,
        'token_balances': token_balances,
    }
    return summary

def print_and_save_summary(summary: dict):
    addr = summary['address']
    print(f"Balance: {summary['eth_balance']} ETH")
    print(f"Total txs: {summary['total_txs']}")
    print(f"Total sent: {summary['total_sent_eth']} ETH")
    print(f"Total received: {summary['total_received_eth']} ETH")
    print("\nToken balances (approx, from transfer history):")
    for c, info in summary['token_balances'].items():
        print(f" - {info['symbol']} ({c}): {info['balance']}")

    csv_name = f"report_{addr}.csv"
    with open(csv_name, 'w', newline='') as f:
        w = csv.writer(f)
        w.writerow(['address', 'eth_balance', 'total_txs', 'total_sent_eth', 'total_received_eth'])
        w.writerow([addr, str(summary['eth_balance']), summary['total_txs'], str(summary['total_sent_eth']), str(summary['total_received_eth'])])
    print(f"\nSaved summary CSV to {csv_name}")

if __name__ == '__main__':
    p = argparse.ArgumentParser()
    p.add_argument('--address', help='single Ethereum address to check')
    p.add_argument('--address-file', help='file with addresses, one per line')
    args = p.parse_args()

    if not args.address and not args.address_file:
        p.print_help()
        raise SystemExit(1)

    addresses = []
    if args.address:
        addresses.append(args.address)
    if args.address_file:
        with open(args.address_file) as fh:
            for line in fh:
                line = line.strip()
                if line:
                    addresses.append(line)

    for addr in addresses:
        summary = summarize_address(addr)
        print_and_save_summary(summary)
