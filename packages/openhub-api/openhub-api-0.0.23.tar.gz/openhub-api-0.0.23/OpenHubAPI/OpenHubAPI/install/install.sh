#!/bin/sh

sudo adduser openhubdaemon
sudo adduser openhubdaemon spi
sudo adduser openhubdaemon gpio


cd /home/openhubdaemon
sudo mkdir OpenHubApi
cd OpenHubApi
sudo mkdir OpenHubApi


sudo echo "[Unit]
Description = OpenHub daemon
Wants = network-online.target systemd-networkd-wait-online.service OpenHubAPI.service
After = network-online.target systemd-networkd-wait-online.service local-fs.target OpenHubAPI.service

[Service]
User = openhubdaemon
Environment=\"PATH=/usr/local/lib/python3.7/dist-packages\"
# Script starting HAP-python, e.g. main.py
# Be careful to set any paths you use, e.g. for persisting the state.
ExecStart = /usr/bin/python3 -m OpenHub

[Install]
WantedBy = multi-user.target" > /etc/systemd/system/OpenHub.service

echo "[Unit]
Description = OpenHubAPI daemon
Wants = network-online.target systemd-networkd-wait-online.service
After = network-online.target systemd-networkd-wait-online.service local-fs.target

[Service]
User = openhubdaemon
Environment=\"PATH=/usr/local/lib/python3.7/dist-packages\"
# Script starting HAP-python, e.g. main.py
# Be careful to set any paths you use, e.g. for persisting the state.
ExecStart = /usr/bin/python3 -m OpenHubAPI

[Install]
WantedBy = multi-user.target" > /etc/systemd/system/OpenHubAPI.service

sudo systemctl enable OpenHubAPI


sudo set -o noclobber

sudo echo "[Unit]
Description=Wait for Network to be Online
Documentation=man:systemd.service(5) man:systemd.special(7)
Conflicts=shutdown.target
After=network.target
Before=network-online.target

[Service]
Type=oneshot
ExecStart= \
    /bin/bash -c ' \
    if [ -e /etc/systemd/system/dhcpcd.service.d/wait.conf ]; \
    then \
        echo Wait for Network: enabled; \
        while [ -z \$(hostname --all-fqdns) ]; \
        do \
            sleep 1; \
        done; \
    else \
        echo Wait for Network: disabled; \
        exit 0; \
    fi'
TimeoutStartSec=1min 30s

[Install]
WantedBy=network-online.target" > /lib/systemd/system/network-wait-online.service

sudo systemctl enable network-wait-online.service

echo 'Please reboot.'
