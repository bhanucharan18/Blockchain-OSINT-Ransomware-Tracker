import requests
from ransomware_db import known_ransomware_wallets


def get_wallet_transactions(wallet_address):
    url = f"https://api.blockcypher.com/v1/btc/main/addrs/{wallet_address}/full"
    response = requests.get(url)

    if response.status_code == 200:
        data = response.json()
        print(f"[+] Found {len(data['txs'])} transactions")

        for tx in data['txs'][:5]:
            print("TX:", tx['hash'])
            print("Amount:", tx['total'] / 1e8, "BTC")
            print("Confirmations:", tx['confirmations'])
            print("-" * 40)
        return data
    else:
        print("[-] API Error")
        return None


def check_wallet(wallet):
    for group, wallets in known_ransomware_wallets.items():
        if wallet in wallets:
            return f"[!] Wallet linked to {group} ransomware"
    return "[+] No ransomware match"
