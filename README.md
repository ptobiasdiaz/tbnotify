# Telegram Bot Notifier

## Installation

```
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
python setup.py install
```

## Usage

Get a bot token using BotFather and then run server:
```
tbnotify_server -t <BOT TOKEN>
```

Open a chat with the bot, use "/start" or "/subscribe" to get notifications. To send notifications to the bot, just enter:
```
tbnotify_send "<MESSAGE>"
```

## Additional options

The notification bot uses an UDP socket to receive messages, by default it listens on `localhost` and port `9999`. User can change this behaviour with "-a" and "-p" respectively.

The BOT token can be defined in a environment veriable instead of a CLI option. The environment variable is `TBNOTIFY_TOKEN` and it can be bypassed with the "-t" option. Token is mandatory so user should provide it by the CLI option or by the environment variable. If no token is provided, the server cannot be executed.

## Usage as a service

You can create a systemd service to run the bot's server as a service:

```
sudo mkdir -p /opt/telegram-bot
wget https://raw.githubusercontent.com/ptobiasdiaz/tbnotify/main/tbnotify/server.py -O /opt/telegram-bot/server.py
wget https://raw.githubusercontent.com/ptobiasdiaz/tbnotify/main/requirements.txt -O /opt/telegram-bot/requirements.txt
```
Then, create a virtual environment and install the requirements:
```
cd /opt/telegram-bot
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
```

Finally, create a systemd service file:
```
sudo wget https://raw.githubusercontent.com/ptobiasdiaz/tbnotify/main/tbnotify/telegram.service -O /etc/systemd/system/telegram.service
```

Restart the systemd daemon and enable the service:
```
sudo systemctl daemon-reload
sudo systemctl enable telegram.service
sudo systemctl restart telegram.service
```

To check the status of the service:
```
sudo systemctl status telegram.service
```

To check the correct operation of the bot, you can send a message to the bot using the command:
```
echo "Hello, world!" | nc -u -w1 127.0.0.1 9999
```
And a message should be sent to the bot, and, consequently, to the chatbot.

> 🚨 Every time "telegram" is restarted, you need to send `/start` to the Telegram Bot.

To check the logs of the bot, you can use:
```
sudo tail -f /var/log/telegram-error.log
```