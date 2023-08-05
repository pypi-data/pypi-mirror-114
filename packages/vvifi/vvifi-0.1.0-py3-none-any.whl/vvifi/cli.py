import sys
from typing import Optional

import click
from string_utils import strip_margin

from . import __version__
from .constants import AIRPORT_PATH, DEVICE_RE, NETWORK_SYMBOL, SSID_RE
from .utils import print_error, run_single_command


# Typing: https://github.com/pallets/click/blob/8.0.0/src/click/decorators.py#L356
def print_networks(ctx: click.Context, param: click.Parameter, value: bool) -> None:
    if not value or ctx.resilient_parsing:
        return

    hardware = run_single_command(["networksetup", "-listallhardwareports"]).strip()

    device = DEVICE_RE.search(hardware)

    if device:
        networks = run_single_command(
            [
                "networksetup",
                "-listpreferredwirelessnetworks",
                device.group("device"),
            ]
        ).rstrip()

        click.echo(networks)
        # click.echo(repr(networks))

    ctx.exit()


def print_password(network: str, password: str) -> None:
    click.secho(f"{NETWORK_SYMBOL} {network}\n", bold=True)
    click.echo(password)


def get_ssid_macos(network: Optional[str]) -> str:
    if network:
        return network

    wifi_info = run_single_command([AIRPORT_PATH, "-I"])
    wifi_info = strip_margin(wifi_info).rstrip()

    # click.echo(repr(wifi_info))
    # click.echo(wifi_info)

    ssid = SSID_RE.search(wifi_info)

    # click.echo(repr(ssid))
    # click.echo(ssid)

    name = ssid.group("name") if ssid else ""

    return name


@click.command()
# More info:
# - https://click.palletsprojects.com/en/7.x/options/#boolean-flags
# - https://click.palletsprojects.com/en/7.x/options/#callbacks-and-eager-options
@click.option(
    "--networks",
    is_flag=True,
    callback=print_networks,
    expose_value=False,
    is_eager=True,
    help="Show the names (SSIDs) of saved Wi-Fi networks and exit.",
)
@click.option(
    "-n",
    "--network",
    type=str,
    metavar="NAME",
    help="The name (SSID) of a Wi-Fi network you have previously connected to.",
)
@click.version_option(version=__version__)
@click.pass_context
def main(ctx: click.Context, network: Optional[str]) -> None:
    """
    A Python CLI to quickly check your Wi-Fi network password.
    By default, the network you are connected to is considered.
    """
    if sys.platform.startswith("darwin"):
        # macOS.
        name = get_ssid_macos(network)

        password = run_single_command(
            [
                "security",
                "find-generic-password",
                "-l",  # or `-a`
                name,
                "-D",
                "AirPort network password",
                "-w",
            ]
        ).rstrip()

        print_password(name, password)
    else:
        print_error(f"{repr(sys.platform)} is not supported.", ctx)
