#!/usr/bin/python3

import sys
import os
import time
import json
import csv

import xml.etree.ElementTree as ET
from collections import OrderedDict
import config.path as target
import config.name as file
import config.subrecon as numberOf
import config.const as const

# Global variables
_start_time = 'TIME'

_site_name = file.Name # Output file name

_site_list = [] # Diretory list in 'Site' directory
_site_size: int = 0 # The total number of diretories in 'Site' directory

_search_key = {} # Search key dictionary

_value_dict = {} # Parameters' value dictionary
_result = OrderedDict() # Result
_num_of_subrecon: int = 0 # The number of subrecon

_protocol_no_list = OrderedDict() # protocol's number(id) list

_TAB = '\t' # Next Cell (tab⇄)
_ENTER = '\n' # New line (enter↲)

"""
prime (Pre-processing)
    (1) List up directories from .protoMiscInfo.xml OR target.Path 
    (2) Set number of Subrecon
    (3) Excute 'main' function
"""
def prime():
    global _site_list
    global _site_size
    global _num_of_subrecon

    # (1) List up directories from .protoMiscInfo.xml OR target.Path  
    if len(_protocol_no_list) > 0:
        _site_list = [key for key in _protocol_no_list.keys()]
    else:
        _site_list = [element for element in os.listdir(target.Path) if os.path.isdir(os.path.join(target.Path, element))]

    _site_size = len(_site_list)

    # (2) Set the number of Subrecon
    try:
        _num_of_subrecon = numberOf.Subrecon
    except:
        _num_of_subrecon = 0
        print(f"[Warning] {const.config}subrecon.py is unavailable. The number of sub recon setting is 0")
        pass

    # (3) Excute 'main' function 
    main()

"""
main (Controller)
    (1) Create a .txt file
    (2) Call directories in order
    (3) Convert .txt to .csv
"""
def main():
    file_name = _site_name + "_" + time.strftime("%Y%m%d%H%M%S", _start_time)
    # (1) Create a .txt file
    try:
        txt_file_name = file_name + '.txt'

        with open(txt_file_name, 'w') as file:
            # Header space
            for _ in range(2):
                file.write(_ENTER)

    except Exception as error:
        print("Failed to create .txt file;", error)
    
    # (2) Call directories in order
    factory(_site_list, 0, txt_file_name)

    # (3) Convert .txt to .csv
    try:
        convert_txt_to_csv(file_name)
    except Exception as error:
        print("Failed to convert text to csv;", error)

"""
factory
    (1) Parse 'UIRx.xml' ⇒ If failed to pase, sys.exit
    (2) Extract parameters
    (3) Append contents to the .txt
    (4) Create and append a header to the .txt
    (5) recusive call

@param
    - site_list: list of directories in 'Site'
    - list_number: index of site_list
    - file_name: file name of .txt
"""
def factory(site_list: list, list_number: int, file_name: str):
    global _result
    dir_name = site_list[list_number]
    dir_no = list_number + 1
    UIRx_path = target.Path + dir_name + '/' + const.UIRx_xml

    # (1) Parse the 'UIRx.xml' file
    try:
        UIRx_tree = ET.parse(UIRx_path)
        UIRx_root = UIRx_tree.getroot()
    # If failed to pase, Stop all process.
    except Exception as error:
        print("Failed to parse UIRx.xml; exit;", error)
        sys.exit()

    # Initialize _result
    _result.clear()
    # _result basic set
    _result.update({f'#{dir_no}': OrderedDict()})
    _result[f'#{dir_no}'].update({f'{dir_name}': OrderedDict()})

    # (2) Extract series & parameter settings
    try:
        extract_params(dir_no, dir_name, UIRx_root)
    except Exception as error:
        print("Failed to extract protocol information;", error)

    # (3) Append contents to the .txt
    try:
        create_info_txt(dir_no, dir_name, file_name)
    except Exception as error:
        print("Failed to append contents to the .txt.file;", error)

    # (4) Create and append a header to the .txt
    try:
        create_header(dir_no, dir_name, file_name)
    except Exception as error:
        print("Failed to write the first row of header;", error)

    motion = {0:'-', 1:'\\', 2:'|', 3:'/'}
    
    if not (dir_no == _site_size):
        print(f'{motion[dir_no % 4]} Processing.. [{dir_no}/{_site_size}] ', end = '\r')
    else:
        print(f'Processing Completed. [{dir_no}/{_site_size}]')

    # (5) recusive call
    if list_number + 1 < len(site_list):
        factory(site_list, list_number + 1, file_name) 

"""
extract_params
Extract Scan Parameters from 'UIRx.xml'
    (1) Extract value from 'exam'
    (2) Extract value from 'proto'
    (3) Extract value from 'series'
        ┕ Extract value from 'group'
            ┕ Extract value from 'recon'
               ┕ Extract value from 'subrecon'

@param
    - dir_no: directory number
    - dir_name: direcotry name
    - UIRx_xml: xml etree object
"""
def extract_params(dir_no: int, dir_name: str, UIRx_xml: object):
    global _result

    #❇ Define jrx namespace jrx:*
    jrx_ns = {'jrx': 'http://fct.med.xy.com/jrx'}

    #❇ jrx:exam
    exam = UIRx_xml.find('.//jrx:exam', jrx_ns)
    exam_index = 'exam'
    #❇ Set 'exam' parameter keys from search key dictionary
    for exam_key in _search_key[exam_index].keys():
        _result[f'#{dir_no}'][f'{dir_name}'].update({f'{_search_key[exam_index][exam_key]}': ""})
    
    #❇ (1) Extract value from 'exam'
    for exam_element in exam:
        exam_element_visible = exam_element.get('visible')
        if exam_element_visible and exam_element_visible == 'false':
            pass
        else:
            exam_element_name = exam_element.get('name')
            #❇❇ Verify element contains in and translate with search key dictionary
            if exam_element_name in _search_key[exam_index].keys():
                exam_element_value = exam_element.get('value')
                _result[f'#{dir_no}'][f'{dir_name}'][f'{_search_key[exam_index][exam_element_name]}'] = translate(_search_key[exam_index][exam_element_name], exam_element_value)
    
    #❇ jrx:proto
    proto = exam.find('.//jrx:proto', jrx_ns)
    proto_index = 'proto'
    #❇ Set 'proto' parameter keys from search key dictionary
    for proto_key in _search_key[proto_index].keys():
        if proto_key == 'id' and dir_name in _protocol_no_list.keys():
            _result[f'#{dir_no}'][f'{dir_name}'].update({f'{_search_key[proto_index][proto_key]}': _protocol_no_list[dir_name] })
        else:
            _result[f'#{dir_no}'][f'{dir_name}'].update({f'{_search_key[proto_index][proto_key]}': ""})

    #❇ (2) Extract value from 'proto'
    for proto_element in proto:
        proto_element_visible = proto_element.get('visible')
        if proto_element_visible and proto_element_visible == 'false':
            pass
        else:
            proto_element_name = proto_element.get('name')
            #❇❇ Verify element contains in and translate with search key dictionary
            if proto_element_name in _search_key[proto_index].keys():
                proto_element_value = proto_element.get('value')
                _result[f'#{dir_no}'][f'{dir_name}'][f'{_search_key[proto_index][proto_element_name]}'] = translate(_search_key[proto_index][proto_element_name], proto_element_value)

    #❇ jrx:series
    series = proto.findall('.//jrx:series', jrx_ns)
    series_index = 'series'
    series_no = 0
    #❇ series can be plural(from 'findall')
    for a_series in series:

        #❇❇ Set series number and series parameter space
        series_no += 1
        series_title = 'Series ' + str(series_no)
        _result[f'#{dir_no}'][f'{dir_name}'].update({f'{series_title}': OrderedDict()})

        #❇❇ Set 'series' parameter keys from search key dictionary
        for series_key in _search_key[series_index].keys():
            _result[f'#{dir_no}'][f'{dir_name}'][f'{series_title}'].update({f'{_search_key[series_index][series_key]}': ""})

        #❇❇ (3) Extract value from 'series'
        for series_element in a_series:
            series_element_visible = series_element.get('visible')
            if series_element_visible and series_element_visible == 'false':
                pass
            else:
                series_element_name = series_element.get('name')
                #❇❇❇ Verify element contains in and translate with search key dictionary
                if series_element_name in _search_key[series_index].keys():
                    series_element_value = series_element.get('value')
                    _result[f'#{dir_no}'][f'{dir_name}'][f'{series_title}'][f'{_search_key[series_index][series_element_name]}'] = translate(_search_key[series_index][series_element_name], series_element_value)

        #❇❇ jrx:group
        #❇❇ groups of a series
        groups = a_series.findall('.//jrx:group', jrx_ns)
        group_index = 'group'
        group_no = 0

        #❇❇ group can be plural(from 'findall')
        for group in groups:

            #❇❇❇ Set group number and group parameter space
            group_no += 1
            group_title = 'Group ' + str(group_no)
            _result[f'#{dir_no}'][f'{dir_name}'][f'{series_title}'].update({f'{group_title}': OrderedDict()})

            #❇❇❇ Set 'group' parameter keys from search key dictionary
            for group_key in _search_key[group_index].keys():
                _result[f'#{dir_no}'][f'{dir_name}'][f'{series_title}'][f'{group_title}'].update({f'{_search_key[group_index][group_key]}': ""})

            #❇❇❇ ┕Extract value from 'group' of a series
            for group_element in group:
                group_element_visible = group_element.get('visible')
                if group_element_visible and group_element_visible == 'false':
                    pass
                else:
                    group_element_name = group_element.get('name')
                    #❇❇❇ Verify element contains in and translate with search key dictionary
                    if group_element_name in _search_key[group_index].keys():
                        group_element_value = group_element.get('value')
                        _result[f'#{dir_no}'][f'{dir_name}'][f'{series_title}'][f'{group_title}'][f'{_search_key[group_index][group_element_name]}'] = translate(_search_key[group_index][group_element_name], group_element_value)

            #❇❇❇ jrx:recon
            #❇❇❇ recon of group
            recons = group.findall('.//jrx:recon', jrx_ns)
            recon_index = 'recon'
            recon_no = 0

            #❇❇❇ recon can be plural(from 'findall')
            for recon in recons:

                #❇❇❇❇ Set recon number and recon parameter space
                recon_no += 1
                recon_title = 'Recon ' + str(recon_no)
                _result[f'#{dir_no}'][f'{dir_name}'][f'{series_title}'][f'{group_title}'].update({f'{recon_title}': OrderedDict()})

                #❇❇❇❇ Set 'recon' parameter keys from search key dictionary
                for recon_key in _search_key[recon_index].keys():
                    _result[f'#{dir_no}'][f'{dir_name}'][f'{series_title}'][f'{group_title}'][f'{recon_title}'].update({f'{_search_key[recon_index][recon_key]}': ""})

                #❇❇❇❇ ┕Extract value from 'recon' of group
                for recon_element in recon:
                    recon_element_visible = recon_element.get('visible')
                    if recon_element_visible and recon_element_visible == 'false':
                        pass
                    else:
                        recon_element_name = recon_element.get('name')
                        #❇❇❇❇❇ Verify element contains in and translate with search key dictionary
                        if recon_element_name in _search_key[recon_index].keys():
                            recon_element_value = recon_element.get('value')
                            _result[f'#{dir_no}'][f'{dir_name}'][f'{series_title}'][f'{group_title}'][f'{recon_title}'][f'{_search_key[recon_index][recon_element_name]}'] = translate(_search_key[recon_index][recon_element_name], recon_element_value)

                #❇❇❇❇ jrx:subrecon
                #❇❇❇❇ subrecon of recon
                subrecons = recon.findall('.//jrx:subrecon', jrx_ns)
                subrecon_index = 'subrecon'
                subrecon_no = 0

                #❇❇❇❇ subrecon can be plural(from 'findall')
                for subrecon in subrecons:

                    #❇❇❇❇❇ Set subrecon number and subrecon parameter space
                    subrecon_no += 1
                    subrecon_title = 'Subrecon ' + str(subrecon_no)
                    _result[f'#{dir_no}'][f'{dir_name}'][f'{series_title}'][f'{group_title}'][f'{recon_title}'].update({f'{subrecon_title}': OrderedDict()})

                    #❇❇❇❇ Set 'subrecon' parameter keys from search key dictionary
                    for subrecon_key in _search_key[subrecon_index].keys():
                        _result[f'#{dir_no}'][f'{dir_name}'][f'{series_title}'][f'{group_title}'][f'{recon_title}'][f'{subrecon_title}'].update({f'{_search_key[subrecon_index][subrecon_key]}': ""})

                    #❇❇❇❇❇ Extract value from 'subrecon' of recon
                    for subrecon_element in subrecon:
                        subrecon_element_visible = subrecon_element.get('visible')
                        if subrecon_element_visible and subrecon_element_visible == 'false':
                            pass
                        else:
                            subrecon_element_name = subrecon_element.get('name')
                            #❇❇❇❇❇❇ Verify element contains in and translate with search key dictionary
                            if subrecon_element_name in _search_key[subrecon_index].keys():
                                subrecon_element_value = subrecon_element.get('value')
                                _result[f'#{dir_no}'][f'{dir_name}'][f'{series_title}'][f'{group_title}'][f'{recon_title}'][f'{subrecon_title}'][f'{_search_key[subrecon_index][subrecon_element_name]}'] = translate(_search_key[subrecon_index][subrecon_element_name], subrecon_element_value)
"""
create_info_txt
Write protocol information to txt
    (1) Write directory number and name
    (2) Write exam & protocol information
        ┕ Write series information
            ┕ Write group information
                ┕ Write recon information
                    ┕ Write subrecon information

@param
    - dir_no: directory number
    - dir_name: directory name
    - file_name: filename of .txt
"""
def create_info_txt(dir_no: int, dir_name: str, file_name: str):
    global _result

    # Open a text file to append the extracted information
    with open(file_name, 'a') as file:

        # Write Contents
        # (1) Write target directory number and name
        series_front = f'#{dir_no}' + _TAB + dir_name + _TAB

        # (2) Write exam & protocol information
        series_count = 1
        for exam_key in _result[f'#{dir_no}'][f'{dir_name}'].keys():
            # Weather value of dict contains only value or contains nested dict
            if not is_dict(_result[f'#{dir_no}'][dir_name][exam_key]):
                series_front += _result[f'#{dir_no}'][dir_name][exam_key] + _TAB
            # ┕ Write series information
            else:
                group_front = series_front + str(series_count) + _TAB
                group_count = 1
                for series_key in _result[f'#{dir_no}'][f'{dir_name}'][exam_key].keys():
                    # Weather value of dict contains only value or contains nested dict
                    if not is_dict(_result[f'#{dir_no}'][dir_name][exam_key][series_key]):
                        group_front += _result[f'#{dir_no}'][dir_name][exam_key][series_key] + _TAB
                    # ┕ Write group information
                    else:
                        file.write(group_front)
                        file.write(str(group_count))
                        file.write(_TAB)
                        for group_key in _result[f'#{dir_no}'][f'{dir_name}'][exam_key][series_key].keys():
                            # Weather value of dict contains only value or contains nested dict
                            if not is_dict(_result[f'#{dir_no}'][dir_name][exam_key][series_key][group_key]):
                                file.write(_result[f'#{dir_no}'][dir_name][exam_key][series_key][group_key])
                                file.write(_TAB)
                            # ┕ Write recon information
                            else:
                                subrecon_count = 1 
                                for recon_key in _result[f'#{dir_no}'][f'{dir_name}'][exam_key][series_key][group_key].keys():
                                    # Weather value of dict contains only value or contains nested dict
                                    if not is_dict(_result[f'#{dir_no}'][dir_name][exam_key][series_key][group_key][recon_key]):
                                        file.write(_result[f'#{dir_no}'][dir_name][exam_key][series_key][group_key][recon_key])
                                        file.write(_TAB)
                                    # ┕ Write subrecon information
                                    else:
                                        if subrecon_count < _num_of_subrecon + 1:
                                            for subrecon_key in _result[f'#{dir_no}'][f'{dir_name}'][exam_key][series_key][group_key][recon_key].keys():
                                                # Weather value of dict contains only value or contains nested dict
                                                if not is_dict(_result[f'#{dir_no}'][dir_name][exam_key][series_key][group_key][recon_key][subrecon_key]):
                                                    file.write(_result[f'#{dir_no}'][dir_name][exam_key][series_key][group_key][recon_key][subrecon_key])
                                                    file.write(_TAB)
                                                else:
                                                    pass
                                            subrecon_count += 1
                                # Write empty cell of subrecon
                                while(subrecon_count < _num_of_subrecon + 1):
                                    for _ in range(len(_search_key['subrecon'])):
                                        file.write(_TAB)
                                    subrecon_count += 1
                        group_count += 1
                        # New line for each group  
                        file.write(_ENTER)
                series_count += 1

""" 
Create header
    (1) Create exam information
    (2) Create protocol information
    (3) Create series information
    (4) Create group information
    (5) Create recon information

@param
    - dir_no: directory number
    - dir_name: directory name
    - file_name: filename of .txt
"""
def create_header(dir_no: int, dir_name: str, file_name : str):
    # Init header
    header_row1 = _TAB + time.strftime("%Y-%m-%d %H:%M:%S", _start_time) + _TAB + 'Recon Name'
    header_row2 = 'No.' + _TAB + 'Session Name' + _TAB 

    # (1) Create exam parameter header
    for exam_key in _search_key['exam'].values():
        header_row1 += _TAB
        header_row2 += exam_key + _TAB

    # (2) Create protocol parameter header
    for proto_key in _search_key['proto'].values():
        header_row1 += _TAB
        header_row2 += proto_key + _TAB

    header_row1 += _TAB
    header_row2 += 'Series' + _TAB
    # (3) Create series parameter header
    for series_key in _search_key['series'].values():
        header_row1 += _TAB
        header_row2 += series_key + _TAB

    header_row1 += _TAB
    header_row2 += 'Group' + _TAB
    # (4) Create group parameter header
    for group_key in _search_key['group'].values():
        header_row1 += _TAB
        header_row2 += group_key + _TAB

    # (5) Create recon parameter header
    max_length_titles = str()
    max_length_params = str()
    for series in [key for key in _result[f'#{dir_no}'][f'{dir_name}'].keys() if 'Series' in key]:

        for group in [key for key in _result[f'#{dir_no}'][f'{dir_name}'][f'{series}'].keys() if 'Group' in key]:
            # Recons of Group in a series
            recon_titles = str()
            recon_params = str()
            second_recon_count = 1
            for recon in [key for key in _result[f'#{dir_no}'][f'{dir_name}'][f'{series}'][f'{group}'].keys() if 'Recon' in key]:
                # The 1st Recon
                if recon == 'Recon 1':
                    recon_titles += 'Primary Recon'
                # Other Recons
                else:
                    recon_titles += 'Secondary Recon ' + str(second_recon_count)
                    second_recon_count += 1

                for recon_key in _search_key['recon'].values():
                    recon_titles += _TAB
                    recon_params += recon_key + _TAB
                
                # For header of Subrecon in Recon If '_num_of_subrecon' > 0
                if _num_of_subrecon > 0:
                    sub_recon_count = 0
                    for sub_recon_count in range(_num_of_subrecon):
                        recon_titles += 'SubRecon' + str(sub_recon_count + 1)
                        for subrecon_key in _search_key['subrecon'].values():
                            recon_titles += _TAB
                            recon_params += subrecon_key + _TAB

            # Update for header (with the longest one) 
            if len(max_length_titles) < len(recon_titles):
                max_length_titles = recon_titles
            if len(max_length_params) < len(recon_params):
                max_length_params = recon_params
    
    # New line for each header row
    header_row1 += max_length_titles + _ENTER
    header_row2 += max_length_params + _ENTER

    # Write contents of header to .txt file
    write_header(file_name, 0, header_row1)
    write_header(file_name, 1, header_row2)

""" 
write_header
Write contents of header to .txt file

@param
    - file_name: filename of .txt
    - row_no: row number of header
    - contents: contents
"""
def write_header(file_name: str, row_no: int, contents: str):
    # Read each line of the file 
    with open(file_name, 'r') as file:
        lines = file.readlines()

    # Write new header (with the longest one) 
    if len(lines[row_no]) < len(contents):
        lines[row_no] = contents
    
    # Write each line of the file
    with open(file_name, 'w') as file:
        file.writelines(lines)

"""
is_dict
Weather variable is dictionary or not 

@param
    - it: variable

@return
    - bool: True if variable is dictionary, False otherwise.
"""
def is_dict(it):

    return isinstance(it, dict)

"""
convert_txt_to_csv
Convert .txt to .csv

@param
    - file_name: file name of .txt
"""
def convert_txt_to_csv(file_name: str):
    input_file_path = file_name + '.txt'
    output_file_path = file_name + '.csv'
    delimiter = '\t'  # Adjust based on your text file's delimiter

    # Read .txt and Write .csv with contents of .txt
    with open(input_file_path, 'r') as infile, open(output_file_path, 'w', newline='') as outfile:
        reader = csv.reader(infile, delimiter=delimiter)
        writer = csv.writer(outfile)

        for row in reader:
            writer.writerow(row)

    print(f"Create '{file_name}.csv' successfully")

"""
json_loader
Load json

@param
    - json_name: json file name

@return
    - data: json file contents
"""
def json_loader(json_name: str):
    
    target_json = const.config + json_name
    try:
        with open(target_json, 'r') as file:
            data = json.load(file)
    except Exception as error:
        print(f"Fail to load {json_name}.json;", error)
    
    return data

"""
create_dictionary
Set global variable from json contents
"""
# 
def create_dictionary():
    global _search_key
    global _value_dict

    # Refer 'config' directory and list up directories in 'json'
    config_files = os.listdir(const.config)

    for json in config_files:
        
        if json.endswith('.json'):
            if json == 'search_key.json':
                try:
                    _search_key = json_loader(json)
                except:
                    print(f"[Warning] {json} is unavailable. the result might be empty.")
                    pass

            elif json == 'dictionary.json':
                try:
                    _value_dict.update(json_loader(json))
                except:
                    print(f"[Warning] {json} is unavailable. value of parameter does NOT be translated.")
                    pass
        
            else:
                print(f"Except {json}" ) 

"""
extract_misc_info
Set protocol's number list from '.protoMiscInfo.xml'

@param
    - path: direcory path of '.protoMiscInfo.xml'
"""
# 
def extract_misc_info():
    global _protocol_no_list

    result = OrderedDict()
    try:
        UIRx_tree = ET.parse(target.Path + '.protoMiscInfo.xml')
        UIRx_root = UIRx_tree.getroot()
    except Exception as error:
        print(f"Fail to parse .protoMiscInfo.xml;", error)
        return

    #❇ Define config namespace con:*
    con_ns = {'con': 'http://wf.di.med.xy.com/config'}
    property_sets = UIRx_root.findall('.//con:PropertySet', con_ns)
    for property_set in property_sets:
        session_name = None
        id_value = None
        for property in property_set:
            if property.get('name') == 'uid':
                session_name = property.get('value').split('/')[-2]
            elif property.get('name') == 'id':
                id_value = property.get('value')
            else:
                pass
        if session_name is not None and id_value is not None :
            #❇❇ For sorting, id_value splited by '.' and store as value, i.e. 5.11 → [5, 11]
            result.update({f'{session_name}': [int(id_value.split('.')[0]), int(id_value.split('.')[1])]})
    
    # Sorting the protocol's number list by splited id_value
    sorted_result = OrderedDict(sorted(result.items(), key=lambda item: (item[1][0], item[1][1])))
    _protocol_no_list = recover_id_value(sorted_result)

"""
recover_id_value
Recover splited id value of protocol

@param
    - obj: dicitionary of information from '.protoMiscInfo.xml'
"""
def recover_id_value(obj: OrderedDict):
    
    # Recover splited id_value i.e. [5, 11] → 5.11 
    for key in obj.keys():
        if type(obj[key]) is list:
            recovered_value = str(obj[key][0]) + '.' + str(obj[key][1])
            obj[key] = recovered_value

    return obj

"""
translate
Translate value of key

@param
    - key: key of key-value data
    - value: value of key-value data

@return
    - value: translated value
"""
# Translate value
def translate(key: str, value: str):

    if key in _value_dict.keys() :
        if value in _value_dict[key].keys():
            value = _value_dict[key][value]
        else:
            pass
    else:
        pass

    return value

"""
Init
    (1) Exatract protocol's number from '.protoMiscInfo.xml'  
    (2) Create value dictionary from jsons
    (3) Prime
""" 
if __name__ == '__main__':

    _start_time = time.gmtime()
    
    print(f'<< Executed. [{time.strftime("%Y-%m-%d %H:%M:%S", _start_time)}]>>')

    # (1) Exatract protocol's number from '.protoMiscInfo.xml' 
    try:
        extract_misc_info()
    except Exception as error:
        print("[Warning] .protoMiscInfo.xml is unavailable; Protocol No. is empty", error)
        pass

    # (2) Create value dictionary from jsons
    try:
        create_dictionary()
    except Exception as error:
        print("Fail to create Dictionary;", error) 
    
    # (3) Prime
    prime()

