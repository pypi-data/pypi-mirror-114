# x735-v2.5
This is the safe shutdown script and some python sample code.

## Install

Assuming your system is updated, add these packages:

### Install dependencies

```
sudo apt-get install python-smbus
sudo apt-get install pigpio python3-pigpio
```

### Add package

```
sudo pip3 install x735-v2.5
```

### Add service to systemd

``
cat > sudo /etc/systemd/system/x735fan.service <<- EOM
[Unit]
Description=Run fan for x735 board
After=multi-user.target

[Service]
Type=simple
Restart=always
RestartSec=1
ExecStart=/usr/bin/python3 /usr/local/bin/x735fan run

[Install]
WantedBy=multi-user.target
EOM

sudo systemctl daemon-reload
sudo systemctl enable x735fan.service
sudo systemctl start x735fan.service
sudo systemctl status x735fan.service
``

## Update

```
sudo pip3 install x735-v2.5 -U
```

# Use

```
x735fan run  # Run set speed
x735fan info # Get fan information
```

# Develop

```
python3 -m venv venv
pip install -e .
```

## Deploy to pypi
```
python setup.py register -r pypi
python setup.py sdist upload -r pypi
```
