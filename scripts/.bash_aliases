# Packages
alias update-pkg="brew update && brew upgrade && brew cleanup && brew doctor"

# Easier navigation: .., ..., ...., .....
alias ..="cd .."
alias ...="cd ../.."
alias ....="cd ../../.."
alias .....="cd ../../../.."

# Navigation
alias go_rpi="cd ~/Documents/Projects/Embed-Control/src/command/Rpi/"
alias go_esp="cd ~/Documents/Projects/Embed-Control/src/command/ESP/"
alias go_home="cd ~/Documents/"

# Python
alias py="python"
alias pip-req="pip list --format=freeze > requirements.txt"

# Copy utils
alias copy="| pbcopy"

# Reload the shell (i.e. invoke as a login shell)
alias reload="exec ${SHELL} -l"

# Print each PATH entry on a separate line
alias path='echo -e ${PATH//:/\\n}'

# Create wifi hotspot
alias hotspot="sudo nmcli device wifi hotspot ssid ntw_TRAVELERS password TRAVELERS"