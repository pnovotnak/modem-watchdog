# Modem Watchdog

Periodically ping both a local and remote server to verify connectivity. If the remote address not responding, but the 
local address is we assume the modem has lost connectivity and issue a reboot.

`modem_watchdog.py` is the entrypoint.
