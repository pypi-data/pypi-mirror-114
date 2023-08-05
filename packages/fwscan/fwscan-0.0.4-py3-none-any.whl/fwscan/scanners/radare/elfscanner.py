class RadareELFScanner(object):
    def scan(args, folder, output):
        """Scan for ELF files using Radare

        Good

        Args:
            folder (str): Folder to scan
            output (str): Results Folder
        """
        print("Radare ELF Scanner: " + folder)
        print("Radare ELF Scanner: " + str(output))