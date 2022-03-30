import os
import pathlib
import linecache
import numpy as np
import matplotlib.pyplot as plt
from py_project import log


class _Daily:
    def __init__(self, sm, wind, args, _format, display):
        """
        DrawDataOfDay
        """
        self._sm = sm
        self._wind = wind
        self._sta, self._year, self._day = args
        self._display = display
        self._format = _format

    @staticmethod
    def color24(hour: int):
        colors = ['lightgreen', 'forestgreen', 'limegreen',
                  'green', 'lime', 'seagreen',
                  'mediumseagreen', 'springgreen', 'mediumaquamarine',
                  'aquamarine', 'turquoise', 'lightseagreen',
                  'mediumturquoise', 'darkslategray', 'darkcyan',
                  'cyan', 'aqua', 'darkturquoise',
                  'cadetblue', 'lightblue', 'deepskyblue',
                  'lightskyblue', 'steelblue', 'dodgerblue']
        return colors[hour]

    def get_wind_data(self):
        hours, data = [[], []]
        file_dir = self._wind.joinpath("km.{0}.wind".format(self._day))

        if os.path.exists(file_dir):
            with open(file_dir, 'r') as file:
                file_data = file.readlines()
            for i in range(0, len(file_data)):
                hours.append(float(file_data[i].split(' ')[0]))
                data.append(float(file_data[i].split(' ')[1].replace('\n', '')))

            return hours, data
        else:

            msg = "No such file or directory: {0}".format(file_dir)
            log.w("get_wind_data", msg)

            return None

    def draw_daily_image(self, out_file_dir):
        """
        Get data for the required date (eg: 2012.50) then drawing images with the help of the library matplotlib.pyplot
        """

        file_dir_year = self._sm.joinpath(str(self._sta)).joinpath(str(self._year))
        day = "%03d" % self._day
        file_dir_day = file_dir_year.joinpath(str(day))

        if not os.path.exists(file_dir_day):

            msg = "No such file or directory: {0}".format(file_dir_day)
            log.w("draw_daily_image", msg)

        else:

            msg = "{0}.{1}.{2}".format(self._sta, self._year, day)
            log.i("draw_daily_image", msg)

            plt.figure(figsize=(12, 6))
            plt.subplot(1, 2, 1)
            for hour in range(0, 24):
                hour = "%02d" % hour
                file_dir_hour = str(file_dir_day) + '/' + str(hour)
                if os.path.exists(file_dir_hour):
                    file_name = file_dir_hour + '/' + str(os.listdir(file_dir_hour)[0])
                    if linecache.getline(file_name, 2)[0:8] != '':
                        freq, z_pow = [[], []]
                        for line in range(126, 187):
                            _freq = linecache.getline(file_name, line)[0:8]
                            if _freq == '':
                                msg = "{0}: Missing data since {1} Hz".format(
                                    file_name.split('/')[-1], linecache.getline(file_name, line - 1)[0:8].lstrip())
                                log.w("draw_daily_image", msg)

                                break

                            freq.append(1 / float(_freq))
                            z_pow.append(float(linecache.getline(file_name, line)[9:19]) + 4.0 * float(hour))

                        plt.plot(freq, z_pow, color=self.color24(int(hour)))
                        if int(hour) in range(0, 24, 3):
                            plt.annotate(str(hour), (freq[31], z_pow[31]), size=10, color='black', weight='bold')

                        freq.clear()
                        z_pow.clear()

                    else:
                        msg = "{0} is empty".format(file_name.split('/')[-1])
                        log.w("draw_daily_image", msg)

            plt.subplots_adjust(wspace=0, left=0.1, right=0.9)
            plt.title(self._sta + '.' + str(self._year) + '.' + str(self._day) + '.' + self._format)
            plt.xscale('log')
            plt.xlabel('Freq (s)')
            plt.xticks([0.5, 0.6, 1.0, 1.5, 2.0], [0.5, 0.6, 1.0, 1.5, 2.0])
            plt.ylabel('Power (dB)')
            plt.yticks([-40, -60, -80, -100, -120, -140], [])

            if self.get_wind_data() is not None:
                y1, x1 = self.get_wind_data()
                x1 = np.array(x1)
                y1 = np.array(y1)
                rect2 = [0.55, 0.11, 0.08, 0.77]
                ax2 = plt.axes(rect2)
                ax2.plot(x1, y1, color='dodgerblue')
                plt.ylim(-2, 28)
                plt.yticks(np.arange(0, 24, 3))
                plt.ylabel('Hour')
                plt.xlabel('Avg wind speed (m/s)')

            out_file_dir = out_file_dir.joinpath(self._sta).joinpath(str(self._year))
            if not os.path.exists(out_file_dir):
                os.makedirs(out_file_dir)
            out_file = out_file_dir.joinpath(
                self._sta + '.' + str(self._year) + '.' + str(self._day) + '.' + self._format)
            plt.savefig(out_file, format=self._format)

            if self._display == 'y':
                plt.show()
            else:
                plt.close()


def draw_daily(sm: pathlib.Path, wind: pathlib.Path, args: list, out: pathlib.Path,
               _format='pdf', display='n'):
    return _Daily(sm, wind, args, _format, display).draw_daily_image(out)
