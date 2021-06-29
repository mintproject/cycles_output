![Python 3.9](https://img.shields.io/badge/python-3.9-blue.svg)

# Transforming Cycles outputs to a standard file format

This repository contains routines and recipes to transform cycles outputs to standard format.

## Software
### Requirements
1. Python 3.9
2. pandas == 1.2.5

The software needs write/delete access to the folder in which it runs.  

### Command line execution

`python cycles2standard.py config.json`

#### Input
The `config.json` file gathers the following information:
1. season: path to season.dat
2. summary: path to summary.dat
3. lat: latitude
4. lon: longitude
5. execution_id: MINT execution ID
6. ensemble_id: MINT ensemble ID
7. params: model parameters as a dictionary. Number of parameters can vary, as can the keys.
8. model_name: 'Cycles' - leave
9. model_version: The version of the model
10. model_description: Description of the model

#### Outputs
The output consists of a zip file named as `cycles_execution_id.zip`. The zip file contains the data contained in season.dat and summary.dat in csv and the metadata in JSON format.

**WARNING** Software creates a temporary folder for the csv and json file for zipping. Needs permission to delete this file.

Description of the metadata output in the next section.

## MINT Point data conventions

The JSON file contains the same metadata information as previously defined for NetCDF MINT on [this GitHub repository](https://github.com/mintproject/MINT-NetCDF-Convention).

1. Root metadata
	1. title:  Outputs from Cycles model
	2. summary: Results from a single execution of the Cycles model. Values for the parameters used for the simulation can be found in the ModelParameters Section of the JSON file
	3. naming_authority: MINT Workflow
	4. id:  generate a unique id for registration
	5. keywords: 'Cycles, Agriculture model'
	6. date_created:
	7. date_modified:
	8. creator_email: mint@isi.edu
	9. convention: MINT
	10. time_coverage_start
	11. time_coverage_end
	12. ensemble_id
	13. execution_id
2. Location metadata
	1. geo: GeoJSON Point
	2. geospatial_bounds
3. Model information:
	1. parameters: Exposed parameters from the configuration
	2. model_name: Model name (The actual model, not config)
	3. model_version: Model version
	4. model_description: Model_description
4. Data
	1. short name
	2. Title
	3. Standard_name
	4. long_name
	5. units
	6. valid_min
	7. valid_max
	8. valid_range
	9. missing_value
	10. fill_value
