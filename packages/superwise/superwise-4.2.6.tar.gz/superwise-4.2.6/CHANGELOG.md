# Changelog
Here you will find a changelog of all the SDK releases.

## [4.2.3] 2021-12-07
- fix bug in binning for numeric features with null values

## [4.2.2] 2021-12-01
- Change the binning mechanism for numeric data entities

## [4.1.0] 2021-11-28
This release not has breaking changes - add functionality for transaction:
- add functionality to upload data from s3 to superwise
- add functionality to upload data from gcs to superwise

## [4.0.0] 2021-11-23
This release has breaking changes - task changed following properties:
- task_description &rarr; description
- title &rarr; name
- task_type &rarr; removed

## [3.2.0] - 2021-11-16
This release has breaking changes.
Refactor tasks model

## [3.1.2] - 2021-11-15

Improve requirements.txt - lock versions and added jwt as a requirement.

remove DEBUG mode

log.debug added for each API call

## [3.1.0] - 2021-11-11
This release has breaking changes.
removed client_name as a param from superwise object


## [3.0.0] - 2021-10-19
This release has breaking changes.
We define new entity named transaction, which responsible to manage all the data send to superwise.

### Added
- Add Class Transaction, which have 2 methods to send data to superwise (file , batch).

### Removed
- Removed Data Class and send_file methods, for send data to superwise you should use the Transaction class.
