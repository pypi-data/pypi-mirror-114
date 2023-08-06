import os
import magic
import subprocess
from tqdm import tqdm
from scanfs.fsscannerex import FSScannerException


class FileSystemScanner:

    """
    FileSystemScanner

    This scanner scans the folder in the filesystem
    with various filetype filters and provides a hook
    whenever the filetype is found in the provided path

    Attributes:
        fpath (str): Folder in the filesytem to scan

    Raises:
        FSScannerException: [Exception when the
        folder path fpath is empty or not valid]
    """

    def __init__(self, fpath: str) -> None:
        super().__init__()
        self._check_str_param(fpath)
        self.fpath = fpath

    def scan_for(self, filetype, callback):
        """
        Scans for specific filetype in the nested folder

        Args:
            filetype ([type]): Filetype
            callback (function): Function called when the filetype
            is found
        """
        nodes = os.scandir(self.fpath)

        for node in nodes:
            callback(self.fpath, node)

    def scan_for_elfs(self, callback):
        """
        Scans for elf file types in the nested folder

        Args:
            callback (function): Function called when the elf file type
            is found
        """
        nodes = os.scandir(self.fpath)

        try:
            for node in nodes:
                fpath = os.path.join(self.fpath, node.name)

                if magic.from_file(fpath).find("ELF") != -1 and not node.is_symlink():
                    callback(self.fpath, node)
        except:
            pass  # TODO: Handle the exceptions while scanning directory

    def _check_str_param(self, param):
        if not isinstance(param, str) or not param:
            raise FSScannerException(
                f'Firmware path "{param}" is empty or not valid string!!!'
            )
