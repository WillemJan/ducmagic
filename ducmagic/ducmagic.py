#!/usr/bin/env python3

"""
ducmagic.py
"""

import bz2
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

from pprint import pprint
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
  index     : Scan the filesystem and generate the Ducmagic index
  info      : Dump database info
  ls        : List sizes of directory

  sync      : Sync ducmagic with duc

Global options:
  -h,  --help                show help
       --version             output version information and exit
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
        log.debug("Ducmagic db %s empty.", DUC_MAGIC_STORE)
        return {}

    if log.level == logging.DEBUG:
        log.debug("Trying to read %s.", DUC_MAGIC_STORE)
        start_time = time.time()

    with open(DUC_MAGIC_STORE, "rb") as file_handle:
        with bz2.open(file_handle) as data:
            try:
                res = pickle.load(data)
            except Exception as error:
                log.fatal("Error while reading %s", DUC_MAGIC_STORE)
                raise error

    if log.level == logging.DEBUG:
        log.debug(
            "Read %s in %f sec.", DUC_MAGIC_STORE,
            time.time() - start_time)
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

    file_path = file_path[0]

    try:
        file_stat = os.lstat(file_path)
    except PermissionError:
        return "None", ""
    except FileNotFoundError:
        return "None", ""

    ftype = stat.S_IFMT(file_stat.st_mode)

    if ftype == stat.S_IFLNK:
        return "Link", ""
    if ftype == stat.S_IFDIR:
        return "Dir", ""

    try:
        with open(file_path, "rb") as file_handle:
            memmap = mmap.mmap(file_handle.fileno(), 0, access=mmap.ACCESS_READ)
            magic_bytes = memmap.read(MIN_INSPECT)
            magic_out = cmagic.guess_bytes(magic_bytes)
            # I'm not sure why I pass on the actual bytes here.
            # maybe for futher inspection? The mind is a mystery.
            return magic_out, magic_bytes
    except IOError as error:
        return "None", ""


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


def do_info() -> None:
    '''
    do_info

    '''

    m_time = ""
    if os.path.isfile(DUC_MAGIC_STORE):
        m_time = os.path.getmtime(DUC_MAGIC_STORE)

    return m_time


def do_ls_backoff(res: dict,
                  path: str = None,
                  backoff_path: str = None) -> dict:

    '''
    do_ls_backoff.

    When / is indexed and you are in /home/me,
    ducmagic ls has to figure out that /home/me is indexed as /.
    '''

    # Try to backoff the given path.
    res1 = {backoff_path: {}}
    for f_type in list(res[backoff_path]):
        for (f_name, f_size) in res[backoff_path][f_type]:
            if f_name.startswith(path):
                if f_type not in res1[backoff_path]:
                    res1[backoff_path][f_type] = [(f_name, f_size)]
                else:
                    res1[backoff_path][f_type].append((f_name, f_size))

    return res1


def do_ls(path: str, res: dict = None) -> dict:
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

    if res is None:
        res = {}

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
        log.fatal('%s not in ducmagic db, run ducmagic .', path)
        return {path: {}}

    backoff = do_ls_backoff(res, path, backoff_path)
    backoff = backoff.get(backoff_path)
    pprint(backoff)
    return backoff


def do_index(path: str, res: dict = None) -> dict:
    '''
    do_index:
    '''

    if res is None:
        res = {}

    if os.path.isfile(DUC_MAGIC_STORE):
        res = load_ducmagic()

    if not res.get(path):
        res[path] = {}
    else:
        log.debug("Re-indexing %s", path)
        res[path] = {}

    duc_info = get_duc_path(path)
    wanted, _ = remove_small_files(duc_info, path)
    file_types = get_file_types(wanted)

    for file_path, file_type in zip(wanted, file_types):
        ftype = file_type[0]
        fpath, fsize = file_path
        if ftype in ['Dir', 'Link', 'None']:
            fsize = 0
        if ftype not in res[path]:
            res[path][ftype] = [(fpath, fsize)]
        else:
            res[path][ftype].append((fpath, fsize))

    if not res[path]:
        return {}

    log.debug("Trying to write out ducmagic db at %s",
              DUC_MAGIC_STORE)

    gc.disable()

    try:
        gc.collect()
        with bz2.open(DUC_MAGIC_STORE, "wb") as file_handle:
            pickle.dump(res, file_handle)
    except pickle.UnpicklingError as error:
        raise error
    finally:
        gc.enable()

    log.debug("Write out ducmagic to %s completed.",
              DUC_MAGIC_STORE)

    return res


def cli_handle_index(sane: list, args: list) -> None:
    '''
    cli_handle_index
    '''

    if sane[0] <= 1:
        log.fatal('Duc db is empty, run: duc index .')
        sys.exit(-1)

    if len(args) >= 2:
        result = load_ducmagic()
        for path in args[2:]:
            path = os.path.abspath(os.path.expanduser(path))
            do_index(path, result)
    else:
        result = load_ducmagic()
        path = os.getcwd()
        do_index(path, result)


def cli_handle_ls(sane: list, args: list) -> None:
    '''
    cli_handle_ls
    '''
    if not sane[1]:
        log.fatal('Ducmagic db is empty, run: ducmagic index .')
        sys.exit(-1)

    res = load_ducmagic()

    if len(args[2:]) > 0:
        for path in args[2:]:
            path = os.path.abspath(os.path.expanduser(path))
            do_ls(path, res)
    else:
        path = os.path.abspath(os.getcwd())
        do_ls(path, res)


def cli(args=None) -> any:
    '''
    cli:

    Command Line Interface.

    Takes in errors from users,
    and tries to make the best of it.
    '''

    if args is None:
        args = sys.argv

    cmd_list = ["-h", "--help", "index",
                "ls", "info", "--test"]

    if len(args) == 1:
        log.fatal("No argument given.")
        print(USAGE)
        sys.exit(-1)

    if not args[1] in cmd_list:
        log.fatal("Error, %s not a known argument.", args[1])
        print(USAGE)
        sys.exit(-1)

    if args[1] == "info":
        do_info()
        sys.exit(0)

    if args[1] == "--help":
        print(USAGE)
        sys.exit(0)

    sane = do_is_sane()

    if args[1] == "index":
        cli_handle_index(sane, args)

    if args[1] == "ls":
        cli_handle_ls(sane, args)


if __name__ == '__main__':
    doctest.testmod(verbose=True)
