# brainwallet - What this script does
This Python script generates Bitcoin addresses from a wordlist of brain wallet passphrases. It then checks the balances of the wallets generated from the passphrases in the wordlist. This script helps you find brain wallet addresses that contain Bitcoin balance in them.


# Install
```pip install ecdsa base58 requests colorama```

Put a list of passphrases you want to check in passphrases.txt. Example:
```
mysecretpassphrase1
anotherpassphrase
yetanotherpassphrase
```

# Run the Script
```Python brain_wallet_checker.py```
Execute the script to generate addresses from ```passphrases.txt``` and check their balances. If the script finds a wallet address with balance more than zero, the input, along with the private key and address, will be written to ```wallets_with_balance.txt```



