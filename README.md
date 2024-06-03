# brainwallet
This Python script generates Bitcoin addresses from a wordlist of brain wallet passphrases. It then checks the balances of the wallets generated from the passphrases in the wordlist. If a wallet generated has a balance > 0, its passphrase, its private key and bitcoin address is saved to wallets_with_balance.txt


# Install
Install the required libraries using pip:
```pip install -r requirements.txt```

Put a list of passphrases you want process in passphrases.txt. Example:
```
mysecretpassphrase1
anotherpassphrase
yetanotherpassphrase
```

# Run the Script
```Python brainwallet.py```

The script will generate addresses from ```passphrases.txt``` and check the balances of the wallets created. If the script finds a wallet address with balance more than zero, the passphrase, along with the private key and address, will be written to ```wallets_with_balance.txt```

# Sample output
```
Passphrase: mysecretpassphrase1
Private Key: 4a8a08f09d37b73795649038408b5f33f2e3d8c9
Bitcoin Address: 1A1zP1eP5QGefi2DMPTfTL5SLmv7DivfNa
Balance: 0.0 BTC
Status: DEAD

Passphrase: anotherpassphrase
Private Key: 5f4dcc3b5aa765d61d8327deb882cf99
Bitcoin Address: 1dice8EMZmqKvrGE4Qc9bUFf9PX3xaYDp
Balance: 0.1 BTC
Status: ACTIVE!
```

# Donations
If you found this script useful and would like to support its maintainer, feel free to donate.
- BTC: bc1qhx4pdfxfrr5z7whg9zx96502uq5kvanpj4nfsx
