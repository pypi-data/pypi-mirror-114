from typing import List

class Error(Exception):
    """Error thrown when executing DataWeave script.
    """

    def __init__(self, message: str, *, executable: str, parameters: List[str], stdout: bytes=None, stderr: bytes=None):
        """Creates a new error with information about a failed DataWeave script execution.

        Args:
            message (str): human-readable error message
            executable (str): path to the `dw` executable
            parameters (List[str]): parameter list passed to the executable
            stdout (bytes, optional): contents of the standard output stream
            stderr (bytes, optional): contents of the standard error stream
        """

        super().__init__(message)
        self.executable = executable
        self.parameters = parameters
        self.stdout = stdout
        self.stderr = stderr

