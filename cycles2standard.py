#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Fri Jun 18 14:03:33 2021

@author: deborahkhider

Transform Cycles data to netcdf
"""

import pandas as pd
import numpy as np
import json
import os
import uuid
from datetime import date

def openCycles(season, summary):
    df_season = pd.read_table(season)
    df_summary = pd.read_table(summary)
    return df_season, df_summary

def summary_metadata(df_summary):
    summary_var = list(df_summary.keys())
    summary_units = list(np.array(df_summary.iloc[0,:]))

def root_metadata(time, ensemble_id):
    title = 'Outputs from Cycles model'
    summary = 'Results from a single execution of the Cycles model. Values for the parameters used for the simulation can be found in the ModelParameters Section of the JSON file'
    naming_authority = 'MINT workflow'
    uid = str(uuid.uuid4())
    keywords = 'Cycles, agriculture model'
    date_created = str(date.today())
    date_modified = str(date.today())
    creator_email = 'mint@isi.edu'
    convention = 'MINT'
    time_coverage_start = time[0]
    time_coverage_end =time[-1]  
    
    res = {'title':title,
           'summary':summary,
           'naming_authority':naming_authority,
           'id':uid,
           'keywords': keywords,
           'date_created':date_created,
           'date_modified':date_modified,
           'creator_email':creator_email,
           'convention': convention,
           'time_coverage_start':time_coverage_start,
           'time_coverage_end': time_coverage_end,
           'ensemble_id': ensemble_id}
    
    return res

#main function

season = '/Users/deborahkhider/Documents/GitHub/cycles_to_netcdf/season.dat'
summary = '/Users/deborahkhider/Documents/GitHub/cycles_to_netcdf/summary.dat'
lat = 6.5
lon = 54.5
ensemble_id = 'fshfufbfbubfjdbfsj45'


df = pd.read_table(season)