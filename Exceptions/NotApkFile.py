

class NotApkFile(Exception):
    """Exception Raised when File is not a Apk"""

    def __init__(self,path,message = "Provided File is not a Apk File"):
        self.apk_path = path
        self.message = message

    def __str__(self):
        return " ".join((self.message,self.apk_path))

