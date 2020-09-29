import logging
import time

import modems
import utils


def watchdog(modem: modems.Modem, ttl: int = 120, internal_addr: str = None, external_addr: str = '8.8.8.8'):
    if internal_addr is None:
        internal_addr = utils.get_gateway()

    if internal_addr is None:
        logging.error('unable to determine gateway address')
        raise EnvironmentError('internal address not provided, and unable to determine internal address')

    logging.info(f'{modem.name()} initialized, internal check address is {internal_addr}')

    while True:
        if not utils.ping_retry(internal_addr, ttl):
            logging.warning(f'unable to ping internal check address ({internal_addr}) - please check your connections')
        elif not utils.ping_retry(external_addr, ttl):
            logging.warning(f'modem seems to be unresponsive (gateway is reachable, but external addresses are not). '
                            f'Rebooting the modem.')
            modem.reboot()

        time.sleep(10)
