# ------------------------------------------
# --- Author: Chanthujan Chandrakumar
# --- Date: 11th July 2023
# --- Python Ver: 3.8
# ------------------------------------------

# your code starts here


import socket as s
from datetime import datetime, timedelta
from obspy import UTCDateTime
from obspy.core import read
from collections import deque
import numpy as np
import os
import matplotlib

matplotlib.use('TkAgg')
import matplotlib.pyplot as plt

################################IP address and the Port number of the sensor ###############################
host = ''
port = 50156


###############################################################################


####Functions


def create_dir(dir):
    if not os.path.exists(dir):
        os.makedirs(dir)
    return dir


global flag_sta_assign, flag_plot_assign, flag_chrt_assign
flag_sta_assign = True
flag_plot_assign = True
flag_chrt_assign = True


def classic_sta_lta_py(a, nsta, nlta, df, prev_sta = None, prev_lta = None):
    global flag_sta_assign,  flag_chrt_assign
    # The cumulative sum can be exploited to calculate a moving average (the
    # cumsum function is quite efficient)
    if flag_sta_assign:
        sta =  np.cumsum(a ** 2)
        lta = sta.copy()
        flag_sta_assign = False
    else:
        sta = np.concatenate([prev_sta, np.cumsum(a ** 2)])
        lta = np.concatenate([prev_lta, np.cumsum(a ** 2)])
        sta = sta[-61 * df:]
        lta = lta[-61 * df:]

    #check the length of the sta and lta whether it is greater than the 30 * df then remove the initial part and make it 30 * df
    # if len(sta) > 30 * df:
    #     sta = sta[-30 * df:]
    #     lta = lta[-30 * df:]


    # Convert to float
    sta = np.require(sta, dtype=np.float)
    lta = np.require(lta, dtype=np.float)

    # Compute the STA and the LTA
    sta[nsta:] = sta[nsta:] - sta[:-nsta]
    sta /= nsta
    lta[nlta:] = lta[nlta:] - lta[:-nlta]
    lta /= nlta

    # Pad zeros
    sta[:nlta - 1] = 0

    # Avoid division by zero by setting zero values to tiny float
    dtiny = np.finfo(0.0).tiny
    idx = lta < dtiny
    lta[idx] = dtiny

    charfct = sta/lta
    print("length of charfct: ", len(charfct))
    for i in range(len(charfct) - 100):
        charfct[i] = 0.0
    return sta, lta, charfct


def plot_trigger(trace, cft, prev_cft, thr_on, thr_off, batch, stn, show=True): #function to plot the trigger on and off values
    global flag_plot_assign
    df = 100
    npts = len(trace.data)

    t = np.arange(npts, dtype=np.float32) / df
    # x_values = [trace.stats.starttime + timedelta(seconds=t_val) for t_val in t]

    # t = float(trace.stats.starttime) + np.arange(npts) / df
    # t = trace.stats.starttime + np.arange(npts, dtype=np.float32) / df
    fig = plt.figure()
    #plot title with the trace.stats.starttime and the station name
    ax1 = fig.add_subplot(211)
    ax1.plot(t, trace.data, 'k')
    ax2 = fig.add_subplot(212, sharex=ax1)
    if flag_plot_assign:
        ax2.plot(t, cft[2], 'k')
        flag_plot_assign = False
        current_cft = cft[2]
    else:
        #assign the non zero values of the current cft to a new array named new_cft
        new_cft_values = cft[2][np.nonzero(cft[2])]
        print("length of new_cft_values: ", len(new_cft_values))
        print("length of prev_cft: ", len(prev_cft))
        current_cft = np.concatenate((prev_cft, new_cft_values))
        #concataneate
        ax2.plot(t, current_cft, 'k')  # Concatenate previous and current cft values
    on_off = np.array(trigger_onset(current_cft, thr_on, thr_off))
    i, j = ax1.get_ylim()
    try:
        ax1.vlines(on_off[:, 0] / df, i, j, color='r', lw=2, label="Trigger On")
        print("on_off[:, 0] / df", on_off[:, 0])
        ax1.vlines(on_off[:, 1] / df, i, j, color='b', lw=2, label="Trigger Off")
        ax1.legend()
    except IndexError:
        pass
    ax2.axhline(thr_on, color='red', lw=1, ls='--')
    ax2.axhline(thr_off, color='blue', lw=1, ls='--')
    # ax2.set_xlabel("Time after %s [s]" % trace.stats.starttime.isoformat())
    fig.suptitle("Station Name: " + str(trace.stats.station) + "start_time" + str(trace.stats.starttime))
    fig.canvas.draw()
    print("Saving figure")

    if show:
        path_temp = "Results/standard_STA_LTA/" + stn + "/"
        create_dir(path_temp)
        plt.savefig(path_temp + "batch number" + str(batch) + ".png", bbox_inches='tight')
        # plt.show()
        plt.close()

    # Return the current cft for the next function call
    return current_cft
def trigger_onset(charfct, thres1, thres2, max_len=9e99, max_len_delete=False):
    ind1 = np.where(charfct > thres1)[0]
    if len(ind1) == 0:
        return []
    print("ind1", ind1[0])
    print("STA/LTA value:" + str(charfct[ind1[0]]))
    ind2 = np.where(charfct > thres2)[0]
    #
    on = deque([ind1[0]])
    of = deque([-1])
    # determine the indices where charfct falls below off-threshold
    ind2_ = np.empty_like(ind2, dtype=bool)
    ind2_[:-1] = np.diff(ind2) > 1
    # last occurence is missed by the diff, add it manually
    ind2_[-1] = True
    of.extend(ind2[ind2_].tolist())
    on.extend(ind1[np.where(np.diff(ind1) > 1)[0] + 1].tolist())
    # include last pick if trigger is on or drop it
    if max_len_delete:
        # drop it
        of.extend([1e99])
        on.extend([on[-1]])
    else:
        # include it
        of.extend([ind2[-1]])
    #
    pick = []
    while on[-1] > of[0]:
        while on[0] <= of[0]:
            on.popleft()
        while of[0] < on[0]:
            of.popleft()
        if of[0] - on[0] > max_len:
            if max_len_delete:
                on.popleft()
                continue
            of.appendleft(on[0] + max_len)
        pick.append([on[0], of[0]])
    return np.array(pick, dtype=np.int64)


def detect_p_amp(data, charfct, thres1):
    ind1 = np.where(charfct > thres1)[0]
    if len(ind1) == 0:
        return []
    print("ind1", ind1[0])
    print("STA/LTA value:" + str(charfct[ind1[0]]))
    return ind1[0], data[ind1[0]]


def demean_func(L):  # Function which returns the average of signal readings
    sense_data = s[2:len(s)]
    sense_int = [int(i) for i in sense_data]
    mean = sum(sense_int) / 25
    count = [x - mean for x in sense_int]
    return count


st_ENZ = [] #initialise the st_ENZ array
station_name = 'R59BB' #station name
st_main = read("ENZ_0_DATA.mseed") #read the data from the mseed file to the variable st_main
st = read("ENZ_0_DATA.mseed") #read the data from the mseed file to the variable st
time_rec = 0 #initialise the time_rec variable



#UDP socket connection
sock = s.socket(s.AF_INET, s.SOCK_DGRAM)
sock.setsockopt(s.SOL_SOCKET, s.SO_REUSEADDR, 1)
sock.bind((host, port))


batch = 0
prev_sta = 0.0
prev_lta = None
prev_cft = None
# Parameters for STA/LTA
sta = 3
lta = 60
thrOn = 2.5
thrOff = 2
df = 100 #sampling frequency of the data
time_assign_flag = True
while 1:  # loop forever
    data, addr = sock.recvfrom(1024)  # wait to receive data
    s = data.decode('UTF-8').strip("'{}").split(', ')  # clean and listify the data

    if (s[0] == "ENN'"):
        time_rec = s[1]
        mag_NS = demean_func(s)

    elif (s[0] == "ENE'"):
        if (s[1] == time_rec):
            mag_EW = demean_func(s)

    elif (s[0] == "ENZ'"):
        if (s[1] == time_rec):
            if (time_assign_flag):
                st_main[0].stats.starttime = UTCDateTime(float(time_rec))
                time_assign_flag = False
            print("start time: " + str(st_main[0].stats.starttime))
            st_ENZ = st_ENZ + demean_func(s)
            st_main[0].data = np.array(st_ENZ)
            print("Length of ENZ: " + str(len(st_main[0].data)))
            if (len(st_ENZ) >= 6100 and len(st_ENZ) % 100 == 0):
                st_main.filter("bandpass", freqmin=0.1, freqmax=20)
                data_pckt = st_main[0].data[len(st_main[0].data) - 6100:]
                st[0].data = np.array(data_pckt) #datapack of 1000 samples for the recursive STA/LTA function
                print("Length of LTA" + str(len(st[0].data)))
                prev_sta, prev_lta, cft = classic_sta_lta_py(st[0].data, int(sta * df), int(lta * df), df, prev_sta, prev_lta)
                prev_cft = plot_trigger(st_main[0], [prev_sta, prev_lta, cft], prev_cft, thrOn, thrOff, batch,station_name)
                batch = batch + 1