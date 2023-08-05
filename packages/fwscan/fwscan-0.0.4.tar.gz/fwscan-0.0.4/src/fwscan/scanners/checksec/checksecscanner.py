import logging
from fwscan.utils.console import console

log = logging.getLogger(__name__)


class ChecksecScanner(object):
    """Scanner for extracting, processing and visualizing
    protections in binaries

    Examples usages:
    fwscan checksec --help
    fwscan checksec scan --help

    Scan folder /usr/bin and store results in folder output
    fwscan checksec scan /usr/bin output
    """

    def __init__(self, verbose=False):
        # TODO Fix this verbose optional option.
        """
        Parameters
        ----------
        verbose : boolean, optional
            Enable verbose logging
        """
        self.verbose = verbose
        if verbose:
            log.setLevel(logging.DEBUG)
        log.debug("---------")

    def scan(self, folder, ofolder):
        """
        Scan for ELF binaries in the folder, extracts protection features
        and stores result in output file. Generates plots for each protection
        features.

        Parameters
        ----------
        folder : string
            Target folder to scan
        ofolder : string
            Output folder to store the results & plots
        """
        console.print(
            f"[bold green] :mag: Scanning folder: [bold magenta]{folder}[/bold magenta]"
        )
