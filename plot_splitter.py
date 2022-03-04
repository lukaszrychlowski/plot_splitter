import pandas as pd
from matplotlib import pyplot as plt

path = '/Users/ryszard/Downloads/DANE Z WYCISKANIA 24.02.2022.xlsx'
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
    df = pd.read_excel(path,header=0, names=['time','F', 'T','v','pos'])
    df['time'] = df['time'].astype(str)
    df['time'] = df['time'].str[11:]
    return df

''' plot with mouse event implemented '''
def plotter_general(df, x, y, color):
    fig, ax = plt.subplots()
    ax.plot(df[x],df[y], linewidth=1, c=color, picker=3)
    cid = fig.canvas.mpl_connect('pick_event', on_pick)
    return None

def plotter_splitted(df,x,y1,y2,y3):
    fig, ax = plt.subplots()
    twin1 = ax.twinx()
    twin2 = ax.twinx()
    twin2.spines['right'].set_position(("axes", 1.2))
    plot1 = ax.plot(x, y1, 'o', markersize=1, c='black')
    plot2 = twin1.plot(x, y2, 'o', markersize=1, c='red')
    plot3 = twin2.plot(x, y3, 'o', markersize=1, c='blue')
    ax.set_xlabel(x)
    ax.set_ylabel(y1)
    twin1.set_ylabel(y2)
    twin2.set_ylabel(y3)
    ax.yaxis.label.set_color('black')
    twin1.yaxis.label.set_color('red')
    twin2.yaxis.label.set_color('blue')
    #ax.legend()

 ### 34 clicksy
df = file_reader(path)
plotter_general(df,'time','F', 'black')
plt.show()

for i in range(len(points)):
    try:
        df_filtered = df[(df['time'] >= points[i]) & (df['time'] <= points[i+1])]
        i += 1
        fig1, ax1 = plt.subplots()
        fig1.subplots_adjust(right=0.75)
        twin1 = ax1.twinx()
        twin2 = ax1.twinx()
        twin2.spines['right'].set_position(('axes', 1.2))
        ax1.plot(df_filtered['time'], df_filtered['F'], 'o', markersize=3, c='black', label='force')
        twin1.plot(df_filtered['time'], df_filtered['T'], 's', markersize=3, c='red', label='temp')
        twin2.plot(df_filtered['time'], df_filtered['v'], '*', markersize=3, c='blue', label='velocity')
        ax1.set_xlabel('time')
        ax1.set_ylabel("force")
        twin1.set_ylabel("temp")
        twin2.set_ylabel("velocity")
        ax1.tick_params(axis='y', colors='black')
        twin1.tick_params(axis='y', colors='red')
        twin2.tick_params(axis='y', colors='blue')
        plt.savefig('/Users/ryszard/Downloads/wykresy/' + str(i) + '.png', dpi=300)
        plt.show()
        plt.close()
    except IndexError:
        points.pop()

#plt.show()