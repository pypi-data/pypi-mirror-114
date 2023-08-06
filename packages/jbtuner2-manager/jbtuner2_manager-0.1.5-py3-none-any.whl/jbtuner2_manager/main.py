import socket
import subprocess
from pathlib import Path
from typing import Optional

import typer

from jbtuner2_manager import __version__
from . import espota

app = typer.Typer()
jbtuner_list = [
    ("jbt001", "10.0.0.11"),
    ("jbt002", "10.0.0.12"),
    ("jbt003", "10.0.0.13")
]


def version_callback(value: bool):
    if value:
        typer.secho(f"CLI Version: {__version__}", fg=typer.colors.MAGENTA)
        raise typer.Exit()


# Main command
@app.callback()
def main(
        _version: Optional[bool] = typer.Option(
            None, "--version", "-v", callback=version_callback, is_eager=True
        ),
):
    """
    ===================================================================
    JBTuner2 Manager - An integrated tool for managing ChordX JBTuner2 
    ===================================================================
    """
    typer.echo(f"Welcome to use JBTuner2 manager <{__version__}>\n")


def search(dest_ip, udp_port, timeout):
    with socket.socket(socket.AF_INET, socket.SOCK_DGRAM, socket.IPPROTO_UDP) as sock:
        sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEPORT, 1)
        sock.setsockopt(socket.SOL_SOCKET, socket.SO_BROADCAST, 1)
        sock.settimeout(timeout)
        sock.sendto(bytes("hello", "utf-8"), (dest_ip, udp_port))
        try:
            for i in range(10):
                data, addr = sock.recvfrom(1024)
                typer.echo(f"{addr} response: {data}")
        except Exception:
            pass


def get_info(dest_ip, udp_port, timeout):
    with socket.socket(socket.AF_INET, socket.SOCK_DGRAM, socket.IPPROTO_UDP) as sock:
        sock.settimeout(timeout)
        sock.sendto(bytes("hello", "utf-8"), (dest_ip, udp_port))
        try:
            data, addr = sock.recvfrom(1024)
            if data:
                # typer.echo(f"{addr} response: {data}")
                return data
        except Exception:
            pass


@app.command("list")
def ls(
        port: Optional[int] = typer.Option(1979, "--port", "-p", help="the port number"),
        timeout: Optional[float] = typer.Option(1.0, "--timeout", "-t", help="the timeout seconds"),
):
    """
    List all pre-defined JBTuners.
    """
    typer.echo("List pre-defined JBTuners...")
    for dev, addr in jbtuner_list:
        data = get_info(addr, port, timeout)
        if data:
            typer.echo(f"{dev}({addr}): {data}")
        else:
            typer.echo(f"{dev}({addr}): Timeout")


@app.command("scan")
def scan(
        ip: str = typer.Option("10.0.0.255", "--ip-address", "-a", help="the IP/Broadcast address"),
        port: Optional[int] = typer.Option(1979, "--port", "-p", help="the port number"),
        timeout: Optional[float] = typer.Option(1.0, "--timeout", "-t", help="the timeout seconds"),
):
    """
    Scan for all available JBTuners.
    """
    typer.echo(f"Scanning for {timeout} seconds... ")
    search(ip, port, timeout)


@app.command("update")
def update_program(
        host: str = typer.Argument(..., help="the hostname or IP address of JBTuner"),
        fwfile: str = typer.Option(..., "--firmware", "-f", help="the file of firmware"),
):
    """
    Update firmware of JBTuners (FOTA)
    """
    typer.echo(f"Updating firmware of JBTuner: {host}")
    command = ['-i', host, '-p', '3232', '-r', '-f', fwfile]
    espota.main(command)


@app.command("config")
def config(
        host: str = typer.Argument(..., help="the hostname or IP address of JBTuner"),
        configfolder: Optional[str] = typer.Option(None, "--config", "-c", help="the folder contains config files"),
):
    """
    Update configuration of JBTuners
    """
    if not configfolder:
        p = Path(f"{host}")
        if p.exists() and p.is_dir():
            typer.echo(f"Auto detected the config folder named '{host}'.")
            configfolder = host
        else:
            typer.echo(f"No default folder '{host}' found, please specify a config folder.")
            return
    typer.echo(f"Compiling spiffs image from {configfolder}...")
    command = ["mkspiffs_espressif32_arduino", "-c", f"{configfolder}", "-b", "4096", "-p", "256", "-s", "0x170000", ".spiffs.bin"]
    subprocess.run(command)
    typer.echo("Generated SPIFFS binary.")
    typer.echo(f"Updating configuration of JBTuner: {host}")
    command = ['-i', host, '-p', '3232', '-r', '-s', '-f', '.spiffs.bin']
    espota.main(command)


if __name__ == "__main__":
    app()
