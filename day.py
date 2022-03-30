import os
import pathlib
from py_project import py_daily

root_folder = pathlib.Path(__file__).resolve().parent
sm_folder = root_folder.parent.joinpath("data").joinpath("SM-1")
wind_folder = root_folder.joinpath("km2016")
out_folder = root_folder.joinpath("day_pdf")

if not os.path.exists(out_folder):
    os.mkdir(out_folder)
for day in range(1, 367):
    args = ['9A4B', 2013, day]
    py_daily.draw_daily(sm_folder, wind_folder, args, out_folder, _format='pdf')
