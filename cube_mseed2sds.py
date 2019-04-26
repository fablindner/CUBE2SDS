from obspy import read, UTCDateTime
from configparser import ConfigParser
import numpy as np
import glob
import os


def new_net_stn_chn(fn, stn_mapping):
    #fn_ = fn.split("/")[-1]
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
    # check if start and endtime are in same year - raise error otherwise!
    if st[0].stats.starttime.year != st[-1].stats.endtime.year:
        raise ValueError("Starttime and endtime are in different years.")

    # obtain minimum and maximum day of the year
    jday_min = st[0].stats.starttime.julday
    jday_max = []
    for tr in st:
        jday_max.append(tr.stats.endtime.julday)
    jday_max = max(jday_max)

    # slice stream into daily (sub)streams
    st_dict = {} 
    year = st[0].stats.starttime.year
    dt = st[0].stats.delta
    for j in range(jday_min, jday_max+1):
        t1 = UTCDateTime(year, 1, 1, 0, 0, 0)
        t1.julday = j
        t2 = t1 + 24. * 3600. - dt
        jday = "%03d" % j
        st_dict[jday] = st.slice(t1, t2)
    return st_dict, year






# import config data
cparser = ConfigParser()
cparser.read("config.ini")

# read cube file names
path_output = cparser.items("directories")[2][1]
file_list  = glob.glob("%s/*.pri*" % path_output)
file_pttrn = list(set([fn.split("/")[-1][:11] for fn in file_list]))

# read station mapping
stn_mapping = cparser.items("stn_mapping")


for fp in file_pttrn:
    for ch in [".pri0", ".pri1", ".pri2"]:
        fn = fp + "*" + ch
        print("processing files matching '%s'" % fn)
        
        # extract network, station and channel corresponding to the CUBE file
        # according to the station mapping.
        net, stn, chn = new_net_stn_chn(fn, stn_mapping)
        
        # read file and update network, station and channel code
        st = read(path_output + "/" + fn)
        st = update_stats(st, net, stn, chn)
        
        # slice stream into daily records
        st_dict, year = slice_st_jday(st)

        # create directory for station and channel
        directory = "/%s/%s/%s/%s/%s.D/" % (path_output, year, net, stn, chn)
        if not os.path.exists(directory):
            os.makedirs(directory)
        
        # write daily records
        jdays = st_dict.keys()
        for jday in jdays:
            fn_new = "%s/4D.%s..%s.D.%i.%s" % (directory, stn, chn, year, jday)
            st_ = st_dict[jday]
            st_.write(fn_new, format="MSEED")
