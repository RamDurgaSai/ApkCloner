# Apk Signer
## Small Python Script that can make dozens of clones of android apk
# 

## Installation
    Just clone the repo from Github
# 

## Basic usage

    python apkcloner.py -i /path/to/apk/file



## Command Line Interface

    usage: main.py [-h] -i INPUT [-n NO_OF_APKS] [-l LEVEL]
    optional arguments:
    -h, --help            show this help message and exit
    -i INPUT, --input INPUT
                        Path to apk fil
    -n NO_OF_APKS, --no_of_apks NO_OF_APKS
                        No of cloned apks (Default = 1)
    -l LEVEL, --level LEVEL
                        App resources level



## Config Json
     By Default apk cloner search for java, apkTool in Env
     If want to use own JDK or not in Env
     Set Path of JDK, Apk Tool and Uber Apk Signer
     Don't want sign apks ... Just leave Apk signer Path as null

## Signing
    Apk cloner Supports Apk Signer(By Uber Apk Signer)
    Set Keystore Path and other information in config.json
### Level
    If your cloned apk crashes then increase the level
### Example
    $python apkcloner.py -i swiggy.apk -l 3 -n 1
    Apk Cloner V 2.0 copyright (C) 2021 https://github.com/RamDurgaSai/ApkCloner

    Running on win32 | Cpu Count 4
    
    java    java
    ApkTool D:\Softwares\ApkTools\apktool.jar
    Signer  D:\Softwares\ApkTools\uber-apk-signer-1.2.1.jar
    
    
    Working On swiggy
    Decompiling Apk
    I: Using Apktool 2.5.0 on swiggy.apk
    I: Loading resource table...
    I: Decoding AndroidManifest.xml with resources...
    I: Loading resource table from file: C:\Users\RamDurgaSai\AppData\Local\apktool\framework\1.apk
    I: Regular manifest package...
    I: Decoding file-resources...
    I: Decoding values */* XMLs...
    I: Baksmaling classes.dex...
    I: Baksmaling classes2.dex...
    I: Baksmaling classes3.dex...
    I: Baksmaling classes4.dex...
    I: Copying assets and libs...
    I: Copying unknown files...
    I: Copying original files...
    I: Copying META-INF/services directory
    
    Building Clone :- 1
    
    Compiling Apk
    I: Using Apktool 2.5.0
    I: Checking whether sources has changed...
    I: Smaling smali folder into classes.dex...
    I: Checking whether sources has changed...
    I: Smaling smali_classes2 folder into classes2.dex...
    I: Checking whether sources has changed...
    I: Smaling smali_classes3 folder into classes3.dex...
    I: Checking whether sources has changed...
    I: Smaling smali_classes4 folder into classes4.dex...
    I: Checking whether resources has changed...
    I: Building resources...
    I: Copying libs... (/lib)
    I: Copying libs... (/kotlin)
    I: Copying libs... (/META-INF/services)
    I: Building apk file...
    I: Copying unknown files/dir...
    I: Built apk...
    
    Singing Apk
    source:
            C:\Users\RamDurgaSai\PycharmProjects\clone\ApkCloner
    zipalign location: BUILT_IN
            C:\Users\RAMDUR~1\AppData\Local\Temp\uapksigner-706793706693859316\win-zipalign_29_0_2.exe7335851606196422853.tmp
    keystore:
            [0] 98e21868 C:\Users\RamDurgaSai\Desktop\Keys\keystore.jks (RELEASE_CUSTOM)
    
    01. swiggy-decompiled-1.apk
    
            SIGN
            file: C:\Users\RamDurgaSai\PycharmProjects\clone\ApkCloner\swiggy-decompiled-1.apk (93.62 MiB)
            checksum: 3918c04d1129e6fca39a4401824c524d8c18d94346aafd9f125650c9988cf46c (sha256)
            - zipalign success
            - sign success
    
            VERIFY
            file: C:\Users\RamDurgaSai\PycharmProjects\clone\ApkCloner\swiggy-decompiled-1.apk (94.14 MiB)
            checksum: 66686114c8ad3bf65e369b3a7b45e3a6466c9dce981d001e80b8a8470f4bbfb9 (sha256)
            - zipalign verified
            - signature verified [v1, v2, v3]
                    6 warnings
                    Subject: CN=Swiggy Delivery, OU=Swiggy, O=Swiggy, L=Samalkot, ST=Andhra Pradesh, C=IN
                    SHA256: 6aba5f25b5cd7a0a98a0946406615c72dae04e8b12be511815a0980aecc580e2 / SHA256withRSA
                    Expires: Sat May 19 22:58:53 IST 2046
    
    [Tue Aug 17 17:05:59 IST 2021][v1.2.1]
    Successfully processed 1 APKs and 0 errors in 7.92 seconds.
## Note 
    This Not Work For All Apks

