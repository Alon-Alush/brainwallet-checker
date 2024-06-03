import hashlib
import ecdsa
import base58
import requests
import logging
import os
import re
from urllib.request import urlopen
from time import sleep
from colorama import init, Fore, Style
from concurrent.futures import ThreadPoolExecutor, as_completed
from tqdm import tqdm
from ratelimit import limits, sleep_and_retry

# Initialize colorama
init(autoreset=True)

# Setup logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

# Constants
RATE_LIMIT = 1  # Max 1 request per second
TIME_PERIOD = 1  # Time period in seconds for rate limit
SATOSHIS_PER_BITCOIN = 1e8
blockchain_tags = ['total_received', 'final_balance']

# Adjust the check_balance function
@sleep_and_retry
@limits(calls=RATE_LIMIT, period=TIME_PERIOD)
def check_balance(address):
    try:
        url = f"https://blockchain.info/address/{address}?format=json"
        htmlfile = urlopen(url, timeout=10)
        htmltext = htmlfile.read().decode('utf-8')

        blockchain_info = []
        for tag in blockchain_tags:
            blockchain_info.append(
                float(re.search(rf'{tag}":(\d+),', htmltext).group(1))
            )
        
        balance = blockchain_info[1] / SATOSHIS_PER_BITCOIN  # final_balance
        return balance
    except Exception as e:
        logging.error(f"Request failed for address {address}: {e}")
        return 0

def generate_brain_wallet(passphrase):
    try:
        private_key = hashlib.sha256(passphrase.encode('utf-8')).digest()
        sk = ecdsa.SigningKey.from_string(private_key, curve=ecdsa.SECP256k1)
        vk = sk.get_verifying_key()
        public_key = b'\x04' + vk.to_string()
        ripemd160 = hashlib.new('ripemd160')
        ripemd160.update(hashlib.sha256(public_key).digest())
        hashed_public_key = ripemd160.digest()
        checksum = hashlib.sha256(hashlib.sha256(b'\x00' + hashed_public_key).digest()).digest()[:4]
        address = base58.b58encode(b'\x00' + hashed_public_key + checksum)
        return private_key.hex(), address.decode()
    except Exception as e:
        logging.error(f"Failed to generate wallet for passphrase {passphrase}: {e}")
        return None, None

def process_passphrase(passphrase):
    private_key, address = generate_brain_wallet(passphrase)
    if not private_key or not address:
        return passphrase, None, None, 0
    balance = check_balance(address)
    return passphrase, private_key, address, balance

def load_passphrases(input_file):
    try:
        with open(input_file, 'r') as f:
            passphrases = [line.strip() for line in f if line.strip()]
        return passphrases
    except FileNotFoundError:
        logging.error(f"Input file {input_file} not found.")
        return []

def save_results(output_file, results):
    try:
        with open(output_file, 'w') as f_out:
            for result in results:
                passphrase, private_key, address, balance = result
                if balance > 0:
                    f_out.write(f"Passphrase: {passphrase}\n")
                    f_out.write(f"Private Key: {private_key}\n")
                    f_out.write(f"Bitcoin Address: {address}\n")
                    f_out.write(f"Balance: {balance} BTC\n")
                    f_out.write("\n")
                else:
                    logging.info(f"Passphrase {passphrase} resulted in an empty wallet.")
    except IOError as e:
        logging.error(f"Failed to write results to {output_file}: {e}")

def main():
    input_file = os.getenv('INPUT_FILE', 'passphrases.txt')
    output_file = os.getenv('OUTPUT_FILE', 'wallets_with_balance.txt')
    num_workers = int(os.getenv('NUM_WORKERS', 10))

    passphrases = load_passphrases(input_file)
    if not passphrases:
        logging.error("No passphrases to process.")
        return

    results = []
    with ThreadPoolExecutor(max_workers=num_workers) as executor:
        future_to_passphrase = {executor.submit(process_passphrase, passphrase): passphrase for passphrase in passphrases}

        for future in tqdm(as_completed(future_to_passphrase), total=len(passphrases), desc="Processing passphrases"):
            try:
                result = future.result()
                results.append(result)
                passphrase, private_key, address, balance = result
                
                if balance > 0:
                    status = Fore.GREEN + "ACTIVE!" + Style.RESET_ALL
                else:
                    status = Fore.RED + "DEAD" + Style.RESET_ALL
                
                # Print the details with status
                print(f"Passphrase: {passphrase}")
                print(f"Private Key: {private_key}")
                print(f"Bitcoin Address: {address}")
                print(f"Balance: {balance} BTC")
                print(f"Status: {status}")
                print()
            except Exception as e:
                logging.error(f"Future processing failed: {e}")

    save_results(output_file, results)
    logging.info(f"Processing complete. Results saved to {output_file}")

if __name__ == "__main__":
    main()
