import hashlib
import ecdsa
import base58
import requests
from colorama import init, Fore, Style
from concurrent.futures import ThreadPoolExecutor, as_completed

# Initialize colorama
init(autoreset=True)

def generate_brain_wallet(passphrase):
    # Hash the passphrase to generate a private key
    private_key = hashlib.sha256(passphrase.encode('utf-8')).digest()
    
    # Generate the public key
    sk = ecdsa.SigningKey.from_string(private_key, curve=ecdsa.SECP256k1)
    vk = sk.get_verifying_key()
    public_key = b'\x04' + vk.to_string()

    # Generate the Bitcoin address
    ripemd160 = hashlib.new('ripemd160')
    ripemd160.update(hashlib.sha256(public_key).digest())
    hashed_public_key = ripemd160.digest()
    checksum = hashlib.sha256(hashlib.sha256(b'\x00' + hashed_public_key).digest()).digest()[:4]
    address = base58.b58encode(b'\x00' + hashed_public_key + checksum)
    
    return private_key.hex(), address.decode()

def check_balance(address):
    url = f"https://blockchain.info/q/addressbalance/{address}"
    response = requests.get(url)
    if response.status_code == 200:
        balance = int(response.text) / 1e8  # Convert satoshi to BTC
        return balance
    return 0

def process_passphrase(passphrase, api_key=None):
    private_key, address = generate_brain_wallet(passphrase)
    balance = check_balance(address)
    return passphrase, private_key, address, balance

def main():
    input_file = 'passphrases.txt'
    output_file = 'wallets_with_balance.txt'
    num_workers = 10  # Number of concurrent threads

    with open(input_file, 'r') as f:
        passphrases = [line.strip() for line in f if line.strip()]

    with open(output_file, 'w') as f_out:
        with ThreadPoolExecutor(max_workers=num_workers) as executor:
            future_to_passphrase = {executor.submit(process_passphrase, passphrase): passphrase for passphrase in passphrases}
            
            for future in as_completed(future_to_passphrase):
                passphrase, private_key, address, balance = future.result()
                
                if balance > 0:
                    status = Fore.GREEN + "ACTIVE!" + Style.RESET_ALL
                    f_out.write(f"Passphrase: {passphrase}\n")
                    f_out.write(f"Private Key: {private_key}\n")
                    f_out.write(f"Bitcoin Address: {address}\n")
                    f_out.write(f"Balance: {balance} BTC\n")
                    f_out.write("\n")
                else:
                    status = Fore.RED + "DEAD" + Style.RESET_ALL
                
                # Print the details with status
                print(f"Passphrase: {passphrase}")
                print(f"Private Key: {private_key}")
                print(f"Bitcoin Address: {address}")
                print(f"Balance: {balance} BTC")
                print(f"Status: {status}")
                print()

if __name__ == "__main__":
    main()