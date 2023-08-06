class AutoControlException(Exception):

    def __init__(self, message="Auto control error"):
        self.message = message
        super().__init__(message)

    def __str__(self):
        return f"{self.message}"


class AutoControlKeyboardException(Exception):
    def __init__(self, message="Auto control keyboard error"):
        self.message = message
        super().__init__(message)

    def __str__(self):
        return f"{self.message}"


class AutoControlMouseException(Exception):
    def __init__(self, message="Auto control mouse error"):
        self.message = message
        super().__init__(message)

    def __str__(self):
        return f"{self.message}"


class AutoControlScreenException(Exception):
    def __init__(self, message="Auto control screen error"):
        self.message = message
        super().__init__(message)

    def __str__(self):
        return f"{self.message}"


class AutoControlCantFindKeyException(Exception):
    def __init__(self, message="Auto control can't find key error"):
        self.message = message
        super().__init__(message)

    def __str__(self):
        return f"{self.message}"


class ImageNotFoundException(Exception):

    def __init__(self, image, message="Auto control image not found error"):
        self.message = message
        self.image = image
        super().__init__(message)

    def __str__(self):
        return f"{self.message} cause by: {self.image}"
