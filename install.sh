dl_orcaSH() {
    wget https://raw.githubusercontent.com/OCruise2/autoSH/main/orcaSH.py -O ~/orcaSH
    chmod +x ~/orcaSH
    echo "export PATH=\"\$HOME:\$PATH\"" >> ~/.bash_profile
    source ~/.bash_profile
}

dl_orcaSH