from typing import Optional

import netifaces
from icmplib import ping


def get_gateway() -> Optional[str]:
    gws = netifaces.gateways()
    gw = gws.get('default', {}).get(netifaces.AF_INET, [None, ])[0]
    return gw


def ping_retry(addr: str, ttl: int) -> bool:
    if ttl <= 0:
        return False

    if not ping(addr, count=1).is_alive:
        return ping_retry(addr, ttl-1)

    return True
