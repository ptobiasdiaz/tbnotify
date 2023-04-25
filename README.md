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
