class IncorrectFileFormatError(Exception):
    """Excepción lanzada cuando el formato del archivo es incorrecto."""
    def __init__(self, message="Incorrect File Format: Report file should be a .txt file"):
        self.message = message
        super().__init__(self.message)