import re
from typing import Pattern

AIRPORT_PATH: str = (
    "/System/Library/PrivateFrameworks/"
    "Apple80211.framework/Versions/"
    "Current/Resources/airport"
)

# SSID: the name of the Wi-Fi network.
SSID_RE: Pattern[str] = re.compile(r"^SSID: (?P<name>\S+)$", re.MULTILINE)
DEVICE_RE: Pattern[str] = re.compile(r"Hardware Port: Wi-Fi\nDevice: (?P<device>\w+)")

NETWORK_SYMBOL: str = "🌐"
