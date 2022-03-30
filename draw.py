import pathlib
from py_project import py_original

root_folder = pathlib.Path(__file__).resolve().parent
sm_folder = root_folder.parent.joinpath("data").joinpath("SM-1")
util_folder = root_folder.joinpath("util")
out_folder = root_folder.joinpath("png")

# sta = ['9C14', '9B42', '9A4B', '9A27', '9C64', '9C94', '9CA4', 'B03A', 'B053']
sta = ['9C14']

args = [sta, 2012, 2013]
py_original.draw_original(sm_folder, util_folder, args, out_folder, _format='png', cover='y')
