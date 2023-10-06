class Emitter:
    """
    Emitter keeps track of the generated code and outputs it.
    """
    def __init__(self, fullPath: str):
        self.fullPath = fullPath
        self.header = ""
        self.code = ""

    def emit(self, code: str) -> None:
        """
        Add some code to the output.
        
        Parameters:
        code (str): The code to add.
        """
        self.code += code

    def emitLine(self, code: str) -> None:
        """
        Add some code to the output, followed by a newline.
        
        Parameters:
        code (str): The code to add.
        """
        self.code += code + '\n'

    def headerLine(self, code: str) -> None:
        """
        Add some code to the start of the output, followed by a newline.
        
        Parameters:
        code (str): The code to add.
        """
        self.header += code + '\n'

    def writeFile(self):
        """
        Write the output contents of the output file.
        """
        with open(self.fullPath, 'w') as outputFile:
            outputFile.write(self.header + self.code)

