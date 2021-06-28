# Transforming Cycles outputs to a standard file format

Routines and recipes to transform cycles outputs to standard format.

NetCDF MINT conventions are defined on [this GitHub repo](https://github.com/mintproject/MINT-NetCDF-Convention).

Use a combination of JSON/csv to represent the Cycles data. Metadata in the JSON file should include the following: 

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
	1. GeoJSON Point
	2. geospatial_bounds
3. Model parameters
	1. Exposed parameters from the configuration
	2. Model name (The actual model, not config)
	3. Model version
	4. Model_description
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
