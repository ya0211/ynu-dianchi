import os
import linecache
import pathlib
import matplotlib.pyplot as plt
import numpy as np
from py_project import log


class _Year:
    def __init__(self, sm, args):
        """
        GetDataOfYear
        """
        self._sm = sm
        self._sta, self._start, self._stop, self._line = args

    def get_hourly_data(self, file_dir_day: str):
        """
        Get the data of the required line as the hourly peak, returns the median of 24 data as the day's value
        """
        Z_pow = []

        for hour in range(0, 24):
            hour = "%02d" % hour
            file_dir_hour = str(file_dir_day) + '/' + str(hour)
            if os.path.exists(file_dir_hour):
                file_name = file_dir_hour + '/' + str(os.listdir(file_dir_hour)[0])
                z_pow = linecache.getline(file_name, self._line)[9:19]
                if z_pow != '':
                    Z_pow.append(float(z_pow))
        Z_pow = sorted(Z_pow)
        return Z_pow[int(len(Z_pow) / 2)]

    def get_yearly_data(self):
        """
        Get the peak value for each day of the year
        """
        all_data = []
        file_dir_sta = self._sm.joinpath(self._sta)

        for year in range(self._start, self._stop + 1):
            year_data = []
            file_dir_year = file_dir_sta.joinpath(str(year))
            if os.path.exists(file_dir_year):
                for day in range(1, 367):
                    day = "%03d" % day
                    file_dir_day = str(file_dir_year) + '/' + str(day)
                    if os.path.exists(file_dir_day):

                        msg = "{0}.{1}.{2}".format(self._sta, year, day)
                        log.i("get_yearly_data", msg)

                        media = self.get_hourly_data(file_dir_day)
                        year_data.append(str(int(day)) + ',' + str(media))
                    else:

                        msg = "No such file or directory: {0}".format(file_dir_day)
                        log.w("get_yearly_data", msg)

            all_data.append(year_data)

        return all_data


def get_dependent_data(file_dir):
    day, data = [[], []]

    with open(file_dir, 'r') as file:
        file_data = file.readlines()
    for i in range(0, len(file_data)):
        day.append(float(file_data[i].split(' ')[0]))
        data.append(float(file_data[i].split(' ')[1].replace('\n', '')))

    return day, data


def draw_yearly_image(data_plot: list, dep_file_dir: pathlib.Path, out_file_dir: pathlib.Path, args: list, display='n'):
    """
    Drawing images by the library matplotlib.pyplot
    """

    y_min, y_max = args

    x_ticks = [15, 45, 80, 110, 140, 170, 200, 235, 265, 295, 325, 355]
    x_ticks_label = ['Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun', 'Jul', 'Aug', 'Sep', 'Oct', 'Nov', 'Dec']

    x, y = [[], []]
    for i in range(0, len(data_plot)):
        x.append(float(data_plot[i].split(',')[0]))
        y.append(float(data_plot[i].split(',')[1]))

    plt.figure(figsize=(9, 11))
    plt.subplots_adjust(hspace=0.1)

    plt.subplot(3, 1, 1)
    plt.title(str(out_file_dir).split('/')[-1])
    plt.xlim(1, 366)
    plt.xticks(x_ticks, [])
    plt.ylim(y_min, y_max)
    plt.yticks(np.arange(y_min, y_max+1, 5))
    plt.plot(x, y, color='black', linewidth=0.8)
    plt.ylabel('1−sec Power (dB)')

    plt.subplot(3, 1, 2)
    plt.xlim(1, 366)
    plt.xticks(x_ticks, [])
    plt.ylim(0, 4)
    plt.yticks(np.arange(0, 5, 1))
    x, y = get_dependent_data(dep_file_dir.joinpath("wind.8110.jinning"))
    plt.plot(x, y, color='black', linewidth=0.8)
    plt.ylabel('Avg wind speed (m/s)')

    plt.subplot(3, 1, 3)
    plt.xlim(1, 366)
    plt.xticks(x_ticks, x_ticks_label)
    plt.ylim(0, 10)
    plt.yticks(np.arange(0, 11, 2))
    x, y = get_dependent_data(dep_file_dir.joinpath("rain.jinning"))
    plt.plot(x, y, color='black', linewidth=0.8)
    plt.ylabel('Rain (mm)')

    _format = str(out_file_dir).split('.')[-1]
    plt.savefig(out_file_dir, format=_format)
    if display == 'y':
        plt.show()
    else:
        plt.close()


def get_yearly_data(sm: pathlib.Path, args: list):
    return _Year(sm, args).get_yearly_data()
