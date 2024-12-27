class IncorrectFileFormatException(Exception):
    """Excepción lanzada cuando el formato del archivo es incorrecto."""
    def __init__(self, extension):
        self.message = f"Incorrect File Format: Report file should be a {extension} file"
        super().__init__(self.message)