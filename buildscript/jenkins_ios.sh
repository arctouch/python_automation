#!/bin/bash
COUNT=0

idevice_id -l | while read line
do
    if [ ! "$line" = "" ] 
    then
        echo $(cat resources/device_config.json | jq  '.devices[.devices| length] |= . + {"deviceName": "'${line}'", "udid": "'${line}'", "platformName": "ios", "platformVersion": "9.3"}' resources/device_config.json ) > resources/device_config.json &
    fi
done
