#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
Functions to test the lcheapo functions
There are two types of testing functionalities.
a) If the file name includes "test--attributes" the output of the corresonding obsinfo test function
will be checked against data contained in this class.
b) If the fine name is "normal", it will simply run through to make sure there are no errors
Testing for filters uses data from obsinfo/tests/data/Information_Files/responses/_filters. 
Testing for all other classes uses data from obsinfo/_examples/Information_Files 
WARNING: many tests are crtically dependent on file hierarchy, including names. Do not change names
in tests or _examples hierarchy, or else change the names here.
Also, the following methods use four specific filen names:
test_all_stage_types()
test_senso()
test_preamplifier()
test_datalogger()
test_station()
"""
from __future__ import (absolute_import, division, print_function,
                        unicode_literals)
from future.builtins import *  # NOQA @UnusedWildImport

import os
import warnings
warnings.simplefilter("once")
warnings.filterwarnings("ignore", category=DeprecationWarning)
import sys
from pathlib import Path, PurePath
import unittest
import inspect
import difflib
import re
import glob
from json.decoder import JSONDecodeError

from obspy.core.utcdatetime import UTCDateTime
# from pprint import pprint
# import xml.etree.ElementTree as ET
# from CompareXMLTree import XmlTree
from obsinfo.obsMetadata.obsmetadata import (ObsMetadata)
from obsinfo.instrumentation import (Instrumentation, InstrumentComponent,
                                     Datalogger, Preamplifier, Sensor,
                                     ResponseStages, Stage, Filter)
from obsinfo.instrumentation.instrumentation import (Location)
from obsinfo.network import (Station, Network)
from obsinfo.instrumentation.filter import (Filter, PolesZeros, FIR, Coefficients, ResponseList,
                     Analog, Digital, AD_Conversion)
from obsinfo.misc.printobs import  (PrintObs)
from obsinfo.misc.discoveryfiles import Datapath
import obsinfo

class JsonRefTest(unittest.TestCase):
    
    def assertTextFilesEqual(self, first, second, msg=None):
        with open(first) as f:
            str_a = f.read()
        with open(second) as f:
            str_b = f.read()

        if str_a != str_b:
            first_lines = str_a.splitlines(True)
            second_lines = str_b.splitlines(True)
            delta = difflib.unified_diff(
                first_lines, second_lines,
                fromfile=first, tofile=second)
            message = ''.join(delta)

            if msg:
                message += " : " + msg

            self.fail("Multi-line strings are unequal:\n" + message)

    def test_readJSONREF_json(self):
        """
        Test JSONref using a JSON file.
        """
        fname_A =  PurePath(self.testing_path).joinpath("jsonref_A.json")
        A = ObsMetadata.read_json_yaml_ref(fname_A, None)
        AB = ObsMetadata.read_json_yaml_ref(PurePath(self.testing_path).joinpath(
                                              "jsonref_AB.json"), None)
        self.assertTrue(A == AB)

    def test_readJSONREF_yaml(self):
        """
        Test JSONref using a YAML file.
        """
        A = ObsMetadata.read_json_yaml_ref(PurePath(self.testing_path).joinpath(
                                             "jsonref_A.yaml"), None)
        AB = ObsMetadata.read_json_yaml_ref(PurePath(self.testing_path).joinpath(
                                              "jsonref_AB.yaml"), None)
        self.assertTrue(A == AB)

    def test_validate_json(self):
        """
        Test validation on a YAML file.

        The test file as an $ref to a file that doesn't exist, a field that
        is not specified in the the schema, and lacks a field required in
        the schema
        """
        test_file = PurePath(self.testing_path).joinpath( 'json_testschema.json')
        test_schema = PurePath(self.testing_path).joinpath(
                                   'json_testschema.schema.json')
        # self.assertFalse(validate(test_file, schema_file=test_schema,
        #                           quiet=True))

        # Run the code
        cmd = f'obsinfo-validate -s {test_schema} {test_file} > temp'
        os.system(cmd)

        # Compare text files
        self.assertTextFilesEqual(
            'temp',
            PurePath(self.testing_path).joinpath( 'json_testschema.out.txt')
            )
        os.remove('temp')
          

class TestObsinfo(unittest.TestCase):
    """
    Test suite for obsinfo operations.
    """
    def setUp(self, verbose=True, test=True, print_output=False, level=None, ):
        """
        Set up default values and paths
        """   
        self.infofiles_path =  Datapath()
    
        self.level = level
        self.verbose = verbose
        self.test = test
        self.print_output = print_output
        
    def test_all_filters(self):
        """
        Test all information files in test/data/Information_Files/responses/_filters" subdirectory
        If you wish to test individual files, use test_filter(file) with file an absolute or 
        relative file name.
        """
        for dir in self.infofiles_path.datapath_list:
            files_in_validate_dir = Path(dir).joinpath(
                "*rs", # includes sensors, preamplifiers and dataloggers
                "responses",
                "filters/*.yaml")
            
            filelist = glob.glob(str(files_in_validate_dir))
            
            for file in filelist:
                self._test_filter(file)
            
            #if self.test:
            #   self._test_PZ_conditionals()
                    

    def _test_filter(self, info_file):
        """
        Test reading a filter file. All are actual examples except the info files called "test---attributes. 
        In this special cases there will also be a comparison against a dict of expected results
        """
        test_expected_result = { 
            'PolesZeros' : 
                {
                    "type": "PolesZeros",
                    "transfer_function_type": "LAPLACE (RADIANS/SECOND)",
                    "zeros": [(0.0+0.0j)],
                    "poles": [(0.546+0.191j), (4.00004e4+0.000j),],
                    "normalization_frequency" : 1.,
                    "normalization_factor" : 42833.458122775904,
                    "offset": 0,  
                },
            'FIR' : 
                {
                    "type": "FIR",
                    "symmetry": "ODD",
                    "coefficient_divisor": 8388608,
                    "coefficients": [-10944, 0, 103807, 0, -507903, 0, 2512192, 4194304,],
                    "offset": 7,  
                },
            'Coefficients' : 
                {
                    "type" : "Coefficients",
                    "transfer_function_type" : "DIGITAL", 
                    "numerator_coefficients" :   [1, 0.1, -0.3, 0.6],
                    "denominator_coefficients" : [-0.2, 0.8, 0.4, -0.3],
                    "offset": 0,
                },
            'ResponseList' : 
                {
                    "type" : "ResponseList",
                    "offset": 0,  
                    "response_list" : [[ 0.050, 0.56, 0.0], [ 0.075, 0.73, 0.0], [ 1, 1, 0.0], [10, 0.97, -179], [100, 0.96, 179], [1000, 0.96, 179], [5000, 0.82, 143], [7500, 0.69, 129]],
                },
            'AD_CONVERSION' : 
                {
                    "type" : "AD_CONVERSION",
                    "input_full_scale" : 5,
                    "output_full_scale" : 4294967292,
                    "transfer_function_type" : "DIGITAL",
                    "numerator_coefficients" :   [1.0],
                    "denominator_coefficients" : [],
                    "offset": 0,  
                },
            'ANALOG' : 
                {
                    "type" : "ANALOG",
                    "transfer_function_type" : "LAPLACE (RADIANS/SECOND)",
                    "zeros": [],
                    "poles": [],
                    "normalization_frequency" : 0.,
                    "normalization_factor" : 1.0,
                    "offset": 0,      
                },
            'DIGITAL' : 
                {
                    "type" : "DIGITAL",
                    "transfer_function_type" : "DIGITAL",
                    "numerator_coefficients" :   [1.0],
                    "denominator_coefficients" : [],
                    "offset": 0,                   
                },
             }
            
        read_stream = ObsMetadata.read_info_file(info_file, self.infofiles_path)
        obj = Filter.dynamic_class_constructor(ObsMetadata(read_stream['filter']), "")
        
        if self.test:    
        #   self.assertTrue(isinstance(obj, obj.type), f'Object {info_file} is not a {obj.type} filter')    
            
           if re.match("test---attributes", str(info_file)): # compare with expected result
               self._filter_compare(info_file, obj, test_expected_result)
        
        
        if self.verbose:
           print(f'Filter test for: {info_file}: PASSED')
        
        if self.print_output:    
           print(obj)
           
    
    def _filter_compare(self, info_file, filter, expected_result):
        """
        Test a created filter object against an expected result to make sure all values are right
        """
        ftype = filter.type 
        read_dict = vars(filter)
        
        # Remove notes and extras
        if read_dict.get('notes', None) == []:
            read_dict.pop('notes')
        if read_dict.get('extras', None) == None:
            read_dict.pop('extras')
        
        self.assertEqual(read_dict,expected_result.get(ftype, None), 
f" File: '{info_file}'. Computed result: {read_dict} and expected result: {expected_result.get(ftype, None)} are different")
        
    
    def _test_PZ_conditionals(self):
        """
        Test all the conditionals in the PZ filter, and the function to calculate the normalization factor.
        """
        obj = Filter.dynamic_class_constructor(ObsMetadata({'type': 'PolesZeros', 
                                         'transfer_function_type' : 'LAPLACE (RADIANS/SECOND)',
                                         'zeros': [[0.3, 0.2],],
                                         'poles': [[0.546, 0.191], [4.40e4, 0.000],],
                                         'normalization_frequency' : 1.,
                                         'normalization_factor' : None,
                                          }), None, None, None)
        self.assertIn(obj.transfer_function_type, ['LAPLACE (RADIANS/SECOND)', 'LAPLACE (HERTZ)', 'DIGITAL (Z-TRANSFORM)'], 
                                              f'transfer function type wrong in test case for PZ {obj.transfer_function_type}')
        self.assertEqual(obj.normalization_factor,  44188.013594177224, 
                f'object normalization factor in test case for PZ {obj.normalization_factor} in PZ test is different from 44188.013594177224')
        print("1", end=" ")
        
        obj = Filter.dynamic_class_constructor(ObsMetadata({'type': 'PolesZeros', 
                                         'transfer_function_type' : 'LAPLACE (HERTZ)',
                                         'zeros': [[0.3, 0.2],],
                                         'poles': [[0.546, 0.191], [4.40e4, 0.000],],
                                         'normalization_frequency' : 1.,
                                         'normalization_factor' : None,
                                          }), None, None, None)
        self.assertIn(obj.transfer_function_type, ['LAPLACE (RADIANS/SECOND)', 'LAPLACE (HERTZ)', 'DIGITAL (Z-TRANSFORM)'], 
                                              f'transfer function type wrong in test case for PZ {obj.transfer_function_type}')
        self.assertEqual(obj.normalization_factor,  50262.70428857582, 
                    f'object normalization factor in test case for PZ {obj.normalization_factor} is different from 50262.70428857582')
        print("2", end=" ")
        
        obj = Filter.dynamic_class_constructor(ObsMetadata({'type': 'PolesZeros', 
                                         'transfer_function_type' : 'LAPLACE (RADIANS/SECOND)',
                                         'zeros': [[0.3, 0.2],],
                                         'poles': [[0.546, 0.191], [4.40e4, 0.000],],
                                         'normalization_frequency' : 120.,
                                         'normalization_factor' : None,
                                          }), None, None, None)
                                          
        self.assertEqual(obj.normalization_factor, 44006.99311749303, f'{obj.normalization_factor} in test case for PZ is different from 44006.99311749303')
        print("3", end=" ")
        
        obj = Filter.dynamic_class_constructor(ObsMetadata({'type': 'PolesZeros', 
                                         'transfer_function_type' : 'LAPLACE (RADIANS/SECOND)',
                                         'zeros': [],
                                         'poles': [],
                                         'normalization_frequency' : 1.,
                                         'normalization_factor' : None,
                                          }), None, None, None)
        
        self.assertEqual(obj.normalization_factor, 1., f'{obj.normalization_factor} is different from 1.')
        print("4", end=" ")
        
        obj = Filter.dynamic_class_constructor(ObsMetadata({'type': 'PolesZeros', 
                                         'transfer_function_type' : 'DIGITAL (Z-TRANSFORM)',
                                         'zeros': [[0.3, 0.2],],
                                         'poles': [[0.546, 0.191], [4.40e4, 0.000],],
                                         'normalization_frequency' : 1.,
                                         'normalization_factor' : None,
                                          }), None, None, None)
        
        self.assertIn(obj.transfer_function_type, ['LAPLACE (RADIANS/SECOND)', 'LAPLACE (HERTZ)', 'DIGITAL (Z-TRANSFORM)'], 
                                              f'transfer function type wrong in test case for PZ {obj.transfer_function_type}')
        self.assertEqual(obj.normalization_factor,  None, 
                    f'object normalization factor {obj.normalization_factor} is different from None')
        print("5", end=" ")
        
        obj = Filter.dynamic_class_constructor(ObsMetadata({'type': 'PolesZeros', 
                                         'transfer_function_type' : 'LAPLACE (RADIANS/SECOND)',
                                         'zeros': [[0.3, 0.2],],
                                         'poles': [[0.546, 0.191], [4.40e4, 0.000],],
                                         'normalization_frequency' : None,
                                         'normalization_factor' : None,
                                          }), None, None, None)
        
        self.assertEqual(obj.normalization_factor, None, f'{obj.normalization_factor} is different from None')
        print("6: Should have returned error", end=" ")
        
        
    
    
    def _test_all_stage_types(self):
        """
        Test reading and converting to obspy a stage file with each filter type. 
        This is the first time obspy conversion occurs so make sure it's done right
        Only one example stage for each type. If you wish to test all stage files,
        use test_all_responses(). If you wish to test individual files use test_state_with_XXX(file)
        with file as stripped file name. 
        File must exist in obsinfo/Information_files/instrumentation/YYY/responses
        """
        self.test_stage('TI_ADS1281_FIR1.stage.yaml')
        self.test_stage('SIO-LDEO_DPG_5018_calibrated.stage.yaml')
        self.test_stage('test-with-coeff.stage.yaml')
        self.test_stage('test-with-response-list.stage.yaml')
        
    def test_all_stages(self):
        """
        Test all information files in each responses subdirectory.
        """
        for dir in self.infofiles_path.datapath_list:
            files_in_validate_dir = Path(dir).joinpath(
                "*rs", # includes sensors, preamplifiers and dataloggers
                "responses/*.yaml"
                )
            
            filelist = glob.glob(str(files_in_validate_dir))
            
            for file in filelist:
                self._test_stage(file)
        
        
    def _test_stage(self, file):
        """
        Test stage according to filter type
        """
        
        info_file_dict = ObsMetadata.read_info_file(file, self.infofiles_path)
           
        stage_from_info_file = Stage(ObsMetadata(info_file_dict['stage']))
        
        obspy_result = stage_from_info_file.to_obspy()
        self._test_common_attributes(stage_from_info_file, obspy_result)
        
        if self.test:
            if isinstance(filter, FIR):
                self.assertEqual(stage_from_info_file.filter.symmetry, obspy_result._symmetry)
                for info_file_coeff in stage_from_info_file.filter.coefficients:
                    for obspy_coeff in obspy_result.decimation_correction:
                        self.assertEqual(info_file_coeff / 512, obspy_coeff (f))
            elif isinstance(filter, PolesZeros):
                self.assertEqual(stage_from_info_file.filter.transfer_function_type, obspy_result.pz_transfer_function_type)
                self.assertEqual(stage_from_info_file.filter.normalization_frequency, obspy_result.normalization_frequency)
                self.assertEqual(stage_from_info_file.filter.normalization_factor, obspy_result.normalization_factor)
                self.assertEqual(stage_from_info_file.filter.zeros, obspy_result.zeros)
                self.assertEqual(stage_from_info_file.filter.poles, obspy_result.poles)
            elif isinstance(filter, ResponseList):
                self.assertEqual(stage_from_info_file.filter.response_list, obspy_result.response_list_elements)
            elif isinstance(filter, Coefficients):
                self.test_common_attributes(stage_from_info_file, obspy_result)
                self.assertEqual(stage_from_info_file.filter.transfer_function_type, obspy_result.cf_transfer_function_type)
                self.assertEqual(stage_from_info_file.filter.numerator_coefficients, obspy_result.numerator)
                self.assertEqual(stage_from_info_file.filter.denominator_coefficients, obspy_result.denominator)                
                
        if self.verbose:
            print(f'Stage test for: {file}: PASSED')
            
        if self.print_output:
            print(obj)
            if self.level == "all":
                print(s.filter) 
    
    def _test_common_attributes(self, stage_from_info_file, obspy_result):
        self.assertEqual(stage_from_info_file.name, obspy_result.name)
        self.assertEqual(stage_from_info_file.description, obspy_result.description)
        self.assertEqual(stage_from_info_file.input_units, obspy_result.input_units)
        self.assertEqual(stage_from_info_file.output_units, obspy_result.output_units)
        self.assertEqual(stage_from_info_file.input_units_description, obspy_result.input_units_description)
        self.assertEqual(stage_from_info_file.output_units_description, obspy_result.output_units_description)
        self.assertEqual(stage_from_info_file.gain, obspy_result.stage_gain)
        self.assertEqual(stage_from_info_file.gain_frequency, obspy_result.stage_gain_frequency)
        self.assertEqual(stage_from_info_file.decimation_factor, obspy_result.decimation_factor)
        self.assertEqual(stage_from_info_file.filter.offset, obspy_result.decimation_offset)
        self.assertEqual(stage_from_info_file.delay, obspy_result.decimation_delay)
        self.assertEqual(stage_from_info_file.correction, obspy_result.decimation_correction)
         
         
    def _test_response_stage_addition(self):
        """
        Test reading and combining response_stages.
        """
        read_info_A = ObsMetadata.read_info_file(PurePath(self.infofiles_path).joinpath( 
            'sensors',
            'responses',
            'Trillium_T240_SN400-singlesided_theoretical.stage.yaml'))
        read_info_B = ObsMetadata.read_info_file(PurePath(self.infofiles_path).joinpath(
            'dataloggers',
            'responses',
            'TexasInstruments_ADS1281_100sps-linear_theoretical.response_stages.yaml'))
        stages_A = ResponseStages(read_info_A['response']['stages'])
        stages_B = ResponseStages(read_info_B['response']['stages'])
        stages = stages_A + stages_B
        
        
    def test_all_components(self):
        """
        Test all information files in each responses subdirectory.
        """
        components_list = [
            "sensors",
            "preamplifiers",
            "dataloggers"
            ]
        
        for dir in self.infofiles_path.datapath_list:
            for comp in components_list:
                files_in_validate_dir = Path(dir).joinpath(
                    comp,
                    "*.yaml"  # includes sensors, preamplifiers and dataloggers
                    )
                
                filelist = glob.glob(str(files_in_validate_dir))
                
                for file in filelist:
                    info_file_dict = ObsMetadata.read_info_file(file, self.infofiles_path)
        
                    #OJO: no configuraton passed from above. No delay_correction either.
                    obj = InstrumentComponent.dynamic_class_constructor(comp[:-1], info_file_dict)
                    
                    #if self.test:
                    #    self.assertTrue(isinstance(obj. comp[:-1]))
                        
                    if self.verbose:   
                       print(f'{file}: PASSED')
                       
                    if self.print_output:
                        PrintObs.print_component(obj, self.level)
                        
    
    def test_all_instrumentations(self):
        """
        Test all information files in each responses subdirectory.
        """
        for dir in self.infofiles_path.datapath_list:
            files_in_validate_dir = Path(dir).joinpath(
                "instrumentation/*.yaml" # includes sensors, preamplifiers and dataloggers
                )
            
            filelist = glob.glob(str(files_in_validate_dir))
            
            for file in filelist:
                self._test_instrumentation(file)
                    
         
    def _test_instrumentation(self, file):
        """
        Test reading instrumentation.
        """
        dict = ObsMetadata.read_info_file(file, self.infofiles_path)
        
        start_date = end_date = UTCDateTime(0)
        
        location_dict = {
                           "position": {"lon": 0., "lat": 0., "elev": 0.},
                           "base":  { "depth.m": 0.,
                                "geology": "unknown",
                                "vault": "Sea floor",
                                "uncertainties.m": {"lon": 0., "lat": 0., "elev": 0.},
                                "localisation_method": "Sea surface release point"
                               }
                        }
        
        location = Location(location_dict)
        locations={"00": location}
        
        print(f'Processing "{file}"')
        obj = Instrumentation(ObsMetadata(dict['instrumentation']), locations, start_date, end_date, {})
     
        if self.verbose:   
           print(f'{file}: PASSED')
        
        if self.print_output:
            PrintObs.print_instrumentation(obj, self.level)
            
        
    def _test_station(self, file_name):
        """
        Test reading a station.
        """
        info_dict = ObsMetadata.read_info_file(file_name, self.infofiles_path)
        
        info_dict = info_dict['stations']
        key = list(info_dict.keys())[0]
        value = ObsMetadata(list(info_dict.values())[0])
        
        obj = Station(key, value)
        
        if self.verbose:
           print(f'Station test for: {file_name}: PASSED')
           
        if self.print_output:
            PrintObs.print_station(obj, self.level)
            
    
    def test_all_networks(self):
        """
        Test all information files in each responses subdirectory.
        """
        for dir in self.infofiles_path.datapath_list:
            files_in_validate_dir = Path(dir).joinpath(
                "network/*.yaml" # includes sensors, preamplifiers and dataloggers
                )
            
            filelist = glob.glob(str(files_in_validate_dir))
            
            for file in filelist:
                self._test_network(file)
                    
             
    def _test_network(self, file_name):
        """
        Test reading a network.
        """
        info_dict = ObsMetadata.read_info_file(file_name, self.infofiles_path)
        
        net_dict = info_dict.get('network',None)
        if not net_dict:
            return 
        
        if self.verbose:
            print(f'Processing network file: {file_name}')
        obj = Network(ObsMetadata(net_dict))
        
        if self.verbose:
           print(f'Network test for: {file_name}: PASSED')
           
        if self.print_output:
            PrintObs.print_network(obj, self.level)
       
    
def run_suite_yaml():
    """
    Create and run test suite for jsonref
    """
    
    suite_yaml = unittest.TestSuite()
    suite_yaml.addTests(unittest.makeSuite(JsonRefTest))
     
    result = unittest.TextTestRunner(verbosity=1).run(suite_yaml)
    
    report_result_summary(result)
    
    return suite_yaml
    
def run_suite_info_files():
    """
    Create test suites for information files  
    """
    def suite():
        suite_info_files = unittest.TestSuite()
        suite_info_files.addTest(TestObsinfo('test_all_filters'))
        suite_info_files.addTest(TestObsinfo('test_all_stages'))
        suite_info_files.addTest(TestObsinfo('test_all_components'))
        suite_info_files.addTest(TestObsinfo('test_all_instrumentations'))
        suite_info_files.addTest(TestObsinfo('test_all_networks'))
        
        return suite_info_files
        
    
    result = unittest.TextTestRunner(verbosity=1).run(suite())
      
    report_result_summary(result)
        
    
def report_result_summary(result):
    """
    Report a summary of errors and failures
    """
    
    n_errors = len(result.errors)
    n_failures = len(result.failures)

    if n_errors or n_failures:
        print('\n\nSummary: %d errors and %d failures reported\n'%\
            (n_errors, n_failures)) 
           

def print_obs():
    """
    Print an information file
    """

    level, print_output, debug, input_filename = retrieve_arguments()
    val = TestObsinfo()
    val.setUp(verbose=False, test=False, print_output=print_output, level=level) 
    dp = Datapath() 
        
    try:               
        
        type = ObsMetadata.get_information_file_type(input_filename)
         
        print(f'Printing {type} file: {input_filename}')
            
        if type == "filter":
            val._test_filter(val.infofiles_path.build_datapath(input_filename))
        elif type == "stage":
            val._test_stage(val.infofiles_path.build_datapath(input_filename))
        elif type == "datalogger":
            val._test_datalogger(val.infofiles_path.build_datapath(input_filename))
        elif type == "preamplifier":
            val._test_preamplifier(val.infofiles_path.build_datapath(input_filename))
        elif type == "sensor":
            val._test_sensor(val.infofiles_path.build_datapath(input_filename))
        elif type == "instrumentation":
            val._test_instrumentation(val.infofiles_path.build_datapath(input_filename))
        elif type == "station":
            val._test_station(val.infofiles_path.build_datapath(input_filename))
        elif type == "network":
            val._test_network(val.infofiles_path.build_datapath(input_filename))
                       
    except TypeError:
        if debug:
            raise
        print("Illegal format: fields may be missing or with wrong format in input file.")
    except (KeyError, IndexError):
        if debug:
            raise
        print("Illegal value in dictionary key or list index")
    except ValueError:
        if debug:
            raise
        print("An illegal value was detected")
    except (IOError, OSError, LookupError):
        if debug:
            raise
        print("File could not be opened or read")
    except FileNotFoundError:
        if debug:
            raise
        print("File could not be found")
    except JSONDecodeError:
        if debug:
            raise
        print("File format is not recognized as either JSON or YAML. Check syntax.") 


def retrieve_arguments():
    
    options_dict = {
                       "level" : "l",
                       "debug": "d",
                       "help" : "h",
                     }
    
    input_filename = output_filename = None
    level ="all"
    print_output = True 
    debug = False
    
    long_option = re.compile("^[\-][\-][a-zA-Z_]+$")
    short_option = re.compile("^[\-][a-zA-Z]$")
    possible_options = re.compile("^[ldh]+$")
    
    input_filename = ""
    
    option = None
    skip_next_arg = False
    
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
            raise ValueError(s)
        
        for opt in option:
    
            if opt == "l":
                if len(option) == 1:
                    level = sys.argv[sys.argv.index("-l" if "-l" in sys.argv else "--level")+1]
                    skip_next_arg = True
                else:
                    warnings.warn('-l option should stand alone and be followed by a depth number')
                    break
            elif opt == "d":
                debug = True
            elif opt == "h": 
                print(usage())
                sys.exit()
             
    return (level, print_output, debug, input_filename)   

def usage():
    s = f'Usage: {sys.argv[0]} -pdh [-l <level name>]<filename>\n'
    s += f'Where:\n'
    s += f'      -l or --level: prints up to <level name>, where <level name> is:\n'
    s += f'                     all\n'
    s += f'                     stage\n'
    s += f'                     component\n'
    s += f'                     instrumentation\n'
    s += f'                     channel\n'
    s += f'                     station\n'
    s += f'                     network\n'
    s += f'      -d or --debug: do not catch exceptions to show error trace.\n'
    s += f'      -h or --help: prints this message\n'
    
    return s
