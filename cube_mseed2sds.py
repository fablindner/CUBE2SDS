from obspy import read, UTCDateTime
from configparser import ConfigParser
import numpy as np
import glob
import os


def new_net_stn_chn(fn, stn_mapping):
    """
    Extract DATA-CUBE name and channel number from file name. Return the 
    corresponding network, station, and channel code.
    :param fn: The filename pattern.
    :param stn_mapping: Station mapping from the config.ini file as read with
        the ConfigParser.
    """
    stn_old = fn[2:5]
    chn_old = fn[-1]

    cubes = [item[0] for item in stn_mapping]
    net_stn_chns = stn_mapping[cubes.index(stn_old)][1].split(",")
    net_new  = net_stn_chns[0]
    stn_new  = net_stn_chns[1]
    chns     = net_stn_chns[2:]
    chn_new  = chns[int(chn_old)]
    return net_new, stn_new, chn_new


def update_stats(st, network, station, channel):
    """
    Function to update the network, station and channel code of traces in
    a stream object.
    :param st: stream object
    :param network: new network code
    :param station: new station code
    :param channel: new channel code
    """
    for tr in st:
        tr.stats.network = network
        tr.stats.station = station
        tr.stats.channel = channel
    return st


def slice_st_jday(st):
    """
    Function to slice stream into daily stream objects.
    :param st: stream object
    """
    # extract all year-julday combinations
    year_jday_st = [(tr.stats.starttime.year, tr.stats.starttime.julday) for tr in st]
    year_jday_et = [(tr.stats.endtime.year, tr.stats.endtime.julday) for tr in st]
    year_jday    = sorted(list(set(year_jday_st + year_jday_et)))

    # slice stream into daily (sub)streams
    st_list = []
    for yr_jd in year_jday:
        t1 = UTCDateTime(yr_jd[0], 1, 1, 0, 0, 0)
        t1.julday = yr_jd[1] 
        t2 = t1 + 24. * 3600. - st[0].stats.delta 
        st_list.append(st.slice(t1, t2))
    return year_jday, st_list






# import config data
cparser = ConfigParser()
cparser.read("config.ini")

# read cube file names
path_output = cparser.items("directories")[2][1]
file_list   = glob.glob("%s/*.pri*" % path_output)
file_pttrn  = sorted(list(set([fn.split("/")[-1][:11] + "*" + fn.split("/")[-1][-5:] \
    for fn in file_list])))

# read station mapping
stn_mapping = cparser.items("stn_mapping")

# loop over file patterns ...
for fp in file_pttrn:

    print("Processing files matching '%s'" % fp)
    # extract network, station and channel corresponding to the CUBE file
    # according to the station mapping.
    net, stn, chn = new_net_stn_chn(fp, stn_mapping)
    
    # read file and update network, station and channel code
    st = read(path_output + "/" + fp)
    st = update_stats(st, net, stn, chn)
    
    # slice stream into daily records
    year_jday, st_list = slice_st_jday(st)

    # write daily records in SDS format
    for i, yr_jd in enumerate(year_jday):
        directory = "/%s/%s/%s/%s/%s.D/" % (path_output, yr_jd[0], net, stn, chn)
        if not os.path.exists(directory):
            os.makedirs(directory)
        fn_new = "%s/%s.%s..%s.D.%04d.%03d" % (directory, net, stn, chn, yr_jd[0], yr_jd[1])
        st_list[i].write(fn_new, format="MSEED")
