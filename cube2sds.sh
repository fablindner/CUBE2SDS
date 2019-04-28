# Import the variables 'path_cbtool', 'path_binary', 'path_output' from the
# config.ini file.
source <(grep '^export .*=' config.ini)

# Execute DATA-CUBE file conversion using the cubetools and the paths provided
# through the previous command.
echo "=========================================================================="
echo "============ Converting DATA-CUBE binaries to MSEED files ... ============"
echo "=========================================================================="
$path_cbtool/cube2mseed -v --output-dir=$path_output $path_binary

# Rename the DATA-CUBE mseed files created through the previous command using the
# station mapping provided in the config.ini file and save them in the SDS format.
echo "=========================================================================="
echo "============ Casting MSEED files into SDS format ...          ============"
echo "=========================================================================="
python cube_mseed2sds.py
# remove the *.pri* files
rm $path_output/c0*.pri*
echo "=========================================================================="
echo "============ Done !                                           ============"
echo "=========================================================================="
