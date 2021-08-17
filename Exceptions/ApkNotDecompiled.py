class ApkNotDecompiled(Exception):
    """Exception Raised when Try to mod without Decompiling"""

    def __init__(self, apk, message="Accessing Internal apk components Without Decompiling"):
        self.apk = apk
        self.message = message

    def __str__(self):
        return " ".join((self.apk.name, self.message))