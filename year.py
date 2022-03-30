import os
import pathlib
from py_project import py_yearly


root_folder = pathlib.Path(__file__).resolve().parent
sm_folder = root_folder.parent.joinpath("data").joinpath("SM-1")
dep_folder = root_folder.joinpath("dep")
out_folder = root_folder.joinpath("year_pdf")

args = ['9C14', 2012, 2013, 156]

data = py_yearly.get_yearly_data(sm_folder, args)

if not os.path.exists(out_folder):
    os.mkdir(out_folder)
for i in range(0, len(data)):
    file_out = out_folder.joinpath(args[0] + '.' + str(args[1] + i) + '.pdf')
    py_yearly.draw_yearly_image(data[i], dep_folder, file_out, args=[-150, -110], display='n')



sta = ['9A4B', '9A27', '9B42', '9C64', '9C94', '9CA4', 'B03A', 'B053']
for s in sta:
    args = [s, 2012, 2013, 156]

    data = py_yearly.get_yearly_data(sm_folder, args)

    if not os.path.exists(out_folder):
        os.mkdir(out_folder)
    for i in range(0, len(data)):
        file_out = out_folder.joinpath(args[0] + '.' + str(args[1] + i) + '.pdf')
        py_yearly.draw_yearly_image(data[i], dep_folder, file_out, args=[-160, -130], display='n')


"""
9A4B = [-160, -130], 2012-2013
9A27 = [-160, -130], 2012-2013
9B42 = [-160, -130], 2013
9C14 = [-150, -110], 2012
9C64 = [-160, -130], 2013
9C94 = [-160, -130], 2012-2013
9CA4 = [-160, -130], 2013
B03A = [-160, -130], 2013
B053 = [-160, -130], 2012-2013
"""
