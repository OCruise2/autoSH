dl_orcaSH() {
    wget https://github.com/OCruise2/autoSH/blob/b9b9811e59f3995c0d4c61e33fd44f12fec5524b/bash_orcaSH.py -O ~/orcaSH
    chmod +x ~/orcaSH
    echo "export PATH=\"\$HOME:\$PATH\"" >> ~/.bash_profile
    source ~/.bash_profile
}

dl_orcaSH