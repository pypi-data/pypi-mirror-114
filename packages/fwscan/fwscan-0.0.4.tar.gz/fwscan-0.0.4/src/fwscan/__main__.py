"""Command-line interface."""
import fire
import logging

from fwscan.utils.console import console

from fwscan.scanners.checksec.checksecscanner import ChecksecScanner
from fwscan.scanners.radare.elfscanner import RadareELFScanner


# Logging setup
logging.basicConfig(
    level=logging.INFO,
    filename="/tmp/fwscan.log",
    format="%(asctime)s %(levelname)s:%(message)s",
)


def main() -> None:
    """fwscan."""
    checksec_scanner = ChecksecScanner()
    radare_elf_scanner = RadareELFScanner()

    # Register commands
    fire.Fire({"radare": radare_elf_scanner, "checksec": checksec_scanner})


if __name__ == "__main__":
    main(prog_name="fwscan")  # pragma: no cover
