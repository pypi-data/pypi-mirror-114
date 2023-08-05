# -*- coding: utf-8 -*-

"""
Preprocessor module - build dataframes from files (e.g. .eaf, .cha, .txt) and edit transcription formats
"""

# This code is a part of scikit-talk library: https://pypi.org/project/scikit-talk/
# :copyright: (c) 2021 Andreas Liesenfeld <lies0002@ntu.edu.sg> and Gabor Parti <gabor.parti@connect.polyu.edu.hk>
# :license: MIT, see LICENSE for more details.

import os
import csv
import regex as re
import numpy as np
import pandas as pd
import pylangacq
from speach import elan
import datetime

# ----------------------------------------------------------------------
# Filereader
# ----------------------------------------------------------------------
class Doc(DataObject):
    
    @classmethod
    def cha_to_df(path, *path_out):
        """
        Help
        """
        data_cha = pd.DataFrame()
        #read chat files one by one in a for loop, and append the conversations line by line to a dataframe
        for filename in os.listdir(path):
          if filename.endswith(".cha"):
              chatfile = pylangacq.read_chat(filename)
              chat_utterances=chatfile.utterances(by_files=False)
              for row in chat_utterances:
                data_cha = data_cha.append(pd.DataFrame({'speaker':row.participant, 'time':str(row.time_marks), 'utterance':str(row.tiers), 'source': path+filename}, index=[0]), ignore_index=True)
          else:
              continue

        # split time markers
        data_cha[['begin','end']] = data_cha.time.str.split(r', ', 1, expand=True)
        #do some reordering
        data_cha = data_cha[['begin', 'end', 'speaker', 'utterance', 'source']]
        # do some cleaning
        data_cha['begin'] = [re.sub(r'\(', "", str(x)) for x in data_cha['begin']]
        data_cha['end'] = [re.sub(r'\)', "", str(x)) for x in data_cha['end']]
        data_cha['utterance'] = [re.sub(r'^([^:]+):', "", str(x)) for x in data_cha['utterance']]
        data_cha['utterance'] = [re.sub(r'^\s+', "", str(x)) for x in data_cha['utterance']]
        data_cha['utterance'] = [re.sub(r'\s+$', "", str(x)) for x in data_cha['utterance']]
        data_cha['utterance'] = [re.sub(r'\}$', "", str(x)) for x in data_cha['utterance']]
        data_cha['utterance'] = [re.sub(r'^\"', "", str(x)) for x in data_cha['utterance']]
        data_cha['utterance'] = [re.sub(r'\"$', "", str(x)) for x in data_cha['utterance']]
        data_cha['utterance'] = [re.sub(r"^\'", "", str(x)) for x in data_cha['utterance']]
        data_cha['utterance'] = [re.sub(r"\'$", "", str(x)) for x in data_cha['utterance']]
        data_cha['utterance'] = [re.sub(r'\\x15\d+_\d+\\x15', "", str(x)) for x in data_cha['utterance']]
        # filling up empty cells with NaN
        data_cha.replace(r'^\s*$', np.nan, regex=True, inplace=True)
        data_cha.replace(r'None', np.nan, regex=True, inplace=True)
        data_cha.fillna(value=np.nan, inplace=True)
        # formatting timestamp
        data_cha['begin'] = pd.to_numeric(data_cha['begin'])
        data_cha['begin'] = pd.to_datetime(data_cha['begin'], unit='ms', errors='ignore')
        data_cha['begin'] = pd.to_datetime(data_cha['begin']).dt.strftime("%H:%M:%S.%f")#[:-3]
        data_cha['end'] = pd.to_numeric(data_cha['end'])
        data_cha['end'] = pd.to_datetime(data_cha['end'], unit='ms', errors='ignore')
        data_cha['end'] = pd.to_datetime(data_cha['end']).dt.strftime("%H:%M:%S.%f")#[:-3]

        if path_out:
            os.mkdir(''.join(path_out))
            data_cha.to_csv(''.join(path_out)+'data_cha.csv')
        return data_cha
      
    cha_to_df = Doc.cha_to_df
    
    
def eaf_to_dataframe(path, *path_out):
    data_eaf = pd.DataFrame([])
    for filename in os.listdir(path):
        if filename.endswith(".eaf"):
            eaf = elan.read_eaf(filename)
            for tier in eaf:
              for ann in tier:     
                   data_eaf = data_eaf.append(pd.DataFrame({'begin': ann.from_ts, 'end' : ann.to_ts, 'speaker' : tier.ID, 'utterance' : ann.text, 'source': path+filename}, index=[0]), ignore_index=True)
        else:
            continue
    if path_out:
      os.mkdir(''.join(path_out))
      data_eaf.to_csv(''.join(path_out)+'data_eaf.csv')
    # return data_eaf.sort_values(['source', 'begin','end'], ascending=[True, True, False], inplace=True)
    return data_eaf

def ldc_to_dataframe(path, *path_out):
    # define in path
    path=r'/content/'
    # create an empty dataframe
    data_ldc = pd.DataFrame()
    # read the txts, turn them into dataframes and append
    for filename in os.listdir(path):
        if filename.endswith(".txt"):
          textfile = pd.DataFrame()
          textfile[['time_speaker', 'utterance']] = pd.read_table(filename, sep=':', header=None)
          textfile['source'] = path+filename
          data_ldc = data_ldc.append(textfile)
        else:
          continue
    #filter out metadata
    meta_pattern = '^\#'
    filter = data_ldc['time_speaker'].str.contains(meta_pattern)
    data_ldc = data_ldc[~filter]
    #reset index
    data_ldc.reset_index(inplace=True, drop=True)
    # split speaker and time markers
    data_ldc[['time','speaker']] = data_ldc.time_speaker.str.split(r'\s(?!.*\s)', 1, expand=True)
    # split time markers
    data_ldc[['begin','end']] = data_ldc.time.str.split(r' ', 1, expand=True)
    # drop extra columns
    data_ldc.drop(columns=['time_speaker', 'time'], inplace=True)
    # reorder
    data_ldc = data_ldc[['begin',  'end', 'speaker', 'utterance', 'source']]
    # formatting timestamp
    data_ldc['begin'] = pd.to_numeric(data_ldc['begin'])
    data_ldc['begin'] = pd.to_datetime(data_ldc['begin'], unit='s', errors='ignore')
    data_ldc['begin'] = pd.to_datetime(data_ldc['begin']).dt.strftime("%H:%M:%S.%f")#[:-3]
    data_ldc['end'] = pd.to_numeric(data_ldc['end'])
    data_ldc['end'] = pd.to_datetime(data_ldc['end'], unit='s', errors='ignore')
    data_ldc['end'] = pd.to_datetime(data_ldc['end']).dt.strftime("%H:%M:%S.%f")#[:-3]
    
    if path_out:
      data_ldc.to_csv('/content/data_ldc.csv')

    return data_ldc

# ----------------------------------------------------------------------
# Transcription formatting
# ----------------------------------------------------------------------
