#!/bin/bash
ANDROID_DEVICES_LIST=""
COUNT=0

/usr/local/platform-tools/adb devices | while read line
do
    if [ ! "$line" = "" ] && [ `echo $line | awk '{print $2}'` = "device" ]
    then
        device=`echo $line | awk '{print $1}'`
        echo "Running first device: " $device &
        echo $(cat resources/device_config.json | jq  '.android.devices[.android.devices| length] |= . + {"deviceName": "'${device}'", "udid": "'${device}'", "platformVersion": "9"}' resources/device_config.json ) > resources/device_config.json &
        COUNT=$((COUNT+1)) &
    fi
done