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
def plotter(df, x, y):
    fig, ax = plt.subplots()
    ax.plot(df[x],df[y], 'o', markersize=1, picker=3)
    cid = fig.canvas.mpl_connect('pick_event', on_pick)
    plt.tight_layout()
    plt.grid(which='both', color='gray', linewidth=0.5, alpha=0.5)
    plt.minorticks_on()
    plt.ylim(bottom=-10, top=570)
    #plt.xlim(left=0, right=20)
    #plt.xlabel('Strain [%]')
    #plt.ylabel('Stress [MPa]')
    return None


 ### 34 clicksy
df = file_reader(path)
plotter(df,'time','F')
plt.show()

for i in range(len(points)):
    try:
        df_filtered = df[(df['time'] >= points[i]) & (df['time'] <= points[i+1])]
        i += 1
        plotter(df_filtered,'time','F')
        #plt.plot(df_filtered['time'],df_filtered['F'], 'o', markersize=1, c='black')
        #plt.savefig('/Users/ryszard/Downloads/wykresy/' + )
        #plt.show()
    except IndexError:
        points.pop()

plt.show()