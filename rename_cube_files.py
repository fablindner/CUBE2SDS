from obspy import read, UTCDateTime
import sys
import os


def extract_stn_chn(fn, stns, chns):
    """
    Function to extraction station and channel code from a cube file name.
    :param fn: cube file name
    :param stns: dictionary mapping the cube names to station codes
    :param chns: dictionary mapping the cube channels to channel codes
    """
    # extract cube ID and cube channel
    cube_id = fn[2:5]
    cube_chn = fn[-4:]
    # get new station and channel names
    stn_new = stns[cube_id]
    chn_new = chns[cube_chn]
    return stn_new, chn_new


def update_stats(st, network, station, channel):
    """
    Function to update the network, station and channel code of traces in
    a stream object.
    :param st: stream object
    :param network: new network code
    :param station: new station code
    :param channel: new channel code
    """
    st = read(fn)
    for tr in st:
        tr.stats.network = network
        tr.stats.station = station
        tr.stats.channel = channel
    return st


def slice_st_jday(st):
    """
    Function to slice stream into daily stram objects.
    :param st: stream object
    """
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
    return st_dict






# allocate cube names to station names
stns = {"AJP": "RA21",
        "??2": "RA22",
        "??3": "RA23", "805": "TEST"}
# allocate cube channels to real channels
chns = {"pri0": "EHZ",
        "pri1": "EH2",
        "pri2": "EH3"}


# read cube file name
fn = sys.argv[1]
print("processing file '%s'" % fn)

# extract station and channel code from cube file name
stn_new, chn_new = extract_stn_chn(fn, stns, chns)

# read file and update network, station and channel code
st = read(fn)
st = update_stats(st, "4D", stn_new, chn_new)

# slice stream into daily records
st_dict = slice_st_jday(st)

# create directory for station and channel
directory = "./%s/%s.D/" % (stn_new, chn_new)
if not os.path.exists(directory):
    os.makedirs(directory)
os.chdir(directory)

# write daily records
jdays = st_dict.keys()
for jday in jdays:
    fn_new = "4D.%s..%s.D.%i.%s" % (stn_new, chn_new, st[0].stats.starttime.year, jday)
    st_ = st_dict[jday]
    st_.write(fn_new, format="MSEED")
