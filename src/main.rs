#![allow(unused)]

use clap::Parser;
use std::collections::btree_map::Entry;
use std::ffi::{OsString, OsStr};
use std::fs::File;
use std::io::{Read, Write};
use std::{env, vec, clone};
use std::{path::{PathBuf, Path}, str::FromStr};
use walkdir::WalkDir;
// use std::os::linux::

mod cli;
mod apk;

const FORMATS: (&str, &str, &str, &str, &str)= ("json", "xml", "smali", "kt", "java");
const NO_EXTENSION: &str = "no_extension";


fn main() {
    let args = cli::Cli::parse();
    let mut apk  = apk::Apk::from_path(args.apk_path.clone());
    
    println!("{:?}", args);
    println!("{:?}", apk);

    println!("working on {:?}", &apk.name);
    println!("Decompiling the Apk\n\n");

    apk.decompile(); // Decompile The apk first

    let original_package_name = apk.package_name();
    let mut sources_path = *apk.sources_path();

    let length = original_package_name.len();
    let last_char = original_package_name.chars().last().unwrap() as u8;
    let first_part = original_package_name[..length-1].to_owned();

    let package_names = (1..args.no_apks+1)
                                        .map(|clone| format!("{}{}", first_part, (last_char + clone) as char))
                                        .collect::<Vec<String>>();
    
    let target_dirs = (1..args.no_apks+1).map(
        |clone| PathBuf::from(format!("{}{}{}", apk.decompiled_path.to_str().unwrap(), "-", clone))
    ).collect::<Vec<PathBuf>>();

    let mut sources_path = sources_path.as_path();

    for _ in 0..args.level{
        sources_path = sources_path.parent().unwrap();

        if sources_path == apk.decompiled_path.parent().unwrap(){
            panic!("Crosed the root dir - Please decrease level ")
        }

    }
    
    let no_extension = OsStr::new(NO_EXTENSION);

    for clone in 1..args.no_apks+1{

        let mut package_name = {
            if clone == 1 {original_package_name.clone()} else {
                format!("{}{}", first_part, (last_char + clone -1) as char)
            }
        };

        let new_package_name = format!("{}{}", first_part, (last_char + clone) as char);

        apk.set_package_name(package_name.to_owned(), new_package_name.to_owned());

        for entry in WalkDir::new(sources_path){
            let entry = entry.unwrap();
            let path = entry.path();
            let extension = entry.path().extension().unwrap_or(no_extension);
        
            if path.is_file() && extension != NO_EXTENSION && (extension == FORMATS.0 || extension == FORMATS.1 
                        || extension == FORMATS.2 || extension == FORMATS.3 || extension == FORMATS.4){
                
                            println!("{:?}", entry.path());
    
                let mut file = File::open(entry.path()).unwrap();
    
                let mut content = String::new();
    
                let result = file.read_to_string(&mut content);
    
                content = content.replace(package_name.as_str(), new_package_name.as_str());
                
                // println!("{:?}", content);
                // println!("{:?}", &new_content);

                let mut new_file = File::create(entry.path()).unwrap();

                new_file.write_all(content.as_bytes()).unwrap();
               
            }
        }
        break;
    }

}
    
