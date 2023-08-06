import sys
import os
import re
import warnings
warnings.simplefilter("once")
warnings.filterwarnings("ignore", category=DeprecationWarning)
from pathlib import Path, PurePath
from json.decoder import JSONDecodeError

import obspy
from obspy.core.inventory import Inventory,  Station, Channel, Site
from obspy.core.inventory import Network as obspy_Network
from obspy.clients.nrl import NRL

from ..network import (Network)
from ..obsMetadata.obsmetadata import (ObsMetadata)
from ..misc.discoveryfiles import (Datapath)
from ..print_version import main as print_version 
import obsinfo



# We'll first create all the various objects. These strongly follow the
# hierarchy of StationXML files.

# Succesful treatment 
EXIT_SUCCESS = 0
# File could not be processed, generic reasons 
EXIT_FAILURE = 1

# Reference: https://www.freebsd.org/cgi/man.cgi?query=sysexits&manpath=FreeBSD+4.3-RELEASE

# bad CLI parameters 
EXIT_USAGE = 64
#bad file content (input file : Network metadata file) 
EXIT_DATAERR = 65
# file not found (input file : Network metadata file) 
EXIT_NOINPUT = 66 
#A service is unavailable (This can occur if a support program or file does not exist) 
EXIT_UNAVAILABLE = 69 

# (technical/internal error)
# An internal software error has been detected 
EXIT_SOFTWARE = 70

#can't create file (report file, output file)
EXIT_CANTCREAT = 73 
#An error occurred while doing I/O on some file */
EXIT_IOERR = 74 

#Something was found in an unconfigured or misconfigured state */
EXIT_CONFIG = 78 


def main():
    
    dp = Datapath()
    # create list of directories to search for files    
    verbose, quiet, test, validate, debug, remote, input_filename, output_filename, schemapath = retrieve_arguments(dp)
    
    if verbose:
        print(f'Using OBSINFO_DATAPATH: {dp.datapath_list}')    
        
    try:               
                         
        file = Path(input_filename).name    
       
        if validate:
            if verbose:
                print(f'Validating network file: {file}')
                
            ret = ObsMetadata().validate(schemapath,  str(input_filename), "yaml", 
                                         "network", verbose, "network", False)
                    
        info_dict = ObsMetadata.read_info_file(input_filename, dp, remote)
        
        net_dict = info_dict.get('network', None)
        if not net_dict:
            return 
                
        if verbose:
            print(f'Processing network file: {file}')
        
        obj = Network(ObsMetadata(net_dict))
                  
        if verbose:
           print(f'Network file parsed successfully for: {file}')
           
        networks=[obj.obspy_network]
        if not isinstance(obj.obspy_network, obspy_Network):
            print("Not a network object")
            
        if not quiet:
           print(obj.obspy_network)
        
            
        version = os.environ.get('OBSINFO_VERSION')
        
        author = get_first_author(info_dict)
    
        inv = Inventory(
                networks,
                module=version,
                module_uri="https://gitlab.com/resif/obsinfo",
                sender=author,
                source="ObsPy")
    
        if not test: # Generate Stationxml file
            stem_name = Path(file).stem      # remove .yaml
            stem_name = Path(stem_name).stem #Remove .network
            
            output_filename = stem_name + ".station.xml"
            stationxml=inv.write(output_filename, format="stationxml", validate=False)
         
        if not quiet:
           print(f'StationXML file created successfully: {output_filename}')        
               
    except TypeError:
        if debug:
            raise
        print("Illegal format: fields may be missing or with wrong format in input file, or there is a programming error")
        sys.exit(EXIT_DATAERR)
    except (KeyError, IndexError):
        if debug:
            raise
        print("Illegal value in dictionary key or list index")
        sys.exit(EXIT_SOFTWARE)
    except ValueError:
        if debug:
            raise
        print("An illegal value was detected")
        sys.exit(EXIT_DATAERR)
    except FileNotFoundError:
        if debug:
            raise
        print("File could not be found")
        sys.exit(EXIT_NOINPUT)
    except JSONDecodeError:
        print("File and/or subfiles have an illegal format. Probably indentation or missing quotes/parentheses/brackets")
        if debug:
            raise 
        sys.exit(EXIT_DATAERR)
    except (IOError, OSError, LookupError):
        if debug:
            raise
        print("File could not be opened or read")
        sys.exit(EXIT_UNAVAILABLE)
    except:
        print("General exception")
        if debug:
            raise
        sys.exit(EXIT_FAILURE)
        
    exit(EXIT_SUCCESS)
    
  
def retrieve_arguments(datapath):
    
    options_dict = {
                       "output": "o",
                       "verbose" : "v",
                       "version" : "v",
                       "quiet" : "q",
                       "debug" : "d",
                       "test" : "t",
                       "validate" : "l",
                       "remote_discovery" : "r",
                       "help" : "h",
                     }
    
    input_filename = output_filename = None
    verbose = quiet = test = False
    validate = debug = remote = False
    
    skip_next_arg = False
    path_exists = False
            
    long_option = re.compile("^[\-][\-][a-zA-Z_]+$")
    short_option = re.compile("^[\-][a-zA-Z]$")
    possible_options = re.compile("^[Vvqtldorh]+$")
    
    input_filename = ""
    
    option = None
    
    for arg in sys.argv[1:]:

        if skip_next_arg:
            skip_next_arg = False
            continue
        
        if re.match(long_option, arg):  
            option = options_dict.get(arg[2:])
        elif not arg[0] == "-":
            input_filename = arg
            continue  
        else:
            option = arg[1:]
        
        if not re.match(possible_options, option):
            s = f'Unrecognized option in command line: -{option}\n'
            s += usage()
            sys.exit(EXIT_USAGE)
        
        for opt in option:
    
            if opt == "o":
                if len(option) == 1:
                    output_filename = sys.argv[sys.argv.index("-o" if "-o" in sys.argv else "--output")+1]
                    skip_next_arg = True
                else:
                    warnings.warn('-o option should stand alone and be followed by a filename')
                    break
            elif opt == "v":
                verbose = True
            elif opt == "q":
                quiet = True
            elif opt == "d":
                debug = True  
            elif opt == "t":
                test = True
            elif opt == "l":
                validate = True
            elif opt == "V":
                print_version()
                sys.exit(EXIT_SUCCESS)
            elif opt == "r":
                remote = True
            elif opt == "h": 
                print(usage())
                sys.exit(EXIT_USAGE)
            
        skip_next_arg = False
    
    # schemas must always be installed under obsinfo/data/schemas   
    schemapath = Path(obsinfo.__file__).parent.joinpath('data', 'schemas')
    
    if not input_filename:
        print("No input filename specified")
        sys.exit(EXIT_USAGE) 
    
    input_filename = str(datapath.build_datapath(arg) if remote \
                         else Path(os.getcwd()).joinpath(input_filename))
    
            
    return (verbose, quiet, test, validate, debug, remote, input_filename, output_filename, schemapath)   

def get_first_author(info_dict):
    """
    Get info file first author info and return a string
    """
    rev = info_dict.get('revision', None)
    if not rev:
        return ""
   
    authors = rev.get('authors', None)

    if authors:
        author = authors[0].get('first_name', "") + " " + authors[0].get('last_name', "") \
           + ", " + authors[0].get('institution', "") +  " Email: " + authors[0].get('email', "") + "  Phones: "
        for phn in authors[0].get('phones', ""):
            author += phn + " "
    
    return author 
        

def usage():
    s = f'Usage: {sys.argv[0]} -vqdtlrdh  [-o <filename>] [-i] <filename>\n'
    s += f'Where:\n'
    s += f'      -v or --verbose: prints processing progression\n'
    s += f'      -q or --quiet: silences a human readable summary of processed information file\n'
    s += f'      -d or --debug: turns on the trace of exceptions\n'
    s += f'      -t or --test: enters test mode, produces no output\n'
    s += f'      -l or --validate: validate the YAML or JSON format of the information file. Used when file syntax is trusted\n'
    s += f'      -r or --assume input filename is discovered through OBSINFO_DATAPATH environment variable. Does not affect treatment of $ref in info files\n'
    s += f'      -h or --help: prints this message\n'
    s += f'      -o or --output: names the output file. Default is station.xml\n'
    
    
    return s
    
if __name__ == '__main__':
    main()