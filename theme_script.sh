#!/bin/bash
echo export DBUS_SESSION_BUS_ADDRESS=$DBUS_SESSION_BUS_ADDRESS > lightscript.sh
echo export DBUS_SESSION_BUS_ADDRESS=$DBUS_SESSION_BUS_ADDRESS > darkscript.sh
echo "gsettings set org.gnome.desktop.interface gtk-theme Ant-Nebula" >> lightscript.sh
echo "gsettings set org.gnome.desktop.background picture-uri 'file:///usr/share/backgrounds/brad-huchteman-stone-mountain.jpg'" >> lightscript.sh
echo "gsettings set org.gnome.desktop.interface gtk-theme BlueSky-Dark" >> darkscript.sh
echo "gsettings set org.gnome.desktop.background picture-uri 'file:///home/sam/Downloads/MacOS-3D-4K-Dark.jpg'" >> darkscript.sh
chmod 755 lightscript.sh
chmod 755 darkscript.sh

currenttime=$(date +%H:%M)
if [[ "$currenttime" > "19:00" ]] || [[ "$currenttime" < "06:00" ]]; then
     ./darkscript.sh
   else
     ./lightscript.sh
   fi
