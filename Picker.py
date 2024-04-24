import csv
from obspy.core import read
import numpy as np
import os
from matplotlib.widgets import Button
import sys
sys.setrecursionlimit(10000000)
import matplotlib
matplotlib.use('TkAgg')
import matplotlib.pyplot as plt
from matplotlib.widgets import TextBox


####Functions
global counter1, counter2, station_arr
counter1 =0
counter2 =0

def create_dir(dir):
    if not os.path.exists(dir):
        os.makedirs(dir)
    return dir

path_temp_2 = "Results/"
create_dir(path_temp_2)
with open(path_temp_2 + "PGA_Analysis.csv", "a") as csv_file: #this is the file that will store the Detected P-wave time, Detected P value and PGA values of P-waves and S-waves
    writer = csv.writer(csv_file, delimiter=',')
    writer.writerow(["EarthquakeID",	"Station", "Detected P-wave Time",	"Detected P value", "(PGA)P-t" ,"t_value", "(PGA)P-3",	"(PGA)P-5",	"(PGA)P-8"	,"(PGA)-Swave"])



def expand_Waveform(st, start, end, earthquake_batch, station_name):
    st_2 = st.slice(starttime=st[0].stats.starttime + start, endtime=st[0].stats.starttime + end)
    st_2.merge(method=0, fill_value='interpolate', interpolation_samples=st_2[0].stats.sampling_rate)
    total_samples = 0
    array = []
    array_main = []
    for i in range(10 / (end - start)):
        total_samples += st_2[0].stats.npts
        array.append(st_2[0].data)
        print("total_samples", total_samples)
    st_2[0].data = np.concatenate(array)
    st_2[0].stats.npts = total_samples
    st_2.merge(method=0, fill_value='interpolate')
    array_main.append(st_2[0].data)
    array_main.append(st[0].data)
    total_ntps = st_2[0].stats.npts + st[0].stats.npts
    st[0].stats.npts = total_ntps
    st[0].data = np.concatenate(array_main)
    st.filter("bandpass", freqmin=0.1, freqmax=20)
    print (st[0].stats.channel)
    path_temp = "Data_File/Expanded_Data/" + earthquake_batch + "/"
    create_dir(path_temp)
    path_temp_2 = path_temp + "/" +station_name + "/"
    create_dir(path_temp_2)
    filename = path_temp_2 + '/' + st[0].stats.channel +  "_" + "DATA" + ".mseed"
    st[0].write(filename, format="MSEED")



def PGA_value(array_ind, df, X, Y,Z, time_interval):
    PGA_S_value = max( max(np.abs(Y)),max(np.abs(X)))
    y =  array_ind + time_interval * df
    print("array_ind", array_ind)
    print("y", y)
    pga = (max(abs(Z[ int(array_ind):int(y)])))
    return pga, PGA_S_value

def save_PGA_3_sec(event):
    print("saving 3 seconds PGA value" + str(PGA3))
    path_temp_2 = "Results/"
    create_dir(path_temp_2)
    with open(path_temp_2 + "PGA_Analysis.csv", "a") as csv_file:
        writer = csv.writer(csv_file, delimiter=',')
        writer.writerow([ EARTHQUAKE_BATCH, STATION_NAME, str(round( X_COORDINATE,1)), DETECT_P, "N/A", "N/A", PGA3, "N/A", "N/A", PGA_S])
        fig_2 = plt.figure()
        npts = trace.stats.npts
        df = trace.stats.sampling_rate
        t = np.arange(npts, dtype=np.float32) / df
        ax1 = fig_2.add_subplot(311)
        ax1.plot(t, trace.data, 'k')
        # title for the plot
        ax1.set_title(  EARTHQUAKE_BATCH + " " +  STATION_NAME + " " + "Chosen P-wave start and End time: " + str(round(X_COORDINATE, 1)) + "--" + str(round(X_COORDINATE, 1) + 3) + " second")
        ax1.axvline(X_COORDINATE, color='green', lw=2, ls='--', label="P-wave arrival time")
        ax1.axvline(X_COORDINATE + 3, color='red', lw=2, ls='--', label="P-wave window end time")
        print("P-wave window end time", X_COORDINATE + 3)
        ax1.legend(bbox_to_anchor=(1.05, 1), loc=2, borderaxespad=0.)
        ax2 = fig_2.add_subplot(312)
        ax2.plot(t, trace_x.data, 'k')
        ax3 = fig_2.add_subplot(313)
        ax3.plot(t, trace_y.data, 'k')
        fig_2.canvas.draw()
        path_temp = "Results/Pick_3_Sec/"  + str(EARTHQUAKE_BATCH) + "/"
        create_dir(path_temp)
        plt.savefig(path_temp + "Station Name: " + str(STATION_NAME) + "_" + str(EARTHQUAKE_BATCH)+ ".png", bbox_inches='tight' , dpi=900)
        print("saved plot for " + str(STATION_NAME) + " station")
        plt.close()


def save_PGA_5_sec(event):
    print("saving 5 seconds PGA value" + str(PGA5))
    path_temp_2 = "Results/"
    create_dir(path_temp_2)
    with open(path_temp_2 + "PGA_Analysis.csv", "a") as csv_file:
        writer = csv.writer(csv_file, delimiter=',')
        writer.writerow([ EARTHQUAKE_BATCH, STATION_NAME, str(round( X_COORDINATE,1)) , DETECT_P, "N/A", "N/A", "N/A", PGA5,  "N/A", PGA_S])
        fig_2 = plt.figure()
        npts = trace.stats.npts
        df = trace.stats.sampling_rate
        t = np.arange(npts, dtype=np.float32) / df
        ax1 = fig_2.add_subplot(311)
        ax1.plot(t, trace.data, 'k')
        # title for the plot
        ax1.set_title(  EARTHQUAKE_BATCH + " " + STATION_NAME + " " + "Chosen P-wave start and End time: " + str(round(X_COORDINATE, 1)) + "--" + str(round(X_COORDINATE, 1) + 5) + " second")
        ax1.axvline(X_COORDINATE, color='green', lw=2, ls='--', label="P-wave arrival time")
        ax1.axvline(X_COORDINATE + 5, color='red', lw=2, ls='--', label="P-wave window end time")
        print("P-wave window end time", X_COORDINATE + 5)
        ax1.legend(bbox_to_anchor=(1.05, 1), loc=2, borderaxespad=0.)
        ax2 = fig_2.add_subplot(312)
        ax2.plot(t, trace_x.data, 'k')
        ax3 = fig_2.add_subplot(313)
        ax3.plot(t, trace_y.data, 'k')
        fig_2.canvas.draw()
        path_temp = "Results/Pick_5_Sec/" + str(EARTHQUAKE_BATCH) + "/"
        create_dir(path_temp)
        plt.savefig(path_temp+ "Station Name: " + str(STATION_NAME) + "_" + str(EARTHQUAKE_BATCH)  + ".png", bbox_inches='tight' , dpi=900)
        print("saved plot for " + str(STATION_NAME) + " station")
        plt.close()

def save_PGA_8_sec(event):
    print("saving 8 seconds PGA value" + str(PGA8))
    path_temp_2 = "Results/"
    create_dir(path_temp_2)
    with open(path_temp_2 + "PGA_Analysis.csv", "a") as csv_file:
        writer = csv.writer(csv_file, delimiter=',')
        writer.writerow([ EARTHQUAKE_BATCH, STATION_NAME, str(round( X_COORDINATE,1)),  DETECT_P, "N/A", "N/A", "N/A", "N/A", PGA8,  PGA_S])
        fig_2 = plt.figure()
        npts = trace.stats.npts
        df = trace.stats.sampling_rate
        t = np.arange(npts, dtype=np.float32) / df
        ax1 = fig_2.add_subplot(311)
        ax1.plot(t, trace.data, 'k')
        # title for the plot
        ax1.set_title( EARTHQUAKE_BATCH + " " + STATION_NAME + " " + "Chosen P-wave start and End time: " + str(round(X_COORDINATE, 1)) + "--" + str(round(X_COORDINATE, 1) + 8) + " second")
        ax1.axvline(X_COORDINATE, color='green', lw=2, ls='--', label="P-wave arrival time")
        ax1.axvline(X_COORDINATE + 8, color='red', lw=2, ls='--', label="P-wave window end time")
        print("P-wave window end time", X_COORDINATE + 8)
        ax1.legend(bbox_to_anchor=(1.05, 1), loc=2, borderaxespad=0.)
        ax2 = fig_2.add_subplot(312)
        ax2.plot(t, trace_x.data, 'k')
        ax3 = fig_2.add_subplot(313)
        ax3.plot(t, trace_y.data, 'k')
        fig_2.canvas.draw()
        path_temp = "Results/Pick_8_Sec/" + str(EARTHQUAKE_BATCH) + "/"
        create_dir(path_temp)
        plt.savefig(path_temp + "Station Name: " + str(STATION_NAME) + "_" + str(EARTHQUAKE_BATCH) + ".png", bbox_inches='tight' , dpi=900)
        print("saved plot for " + str(STATION_NAME) + " station")
        plt.close()

def save_Error_Message(event):
    print("Saving Error Message")
    path_temp_2 = "Results/"
    create_dir(path_temp_2)
    with open(path_temp_2 + "PGA_Analysis.csv", "a") as csv_file:
        writer = csv.writer(csv_file, delimiter=',')
        writer.writerow([ EARTHQUAKE_BATCH, STATION_NAME, "N/A", "NO EARTHQUAKE REPORTED", "N/A", "N/A", "N/A", "N/A", "N/A", "N/A"])
        fig_2 = plt.figure()
        npts = trace.stats.npts
        df = trace.stats.sampling_rate
        t = np.arange(npts, dtype=np.float32) / df
        ax1 = fig_2.add_subplot(311)
        ax1.plot(t, trace.data, 'k')
        # title for the plot
        ax1.set_title( EARTHQUAKE_BATCH + " " + STATION_NAME + " " + "Error Need to check again")
        ax2 = fig_2.add_subplot(312)
        ax2.plot(t, trace_x.data, 'k')
        ax3 = fig_2.add_subplot(313)
        ax3.plot(t, trace_y.data, 'k')
        fig_2.canvas.draw()
        path_temp = "Results/Error_Data/" + str(EARTHQUAKE_BATCH) + "/"
        create_dir(path_temp)
        plt.savefig(path_temp+ "Station Name: " + str(STATION_NAME) + "_" + str(EARTHQUAKE_BATCH) + ".png", bbox_inches='tight' , dpi=900)
        print("saved plot for " + str(STATION_NAME) + " station")
        plt.close()

def save_NO_DATA_Message(event):
    print("Saving NO DATA Message")
    path_temp_2 = "Results/"
    create_dir(path_temp_2)
    with open(path_temp_2 + "PGA_Analysis.csv", "a") as csv_file:
        writer = csv.writer(csv_file, delimiter=',')
        writer.writerow([ EARTHQUAKE_BATCH, STATION_NAME, "N/A", "NO DATA", "N/A", "N/A", "N/A", "N/A", "N/A", "N/A"])
        fig_2 = plt.figure()
        npts = trace.stats.npts
        df = trace.stats.sampling_rate
        t = np.arange(npts, dtype=np.float32) / df
        ax1 = fig_2.add_subplot(311)
        ax1.plot(t, trace.data, 'k')
        # title for the plot
        ax1.set_title( EARTHQUAKE_BATCH + " " + STATION_NAME + " " + "No Earthquake detected")
        ax2 = fig_2.add_subplot(312)
        ax2.plot(t, trace_x.data, 'k')
        ax3 = fig_2.add_subplot(313)
        ax3.plot(t, trace_y.data, 'k')
        fig_2.canvas.draw()
        path_temp = "Results/No_Data/" + str(EARTHQUAKE_BATCH) + "/"
        create_dir(path_temp)
        plt.savefig(path_temp + "Station Name: " + str(STATION_NAME) + "_" + str(EARTHQUAKE_BATCH) + ".png", bbox_inches='tight' , dpi=900)
        print("saved plot for " + str(STATION_NAME) + " station")
        plt.close()



def close_plot(event):
    global counter1, station_arr
    global counter2
    global max_limit
    plt.close()
    counter1 = counter1 + 1
    if counter1 == max_limit:
        print("All the plots have been closed")
        counter2 = counter2 + 1
        station_arr = runner(earthquake_arr[counter2])
        max_limit = len(station_arr)
        counter1 = 0

    plot_first(earthquake_arr[counter2], station_arr[counter1])



def calc_average_P_val(trace, indice, length):
    sum = 0
    print("array_ind", int(indice))
    print("y_calcl_P", int(indice+length))
    for x in range( int(indice), int(indice+length)):
        sum = sum + abs(trace[x])
    return sum/length


def submit(text):
    global trace, df, trace_x, trace_y, trace_z, ydata, PGA_T
    ydata = float(text)
    print("ydata", ydata)
    df = trace.stats.sampling_rate
    if(ydata != 0):
        print("ydata", ydata)
        PGA_T = PGA_value( float(round( X_COORDINATE,1)) *df , df, trace_x, trace_y, trace, ydata)
        print("X_COORDINATE", X_COORDINATE)
        PGA_T = PGA_T[0]
        print("saving PGA value for " + str(ydata) + " seconds: " + str(PGA_T))
        path_temp_2 = "Results/"
        create_dir(path_temp_2)
        with open(path_temp_2 + "PGA_Analysis.csv", "a") as csv_file:
            writer = csv.writer(csv_file, delimiter=',')
            print("PGA value saved")
            writer.writerow([EARTHQUAKE_BATCH, STATION_NAME, str(round( X_COORDINATE,1)), DETECT_P, PGA_T, ydata, "N/A", "N/A", "N/A", PGA_S])
            fig = plt.figure()
            npts = trace.stats.npts
            t = np.arange(npts, dtype=np.float32) / df
            ax1 = fig.add_subplot(311)
            ax1.plot(t, trace.data, 'k')
            #title for the plot
            ax1.set_title(  EARTHQUAKE_BATCH + " " + STATION_NAME + " " + "Chosen P-wave start and End time: " + str(round( X_COORDINATE,1)) + "--"+ str(round( X_COORDINATE,1) + ydata) + " second")
            ax1.axvline(X_COORDINATE, color='green', lw=2, ls='--', label="P-wave arrival time")
            ax1.axvline(X_COORDINATE + ydata, color='red', lw=2, ls='--', label="P-wave window end time")
            ax1.legend(bbox_to_anchor=(1.05, 1), loc=2, borderaxespad=0.)
            ax2 = fig.add_subplot(312)
            ax2.plot(t, trace_x.data, 'k')
            ax3 = fig.add_subplot(313)
            ax3.plot(t, trace_y.data, 'k')
            fig.canvas.draw()
            path_temp = "Results/Pick_T_Sec/" + str(EARTHQUAKE_BATCH) + "/"
            create_dir(path_temp)
            plt.savefig(path_temp + "Station Name: " + str(STATION_NAME) + "_" + str(EARTHQUAKE_BATCH)  + ".png", bbox_inches='tight' , dpi=900)
            print("saved plot for " + str(STATION_NAME) + " station")
            fig.clf()
            #plt.close()

def submit_2(text):
    global ST, ST1, ST2, STATION_NAME, EARTHQUAKE_BATCH
    times = text.split(",")
    start = int(times[0])
    end = int(times[1])
    print("start", start)
    print("end", end)
    expand_Waveform(ST, start, end, EARTHQUAKE_BATCH, STATION_NAME)
    expand_Waveform(ST1, start, end, EARTHQUAKE_BATCH, STATION_NAME)
    expand_Waveform(ST2, start, end, EARTHQUAKE_BATCH, STATION_NAME)


# Global references for the figure and buttons
global fig, buttons


def onpick(event):
    global X_COORDINATE, PGA3, PGA5, PGA8, PGA_S, DETECT_P, INPUT_TIME, fig, buttons
    print("A point has been selected")
    print("value:", event.mouseevent.xdata)
    X_COORDINATE = event.mouseevent.xdata

    # Initialize or clear the existing figure rather than closing it
    if 'fig' in globals():
        fig.clf()  # Clear the current figure
        plt.close()
    else:
        fig = plt.figure()
    fig = plt.figure(figsize=(20, 10))  # Width, Height in inches
    df = trace.stats.sampling_rate
    npts = trace.stats.npts
    t = np.arange(npts, dtype=np.float32) / df

    ax1 = fig.add_subplot(311)
    ax1.plot(t, trace.data, 'k')
    ax1.axvline(X_COORDINATE, color='green', lw=2, ls='--', label="P-wave arrival time")
    ax1.axvline(X_COORDINATE + 3, color='gold', lw=2, ls='--', label="3 sec frame")
    ax1.axvline(X_COORDINATE + 5, color='orange', lw=2, ls='--', label="5 sec frame")
    ax1.axvline(X_COORDINATE + 8, color='brown', lw=2, ls='--', label="8 sec frame")
    ax1.legend(bbox_to_anchor=(1.05, 1), loc=2, borderaxespad=0.)

    # Create or redefine buttons
    buttons = []
    axcut = plt.axes([0.3, 0.0, 0.05, 0.05])
    bcut = Button(axcut, '3', color='cyan', hovercolor='green')
    buttons.append(bcut)
    axcut_2 = plt.axes([0.4, 0.0, 0.05, 0.05])
    bcut_2 = Button(axcut_2, '5', color='cyan', hovercolor='green')
    buttons.append(bcut_2)
    axcut_3 = plt.axes([0.5, 0.0, 0.05, 0.05])
    bcut_3 = Button(axcut_3, '8', color='cyan', hovercolor='green')
    buttons.append(bcut_3)
    axcut_4 = plt.axes([0.6, 0.0, 0.05, 0.05])
    bcut_4 = Button(axcut_4, 'Error', color='cyan', hovercolor='green')
    buttons.append(bcut_4)
    axcut_5 = plt.axes([0.7, 0.0, 0.05, 0.05])
    bcut_5 = Button(axcut_5, 'NO DATA', color='cyan', hovercolor='green')
    buttons.append(bcut_5)
    axcut_6 = plt.axes([0.8, 0.0, 0.05, 0.05])
    bcut_6 = Button(axcut_6, 'Next', color='red', hovercolor='green')
    buttons.append(bcut_6)

    # Connect button events
    bcut.on_clicked(save_PGA_3_sec)
    bcut_2.on_clicked(save_PGA_5_sec)
    bcut_3.on_clicked(save_PGA_8_sec)
    bcut_4.on_clicked(save_Error_Message)
    bcut_5.on_clicked(save_NO_DATA_Message)
    bcut_6.on_clicked(close_plot)

    ax2 = fig.add_subplot(312)
    ax2.plot(t, trace_x.data, 'k')
    ax3 = fig.add_subplot(313)
    ax3.plot(t, trace_y.data, 'k')


    axbox_7 = plt.axes([0.9, 0.0, 0.05, 0.05])
    text_box = TextBox(axbox_7, 'P-wave Length ', initial='0' )
    text_box.label.set_fontsize(12)  # Adjust the font size as needed
    text_box.label.set_weight('bold')
    #put the lavel on top of the text box

    text_box.on_submit(submit)
    #this is for the start value for the expander
    axbox_8 = plt.axes([0.05, 0.0, 0.03, 0.05])
    text_box_2 = TextBox(axbox_8, 'Noise Length ', initial='0')
    text_box_2.label.set_fontsize(12)  # Adjust the font size as needed
    text_box_2.label.set_weight('bold')
    text_box_2.on_submit(submit_2)

    props = dict(boxstyle='round', facecolor='wheat', alpha=0.5)
    ax3.text(0.05, 0.95, str(round( X_COORDINATE,1)) , transform=ax3.transAxes, fontsize=14, verticalalignment='top', bbox=props)
    print ("P-wave arrival time: " + str( round( X_COORDINATE,1)))
    DETECT_P = calc_average_P_val(trace.data, float((round( X_COORDINATE,1) )*df ), 50)

    PGA_3 = PGA_value( float(round( X_COORDINATE,1) *df ), df, trace_x, trace_y, trace, 3)
    PGA3 = PGA_3[0]
    PGA_S = PGA_3[1]
    PGA_5 = PGA_value( float(round( X_COORDINATE,1) *df ),  df, trace_x, trace_y, trace, 5)
    PGA5 = PGA_5[0]
    PGA_8 = PGA_value( float(round( X_COORDINATE,1) *df ), df, trace_x, trace_y, trace, 8)
    PGA8 = PGA_8[0]
    plt.show()

global directory_1, max_limit
directory_1 = "Data_File/"


def plot_first(earthquake_val, station_name):
    global fig
    directory_2 = "/Data_File/" + str(earthquake_val) + "/"
        #for filename in os.listdir(directory_2):
    global trace, trace_x, trace_y, STATION_NAME, EARTHQUAKE_BATCH, ST, ST1, ST2
    filename = station_name
    if (os.path.exists(directory_2 + filename + '/' + 'HNZ-DATA.mseed') == True):
        st = read(directory_2 + filename + '/' + 'HNZ-DATA.mseed')
        st1 = read(directory_2 + filename + '/' + 'HNE-DATA.mseed')
        st2 = read(directory_2 + filename + '/' + 'HNN-DATA.mseed')
    else:
        st = read(directory_2 + filename + '/' + 'BNZ-DATA.mseed')
        st1 = read(directory_2 + filename + '/' + 'BNE-DATA.mseed')
        st2 = read(directory_2 + filename + '/' + 'BNN-DATA.mseed')

    ST = st
    ST1 = st1
    ST2 = st2
    st.filter("bandpass", freqmin=0.1, freqmax=20)
    st1.filter("bandpass", freqmin=0.1, freqmax=20)
    st2.filter("bandpass", freqmin=0.1, freqmax=20)
    st.detrend(type='demean')
    st1.detrend(type='demean')
    st2.detrend(type='demean')

    trace = st[0]
    trace_x = st1[0]
    trace_y = st2[0]
    EARTHQUAKE_BATCH = earthquake_val
    STATION_NAME = trace.stats.station
    df = trace.stats.sampling_rate
    npts = trace.stats.npts
    t = np.arange(npts, dtype=np.float32) / df
    fig = plt.figure(figsize=(20, 10))
    fig.canvas.mpl_connect('pick_event', onpick)
    ax1 = fig.add_subplot(311)
    ax1.plot(t, trace.data, picker=True, pickradius = 100, color='k')
    #title plot

    ax1.set_title("Z-component  " + str(trace.stats.station) + "  " +earthquake_val)
    ax2 = fig.add_subplot(312)
    npts_x = trace_x.stats.npts
    df_x = trace_x.stats.sampling_rate
    t_x = np.arange(npts_x, dtype=np.float32) / df_x
    ax2.plot(t_x, trace_x.data, 'k')
    ax2.set_title("X-component")
    ax3 = fig.add_subplot(313)
    npts_y = trace_y.stats.npts
    df_y = trace_y.stats.sampling_rate
    t_y = np.arange(npts_y, dtype=np.float32) / df_y
    ax3.plot(t_y, trace_y.data, 'k')
    ax3.set_title("Y-component")
    plt.show()


def runner(earthquake):
    STATION_ARRAY = []
    for filename in os.listdir("Data_File/" + earthquake + '/'): #change the directory to the directory where the earthquake data is stored
        if not filename.startswith('.'):
            STATION_ARRAY.append(filename)
    return STATION_ARRAY

def runner_list():
    EARTHQUAKE_ARRAY = []
    for filename in os.listdir("Data_File/"): #change the directory to the directory where the earthquake data is stored, this should contain the folders of various earthquake data
        if not filename.startswith('.') :
            EARTHQUAKE_ARRAY.append(filename)
    return EARTHQUAKE_ARRAY

def main():
    global max_limit
    global station_arr, earthquake_arr
    global counter1, counter2
    EARTHQUAKE_ARRAY = runner_list()
    earthquake_arr = EARTHQUAKE_ARRAY
    print(len(earthquake_arr))
    station_arr = runner(earthquake_arr[counter2])
    print(station_arr)
    max_limit = len(station_arr)
    plot_first(earthquake_arr[counter2], station_arr[counter1])



if __name__ == "__main__":
    main()

