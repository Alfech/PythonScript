#!/bin/bash

# Execution of the discord app
discord=discord

#execution of spotify
spotify=spotify

#execution of firefoox
firefox=firefox 


#Execute the applications
$spotify &
sleep 2s
$discord &
sleep 2s
$firefox &
sleep 4s

#Getting the window ID
firefoxId=$(wmctrl -l -p | grep -E 'Firefox' | awk '{ printf("%s", $1) }')
discordId=$(wmctrl -l -p | grep -E 'Discord' | awk '{ printf("%s", $1) }')
spotifyId=$(wmctrl -l -p | grep -E 'Spotify' | awk '{ printf("%s", $1) }')

#Moving the window
xdotool windowactivate $firefoxId key shift+Super_L+Left
sleep 1s
xdotool windowactivate $spotifyId key shift+Super_L+Right
sleep 1s
xdotool windowactivate $discordId key shift+Super_L+Right
