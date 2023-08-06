# Change log for Bamboo API Client
All notable changes to this project will be documented in this file.

## 1.2.0 - 2021-07-27
- News fields in Sites schema: `country_code`, `timezone`, `latitude` & `longitude`
- Modified `list_sites` to return a simpler schema
- Renamed all `asset_name` arguments to `device_name`
- Added input data validation rules for all data models
- Added all variables in [mapping format](https://bambooenergy.atlassian.net/wiki/spaces/BMD/pages/175472655/Mapping+Format) to DataPoint schema
- Updated battery schema, removing the redundant `max_power` and `min_power` variables
- **BUGFIX**: Decreased min length for device names to 2 characters

## 1.1.5 - 2021-06-22
- Modify setup and requirements to make package compatible with Python 3.5 and up
- Update requirements in README and add dynamic version badges

## 1.1.3 - 2021-06-11
- Restrict exception catching to "NotFoundException" (HTTP 404) in get methods

## 1.1.2 - 2021-06-11
- Updated client based con v1.1.2 of openapi definition for Bamboo API

## 1.1.1 - 2021-06-04
- Updated README with usage instructions

## 1.1.0 - 2021-06-03
- Updated client based con latest openapi definition for Bamboo API
- Renamed `find` method to `get`: `find_site` becomes `get_site`, etc...
- In GET methods, catch `NotFound` API errors (HTTP 404) and return None instead of raising an error
- Added `get_site_id_by_name` method to obtain site ID given a site name
- Added `get_station_id_by_name` method to obtain weather station ID given a station name
- Renamed `read_load_model` to `read_baseline_model` and `update_load_model` to `update_baseline_model`
- Added missing `horizon` parameter in `update_forecasts` method

## 1.0.0 - 2021-05-27
- Initial release
