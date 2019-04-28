# imports the variables 'path_cbtool', 'path_binary', 'path_output'
source <(grep '^export .*=' config.ini)

# execute DATA-CUBE file conversion using the cubetools.
echo "=========================================================================="
echo "============ Converting DATA-CUBE binaries to MSEED files ... ============"
echo "=========================================================================="
$path_cbtool/cube2mseed -v --output-dir=$path_output $path_binary

# rename the new DATA-CUBE mseed files and save using the SDS structure.
echo "=========================================================================="
echo "============ Casting MSEED files into SDS format ...          ============"
echo "=========================================================================="
python cube_mseed2sds.py
# remove the *.pri* files
rm $path_output/c0*.pri*
echo "=========================================================================="
echo "============ Done !                                           ============"
echo "=========================================================================="
