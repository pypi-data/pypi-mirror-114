import click
from fwscan.utils.colorprints import *

from scanfs.fsscanner import FileSystemScanner
from scanfs.scanners.checksecscanner import CheckSecScanner


@click.command()
@click.option("--checksec", "-c", is_flag=True, help="Use checksec scanner")
@click.option("--format", "-f", help="Output file format | default json")
@click.option("--outputfile", "-o", help="Output file name", required=True)
@click.argument("folder", default="/usr/bin", required=True)
def main(folder, checksec, format, outputfile):
    """Firmware security scanner"""

    printg("Folder: " + folder)
    print_color_reset()
    if checksec:
        css = CheckSecScanner(folder, outputfile)
        css.checksec_on_elfs()
