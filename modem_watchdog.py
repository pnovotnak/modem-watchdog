import logging
import sys
import argparse

import modems
import watchdog

# TTL should *always* be set high enough for the modem to come online before rebooting. This provides an opportunity for
# a remote sysadmin to fix the system between reboots
TTL = 120

usage = f'''{sys.argv[0]} [username] [password]

This program monitors connection state via ICMP messages. If it can ping the default gateway but not an external 
address, it will reboot your modem.
'''


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='This program monitors connection state via ICMP messages. If it can '
                                                 'ping the default gateway but not an external address, it will reboot '
                                                 'your modem.')
    parser.add_argument('username', metavar='username', type=str, nargs=1, help='user to log in as')
    parser.add_argument('password', metavar='password', type=str, nargs=1, help='password to use when logging in')
    parser.add_argument('--modem-url', dest='modem_url', type=str, default='http://192.168.100.1',
                        help='modem address')
    parser.add_argument('--check-address', dest='check_address', type=str, help='internal address to ping as a check')
    args = parser.parse_args()

    logging.basicConfig(level=logging.INFO)
    try:
        modem = modems.NetgearCM1100(args.username, args.password, url=args.modem_url)
    except IndexError:
        print(usage)
        print('ERROR: must provide username and password as arguments')
        exit(1)
    else:
        watchdog.watchdog(modem, internal_addr=args.check_address)
