# brainwallet - What this script does
This Python script generates Bitcoin addresses from a text file containing brain wallet passphrases and checks the balances of these addresses. A brain wallet is a cryptocurrency address derived from a passphrase. This tool helps you find brain wallet addresses that contain Bitcoin balance in them.
#How it works
Generate Bitcoin Addresses: Converts passphrases into Bitcoin addresses using the brain wallets method
Check Balances: Checks the Bitcoin balance of each generated address.
Multithreading: Processes multiple passphrases concurrently for efficiency.
Output Results: Writes addresses with a balance to an output file.

# Install
pip install ecdsa base58 requests colorama

Put a list of passphrases you want to check in passphrases.txt. Example:
mysecretpassphrase1
anotherpassphrase
yetanotherpassphrase

# Run the Script
Run the python script brain_wallet_checker.py
Execute the script to generate addresses from passphrases.txt and check their balances. If the script finds a wallet address with balance more than zero, the input, along with the private key and address, will be written to wallets_with_balance.txt



