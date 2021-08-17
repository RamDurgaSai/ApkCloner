import sys
from argparse import ArgumentParser
from os.path import join, basename, dirname
from os import getcwd, walk
from threading import Thread
from typing import List
from os import  cpu_count

from settings import Settings
from apk import Apk

class ApkCloner:
    """
    Class Apk cloner
    """
    DEBUG = False #Debug
    DEFAULT_THREADS = int(cpu_count()) # Threads
    def __init__(self,
                 apk_path:str,
                 no_of_clones=1,
                 level=1):
        if no_of_clones:
            self.clones = int(no_of_clones)
        else:
            self.clones = 1
        if level:
            self.level = int(level)
        else:
            self.level = 1


        self.apk = Apk(apk_path)
        self.settings = Settings()

        self.files:List[str] = [] # To Hold all smali files

        self.say_welcome()

    def run(self):
        """
        Cloning Apk by loop
        :return: None
        """
        print("\n\nWorking On "+ self.apk.name)
        print("Decompiling Apk")
        path = self.apk.decompile(None)

        # Building Clones By loop:
        for clone in range(self.clones):
            print("\nBuilding Clone :- "+ str(clone+1))
            package_name = self.apk.get_package_name()
            sources_path = self.apk.get_sources_path()



            new_package_name = package_name[:-1] + chr(
                    ord(package_name[len(package_name) - 1]) + 1)
            new_sources_path = sources_path[:-1] + chr(ord(sources_path[len(sources_path) - 1]) + 1)

            cloned_apk_path = join(getcwd(), "".join((basename(self.apk.path), "-", str(clone + 1), ".apk")))
            print(f"Package Name:- {package_name} \nNew Package Name:- {new_package_name}")
            # Check Modding Level
            if 1 < self.level:
                for level in range(self.level - 1):
                    sources_path = dirname(sources_path)
                    if sources_path == self.apk.path:
                        sys.exit("Reached root ... Try lower Modding Level")

            for root, dir, files in walk(sources_path,topdown=True):
                for file in files:
                        file_path = join(root, file)
                        if basename(file).endswith(".smali"):
                            self.files.append(file_path)

            '''
            # Starts thread (Default 4)
            # Taken From:- https://stackoverflow.com/questions/2130016/splitting-a-list-into-n-parts-of-approximately-equal-length
            files_es = [self.files[i:i + self.DEFAULT_THREADS] for i in
                        range(0, len(self.files), self.DEFAULT_THREADS)]
            ######################################################################################################################


            threads: List[Thread] = []
            for files in files_es:
                thread = Thread(target=self.mod_files, args=(files,package_name,new_package_name), daemon=True)
                threads.append(thread)
                thread.start()
                thread.join()
            '''

            #Single Threaded
            self.mod_files(self.files,package_name,new_package_name)

            self.apk.set_package_name(new_package_name)
            self.apk.set_sources_path(new_sources_path)
            print("\nCompiling Apk")
            self.apk.compile(apk_path=cloned_apk_path)
            if self.settings.signer_path:
                print("\nSinging Apk")
                self.apk.sign(apk_path=cloned_apk_path)




    def mod_files(self, files,
                  package_name,new_package_name):
        """
        Mod files by changing package name in files

        :param files: all files that needs to mod
        :param package_name: package_name for modding
        :param new_package_name: new package name
        :return: None
        """

        for file_path in files:

            with open(file_path, "r+") as file:
                data = file.read()
            data = data.replace(package_name, new_package_name) #For Strings
            data = data.replace(package_name.replace(".", "/"), new_package_name.replace(".", "/"))# For Classes paths

            with open(file_path, "w") as file:
                file.write(data)

            if self.DEBUG:
                print("Modding File "+file_path)

    def say_welcome(self):
        """
        say welcome to user through console
        :return: None
        """
        welcome_string = " ".join((
            "Apk Cloner V 2.0 copyright (C) 2021 https://github.com/RamDurgaSai/ApkCloner",
            "\n\nRunning on" ,str(sys.platform), "| Cpu Count" ,str(cpu_count()),
            "\n\njava   ",str(self.settings.java_path),
            "\nApkTool",str(self.settings.apkTool_path),
            ))
        if self.settings.signer_path:
            welcome_string = " ".join((welcome_string,"\nSigner ",str(self.settings.signer_path)))
        print(welcome_string)



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
