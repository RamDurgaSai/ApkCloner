from os.path import isfile,isdir,basename, getsize, join as join_paths ,abspath
from os import system, listdir,getcwd
from xml.etree import ElementTree as ET
from shutil import  move as move_files

from Exceptions import NotApkFile,ApkNotDecompiled
from settings import Settings

class Apk:
    """Apk Class"""
    DEBUG = False
    def __init__(self,
                 apk_path:str):
        apk_path = abspath(apk_path)
        if(isfile(apk_path) and apk_path.endswith(".apk")):
            self.apk_path = apk_path
        else:
            raise NotApkFile(path=apk_path)


        self.name = basename(self.apk_path).split(".")[0]
        self.size = getsize(self.apk_path)
        self.package_name:str
        self.is_decompiled:bool


        self.settings = Settings() # Get Settings


    def decompile(self,path:str) -> str:
        """
        Decompiling the Apk

        :param path : where to decompile apk
        :type str

        :return path: Decompiled apk path
        :type str"""
        if not path:
            path = join_paths(getcwd(), "".join((self.name,"-decompiled")))
        decompilation_command = "".join(
            (self.settings.java_path, ' -jar "', self.settings.apkTool_path, '" d -f "', self.apk_path, '" -o', ' "',path,'"'))
        # Decompiling Apk
        if not self.DEBUG:
            system(decompilation_command)
        ################################

        self.path: str = path
        self.is_decompiled = True

        return path
    def compile(self,apk_path: str ) ->str:
        """ Compiles apk by ApkTool

        :param apk_path: path of compiled apk
        :return: apk_path: path of compiled apk (Default path if not specified
        """
        if self.is_decompiled:
            compilation_command = " ".join(
                (self.settings.java_path, "-jar", self.settings.apkTool_path, "b", self.path, " -o ",
                apk_path))

            # Finally Build
            system(compilation_command)
        else:
            raise ApkNotDecompiled(self)
        self.apk_compiled_path = apk_path

    def sign(self,apk_path: str  = None) -> str:
        """
            Sign Apk By Uber Apk Signer
        :param apk_path: path of apk to sign
        :return: apk_path
                    Default apk path if not supplied
        """
        try:
            if self.is_decompiled and self.settings.signer_path:
                if not apk_path:
                    apk_path = self.apk_compiled_path
                signing_command = " ".join((self.settings.java_path, "-jar", self.settings.signer_path, "-a",apk_path,
                                            "--allowResign --overwrite",
                                            "--ks", self.settings.keystore_path,
                                            "--ksPass", self.settings.keystore_password,
                                            "--ksAlias", self.settings.keystore_alias,
                                            "--ksKeyPass", self.settings.keystore_alias_password))
                system(signing_command)

            return apk_path
        except(AttributeError):
            raise AttributeError("Add Signer path and keystore details in config.json")


    def get_sources_path(self) -> str:
        """Getting App Specific Sources Path
        :returns sources_path
                    App Specific Sources (Not with additional Libraries )
                    Ex:- Apk has package Name com.company.app_name and decompiled path
                                                                foo/app-decompiled
                        app_sources_paht is foo/app-decompiled/smali_classes(3)/com/company/app_name
        :type str
        """
        app_sources_path = None
        if self.is_decompiled:
            package_name = self.get_package_name()
            for dir in listdir(self.path):
                if isdir(join_paths(self.path, dir)) and dir.startswith("smali"):
                    app_sources_path = join_paths(self.path, dir)
                    for path in package_name.split("."):
                        app_sources_path = join_paths(app_sources_path, path)
                    if isdir(app_sources_path):
                        break
            self.sources_path = app_sources_path
            return self.sources_path
        else:
            raise ApkNotDecompiled(self)
    def set_sources_path(self,path:str)-> None:
        """ Setting App Specific Sources Path
        :param path: Path of new app sources
                        App Specific Sources (Not with additional Libraries )
                Ex:- Apk has package Name com.company.app_name and decompiled path
                                                            foo/app-decompiled
                    app_sources_paht is foo/app-decompiled/smali_classes(3)/com/company/app_name

        :type str
        :return None
        """
        #move_files(self.get_sources_path(),path)



    def get_package_name(self) -> str:
        """Getting Package name of Apk (EX:- com.company.app_name)

        :return package_name : Package Name for APK
        :type str
        :exception ApkNotDecompiled
        """
        if not self.is_decompiled:
            raise ApkNotDecompiled(self)
        else:
            self.manifest_file = join_paths(self.path, "AndroidManifest.xml")
            return  str(ET.parse(self.manifest_file).getroot().attrib["package"])

    def set_package_name(self,package_name:str)->None:
        """Setting Package name for apk

        :param package_name: Package Name for APK
        :exception ApkNotDecompiled"""

        if self.is_decompiled:
            self.manifest_file = join_paths(self.path, "AndroidManifest.xml")
            with open(self.manifest_file, "r") as manifest:
                manifest_data:str = manifest.read()

            tree = ET.ElementTree(ET.fromstring(
                manifest_data.replace(self.get_package_name(), package_name)))
            tree.write(self.manifest_file)
        else:
            raise ApkNotDecompiled(self)