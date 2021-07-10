import os
import sys
from argparse import ArgumentParser
from os.path import join, basename, isdir, dirname
from os import getcwd, listdir, rename
import xml.etree.ElementTree as ET
import json


class ApkCloner:
    def __init__(self,
                 apk_path,
                 no_of_clones=1,
                 level=1):
        self.apk_path = apk_path
        self.clones = no_of_clones
        self.modding_level = level
        #######################
        self.apk_decompiled_path = join(getcwd(), basename(self.apk_path) + "-decompied")
        _settings = self.load_setting()
        if _settings["java_path"]:
            self.java_path = _settings["java_path"]
        if _settings["apkTool_path"]:
            self.apkTool_path = _settings["apkTool_path"]
        if _settings["uberApkSigner_path"]:
            self.signer_path = _settings["uberApkSigner_path"]
            signature = _settings["signature"]
            self.keystore_path = signature["keystore_path"]
            self.keystore_password = signature["keystore_password"]
            self.keystore_alias = signature["alias"]
            self.keystore_alias_password = signature["alias_password"]
            self.zip_align = signature["zip_align"]

        #####################################

        ####################################

    def run(self):
        decompilation_command = " ".join(
            (self.java_path, "-jar", self.apkTool_path, "d -f", self.apk_path, "-o", self.apk_decompiled_path))
        # Decompiling Apk
        os.system(decompilation_command)
        ###########
        self.original_package_name = ET.parse(join(self.apk_decompiled_path, "AndroidManifest.xml")).getroot().attrib[
            "package"]
        # Building Clones By loop:
        if type(self.clones) == int and self.clones > 0:
            for clone in range(self.clones):
                manifest_file = join(self.apk_decompiled_path, "AndroidManifest.xml")
                self.package_name = ET.parse(manifest_file).getroot().attrib["package"]
                self.package_name_new = self.package_name[:-1] + chr(
                    ord(self.package_name[len(self.package_name) - 1]) + 1)

                # for AndroidManifest.xml
                with open(manifest_file, "r") as manifest:
                    manifest_data = manifest.read()

                tree = ET.ElementTree(ET.fromstring(manifest_data.replace(
                    self.package_name, self.package_name_new)))
                tree.write(manifest_file)
                #####################
                # Getting App Specific Sources Path
                app_sources_path = None
                for dir in listdir(self.apk_decompiled_path):
                    if isdir(join(self.apk_decompiled_path, dir)) and dir.startswith("smali"):
                        app_sources_path = join(self.apk_decompiled_path, dir)
                        for path in self.package_name.split("."):
                            app_sources_path = join(app_sources_path, path)
                        if isdir(app_sources_path):
                            break

                app_sources_path_new = app_sources_path[:-1] + chr(ord(app_sources_path[len(app_sources_path) - 1]) + 1)
                rename(app_sources_path, app_sources_path_new)

                if 1 < self.modding_level:
                    for level in range(self.modding_level - 1):
                        app_sources_path = dirname(app_sources_path)
                        if app_sources_path == self.apk_decompiled_path:
                            sys.exit("Reached root ... Try lower Modding Level")

                if isdir(app_sources_path):
                    self.mod_files(app_sources_path)

                cloned_apk_path = join(getcwd(), "".join((basename(self.apk_path)[:-4], "-", str(clone + 1), ".apk")))

                compilation_command = " ".join(
                    (self.java_path, "-jar", self.apkTool_path, "b", self.apk_decompiled_path, " -o ",
                     basename(cloned_apk_path)))
                # Finally Build
                os.system(compilation_command)
                # Then Sign
                if self.signer_path:
                    signing_command = " ".join((self.java_path, "-jar", self.signer_path, "-a", cloned_apk_path,
                                                "--allowResign --overwrite",
                                                "--ks", self.keystore_path,
                                                "--ksPass", self.keystore_password,
                                                "--ksAlias", self.keystore_alias,
                                                "--ksKeyPass", self.keystore_alias_password))
                    os.system(signing_command)
        try:
            os.remove(self.apk_decompiled_path)
        except Exception as e:
            print(e)

    def mod_files(self, app_sources_path):

        for root, dirs, files in os.walk(app_sources_path, topdown=True):
            for dir in dirs:
                self.mod_files(join(root, dir))
            for file in files:
                file_path = join(root, file)
                print("Working on " + file_path)
                with open(file_path, "r+") as file:
                    data = file.read()
                data = data.replace(self.package_name, self.package_name_new)
                data = data.replace(self.package_name.replace(".", "/"), self.package_name_new.replace(".", "/"))
                with open(file_path, "w") as file:
                    file.write(data)

    def load_setting(self):
        with open("config.json", "r", encoding="utf-8") as config_file:
            settings = json.load(config_file)
        return settings


if __name__ == '__main__':
    argparser = ArgumentParser()
    argparser.add_argument("-i", "--input",
                           required=True,
                           help="Path to apk file")
    argparser.add_argument("-n", "--no_of_apks",
                           required=False,
                           help="No of cloned apks (Default = 1)")
    argparser.add_argument("-l", "--level",
                           required=False,
                           help="App resources level")

    args = vars(argparser.parse_args())

    apkcloner = ApkCloner(apk_path=args["input"],
                          no_of_clones=args["no_of_apks"],
                          level=args["level"])
    apkcloner.run()
