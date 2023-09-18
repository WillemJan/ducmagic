#!/usr/bin/env python3

import bz2
import datetime
import gc
import logging
import mmap
import multiprocessing
import os
import pickle
import stat
import subprocess
import sys
import time
import doctest

import cmagic

try:
    from helper import setup_logger
except ImportError:
    from .helper import setup_logger

from pprint import pprint

MIN_INSPECT = 30  # Nr of bytes to use for magic fingerprinting.

PATH_NOT_IN_INDEX = "Requested path not found"  # Duc's friendly error msg.

DUC_MAGIC_STORE = os.path.expanduser(
    "~/.duc_magic.db"
)  # Store output here for now, no questions asked.

DUC_BINARY = "/usr/bin/duc"  # Path to installed duc.
# Parameters to pass to duc.
# (apparent size, show bytes, recursion, show full_path)

DUC_PARAMS = "ls -a -b -R --full-path"


cmagic = cmagic.Magic(no_check_compress=True,
                      mime_encoding=False,
                      mime_type=True)
cmagic.load()


log = setup_logger()

USAGE = '''Usage: ducmagic [options] [args]

Available subcommands:

  help      : Show help
  index     : Scan the filesystem and generate the Duc index
  info      : Dump database info
  ls        : List sizes of directory

Global options:
  -h,  --help                show help
       --version             output version information and exit

Use 'ducmagic help <subcommand>' or 'ducmagic <subcommand> -h' for a complete list of all
options and detailed description of the subcommand.

Use 'ducmagic help --all' for a complete list of all options for all subcommands.
'''


def get_file_type(file_path) -> str:
    '''
    Returns the magic of a given file.
            Parameters:
                    file_path (str): Path to examine.

            Returns:
                    magic_out (str): Magic type. (eg. Text/html).
                    magic_bytes (bytes): The first X bytes from the entry.

    This function runs without seat-belts so it might crash,
    this is on purpose for now.

    >>> f = [f for f in os.listdir('.') if os.path.isfile(f)]
    >>> len(get_file_type(f)) > 0
    True
    '''

    global cmagic

    file_path = file_path[0]

    st = os.lstat(file_path)
    ftype = stat.S_IFMT(st.st_mode)

    if ftype == stat.S_IFLNK:
        return "Link", ""
    if ftype == stat.S_IFDIR:
        return "Dir", ""

    with open(file_path, "rb") as f:
        mm = mmap.mmap(f.fileno(), 0, access=mmap.ACCESS_READ)
        magic_bytes = mm.read(MIN_INSPECT)
        magic_out = cmagic.guess_bytes(magic_bytes)
        # I'm not sure why I pass on the actual bytes here.
        # maybe for futher inspection? The mind is a mystery.
        return magic_out, magic_bytes


def do_cmd(cmd: str) -> str:
    '''
    Returns the output of a shell command.

            Parameters:
                    cmd (str): The command to execute.

            Returns:
                    output (str): The result from the shell command.

    On error (stderr) this command halts the running code.

    >>> do_cmd('ls ' + __file__).find(__file__) > -1
    True
    '''
    proc = subprocess.Popen(
        cmd,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        shell=True
    )
    output, err = proc.communicate()

    if err:
        if err.decode().startswith(PATH_NOT_IN_INDEX):
            # todo: continue, but invoke duc.
            # log.error(f'Error: {file_path} not in duc db.')
            sys.exit(-1)
        else:
            log.error(err.decode())
            sys.exit(-1)

    return output.decode()


def get_duc_info() -> str:
    '''
    Returns info on the current duc db.

            Parameters:
                    None

            Returns:
                    output (str): see man duc(1) section info.

    >>> len(get_duc_info()) > 0
    True
    '''
    cmd = f"{DUC_BINARY} info"
    return do_cmd(cmd)


def get_duc_path(file_path: str) -> str:
    '''
    Returns contents of duc db for given path.

            Parameters:
                    file_path (str): Path to get from duc db.

            Returns:
                    output (str): see man duc(1) section ls.

    >>> len(get_duc_path('.')) > 0
    True
    '''
    cmd = f"{DUC_BINARY} {DUC_PARAMS} {file_path}"
    return do_cmd(cmd)


def remove_small_files(duc_info: str, base_path: str) -> (set, set):
    '''
    Split duc ls entries into < MIN_INSPECT and > MIN_INSPECT sets,
    otherwise mmap(read) will fail due to lack of bytes.

            Parameters:
                    duc_info (str): Output of the duc ls command.

            Returns:
                    wanted (set): Set of files that need magic.
                    unwanted (set): Set of files that do not need magic.
    '''
    wanted, unwanted = set(), set()

    for line in duc_info.splitlines():
        line = line.strip()
        fsize = int(line.split(" ")[0])
        fname = line[len(str(fsize)) + 1:]

        if fsize < MIN_INSPECT:
            unwanted.add((fname, fsize))
            continue

        wanted.add((base_path + os.sep + fname, fsize))

    return wanted, unwanted


def get_file_types(wanted: set) -> list:
    '''
    Invoke multicore to quickly get the magic fingerprints.

        Parameters:
                wanted (set): Set of entries to process.

        Returns:
                list of file types using magic.

    '''
    with multiprocessing.Pool() as pool:
        file_types = pool.map(get_file_type, wanted)
    return file_types


def cli(args=sys.argv) -> any:
    '''
    Command Line Interface.
    '''
    cmd_list = ["-h", "--help", "index", "ls", "info", "--test"]

    if len(sys.argv) == 1:
        print("No argument given.")
        print(USAGE)
        sys.exit(-1)

    if not sys.argv[1] in cmd_list:
        print(f"Error, {sys.argv[1]} not a known argument.")
        print(USAGE)
        sys.exit(-1)

    if sys.argv[1] == "info":
        do_info()
        sys.exit(0)

    if sys.argv[1] == "--help":
        print(USAGE)
        sys.exit(0)

    if sys.argv[1] == "index":
        if len(sys.argv) >= 2:
            res = load_ducmagic()
            for d in sys.argv[2:]:
                d = os.path.abspath(os.path.expanduser(d))
                res = do_index(d, res)
        else:
            res = load_ducmagic()
            d = os.getcwd()
            res = do_index(d, res)

    ls_res = []
    if sys.argv[1] == "ls":
        res = load_ducmagic()
        if len(sys.argv[2:]) > 0:
            for d in sys.argv[2:]:
                d = os.path.abspath(os.path.expanduser(d))
                ls_res.append(do_ls(d, res))
        else:
            d = os.path.abspath(os.getcwd())
            ls_res.append(do_ls(d, res))


def load_ducmagic() -> dict:
    '''
    Load the (compressed) ducmagic db from disk,
    defaults to ~/.duc_magic.db

        Parameters:
                None

        Returns:
                Decompressed ducmagic database as dict.

    '''
    if not os.path.isfile(DUC_MAGIC_STORE):
        log.warn(f"Ducmagic db {DUC_MAGIC_STORE} empty.\n")
        return {}

    log.debug(f"Trying to read {DUC_MAGIC_STORE}.")
    if log.level == logging.DEBUG:
        st = time.time()
    with open(DUC_MAGIC_STORE, "rb") as fh:
        with bz2.open(fh) as d:
            res = pickle.load(d)
    if log.level == logging.DEBUG:
        log.debug(
            f"Read {DUC_MAGIC_STORE} in {time.time() - st} sec.")
    return res


def do_info():
    if os.path.isfile(DUC_MAGIC_STORE):
        # todo: work with timestamps in ducmagic db.
        m_time = os.path.getmtime(DUC_MAGIC_STORE)
        dt_m = str(datetime.datetime.fromtimestamp(m_time))
        log.info(f'Modified on: {dt_m}')
        res = load_ducmagic()
        for p in res.keys():
            log.info(f'Path found: {p}')
        for line in get_duc_info().splitlines():
            print(line)
    else:
        log.info(f"Ducmagic db {DUC_MAGIC_STORE} empty.\n")


def do_ls(path: str, res: dict) -> dict:
    if not res:
        res = load_ducmagic()

    if path not in res:
        print(f'{path} not found in {DUC_MAGIC_STORE}, \
              run ducmagic index {path} first.')
        return {}

    pprint(res.get(path))
    return res.get(path)


def do_index(path: str, res: dict) -> dict:
    if os.path.isfile(DUC_MAGIC_STORE):
        res = load_ducmagic()
    else:
        log.debug(f"No ducmagic db found at {DUC_MAGIC_STORE}")
        if not res:
            res = {}

    if not res.get(path):
        res[path] = {}
    else:
        log.debug(f"Re-indexing {path}")
        res[path] = {}

    duc_info = get_duc_path(path)
    wanted, unwanted = remove_small_files(duc_info, path)
    file_types = get_file_types(wanted)

    for file_path, file_type in zip(wanted, file_types):
        ftype = file_type[0]
        if ftype not in res[path]:
            res[path][ftype] = [file_path]
        else:
            res[path][ftype].append(file_path)

    log.debug(f"Trying to write out ducmagic db at {DUC_MAGIC_STORE}")
    gc.disable()

    try:
        gc.collect()
        with bz2.open(DUC_MAGIC_STORE, "wb") as fh:
            pickle.dump(res, fh)
    except Exception as error:
        log.error(f"{error.strerror}")
        log.fatal(f"Error while writing to {DUC_MAGIC_STORE}")
        sys.exit(-1)
    finally:
        gc.enable()

    return res


if __name__ == '__main__':
    doctest.testmod(verbose=True)
