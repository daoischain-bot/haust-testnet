This **Haust Network Tesnet** script can perform automatic transfers within a random time range. Additionally, this script will also perform random token transfers with a range of token amounts that can be specified.

install > Use Python

- git clone https://github.com/daoischain-bot/haust-testnet.git
- pip install web3
- pip install colorama
- pip install requests
- pip install pyfiglet
- pip install tzlocal 

• Edit private_key.txt add your private key

• Edit wallets.txt add target address

Done all and Run with python3 bot.py

1. To minimize a script running on a VPS without stopping it you can use **tmux**
- sudo apt install tmux
- tmux -S mysession
- ls
- python3 bot.py
  
2. Detach from the screen session (without stopping the script): Press Ctrl + B, then D
3. Reattach to the screen session (when you want to check on your script):
- tmux attach -t mysession
4. Stoping script press Ctrl + c
  
**Donate: 0xf8a95e3ddbe6b3d31ef773378f101bcbf9fd511a**
