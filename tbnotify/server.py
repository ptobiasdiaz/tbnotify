#!/usr/bin/env python3
# pylint: disable=unused-argument, wrong-import-position
# This program is forked from: https://github.com/python-telegram-bot/python-telegram-bot/blob/master/examples/echobot.py

"""
Simple Bot to send to a list of subscribers a notifications.

Usage:
Press Ctrl-C on the command line or send a signal to the process to stop the
bot.
"""

import os
import sys
import asyncio
import logging
import argparse

try:
    from telegram import __version__ as TG_VER
except ImportError:
    raise RuntimeError(
        "Missing library: python-telegram-bot"
    )

try:
    from telegram import __version_info__
except ImportError:
    __version_info__ = (0, 0, 0, 0, 0)  # type: ignore[assignment]

if __version_info__ < (20, 0, 0, "alpha", 1):
    raise RuntimeError(
        f"This example is not compatible with your current PTB version {TG_VER}. To view the "
        f"{TG_VER} version of this example, "
        f"visit https://docs.python-telegram-bot.org/en/v{TG_VER}/examples.html"
    )
from telegram import ForceReply, Update
from telegram.ext import Application, CommandHandler, ContextTypes, MessageHandler, filters

EXIT_OK = 0
EXIT_CLI_ERROR = 1


# Enable logging
logging.basicConfig(
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s", level=logging.INFO
)
logger = logging.getLogger(__name__)

# Subscribers
APP = None
SUBSCRIBERS = set()

# Define a few command handlers. These usually take the two arguments update and
# context.
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Send a message when the command /start is issued."""
    await update.message.reply_html(
        rf"You are subscribed to this notification bot, use /unsubscribe to stop."
    )
    logging.debug('New subscriber: ', update.effective_message.chat_id)
    SUBSCRIBERS.add(update.effective_message.chat_id)

async def stop(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Send a message when the command /unsubscribe is issued."""
    await update.message.reply_html(
        rf"You are unsubscribed to this notification bot, use /subscribe to start again."
    )
    if update.effective_message.chat_id in SUBSCRIBERS:
        logging.debug('Unsubscribe: ', update.effective_message.chat_id)
        SUBSCRIBERS.remove(update.effective_message.chat_id)


async def help_command(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Send a message when the command /help is issued."""
    await update.message.reply_text("Use /start or /subscribe to get notifications. /unsubscribe to stop.")


async def notify(message: str) -> None:
    """Send notification to all subscribers"""
    if not APP:
        return
    for chat_id in SUBSCRIBERS:
        await APP.bot.send_message(chat_id, text=message)


class NotifyProtocol(asyncio.DatagramProtocol):
    def __init__(self):
        super().__init__()

    def connection_made(self, transport):
        self.transport = transport

    def datagram_received(self, data, add):
        message = data.decode()
        logging.debug(f'Received message: {message}')
        loop = asyncio.get_event_loop()
        notify_task = loop.create_task(notify(message))
        asyncio.gather(notify_task)


def parse_cli():
    """Parse and check CLI"""
    parser = argparse.ArgumentParser("Telegram Bot notifier")
    parser.add_argument(
        "-a", "--address", type=str, default="127.0.0.1",
        help="Address to listen for notifications",
        dest="address"
    )
    parser.add_argument(
        "-p", "--port", type=int, default=9999,
        help="UDP port to listen for notifications",
        dest="port"
    )
    parser.add_argument(
        "-t", "--token", type=str, default=None,
        help="Telgram BOT token",
        dest="token"
    )
    args = parser.parse_args()
    if args.token is None:
        args.token = os.getenv("TBNOTIFY_TOKEN")
    if args.token is None:
        logging.error(
            'Missing Telegram bot token: use "-t" or define "TBNOTIFY_TOKEN" environment variable'
        )
        return None
    return args


def main() -> None:
    """Start the bot."""

    user_options = parse_cli()
    if not user_options:
        sys.exit(EXIT_CLI_ERROR)

    global APP

    udp_endpoint = (user_options.address, user_options.port)

    loop = asyncio.get_event_loop()
    logging.info("Starting UDP server...")
    udp_server = loop.create_datagram_endpoint(NotifyProtocol, local_addr=udp_endpoint)
    loop.run_until_complete(udp_server)

    # Create the Application and pass it your bot's token.
    APP = Application.builder().token(user_options.token).build()

    # on different commands - answer in Telegram
    APP.add_handler(CommandHandler(["start", "subscribe"], start))
    APP.add_handler(CommandHandler(["stop", "unsubscribe"], stop))
    APP.add_handler(CommandHandler("help", help_command))

    # Run the bot until the user presses Ctrl-C
    APP.run_polling()
    loop.close()

    logging.debug("Gracefull exit")
    sys.exit(EXIT_OK)


if __name__ == "__main__":
    main()
