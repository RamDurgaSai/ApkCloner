use std::fmt::format;
use std::path::{PathBuf, Path};
use std::fs::{File, read_dir, read, read_to_string};
use std::process::Command;
use std::env::current_dir;
use std::io::{BufReader, Read, Write};

use xml::reader::{EventReader, XmlEvent};

const APK_EXTENSION: &str = "apk";


#[derive(Debug)]
pub struct Apk{
    pub path : Box<PathBuf>,
    pub name: String,
    pub size: u64,
    pub decompiled_path: Box<PathBuf>,
    is_decompiled: bool

}


impl Apk {

    pub fn from_path(path: PathBuf) -> Self{

        let apk = File::open(&path).unwrap();
        let apk_size = apk.metadata().unwrap().len();
        let path1 = path.clone();
        let name: Vec<&str>  = path.to_str().unwrap().split(".").collect();
        let basename = name[0];
        let extension = name[1];

        

        if extension != APK_EXTENSION{
            panic!("Given File is not a valid apk file ")
        }

        let mut cwd = current_dir().unwrap();

        let name = format!("{}-decompiled", basename);

        cwd.push(name);
        
        Apk { path: Box::new(path1), 
            name: String::from(basename), 
            size: apk_size,
            decompiled_path: Box::new(cwd) ,
            is_decompiled: false }
    }

    pub fn decompile(&mut self ) {

        
        let mut command = Command::new("java").args(["-jar", "apktool.jar", "d", "-f" , self.path.to_str().unwrap(), "-o", self.decompiled_path.to_str().unwrap()  ])
                                        .spawn().expect("Cannot decompile the apk");

        command.wait();
        
        println!("{:?}", command);

        self.is_decompiled = true;

    }

    pub fn sign(&mut self, apk_path: &PathBuf) -> &Self{

        if !self.is_decompiled{
            panic!("Cannot signed the decompiled app");
        }

        let mut command = Command::new("java").args(["-jar", "signer.jar", "-a", apk_path.to_str().unwrap(),
                                                                            "--allowResign --overwrite",
                                                                            "--ks", "",
                                                                            "--ksPass", "",
                                                                            "--ksAlias", "",
                                                                            "-ksKeyPass", "" ]).spawn().expect("Cannot sign the apk");
        self
    }
  
    pub fn sources_path(&mut self) ->Box<PathBuf>{

        let package_name = self.package_name();
        let mut sources_path = self.decompiled_path.clone();

        for dir in self.decompiled_path.read_dir(){

            for file in dir.map(|file| file.unwrap()){
                let file = file;
                let dirname = file.file_name().to_str().unwrap().to_owned();
                let path = file.path();

                if dirname.starts_with("smali"){
                    let mut sources_path = sources_path.join(PathBuf::from(dirname));
                    
                    for path in package_name.split("."){
                        sources_path = sources_path.join(PathBuf::from(path))
                    }

                    if sources_path.is_dir(){
                        return Box::new(sources_path)
                    }
                }
            }

        }
        sources_path
        
    }

    fn manifest_file(&mut self) -> File{
        let manifest_file_path = self.decompiled_path.join(PathBuf::from("AndroidManifest.xml"));

        let manifest_file = File::open(manifest_file_path).unwrap();

        manifest_file
    }
    
    pub fn package_name(&mut self) -> String{

        let manifest_file = self.manifest_file();

       
        let file = BufReader::new(manifest_file);

        let parser = EventReader::new(file);

        let mut package_name = String::new();

        for e in parser {
            match  e {
                Ok(XmlEvent::StartElement {name, attributes, .. }) =>{

                    if name.local_name == "manifest"{
                        for attr in attributes{
                            if attr.name.local_name == "package"{
                                package_name = String::from(attr.value)
                            }
                        }
                    }
                        
                }
                _ => {}
            }
        }
        return package_name
    }

    pub fn set_package_name(&mut self, old_package_name: String, new_package_name: String) {

        let mut manifest_file = self.manifest_file();

        let mut content = String::new();

        manifest_file.read_to_string(&mut content).unwrap();

        content = content.replace(old_package_name.as_str(), new_package_name.as_str());

            {
                let manifest_file_path = self.decompiled_path.join(PathBuf::from("AndroidManifest.xml"));

                let mut manifest_file = File::create(manifest_file_path).unwrap();

                manifest_file.write_all(content.as_bytes()).unwrap();

            }

        }
}
