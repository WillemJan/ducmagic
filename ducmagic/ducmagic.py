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
import sys
import time
import doctest
from collections import Counter

import cmagic

try:
    from helper import do_cmd, \
                       E_DATABASE_NOT_FOUND, \
                       log
except ImportError:
    from .helper import do_cmd, \
                        E_DATABASE_NOT_FOUND, \
                        log

from pprint import pprint

MIN_INSPECT = 30  # Nr of bytes to use for magic fingerprinting.

DUC_MAGIC_STORE = os.path.expanduser(
    "~/.duc_magic.db"
)  # Store output here for now, no questions asked.

DUC_BINARY = "/usr/bin/duc"  # Path to installed duc.
DUC_STORE = os.path.expanduser('~/.duc.db')

# Parameters to pass to duc.
# For now, will only work with ~/.duc.db.
# (apparent size, show bytes, recursion, show full_path)
DUC_PARAMS = f"ls -d {DUC_STORE} -a -b -R --full-path"

cmagic = cmagic.Magic(no_check_compress=True,
                      mime_encoding=False,
                      mime_type=True)
cmagic.load()

USAGE = '''Usage: ducmagic [options] [args]

Available subcommands:

  help      : Show help
  index     : Scan the filesystem and generate the Duc index
  info      : Dump database info
  ls        : List sizes of directory
  sync      : Sync ducmagic with duc

Global options:
  -h,  --help                show help
       --version             output version information and exit

Use 'ducmagic help <subcommand>' or 'ducmagic <subcommand> -h' for a complete list of all
options and detailed description of the subcommand.

Use 'ducmagic help --all' for a complete list of all options for all subcommands.
'''


def get_duc_info() -> str:
    r'''
    Returns info on the current duc db.

        Parameters:
            None

        Returns:
            output (str): See man duc(1) section info.

    >>> len(get_duc_info()) >= 0
    True
    '''

    cmd = f"{DUC_BINARY} info"
    return do_cmd(cmd)


def do_duc_info(duc_out: str = get_duc_info()) -> list:
    r'''
    Get's the command line output of duc info,
    and parses it to computer readable form.

    >>> duc_out="Date       Time       Files    Dirs    Size Path\n"
    >>> duc_out+="2023-09-21 08:24:12     199     134    1.5M "
    >>> duc_out+="/home/aloha/code/ducmagic"
    >>> res = do_duc_info(duc_out)
    >>> res[0][-1]
    '/home/aloha/code/ducmagic'
    '''

    index = []

    for line in duc_out.splitlines()[1:]:
        duc_info = line.split()
        index.append(duc_info)

    return index


def do_is_sane() -> tuple[int, int]:
    '''
    We refuse to directly communicate with the linkable .so from the
    upstream duc procject, so at startup we must make sure we are sane.
    Als preform some internal check to make sure it is possible to exec
    an index or ls call at all.

        Parameters:
                None

        Returns:
            duc_ok (int):
                    -1 Duc missing.
                    0 Duc found.
                    1 Duc found, duc db found.
                    2 Duc found, duc info is avail,
                                 and contains at least one path.

             ducmagic_ok (bool):
                     False Ducmagic db not found.
                     True Ducmagic db is available.
    '''

    duc_ok = -1
    if os.path.isfile(DUC_BINARY):
        duc_ok += 1
        if os.path.isfile(DUC_STORE):
            print(DUC_STORE)
            duc_ok += 1
    if duc_ok == 1:
        if do_duc_info():
            duc_ok += 1

    ducmagic_ok = False
    if os.path.isfile(DUC_MAGIC_STORE):
        ducmagic_ok = True

    return (duc_ok, ducmagic_ok)


def load_ducmagic() -> dict:
    '''
    Load the (compressed) ducmagic db from disk,
    defaults to ~/.duc_magic.db

        Parameters:
            None

        Returns:
            results(dict): Decompressed ducmagic file as dict,
                           or emprty dict.
    '''

    if not os.path.isfile(DUC_MAGIC_STORE):
        log.debug(f"Ducmagic db {DUC_MAGIC_STORE} empty.\n")
        return {}

    if log.level == logging.DEBUG:
        log.debug(f"Trying to read {DUC_MAGIC_STORE}.")
        st = time.time()

    with open(DUC_MAGIC_STORE, "rb") as fh:
        with bz2.open(fh) as d:
            try:
                res = pickle.load(d)
            except Exception as error:
                log.error(f"{error}")
                log.fatal(f"Error while reading {DUC_MAGIC_STORE}")
                sys.exit(-1)

    if log.level == logging.DEBUG:
        log.debug(
            f"Read {DUC_MAGIC_STORE} in {time.time() - st} sec.")
    return res


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


def get_duc_path(file_path: str) -> str:
    '''
    Returns contents of duc db for given path.

        Parameters:
            file_path (str): Path to get from duc db.

        Returns:
            output (str): See man duc(1) section ls.

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

        if line == E_DATABASE_NOT_FOUND:
            continue

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
            file_types (list): List of file types using magic.
    '''

    with multiprocessing.Pool() as pool:
        file_types = pool.map(get_file_type, wanted)

    return file_types


def do_sync():
    '''
    Load the duc db from disk, get all indexed paths,
    compare this to what is available within ducmagcic db,
    add missing entries.
    '''

    # Get all db's from current duc db.
    # TODO
    return


def do_info() -> None:
    if os.path.isfile(DUC_MAGIC_STORE):
        # todo: work with timestamps in ducmagic db.
        m_time = os.path.getmtime(DUC_MAGIC_STORE)
        dt_m = str(datetime.datetime.fromtimestamp(m_time))
        log.info(f'Modified on: {dt_m}')
        res = load_ducmagic()
        for p in res.keys():
            log.info(f'Path found: {p}')
        for line in get_duc_info().splitlines():
            # TODO
            print(line)
    else:
        log.info(f"Ducmagic db {DUC_MAGIC_STORE} empty.\n")


def do_ls_filter(type_str: str, res: dict = {}) -> dict:
    '''
    Implement content filter here.
    '''

    return {}


def do_ls(path: str, res: dict = {}) -> dict:
    '''
    Preform the ls function on the magic db.
    Returns dict containing types and list of file-name and file-size.

        Parameters:
            path(str): Path to preform the ducmagic ls on.
            res(dict): Current in-mem db for ducmagic.

        Returns:
            results(dict): Per file-type contains list of files and file-size.

    For now this function also does the repr().
    '''

    if not res:
        res = load_ducmagic()

    path = os.path.abspath(os.path.expanduser(path))

    roots = sorted([i for i in list(res.keys())
                    if len(i) <= len(path)],
                   key=len,
                   reverse=True)

    if path in roots:
        pprint(res.get(path))
        return res.get(path)

    backoff_path = path

    for i in range(Counter(path).get(os.path.sep)):
        backoff_path = os.path.sep.join(backoff_path.split(os.path.sep)[:-1])
        if backoff_path in roots:
            break

    if not backoff_path:
        # Path not in index.
        log.fatal(f'{path} not in ducmagic db, run ducmagic .')
        return {path: {}}

    # Try to backoff the given path.
    res1 = {backoff_path: {}}
    for f_type in list(res[backoff_path]):
        for (f_name, f_size) in res[backoff_path][f_type]:
            if f_name.startswith(path):
                if f_type not in res1[backoff_path]:
                    res1[backoff_path][f_type] = [(f_name, f_size)]
                else:
                    res1[backoff_path][f_type].append((f_name, f_size))

    pprint(res1.get(backoff_path))
    return res1


def do_index(path: str, res: dict = {}) -> dict:
    '''

    '''
    if os.path.isfile(DUC_MAGIC_STORE):
        res = load_ducmagic()

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
        fpath, fsize = file_path
        if ftype in ['Dir', 'Link']:
            fsize = 0
        if ftype not in res[path]:
            res[path][ftype] = [(fpath, fsize)]
        else:
            res[path][ftype].append((fpath, fsize))

    if not res[path]:
        return {}

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

    log.debug(f"Write out ducmagic to {DUC_MAGIC_STORE} completed.")
    return res


def cli(args=sys.argv) -> any:
    '''
    Command Line Interface.

    Takes in errors from users,
    and tries to make the best of it.
    '''

    cmd_list = ["-h", "--help", "index",
                "ls", "info", "--test"]

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

    sane = do_is_sane()

    if sys.argv[1] == "index":
        if sane[0] <= 1:
            print('Duc db is empty, run: duc index.')
            sys.exit(-1)

        if len(sys.argv) >= 2:
            res = load_ducmagic()
            for d in sys.argv[2:]:
                d = os.path.abspath(os.path.expanduser(d))
                res = do_index(d, res)
        else:
            res = load_ducmagic()
            d = os.getcwd()
            res = do_index(d)

    ls_res = []
    if sys.argv[1] == "ls":
        if not sane[1]:
            print('Ducmagic db is empty, run: ducmagic index.')
            sys.exit(-1)

        res = load_ducmagic()
        if len(sys.argv[2:]) > 0:
            for d in sys.argv[2:]:
                d = os.path.abspath(os.path.expanduser(d))
                ls_res.append(do_ls(d, res))
        else:
            d = os.path.abspath(os.getcwd())
            ls_res.append(do_ls(d, res))


if __name__ == '__main__':
    doctest.testmod(verbose=True)
