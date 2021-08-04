# Apk Signer
## Small Python Script that can make dozens of clones of android apk
# 

## Installation
    Just clone the repo from Github
# 

## Basic usage:

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
## Note 
    This Not Work For All Apks

