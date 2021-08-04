from os import rename,walk
from os.path import join,dirname
def get_name(string):
    for line in string.splitlines():
        if line.startswith("/*") and line.endswith("*/"):
            if line.find("compiled from:") != -1:
                for word in line.split():
                    if word.endswith(".kt") or word.endswith(".java"):
                        return word[:-3]
                return line[18:-3]

def mod_files(sources_path):

    for root, dirs, files in walk(sources_path, topdown=True):
        for dir in dirs:
            mod_files(join(root, dir))
        for file in files:
            file_path = join(root, file)
            print("Working on " + file_path)
            with open(file_path, "r+") as file:
                try:
                    data = file.read()
                except:
                    continue
            name = get_name(str(data))
            if name:
                try:
                    rename(file_path,join(dirname(file_path),"".join((name,".java"))))
                except FileExistsError as e:
                    print("".join(("Conflit found file already exits in ",file_path)))

if __name__ == '__main__':
    mod_files("D:\\Swiggy Env\\swiggy-delivery-partner-app_3.15.4(818).apk-decompiled\\sources\\in\\swiggy")

