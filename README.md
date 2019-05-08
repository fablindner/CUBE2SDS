# CUBE2SDS

CUBE2SDS is a tool to rename and format DATA-CUBE minseed files into the SDS structre. It first converts the DATA-CUBE binary files into miniseed files using the DIGOS conversion software (https://digos.eu/downloads-docs).

## Usage

```bash
./cube2sds.sh
```

Paths to the conversion software, DATA-CUBE binary files and output directory files need to be specified in ```config.ini```. This latter file also contains the station mapping from DATA-CUBE name to network code, station code and channels. Test data and the latest DATA-CUBE conversion tool (as of April 2019) and test data are provided on VAW's vierzack07 server under ```/scratch_net/vierzack07_fourth/GlaSeis/DATA-CUBE3```, which can be used from any Linux machine at VAW.

## Requirements
* Python 3
* NumPy
* ObsPy
