#!/usr/bin/env python3

import socket
import argparse


def parse_cli():
    """Parse and check CLI"""
    parser = argparse.ArgumentParser("Telegram Bot send notification")
    parser.add_argument("MESSAGE", type=str, help="Notification message")
    parser.add_argument(
        "-a", "--address", type=str, default="127.0.0.1",
        help="UDP address to send notification",
        dest="address"
    )
    parser.add_argument(
        "-p", "--port", type=int, default=9999,
        help="UDP port to send notification",
        dest="port"
    )
    args = parser.parse_args()
    return args


def main():
    user_options = parse_cli()
    sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    sock.sendto(bytes(user_options.MESSAGE, "utf-8"), (user_options.address, user_options.port))

if __name__ == '__main__':
    main()