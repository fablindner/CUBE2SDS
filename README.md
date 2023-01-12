# CUBE2SDS

CUBE2SDS is a tool to rename and format DATA-CUBE minseed files into the SDS structre. It first converts the DATA-CUBE binary files into miniseed files using the DIGOS conversion software (https://digos.eu/downloads-docs).

## Usage

```bash
./cube2sds.sh
```

Paths to the conversion software, DATA-CUBE binary files and output directory files need to be specified in ```config.ini```. This file also contains the station mapping from DATA-CUBE name to network code, station code and channels. Check for the latest version of the DATA-CUBE conversion software.

## Requirements
A (ana)conda environment named "obspy" containing the following packages:
* Python 3
* NumPy
* ObsPy
