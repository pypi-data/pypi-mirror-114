from scanfs.fsscanner import FileSystemScanner
import os
import subprocess


class CheckSecScanner(FileSystemScanner):
    def __init__(self, fpath: str, results_fpath: str, fformat: str = "json") -> None:
        super().__init__(fpath)
        self.fpath = fpath
        self.results_fpath = results_fpath
        self.fformat = fformat

    def checksec_dump(self, fpath, node):
        """
        Perform checksec and dump results in a file

        Args:
            result_fpath (str): Store results in this file path
            callback (function): Function called when the elf file type
            is found
        """
        try:
            path = os.path.join(fpath, node.name)
            completed_process = subprocess.run(
                ["checksec", "--format=" + str(self.fformat), "--file=" + str(path)],
                capture_output=True,
                check=True,
            )
            self.fd.write(completed_process.stdout.decode("utf-8"))
            self.fd.write("\n")
        except Exception as e:
            print("An exception occurred: " + str(e))

    def checksec_on_elfs(self):
        """
        Checks the security features enabled on elf

        Args:
            filename (str): Filename to store the results of checksec in JSON
            fformat
        """
        self.fd = open(self.results_fpath, "w")
        self.fd.write(
            "RELRO,CANARY,NX,PIE,RPATH,RUNPATH,Symbols,FORTIFY,Fortified,Fortifiable,FILE"
        )
        self.fd.write("\n")
        self.scan_for_elfs(self.checksec_dump)
        self.fd.close()
