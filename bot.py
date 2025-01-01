from web3 import Web3
import time
import random
import pyfiglet
import sys
from pathlib import Path
from datetime import datetime
from tzlocal import get_localzone
from colorama import Fore, Style, init

init(autoreset=True)
a1 = pyfiglet.figlet_format("DAOISCHAIN")
print(Fore.GREEN + Style.BRIGHT + a1)
print("--------------------------------------------------------------")
print("Haust Network Testnet Auto Send")
print(Fore.BLUE + Style.BRIGHT + "Telegram Channel: https://t.me/newtesnet")
print(Fore.GREEN + Style.BRIGHT + "Donate: 0xf8a95e3ddbe6b3d31ef773378f101bcbf9fd511a")
print("--------------------------------------------------------------")

NETWORK_URL = "https://rpc-test.haust.network"
CHAIN_ID = 1570754601
CURRENCY_SYMBOL = "HAUST"

web3 = Web3(Web3.HTTPProvider(NETWORK_URL))

if not web3.is_connected():
    print("Gagal terhubung ke jaringan Haust Testnet.")
    sys.exit()

print("Terhubung ke jaringan Haust Testnet.")

local_timezone = get_localzone()

PRIVATE_KEY_FILE = "private_key.txt"
try:
    private_key = Path(PRIVATE_KEY_FILE).read_text().strip()
except FileNotFoundError:
    print(f"File {PRIVATE_KEY_FILE} tidak ditemukan. Pastikan file ini ada dan mengandung private key.")
    sys.exit()

try:
    account = web3.eth.account.from_key(private_key)
    wallet_address = account.address
    print(Fore.YELLOW + f"Alamat Wallet Anda: {wallet_address}")
    balance = web3.eth.get_balance(wallet_address)
    print(Fore.YELLOW + f"Saldo: {web3.from_wei(balance, 'ether')} {CURRENCY_SYMBOL}")
except Exception as e:
    print(f"Gagal mendapatkan informasi wallet: {e}")
    sys.exit()

WALLETS_FILE = "wallets.txt"
try:
    target_wallets = Path(WALLETS_FILE).read_text().strip().splitlines()
    if not target_wallets:
        raise ValueError("File kosong.")
except (FileNotFoundError, ValueError):
    print(f"File {WALLETS_FILE} tidak ditemukan atau kosong. Tambahkan alamat tujuan pada file ini.")
    sys.exit()

def get_valid_input(prompt, cast_type):
    while True:
        try:
            return cast_type(input(prompt))
        except ValueError:
            print("Input tidak valid. Coba lagi.")

def log_transaction(message):
    current_time = datetime.now(local_timezone).strftime('%Y-%m-%d %H:%M:%S')
    with open("riwayat.log", "a") as log_file:
        log_file.write(f"{current_time} - {message}\n")

try:
    while True:
        min_amount = get_valid_input("Masukkan jumlah minimum token yang ingin dikirim: ", float)
        max_amount = get_valid_input("Masukkan jumlah maksimum token yang ingin dikirim: ", float)
        if min_amount > max_amount:
            print("Jumlah minimum tidak boleh lebih besar dari jumlah maksimum. Coba lagi.")
            continue
        min_interval = get_valid_input("Masukkan interval waktu minimum antar pengiriman (dalam menit): ", int)
        max_interval = get_valid_input("Masukkan interval waktu maksimum antar pengiriman (dalam menit): ", int)
        if min_interval > max_interval:
            print("Interval minimum tidak boleh lebih besar dari interval maksimum. Coba lagi.")
            continue
        break
except KeyboardInterrupt:
    print("\nScript dihentikan oleh user.")
    sys.exit()

try:
    while True:
        amount = random.uniform(min_amount, max_amount)
        interval = random.randint(min_interval, max_interval) * 60
        amount_in_wei = web3.to_wei(amount, 'ether')
        target_address = random.choice(target_wallets)

        try:
            nonce = web3.eth.get_transaction_count(wallet_address)
            transaction = {
                'to': target_address,
                'value': amount_in_wei,
                'gas': 21000,
                'gasPrice': web3.to_wei('20', 'gwei'),
                'nonce': nonce,
                'chainId': CHAIN_ID
            }

            signed_tx = web3.eth.account.sign_transaction(transaction, private_key)
            tx_hash = web3.eth.send_raw_transaction(signed_tx.raw_transaction)
            tx_hash_hex = web3.to_hex(tx_hash)
            current_time = datetime.now(local_timezone).strftime('%Y-%m-%d %H:%M:%S')
            print(Fore.CYAN + f"Transaksi berhasil dikirim ke {target_address}.")
            print(Fore.CYAN + f"Waktu: {current_time}")
            print(Fore.CYAN + f"Jumlah: {amount:.6f} {CURRENCY_SYMBOL}")
            print(Fore.RED + f"Hash: {tx_hash_hex}")

            log_transaction(f"SUKSES: Transaksi ke {target_address} pada {current_time} dengan hash {tx_hash_hex} (Jumlah: {amount:.6f} {CURRENCY_SYMBOL})")
            balance = web3.eth.get_balance(wallet_address)
            print(Fore.YELLOW + f"Saldo terbaru: {web3.from_wei(balance, 'ether')} {CURRENCY_SYMBOL}")
        except Exception as e:
            error_message = f"GAGAL: Transaksi ke {target_address} - {e}"
            print(error_message)
            log_transaction(error_message)
            continue

        for remaining in range(interval, 0, -1):
            minutes, seconds = divmod(remaining, 60)
            sys.stdout.write(f"Menunggu {minutes} menit {seconds} detik...\r")
            sys.stdout.flush()
            time.sleep(1)
        print("\n")
except KeyboardInterrupt:
    print("\nScript dihentikan oleh user.")
    log_transaction("Script dihentikan oleh user.")
