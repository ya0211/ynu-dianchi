import os
import linecache
import pathlib
import numpy as np
import matplotlib.pyplot as plt
from py_project import log


class _Original:
    def __init__(self, sm, util, args, _format, display):
        """
        DrawDataOfOriginal
        """
        self._sm = sm
        self._util = util
        self._sta, self._start, self._stop = args
        self._display = display
        self._format = _format

    def get_limit_data(self, file_name: str):
        """
        Get the upper and lower limit data of the graph
        """
        x, y = [[], []]

        with open(str(self._util) + '/' + file_name, 'r') as file:
            file_data = file.readlines()
        for i in range(0, len(file_data)):
            row_1, row_2, row_3 = file_data[i].split(' ')
            x.append(float(row_1))
            y.append(float(row_2) + float(row_3.replace('\n', '')) * np.log(float(row_1)) / 2.3026)

        return x, y

    def draw_daily_image(self, file_dir_day: str, out_file_prefix: str, out_file_dir: str, cover: str):
        """
         Get data for the required date (eg: 2012.50) then drawing images with the help of the library matplotlib.pyplot
        """
        for hour in range(0, 24):
            hour = "%02d" % hour
            file_dir_hour = file_dir_day + '/' + str(hour)
            if os.path.exists(file_dir_hour):
                file_name = file_dir_hour + '/' + str(os.listdir(file_dir_hour)[0])

                out_file_name = out_file_prefix + '.' + str(hour) + '.' + self._format

                if cover == 'n':
                    if os.path.exists(out_file_dir + '/' + out_file_name):
                        break

                freq, z_pow = [[], []]
                for line in range(2, 297):
                    if linecache.getline(file_name, line)[0:8] != '':
                        freq.append(1 / float(linecache.getline(file_name, line)[0:8]))
                        z_pow.append(float(linecache.getline(file_name, line)[9:19]))
                    else:

                        if line == 2:
                            msg = "{0} is empty".format(file_name.split('/')[-1])
                            log.w("draw_hourly_image", msg)
                        else:
                            msg = "{0}: Missing data since {1} Hz".format(
                                file_name.split('/')[-1], linecache.getline(file_name, line - 1)[0:8].lstrip())
                            log.w("draw_hourly_image", msg)

                        break

                x_ticks = [0.1, 1, 10, 100]
                plt.figure(figsize=(9, 9))
                plt.title(out_file_name)

                plt.xscale('log')
                plt.xlim(0.05, 120)
                plt.xticks(x_ticks, x_ticks)
                plt.ylim(-200, -80)
                plt.yticks(np.arange(-200, -79, 20))

                plt.plot(freq, z_pow, color='black', linewidth=0.8)
                plt.xlabel('Period (s)')
                plt.ylabel('BHZ Power (db)')

                x, y = self.get_limit_data('pet.high')
                plt.plot(x, y, color='red')
                x, y = self.get_limit_data('pet.low')
                plt.plot(x, y, color='red')

                plt.savefig(out_file_dir + '/' + out_file_name, format=self._format)
                if self._display == 'y':
                    plt.show()
                else:
                    plt.close()

    def draw_all_data(self, out_dir: pathlib.Path, cover: str):
        for sta in self._sta:
            for year in range(self._start, self._stop + 1):
                file_dir_year = str(self._sm) + '/' + sta + '/' + str(year)
                if os.path.exists(file_dir_year):
                    for day in range(1, 367):
                        day = "%03d" % day
                        file_dir_day = str(file_dir_year) + '/' + (str(day))
                        if os.path.exists(file_dir_day):
                            out_file_prefix = sta + '.' + str(year) + '.' + str(day)

                            log.i("draw_all_data", out_file_prefix)

                            out_file_dir = str(out_dir) + '/' + out_file_prefix.replace(".", "/")

                            if not os.path.exists(out_file_dir):
                                os.makedirs(out_file_dir)
                            self.draw_daily_image(file_dir_day, out_file_prefix, out_file_dir, cover)
                        else:

                            msg = "No such file or directory: {0}".format(file_dir_day)
                            log.w("draw_all_data", msg)


def draw_original(sm: pathlib.Path, util: pathlib.Path, args: list, out_dir: pathlib.Path,
                  cover='y', _format='pdf', display='n'):
    return _Original(sm, util, args, _format, display).draw_all_data(out_dir, cover)
