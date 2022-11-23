#!/bin/sh
    if ! [ -x "$(command -v brew)" ];
    then
        echo 'Warning: brew is not installed.' >&2
        echo 'Installing brew...' >&2
        /bin/bash -c "$(curl -fsSL https://raw.githubusercontent.com/Homebrew/install/HEAD/install.sh)"
    fi

    if ! [ -x "$(command -v python3)" ];
    then
        echo 'Warning: python3 is not installed.' >&2
        echo 'Installing python3...' >&2
        brew install python3
    fi

    if ! [ -x "$(command -v pip3)" ];
    then
        echo 'Warning: pip3 is not installed.' >&2
        echo 'Installing pip3...' >&2
        curl https://bootstrap.pypa.io/get-pip.py -o get-pip.py
        python3 get-pip.py
        rm -f get-pip.py
    fi

    if ! [ -x "$(command -v virtualenv)" ];
    then
        echo 'Warning: virtualenv is not installed.' >&2
        echo 'Installing virtualenv...' >&2
        pip3 install virtualenv    
    fi

    mkdir ~/python-automation/core_files/automation_environment
    cd ~/python-automation/core_files/automation_environment || exit
    virtualenv .
    source bin/activate

    cd ~/python-automation/core_files/ || exit
    echo 'Installing pip dependencies...' >&2
    pip3 install -r requirements.txt

    if ! [ -x "$(command -v node)" ];
    then
        echo 'Warning: node is not installed.' >&2
        echo 'Installing node...' >&2
        brew install node
    fi

    echo 'Installing Appium...' >&2
    npm install -g appium

    echo 'Installing Appium Doctor' >&2
    npm install -g appium-doctor

    deactivate

    echo '(!)-(!)-(!)-(!)-(!)-(!)-(!)-(!)-(!)-(!)-(!)-(!)-(!)-(!)-(!)-(!)'>&2
    echo '(!)-(!)-(!)-(!)-(!)-(!)-(!)-(!)-(!)-(!)-(!)-(!)-(!)-(!)-(!)-(!)'>&2
    echo '(!)-(!)-(!)-(!)-(!)-(!)-(!)-(!)-(!)-(!)-(!)-(!)-(!)-(!)-(!)-(!)'>&2
    echo '\\\\\\\\|||||||||||||||||||||/////////'>&2
    echo '>>>>>>>>IMPORTANT INFORMATION<<<<<<<'>&2
    echo '////////|||||||||||||||||||||\\\\\\\\\'>&2
    echo ' '>&2
    echo '1 - The Virtual Environment was created on ~/python-automation/core_files/automation_environment'>&2
    echo ' '>&2
    echo '2 - You should always use/activate this environment to run the automation project.'>&2
    echo ' '>&2
    echo '3 - Use this command to activate: source ~/python-automation/core_files/automation_environment/bin/activate'>&2
    echo ' '>&2
    echo '4 - Use this command to deactivate: deactivate'>&2
    echo ' '>&2
    echo '5 - It is recommended run appium-doctor to verify its dependencies.'>&2
    echo ' '>&2
    echo '^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^'>&2
    echo '(!)-(!)-(!)-(!)-(!)-(!)-(!)-(!)-(!)-(!)-(!)-(!)-(!)-(!)-(!)-(!)'>&2
    echo '(!)-(!)-(!)-(!)-(!)-(!)-(!)-(!)-(!)-(!)-(!)-(!)-(!)-(!)-(!)-(!)'>&2
    echo '(!)-(!)-(!)-(!)-(!)-(!)-(!)-(!)-(!)-(!)-(!)-(!)-(!)-(!)-(!)-(!)'>&2
    exit 1;