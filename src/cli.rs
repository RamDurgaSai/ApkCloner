use clap::Parser;
use std::path::PathBuf;

#[derive(Parser, Debug) ]
#[clap(author="Ram Durga Sai", version="3.0",about="APK Cloner Copyright (C) 2022 https://github.com/RamDurgaSai/ApkCloner" )]
pub(crate) struct Cli {
    #[clap(parse(from_os_str), short='i', long="input", help="Path to apk file" )]
    pub apk_path: PathBuf,

    #[clap(short='n', long="no_of_apks", default_value_t=1, help="No of cloned apks")]
    pub no_apks: u8,

    #[clap(short='r', long="resources", help="resources of application will patched")]
    pub resources: Option<bool>,

    #[clap(short='l', default_value_t=0, long="level",help="level of modding")]
    pub level: u8
}