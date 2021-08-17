import json
from sys import exit

class Settings:
    """ Settings Interface to access configuration """

    def __init__(self):
        self.load_setting()

    def load_setting(self):
        """Load Settings to  self"""
        try:
            with open("config.json", "r", encoding="utf-8") as config_file:
                settings = json.load(config_file)
        except FileNotFoundError:
            raise FileNotFoundError("config.json not found")
        if settings["java_path"]:
            self.java_path = settings["java_path"]
        if settings["apkTool_path"]:
            self.apkTool_path = settings["apkTool_path"]
        else:
            exit("ApkTool Path not Found in config.json")

        if settings["uberApkSigner_path"]:
            self.signer_path = settings["uberApkSigner_path"]
            signature = settings["signature"]
            self.keystore_path = signature["keystore_path"]
            self.keystore_password = signature["keystore_password"]
            self.keystore_alias = signature["alias"]
            self.keystore_alias_password = signature["alias_password"]
            self.zip_align = signature["zip_align"]
