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
import sys
from collections import OrderedDict
from datetime import date
import re
import shutil
#%% Create dictionaries

var_name = {'DATE':'time',
            'CROP':'crop__name',
            'PLANT_DATE':'plant__time',
            'TOTAL BIOMASS':'plant_at-grain-or-forage-harvest-or-death__mass-per-area_density',
            'ROOT BIOMASS':'plant_root_at-grain-or-forage-harvest-or-death__mass-per-area_density',
            'GRAIN YIELD':'grain~dry__mass-per-area_yield',
            'FORAGE YIELD':'forage-or-residue~removed_at-harvest__mass-per-area_yield',
            'AG RESIDUE':'ground~above_residue~remaining_at-harvest__mass-per-area_density',
            'HARVEST INDEX': 'ground~above_biomass~harvested_grain__mass_fraction',
            'POTENTIAL TR': 'crop__potential_transpiration_volume_flux',
            'ACTUAL TR': 'crop_water__time_integral_of_transpiration_volume_flux',
            'SOIL EVAP': 'soil_surface_water__time_integral_of_evaporation_volume_flux',
            'IRRIGATION':'soil__water__irrigation',
            'TOTAL N':'biomass_nitrogen_at-harvest__mass-per-area_accumulation_density',
            'ROOT N':'crop_root_nitrogen_at-harvest__mass-per-area_accumulation_density',
            'GRAIN N':'grain_nitrogen_at-harvest__mass-per-area_density',
            'FORAGE N':'forage-or-residue~removed_nitrogen_at-harvest__mass-per-area_yield',
            'CUM. N STRESS':'crop_nitrogen__thermal-time-to-maturity_weighted_stress_fraction',
            'N IN HARVEST': 'biomass~removed_nitrogen__mass-per-area_density',
            'N IN RESIDUE': 'field_residue~remaining_nitrogen_at-harvest__mass-per-area_density',
            'N CONCN FORAGE': 'forage-or-residue~removed_nitrogen__mass_fraction',
            'N FIXATION':'nitrogen__fixation',
            'N ADDED':'plant__nitrogen_added',
            'INIT PROF C':'soil_carbon_pool~stabilized_carbon__initial_mass',
            'FINAL PROF C':'soil_carbon_pool~stabilized_carbon__final_mass',
            'PROF C DIFF':'soil_carbon_pool~stabilized_carbon__change_of_mass',
            'RES C INPUT':'ground~above_crop_residue-as-carbon__decomposition_mass',
            'ROOT C INPUT':'ground~above_crop_roots-and-rhizodeposits-as-carbon__decomposition_mass',
            'HUMIFIED C':'soil_pool-and-pool~microbial_carbon~decomposed__addition_mass',
            'RESP SOIL C':'crop_biomass~microbial-and-soil_carbon__decomposition_respiration_mass',
            'RESP RES C':'crop_residue_pool_carbon__time_integral_of_decomposition_respiration_mass_flux',
            'RETAINED RES':'ground~above_crop_residue~retained__mass-per-area_density',
            'PRODUCED ROOT':'roots-and-rhizodeposits__time_integral_of_mass-per-area_production_rate',
            'SOIL C CHG/YR':'soil_organic_carbon~rate__change',
            'AVG GROSS N MIN':'nitrogen__average_of_gross_mass_mineralization_rate',
            'AVG N IMMOB':'nitrogen__average_of_gross_mass_immobilization_rate',
            'AVG NET N MIN':'nitrogen__average_of_net_mass_mineralization_rate',
            'AVG NH4 NITRIF':'soil_nitrogen__average_of_mass_nitrification_rate',
            'AVG N2O FR NIT':'soil_nitrous-oxide-as-nitrogen__average_of_nitrification_mass_emission_rate',
            'AVG NH3 VOLATIL':'ammonia-as-nitrogen__average_of_mass_volatilization_rate',
            'AVG NO3 DENIT':'soil_nitrogen__average_of_mass_denitrification_rate',
            'AVG N2O FR DENI':'soil_nitrous-oxide-as-nitrogen__average_of_denitrification_mass_emission_rate',
            'AVG NO3 LEACH':'nitrate-as-nitrogen__average_of_mass_leaching_rate',
            'AVG NH4 LEACH':'ammonium-as-nitrogen__average_of_mass_leaching_rate',
            'AVG TOT N2O EMI':'soil_nitrous-oxide-as-nitrogen__average_of_mass_emission_rate'
            }
var_title = {'DATE':'Harvest Event date',
             'CROP':'Crop Name',
             'PLANT_DATE':'Planting date of harvested crop',
             'TOTAL BIOMASS':'Total biomass produced (all mass is dry matter)',
             'ROOT BIOMASS':'Root Biomass',
             'GRAIN YIELD':'Grain Yield',
             'FORAGE YIELD':'Forage Yield',
             'AG RESIDUE': 'Aboveground residue left after harvest',
             'HARVEST INDEX':'Ratio of grain biomass to aboveground biomass at harvest',
             'POTENTIAL TR':'Potential transpiration (water evaporated from the plant, assuming that soil moisture would not limit transpiration)',
             'ACTUAL TR':'Transpiration (all limitations considered)',
             'SOIL EVAP': 'Soil evaporation (Evaporation of water from the soil from planting to harvest)',
             'IRRIGATION':'Irrigation water (from planting to harvest if irrigation was enabled)',
             'TOTAL N': 'Mass of nitrogen in the plant at harvest',
             'ROOT N': 'Mass of nitrogen in the roots at harvest',
             'GRAIN N':'Mass of nitrogen in the grain at harvest',
             'FORAGE N':'Mass of nitrogen in the forage at harvest',
             'CUM. N STRESS': 'Cumulative nitrogen stress (a measure of the nitrogen stress through the cycle of the crop)',
             'N IN HARVEST':'Mass of nitrogen in the harvested material (grain or forage or underground material)',
             'N IN RESIDUE' : 'Mass of nitrogen left on residue',
             'N CONCN FORAGE': 'Concentration of nitrogen in the harvested forage',
             'N FIXATION': 'Mass of nitrogen from nitrogen fixation',
             'N ADDED': 'Mass of nitrogen that is added to the crop (if auto N is ON)',
             'INIT PROF C':'Initial organic soil carbon in the soil profile',
             'FINAL PROF C':'Final organic soil carbon in the soil profile',
             'PROF C DIFF':'Change in C content of the stabilized soil C pool from the beginning to end of the simulation.',
             'RES C INPUT':'Total quantity of aboveground crop residues decomposed over the duration of the simulation.',
             'ROOT C INPUT':'Total quantity of roots and rhizodeposits decomposed over the duration of the simulation.',
             'HUMIFIED C':'Total quantity of decomposed C added to microbial and soil C pools over the duration of the simulation.',
             'RESP SOIL C':'Total quantity of C respired during decomposition of the microbial biomass and stabilized soil C pools over the duration of the simulation.',
             'RESP RES C':'Total quantity of C respired during decomposition of the residue pools',
             'RETAINED RES':'Total quantity of aboveground crop residues retained in the field over the duration of the simulation',
             'PRODUCED ROOT':'Total quantity of roots and rhizodeposits produced over the duration of the simulation.',
             'SOIL C CHG/YR':'Rate of change of soil organic carbon ',
             'AVG GROSS N MIN':'Gross mineralization of nitrogen',
             'AVG N IMMOB':'Immobilization of nitrogen',
             'AVG NET N MIN':'Net mineralization of nitrogen',
             'AVG NH4 NITRIF':'Ammonium nitrification in units of nitrogen',
             'AVG N2O FR NIT':'Nitrous oxide emitted from nitrification in units of nitrogen',
             'AVG NH3 VOLATIL':'Ammonia volatilization in units of nitrogen ',
             'AVG NO3 DENIT':'Nitrate denitrification in units of nitrogen',
             'AVG N2O FR DENI':'Nitrous oxide emitted from denitrification in units of nitrogen',
             'AVG NO3 LEACH':'Nitrate leaching in units of nitrogen',
             'AVG NH4 LEACH':'Ammonium leaching in units of nitroge',
             'AVG TOT N2O EMI':'Sum of nitrous oxide emitted from nitrification and denitrification in units of nitrogen'
             }

var_units = {'DATE':'YYYY-MM-DD',
             'CROP':'NA',
             'PLANT_DATE':'YYYY-MM-DD',
             'TOTAL BIOMASS':'Mg/ha',
             'ROOT BIOMASS':'Mg/ha',
             'GRAIN YIELD':'Mg/ha',
             'FORAGE YIELD':'Mg/ha',
             'AG RESIDUE':'Mg/ha',
             'HARVEST INDEX': 'Mg/Mg',
             'POTENTIAL TR': 'mm',
             'ACTUAL TR': 'mm',
             'SOIL EVAP': 'mm',
             'IRRIGATION':'mm',
             'TOTAL N':'Mg/ha',
             'ROOT N':'Mg/ha',
             'GRAIN N':'Mg/ha',
             'FORAGE N':'Mg/ha',
             'CUM. N STRESS':'NA',
             'N IN HARVEST': 'kg/ha',
             'N IN RESIDUE': 'kg/ha',
             'N CONCN FORAGE': '%',
             'N FIXATION':'kg/ha',
             'N ADDED':'kg/ha',
             'INIT PROF C':'Mg C/ha',
             'FINAL PROF C':'Mg C/ha',
             'PROF C DIFF':'Mg C/ha',
             'RES C INPUT':'Mg C/ha',
             'ROOT C INPUT':'Mg C/ha',
             'HUMIFIED C':'Mg C/ha',
             'RESP SOIL C':'Mg C/ha',
             'RESP RES C':'Mg C/ha',
             'RETAINED RES':'Mg/ha',
             'PRODUCED ROOT':'Mg/ha',
             'SOIL C CHG/YR':'kg C/yr',
             'AVG GROSS N MIN':'kg N/yr',
             'AVG N IMMOB':'kg N/yr',
             'AVG NET N MIN':'kg N/yr',
             'AVG NH4 NITRIF':'kg N/yr',
             'AVG N2O FR NIT':'kg N/yr',
             'AVG NH3 VOLATIL':'kg N/yr',
             'AVG NO3 DENIT':'kg N/yr',
             'AVG N2O FR DENI':'kg N/yr',
             'AVG NO3 LEACH':'kg N/yr',
             'AVG NH4 LEACH':'kg N/yr',
             'AVG TOT N2O EMI':'kg N/yr'
             }        

#%% Functions
def openCycles(season, summary):
    '''Open the Cycles outputs into a dataframe, forcing what can be forced into floats.
    
    Note that this function doesn't transform the DATE variable into a datetime dtype as to be able to save the files. 
    

    Parameters
    ----------
    season : str
        path to the season.dat file
    summary : str
        path to the summary.dat file

    Returns
    -------
    df_season : pandas.DataFrame
        Content of the season.dat file as a pandas dataframe
    df_summary : pandas. DataFrame
        Content of the summary file as a pandas dataframe

    '''
    df_season = pd.read_csv(season,sep='\t',header=0,skiprows=[1]) # Skip the units when importing
    df_summary = pd.read_csv(summary,sep='\t',header=0,skiprows=[1])
    df_season.columns = variables(df_season) # Remove spaces in the headers
    df_summary.columns = variables(df_summary)
    return df_season, df_summary

def variables(df):
    '''Get the list of variables from the headers of a DataFrame

    Parameters
    ----------
    df : Pandas.DataFrame
       

    Returns
    -------
    list
        A list of hearders, with the spaces at the end removed. 

    '''
    return [item.rstrip() for item in list(df.keys())]   

def title_to_longname(title):
    '''Generate long name from the long titles (i.e. description) by removing everything in parenthesis


    Parameters
    ----------
    title : str
        The description to transform.

    Returns
    -------
    str
        The long name.

    '''
    return re.sub(r"\([^()]*\)", "", title)

def root_metadata(time, ensemble_id, execution_id):
    '''Generates the root dictionary
    

    Parameters
    ----------
    time : list
        Time vector
    ensemble_id : str
        ensemble ID from MINT
    execution_id : str
        execution ID from MINT.

    Returns
    -------
    res : OrderedDict
        Dictionary of relevant metadata

    '''
    title = 'Outputs from Cycles model'
    summary = 'Results from a single execution of the Cycles model. Values for the parameters used for the simulation can be found in the ModelParameters Section of the JSON file'
    naming_authority = 'MINT workflow'
    uid = 'cycles_'+execution_id
    keywords = 'Cycles, agriculture model'
    date_created = str(date.today())
    date_modified = str(date.today())
    creator_email = 'mint@isi.edu'
    convention = 'MINT'
    time_coverage_start = time[0]
    time_coverage_end =time[-1]
    res = OrderedDict({'title':title,
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
           'ensemble_id': ensemble_id,
           'execution_id':execution_id})
    
    return res

def location_metadata(lat,lon):
    '''Create the location dictionary
    

    Parameters
    ----------
    lat : float
        Latitude
    lon : float
        Longitude

    Returns
    -------
    OrderedDict
        Location dictionary

    '''
    geospatial_bounds = [lon,lat,lon,lat]
    geo = {'geometry':{'coordinates':[lon,lat],'type':"Point"},'properties':[],"type":"Feature"} 
    return OrderedDict({'geospatial_bounds': geospatial_bounds, "geo":geo})

def var_metadata(df, var_name, var_title, var_units):
    '''Generate the dictionary for each of the variables present in the dataframe
    

    Parameters
    ----------
    df : Pandas.DataFrame
        the data contained in a dataframe. Each columns represents a variable
    var_name : dict
        dictionary of variable names defined internally
    var_title : dict
        dictionary of variable titles defined internally
    var_units : dict
        dictionary of variable titles defined internally

    Returns
    -------
    columns : OrderedDict
        Dictionary of metadata for each of the variables

    '''
    variables = list(df.keys())
    columns = [] 
    for idx,item in enumerate(variables):
        columns.append(OrderedDict({'name':item,
                        'title':var_title[item],
                        'standard_name':var_name[item],
                        'long_name':title_to_longname(var_title[item]),
                        'units':var_units[item],
                        'valid_min': np.min(np.array(df.iloc[:,idx])),
                        'valid_max': np.max(np.array(df.iloc[:,idx])),
                        'valid range':[np.min(np.array(df.iloc[:,idx])),np.max(np.array(df.iloc[:,idx]))],
                        'missing_value': 'NA',
                        'fill_value': 'NA',
                        'number':idx+1}))
    return columns

def write(df_season,df_summary,meta):
    '''Write the data contained in dataframes to csv and the metadata to JSON. Zip all files.
    
    This function REQUIRES read and write access. 
    

    Parameters
    ----------
    df_season : pandas.DataFrame
        dataframe containing the season information
    df_summary : pandas.DataFrame
        dataframe containing the summary information
    meta : dict
        Dictionary of metadata 

    Returns
    -------
    None.

    '''
    #create a temp directory
    path = meta['id']
    os.mkdir(path)
    # write out the tables to csv
    df_season.to_csv(path+'/season.csv',header=False)
    df_summary.to_csv(path+'/summary.csv',header=False)
    #Write the json file
    with open(path+'/metadata.json','w') as outfile:
        json.dump(meta,outfile)
    #Zip it
    shutil.make_archive(path,'zip',path)
    #remove temporary folder
    shutil.rmtree(path)

#%% Main function
if __name__ == '__main__':
    with open(sys.argv[1]) as json_file:
        config = json.load(json_file)
    season = config['season']#'/Users/deborahkhider/Documents/GitHub/cycles_to_netcdf/season.dat'
    summary = config['summary']#/Users/deborahkhider/Documents/GitHub/cycles_to_netcdf/summary.dat'
    lat = config['lat']#6.5
    lon = config['lon']#54.5
    execution_id = config['execution_id']#fshfufbfbubfjdbfsj45'
    ensemble_id = config['ensemble_id']#fhvjbjvbfjvbjebjebje'
    params = config['params']#{'start_year':1980,'end_year':2019,'crop_name': 'Maize',
              #'start_planting_day': 34, 'end_planting_day':149,
              #'fertilizer_rate':0,'weed_fraction':0.4}
    model_name = config['model_name']#'Cycles'
    model_version = config['model_version']#'v10.3'
    model_description = config['model_description']#Cycles simulates the productivity and the water,carbon and nitrogen balance of soil-crop systems subject to climate conditions and a large array of management constraints.'
    
    #main function
    
    # Open the cycles output
    df_season, df_summary = openCycles(season,summary)
    #Get the root metadata and start the dictionary
    meta = root_metadata(np.array(df_season.iloc[:,0]),ensemble_id,execution_id)
    meta['geo'] = location_metadata(lat,lon)
    meta['model'] = {'parameters':params,'model_name': model_name, 
                     'model_version': model_version,
                     'model_description' : model_description}
    #Deal with tables and variables
    season_table = OrderedDict({'table_name':'season',
                    'filename':'season.csv',
                    'columns': var_metadata(df_season,var_name,var_title,var_units)})
    summary_table = OrderedDict({'table_name':'summary',
                    'filename':'summary.csv',
                    'columns': var_metadata(df_summary,var_name,var_title,var_units)})
    meta['data'] = [season_table,summary_table]
    write(df_season,df_summary,meta)
                
                
