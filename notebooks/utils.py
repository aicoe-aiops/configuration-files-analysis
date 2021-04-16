import os
import json
import pandas as pd
import numpy as np
from itertools import combinations
import nltk
import re
from collections import defaultdict
import configparser
import math
import ntpath
from pathvalidate import is_valid_filename, is_valid_filepath
import ipaddress
import urllib


# Below function parses all the configuration files based on ini type configuration files.        
        
def get_typos(key_freq, confidence_t=0.9, typo_limit=2):
    """This function finds typos based on keyword frequencies.

    We find similar words and filter the results based on the confidence threshold.

    Parameters
    ----------
    key_freq : dictionary 
            Frequency of keyword in configuration files.
    confidence_t : float, default 0.9
            confidence threshold for spell check
    typo_limit : int, default 2
            The number of typos allowed. We calculate typos using edit distance
            For every ten characrters, we increase this argument by 1

    Returns
    ----------
    spell_errors: dictionary
            key in the dictionary is a misspelled keyword, and value is the correct version of a keyword
    """
    spell_errors = {}
    for i, j in combinations(key_freq.keys(), r=2):
        # Calculated similarity between keyword using Levenshtein distance.
        if nltk.edit_distance(i, j) >= min(len(i), len(j))//10+typo_limit:
            continue
        if key_freq[i] >= key_freq[j]:
            if key_freq[i]/(key_freq[i] + key_freq[j]) > confidence_t:
                spell_errors[j] = i
        else:
            if key_freq[j]/(key_freq[i] + key_freq[j]) > confidence_t:           
                spell_errors[i] = j
    return spell_errors

# Create_KeyValue_df function takes input as a folder path and creates a list of dictionaries as output 
def create_keyvalue_df(data_dir, fixed_typos=True):
    """This function creates a list of dictionaries as output for a set of configuration files.

    We parse and convert each configuration file into a dictionary format. 
    and append all this dictionary into a list

    Parameters
    ----------
    folder_path : string
            folder path of the configuration files.
    fixed_typos : bool, default True
            If True, fixed typos in configuration files.

    Returns
    ----------
    dict_list: list of dictionaries
            list where each element is a dictionary of a configuration file.
    """
    dict_list = []
    parse_errors = 0
    errorconfigs_filename = []
    
    for filename in os.listdir(data_dir):
        try:
            ## Adding dummy section to avoid no header error
            with open(os.path.join(data_dir, filename), 'r') as f:
                config_string = '[dummy_section]\n' + f.read()
            config = configparser.ConfigParser(allow_no_value=True, strict=False, inline_comment_prefixes= '#')
            cfgs = {}
            config.read_string(config_string)
            for sect in config.sections():
                cfgs.update(dict(config.items(sect)))
            dict_list.append(cfgs)
        except:
            errorconfigs_filename.append(filename)
            parse_errors += 1
    
    if fixed_typos:
        ## Fixed typos
        ## Create dataframe
        config_df = pd.DataFrame(dict_list)
        ## Find count of each key
        key_dict = config_df.count().to_dict()
        ## get typos based on frequncy of keys
        key_changes = get_typos(key_dict)
        ## Fix typos
        for dict_i in dict_list:
            for key in dict_i.copy():
                if key in key_changes:
                    dict_i[key_changes[key]] = dict_i.pop(key)

    
    return dict_list

### Following function find similar words and filter the results based on confidence thersold
def spell_error(key_freq, total_files, typo_limit=2, confidence_t=0.90, support_t=0.1):
    """This function proposes spelling errors by mapping lower frequency keywords to a similar higher frequency keyword. 

    We filter rules using support and confidence. Also, we calculate the similarity between keywords using Levenshtein distance.

    Parameters
    ----------
    key_freq : dictionary 
            Freqency of keyword in configuration files.
    typo_limit : int, default 2
            The number of typos allowed. We calculate typos using edit distance
            For every ten characrters, we increase this argument by 1
    confidence_t : float, default 0.9
            confidence thersold for spelling errors
    support_t : float, default 0.1
            confidence thersold for spelling errors

    Returns
    ----------
    spell_errors: dictionary
            keys in the dictionary are misspelled keywords, and values are the correct version of the keywords.
    """
    spell_errors = {}
    for i, j in combinations(key_freq.keys(), r=2):
            # Calculated similarity between keyword using Levenshtein distance.
            if nltk.edit_distance(i, j) >= min(len(i),len(j))//10+typo_limit:
                continue
            # Filter using support, we are assuming if a keyword is misspelled, Correctly spell keyword will not be present in the configuration file and vice-versa
            if ((key_freq[i] + key_freq[j])/(total_files)) > support_t:
                if key_freq[i] >= key_freq[j]:
                    # Considered it as a rule only if confidence is more than confidence_t(confidence thersold)
                    if key_freq[i]/(key_freq[i] + key_freq[j])> confidence_t:
                        spell_errors[j] = i
                else:
                    # Considered it as a rule only if confidence is more than confidence_t(confidence thersold)
                    if key_freq[j]/(key_freq[i] + key_freq[j])> confidence_t:                       
                        spell_errors[i] = j
    return spell_errors

## array for boolean
bool_arr = ['on', 'off', 'true', 'false', 'yes', 'no']

def valid_ip(val):
    val, separator, port = val.partition(':')
    for ip in ipaddress.ip_network, ipaddress.ip_address:
        try:                                                           
            if ip==ipaddress.ip_network:
                ip(val,False)
            else:
                ip(val)
            return True
        except ValueError:
            pass
    return False

def is_ip(val):
    """This function check if data type of value is ip address.
    
    Parameters
    ----------
    value : 
            value for which we want to check data type

    Returns
    ----------
    datatype: 
            a binary value based on data type of the given input argument is ipaddress or not
    """
    val_list = val.split(',')
    list_comp = [valid_ip(i) for i in val_list]
    return all(list_comp)

def is_filepath(val):
    """This function check if data type of value or not.
    
    Parameters
    ----------
    value : 
            value for which we want to check data type

    Returns
    ----------
    datatype: 
            a binary value based on data type of the given input argument is filepath or not
    """
    val = val.lstrip('/')
    return is_valid_filepath(val) and (val.find('/')!=-1 or val.find('\\')!=-1)

def is_number(string):
    """This function check if data type of number.
    
    Parameters
    ----------
    value : 
            value for which we want to check data type

    Returns
    ----------
    datatype: 
            a binary value based on data type is number
    """
    try:
        float(string)
        return True
    except ValueError:
        return False

def is_url(url):
    """This function check if data type of value or not.
    
    Parameters
    ----------
    value : 
            value for which we want to check data type

    Returns
    ----------
    datatype: 
            a binary value based on data type of the given input argument is url or not
    """
    url = url.strip()

    result = urllib.parse.urlparse(url)
    scheme = result.scheme
    domain = result.netloc
    if not scheme or not domain:
        return False
    return True


def find_type(value):
    """This function infers the data type of the input argument.
    
    Parameters
    ----------
    value : 
            value for which we want to find data type

    Returns
    ----------
    datatype: 
            data type of the given input argumnet
    """
    value = value.replace("'", "")
    value = value.replace('"', "")
    value = value.replace(" ", "")
    if (value.lower() == 'nan') or (value.lower() == 'none') or len(value)==0:
        datatype = None
    elif value.lower() in bool_arr:
        datatype = 'bool'
    elif value=='0' or value=='1':
        datatype = '0||1'
    elif is_ip(value):
        datatype = 'ip_address'
    elif is_url(value):
        datatype = 'uri'
    elif is_number(value):
        datatype = 'int'
    elif is_valid_filename(ntpath.basename(value)) and ntpath.basename(value).find('.')!=-1:
        datatype = 'filename||filepath+filename'
    elif is_filepath(value):
        datatype = 'filepath'
    elif re.search(r'^[\d ]*(k|m|g|kb|mb|gb)$', value.lower()):
        datatype = 'size'
    else:
        datatype = 'string'
    return datatype

def assign_same_prob(df, curr_datatype, cols):
    new_val = df[cols].sum(axis=1)
    for col in cols:
        df[col] = np.where(df['datatype'] == curr_datatype, new_val, df[col])
    return df

def create_intermediate(config_df):
    """This function takes the configuration files as input and infers the probabilistic data type for each key.
    
    Parameters
    ----------
    config_df : pandas Dataframe
            pandas Dataframe where each row corresponding to a configuration file.

    Returns
    ----------
    datatype: pandas Dataframe
            pandas Dataframe where each row is a probabilistic data type for a key.
    """

    # Below we calculated frequencies of different data types for each key.
    dict_list = []
    for column in config_df:
        my_dict = defaultdict(int)
        my_dict['key_name'] = column
        for i in config_df[column].tolist():
            i = str(i)
            datatype = find_type(i)
            my_dict[datatype] += 1
        dict_list.append(my_dict)
    
    # Finding frequency of each key
    datatype = pd.DataFrame(dict_list)
    datatype['frequency'] = datatype[datatype.columns[~datatype.columns.isin(['key_name', None])]].sum(axis=1)

    # We converted frequencies of data types into probabilities. 
    # We divided frequency by total nonnull entries to calculate the probability.
    datatype[datatype.columns[~datatype.columns.isin(['key_name', 'frequency', None])]] = datatype[datatype.columns[~datatype.columns.isin(['key_name', 'frequency', None])]].div(datatype[datatype.columns[~datatype.columns.isin(['key_name', 'frequency', None])]].sum(axis=1), axis=0)
    datatype = datatype.drop([None], axis=1, errors='ignore')

    # The data type for each keyword is inferred based on maximum probability
    datatype['datatype'] = datatype.drop(['key_name', 'frequency'], axis=1, errors='ignore').idxmax(axis=1)

    # size, 0||1 are also integers. Hence, whenever data type is int we are assigning the same probability to size
    datatype = assign_same_prob(datatype, 'int',['int','size','0||1'])
        
    # int can be also be size. Hence, whenever data type is size we are assigning the same probability to int
    datatype = assign_same_prob(datatype, 'size',['int','size'])

    # 0||1 are also an boolean. Hence, whenever data type is bool we are assigning the same probability to 0||1
    datatype = assign_same_prob(datatype, 'bool',['bool','0||1'])
    
    # bool can be also be 0||1. Hence, whenever data type is 0||1 we are assigning the same probability to bool
    datatype = assign_same_prob(datatype, '0||1',['0||1','bool'])
    
    return datatype

def create_type_rule(datatype, total_files, confidence_t=0.9, support_t=0.1):
    """This function works as a learner and filters the proposed data type rules using support and confidence.
    
    Parameters
    ----------
    datatype : pandas Dataframe
            pandas Dataframe where each row corresponding to a configuration file.
    total_files : int
            total number of configuration files.
    confidence_t : float, default 0.9
            confidence threshold for data type errors.
    support_t : float, default 0.1
            support threshold for data type errors.

    Returns
    ----------
    list_datatype_dict: list
            list of dictionaries which contains two keys,
            The first keys are for key_name in the configuration file; Second keys are the data type of the given key.
    """

    # We filter out all the rules with support below the threshold
    datatype = datatype[datatype['frequency']/total_files>support_t]
    datatype = datatype.drop(['frequency'], axis=1, errors='ignore')
    
    # We filter out all the rules with confidence below the threshold
    datatype = datatype[datatype.drop(['key_name','datatype'], axis=1, errors='ignore').max(axis=1)>confidence_t]

    # We converted the data type column into list because there are multiple data fields possible, such as 0||1 and int, 0||1 and bool, etc.
    datatype_numeric = datatype.drop(['key_name','datatype'], axis=1, errors='ignore')
    datatype_bool = datatype_numeric.eq(datatype_numeric.max(1), axis=0)
    datatype['datatype'] = datatype_bool.apply(lambda x: datatype_bool.columns[x.iloc[:] == True].tolist(), axis=1)
    list_datatype_dict = datatype[['key_name','datatype']].to_dict('records')

    return list_datatype_dict

def mis_spell_detection(key_dict, input_file, confidence_t=0.9, typo_limit=2):
    """This function finds spelling error in a particular configuration file. 

    We parsed the configuration file and checked if there are lower-frequency keywords similar to a higher-frequency keyword.
    If such keywords exist, we throw a misspelling error message.

    Parameters
    ----------
    key_freq : dictionary 
            Frequency of keywords in configuration files.
    input_file : file_path, string
            Path of the configuration file for which we want to find data type error.
    confidence_t : float, default 0.9
            confidence threshold for spelling errors
    typo_limit : int, default 2
        The number of typos allowed. We calculate typos using edit distance
        For every ten characrters, we increase this argument by 1

    Returns
    ----------
    error_message: string
            string with error message corresponding to spelling error.
    """
    key_dict = defaultdict(int,key_dict)
    #Parsed the file
    with open(input_file) as f:
        config_string = '[dummy_section]\n' + f.read()
    config = configparser.ConfigParser(allow_no_value=True, strict=False, inline_comment_prefixes= '#')
    cfgs = {}
    config.read_string(config_string)
    for sect in config.sections():
        cfgs.update(dict(config.items(sect)))
        
    # Increamented frequency dictionary based on the current keys
    for q in cfgs:
        key_dict[q] += 1
    # Calculated all the misspell errors
    for p in cfgs:
        for q in key_dict:
            if nltk.edit_distance(p, q) >= min(len(p),len(q))//10+typo_limit:
                continue
            # Considered it as a error if confidence is more than confidence_t(confidence thersold)
            if key_dict[q]/(key_dict[p] + key_dict[q])> confidence_t:
                print('Spell_Error: Key \''+ p+'\' should be replaced by \''+ q +'\'')


def mis_type_detection(rules, input_file):
    """This function takes the configuration files as input and infers the probabilistic data type for each key.
    
    Parameters
    ----------
    rules : list
             list of dictionaries which contains two keys,
            The first keys are for key_name in the configuration file; Second keys are the data type of the given key.
    input_file : file_path, string
            Path of the configuration file for which we want to find data type error

    This function print the error message
    ----------
    error_message: string
            string with error message correponding to incorrect data type
    """
    with open(input_file) as f:
        config_string = '[dummy_section]\n' + f.read()
    config = configparser.ConfigParser(allow_no_value=True, strict=False, inline_comment_prefixes= '#')
    cfgs = {}
    config.read_string(config_string)
    for sect in config.sections():
        cfgs.update(dict(config.items(sect)))
    
    for q in cfgs:
        val = next((item for item in rules if item["key_name"] == q), None)
        if not val:
            continue
        datatype = find_type(str(cfgs[q]))
        val_type = val['datatype']
        if (datatype not in val_type) and (datatype != None):
            print('Type_Error: Data type of key \'' + q + '\' should be',val_type, 'but its given as \''+ datatype+'\'')


