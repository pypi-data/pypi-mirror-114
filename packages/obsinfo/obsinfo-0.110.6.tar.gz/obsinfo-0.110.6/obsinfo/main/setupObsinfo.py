import os
import sys
import re
import site
import shutil
import datetime
import platform
from pathlib import Path

from argparse import ArgumentParser

import obsinfo

from obsinfo.version import __version__

EXIT_IOERR = 74 

def setup_obsinfo():
    
    # initialize variables
    version = platform.python_version()    
    path_to_package = Path(obsinfo.__file__).parent
    examples_dir = path_to_package.joinpath("_examples/Information_Files")
    templates_dir = path_to_package.joinpath("templates")     
    home = Path.home()
    configuration_file = home.joinpath('.obsinforc')
    
    args = retrieve_arguments()
    
    validate_arguments(args)    
    
    # copy examples and templates
    if args.dest and not args.no_copy:
        try:
            dest = Path(args.dest)
            # if dest dir exists rename it with timestamp in order to preserve it
            if os.path.isdir(dest) or os.path.isfile(dest):
                new_dest = str(dest) + "." + str(datetime.datetime.today())
                os.rename(dest, new_dest)
            shutil.copytree(examples_dir, dest.joinpath("Information_Files"))
            shutil.copytree(templates_dir, dest.joinpath("templates"))
        except NotADirectoryError:
            print("Directory not found")
            exit(EXIT_IOERR)
        except OSError:
            print("Operating system error")
            exit(EXIT_IOERR)
    # create configuration file
    output=[]
    
    output.append("gitlab_repository: " +  args.gitlab + "\n")
    output.append("gitlab_project: " + args.project + "\n")
    output.append("gitlab_path: " + args.remote_path + "\n")
    pat = re.compile("^[0-9]+\.[0-9]+")
    version = pat.match(__version__)
    output.append('obsinfo_version: "' + version.group(0) + '"\n')
    
    remote_repository = args.gitlab + "/" + args.project + "/" + args.remote_path \
          if not args.no_remote else ""
    
    s = build_datapath_list(args, remote_repository)
    if s:
        output.append(s + "\n")
        
    try:
        with open(configuration_file, "w") as fp:
           
          fp.writelines(output)
    
    except OSError:
        warnings.warn("Could not create configuration file. Fix problem and run obsinfo-setup again\n")
        exit(EXIT_IOERR) 
        
        
def retrieve_arguments():
    
    # Parse the arguments
    parser_args = ArgumentParser(prog="obsinfo-validate", description=__doc__)
    parser_args.add_argument("-d", "--dest", nargs='?', default=None,
                             help="Destination directory for templates and examples.",
                            )
    parser_args.add_argument("-g", "--gitlab", nargs='?', default="https://www.gitlab.com",
                             help="Gitlab repository)",
                            )
    parser_args.add_argument("-p", "--project", nargs='?', default="resif/obsinfo",
                             help="path to project and the directory where information files lie within the Gitlab repository)",
                            )
    parser_args.add_argument("-l", "--local_repository", nargs='?', default=None,
                             help="Specify local repository for information files and include it as first or second option in datapath")
    parser_args.add_argument("-w", "--working_directory", nargs='?', default=None,
                             help="Specify working directory for obsinfo and include it as first option in datapath")
    
    parser_args.add_argument("-P", "--remote_path",  default="obsinfo/_examples/Information_Files",
                             help="Specify remote directory under project"
                            ) 
       
    parser_args.add_argument("-x", "--no_examples",  default=False,
                             help="Don't import examples, only templates, and remove examples directory from the datapath\n"
                            ) 
    
    parser_args.add_argument("-c", "--no_copy",  default=False,
                             help="Don't import anything at all, don't create dest directory, which will be removed from datapath\n"
                            ) 
    
     
    parser_args.add_argument("-r", "--no_remote",  default=False,
                             help="Install obsinfo without access to a gitlab repository.\n\
                             May be needed in some operating systems for compatibility issues",
                            )  
    parser_args.add_argument("-v", "--invert_datapath",  default=False,
                             help="Put remote gitlab repositorey first. All local directories will keep their order"
                            )                

    #create configuration file
    return parser_args.parse_args()   

def validate_arguments(args):
    
    if args.dest:
        if not Path(args.dest):
            raise OSError(ENOENT, "Path for example and template destination directory is an illegal path")
    else:
        default_information_files = ""
    
    if args.local_repository:
        if not Path(args.local_repository):
            raise OSError(ENOENT, "Path for local repository for information files is an illegal path")
    
    if args.working_directory:
        if not Path(args.working_directory):
            raise OSError(ENOENT, "Path for obsinfo working directory is an illegal path")
    
    if not args.no_remote:
        if not Path(args.gitlab).as_uri:
            raise ValueError('Gitlab repository must be specified as a legal URI unless "-n" is on')
    
    if not args.no_remote:
        if not Path(args.project):
            raise ValueError('Project must be specified as a legal URI unless "-n" is on')
                    
def build_datapath_list(args, remote_repository):
    """
    # Build datapath
    # Add working_directory as first option if it exists, otherwise build datapath with local repository first if it exists;
    # default for local is destination, but this won't be used if -x is on
    # Final place will be remote unless -v is specified
    
    """
    
    default_information_files = str(Path(args.dest).joinpath("Information_Files")) if args.dest else ""
    remote_first = remote_repository + ", " if args.invert_datapath else ""
    remote_last = remote_repository if not args.invert_datapath else ""
    
    s =  "datapath: ["
    s += remote_first 
    s += args.working_directory + ", " if args.working_directory else "" 
    s += args.local_repository + ", " if args.local_repository else ""
    s += default_information_files  + ", " if default_information_files and not args.no_examples else ""
    s += remote_last if remote_last else ""
    s += "]"
    
    if not remote_last:
         s.replace(", ]", "]")

    return s            
        