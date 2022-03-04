import pandas as pd
from matplotlib import pyplot as plt

path = '/Users/ryszard/Downloads/DANE Z WYCISKANIA 24.02.2022_1.xlsx'
points = []

''' mouse click event to get x value of the points'''
def on_pick(event):
    line = event.artist
    xdata, ydata = line.get_data()
    ind = event.ind[0]
    points.append(xdata[ind])
    print(points)

''' get file content into pandas dataframe, convert datetime to str for simplicity'''
def file_reader(path):
    df = pd.read_excel(path, header=0, names=['time','F', 'T','v','pos'])
    df['time'] = df['time'].astype(str)
    df['time'] = df['time'].str[11:]
    return df

df = file_reader(path)
fig, ax = plt.subplots()
ax.plot(df['time'],df['F'], 'o', markersize=1, c='black', picker=1)
cid = fig.canvas.mpl_connect('pick_event', on_pick)
plt.xticks([])
plt.show()

#points = ['09:56:00.000', '10:01:08.000', '10:05:39.000', '10:08:16.000', '10:08:30.000', '10:10:22.000', '10:10:34.000', '10:12:13.000', '10:14:09.000', '10:15:53.000', '10:19:31.000', '10:23:08.000', '10:46:58.001', '10:50:08.001', '10:53:20.001', '10:55:02.001', '10:55:09.001', '10:57:57.001', '11:03:39.001', '11:06:21.001', '11:06:29.001', '11:07:56.001', '11:08:05.001', '11:09:53.001', '11:10:01.001', '11:18:14.001', '11:33:02.001', '11:35:18.001', '11:35:24.001', '11:37:02.001', '11:39:36.001', '11:42:02.001', '11:43:49.001', '11:52:28.002']
colors = ['black','red','blue']

for i in range(0,len(points),2):
    try:
        df_filtered = df[(df['time'] >= points[i]) & (df['time'] <= points[i+1])]
        fig1, ax1 = plt.subplots()
        fig1.subplots_adjust(right=0.75)
        twin1 = ax1.twinx()
        twin2 = ax1.twinx()
        twin2.spines['right'].set_position(('axes', 1.2))
        #ax1.plot(df_filtered['time'], df_filtered['F'], 'o', markersize=2, c='black', label=colors[0],alpha=0.5)
        #twin1.plot(df_filtered['time'], df_filtered['T'], 's', markersize=2, c='red', label=colors[1],alpha=0.5)
        #twin2.plot(df_filtered['time'], df_filtered['v'], '*', markersize=2, c='blue', label=colors[2],alpha=0.5)
        ax1.plot(df_filtered['pos'], df_filtered['F'], linewidth=1, c='black', label=colors[0],alpha=0.5)
        twin1.plot(df_filtered['pos'], df_filtered['T'], linewidth=1, c='red', label=colors[1],alpha=0.5)
        twin2.plot(df_filtered['pos'], df_filtered['v'], linewidth=1, c='blue', label=colors[2],alpha=0.5)
        ax1.set_xlabel('pos')
        ax1.set_ylabel("force")
        twin1.set_ylabel("temp")
        twin2.set_ylabel("velocity")
        ax1.tick_params(axis='y', colors=colors[0])
        plt.xlim(left=0, right=700)
        twin1.tick_params(axis='y', colors=colors[1])
        twin2.tick_params(axis='y', colors=colors[2])
        ax1.yaxis.label.set_color(colors[0])
        twin1.yaxis.label.set_color(colors[1])
        twin2.yaxis.label.set_color(colors[2])
        ax1.set_ylim(bottom = 0, top=max(df['F']*1.1))
        twin1.set_ylim(bottom=0, top=max(df['T']*1.1))
        twin2.set_ylim(bottom=0, top=max(df['v']*1.1))
        #plt.xticks([])
        plt.grid(which='both', color='gray', linewidth=0.5, alpha=0.3)
        plt.minorticks_on()
        plt.savefig('/Users/ryszard/Downloads/wykresy/pos_' + str(i) + '.png', dpi=300)
        #plt.show()
        plt.close()
    except IndexError:
        points.pop()

#plt.show()