import datetime


def i(tag: str, msg: str):
    print("\033[01;36m", end='')
    print("{0}: {1}".format(tag, msg), end='')
    print("\n\033[0m", end='')


def w(tag: str, msg: str):
    print("\033[01;31m", end='')
    print("{0}: {1}".format(tag, msg), end='')
    print("\n\033[0m", end='')


def write(tag: str, msg: str, log_file):
    time = str(datetime.datetime.now())
    with open(log_file, 'w') as file:
        file.write("{0}:    ".format(time))
        file.write("{0}: {1}".format(tag, msg))
        file.write('\n')

