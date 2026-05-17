#!/bin/bash

export PATH="$PATH:$HOME/.local/bin"

if ! chmod u+x "$(pwd)/src/Thot"; then
    echo -e "\nError: Failed to make src/Thot executable. Please check file permissions."
    exit 1
fi

mkdir -p ~/.local/bin

if ! ln -sf "$(pwd)/src/Thot" ~/.local/bin/thot; then
    echo -e "\nError: Failed to create the symlink in ~/.local/bin/. Please check your permissions."
    exit 1
fi

cat << 'EOF'
 _____ _   _  ___ _____ 
|_   _| | | |/ _ \_   _|
  | | | |_| | | | || |  
  | | |  _  | |_| || |  
  \_/ \_| |_/\___/ \_/  
EOF

echo -e "Thot has just been installed in your system :)\n"
echo "Run: thot example.thot"
