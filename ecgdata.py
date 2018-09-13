import numpy as np
import bitarray
import matplotlib.pyplot as plt
# parser and visualizer for PhysioBank ATM // MIT-BIH Arrhythmia Database (mitdb)
# based on exporting db files into nice csv format with:
# ./rdsamp -r mitdb/100 -c -H -f 40 -t 100 -v -pd > samples_mitdb_100.csv
# given the signal in csv format: diplay it with animations in matplotlib.


"""
=========================
Simple animation examples
=========================

This example contains two animations. The first is a random walk plot. The
second is an image animation.
"""
import datetime as dt
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.animation as animation

sample_path = r'C:\Users\Barak\wfdb-10.6.0\convert\samples101.csv'
ttl_number_of_samples = 21602 #360 * 10
XLIM_REAL = 1

def read_ecg(path=sample_path):
    f = open(path, 'rt')
    ch1_arr, ch2_arr = np.zeros(ttl_number_of_samples), np.zeros(ttl_number_of_samples)
    time_arr = np.zeros(ttl_number_of_samples)
    i, j = 0, 0
    start_time = None
    f.readline()
    f.readline()
    for r in f:
        time, ch1, ch2 = r.split(',')
        ptime = dt.datetime.strptime(time.replace("'",''), '%M:%S.%f')
        ch1, ch2 = float(ch1), float(ch2)
        ch1_arr[i] = ch1
        ch2_arr[i] = ch2
        if i == 0:
            time_arr[i] = 0.0
            start_time = ptime
        else:
            time_arr[i] = (ptime - start_time).total_seconds()
        if j % 300 != 3:
            i += 1
    return time_arr, ch1_arr, ch2_arr

time_arr, ch1_arr, ch2_arr = read_ecg()
data = np.array([time_arr, ch1_arr])
cur_x_start_ind = 0
cur_x_start_val = 0.0

def update_line(num, data, line):
    global cur_x_start_ind, cur_x_start_val
    print(num, line.get_data())
    if (data[0,num-1] > XLIM_REAL):
        cur_x_start_ind += 1
        cur_x_start_val = data[0,cur_x_start_ind] # relating to this as first one.
    line.set_data(data[0,cur_x_start_ind:num]-cur_x_start_val, data[1,cur_x_start_ind:num])
    return line,

fig1 = plt.figure()
'''
data[0,0] = time_0 
data[1,0] = volume_0
data[0,1] = time_1
data[1,1] = volume_1
data[0,2] = time_2
data[1,2] = volume_2
'''

l, = plt.plot([], [], 'r-', linewidth=5)
plt.xlim(0, XLIM_REAL)
plt.ylim(-3, 3)
plt.ylabel('mV')
plt.xlabel('time')
plt.title('ECG')
line_ani = animation.FuncAnimation(fig1, update_line, len(time_arr), fargs=(data, l),
                                   interval=1, blit=True)
# To save the animation, use the command: line_ani.save('lines.mp4')
plt.show()