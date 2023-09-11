#!/usr/bin/env python3

import bz2
import cmagic
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

file_handler = logging.FileHandler(filename="tmp.log")
stdout_handler = logging.StreamHandler(stream=sys.stdout)
handlers = [file_handler, stdout_handler]

logging.basicConfig(
    level=logging.DEBUG,
    format="[%(asctime)s] {%(filename)s:" +
           "%(lineno)d} %(levelname)s - %(message)s",
    handlers=handlers,
)

logger = logging.getLogger(__name__)
log = logger

MIN_INSPECT = 30  # Nr of bytes to use for magic fingerprinting.

PATH_NOT_IN_INDEX = "Requested path not found"  # Duc's friendly error msg.
DUC_MAGIC_STORE = os.path.expanduser(
    "~/.duc_magic.db"
)  # Store output here for now, no questions asked.

DUC_BINARY = "/usr/bin/duc"  # Path to installed duc.
# Parameters to pass to duc. (apparent size, show bytes, recursion, show full_path)
DUC_PARAMS = "ls -a -b -R --full-path"

cmagic = cmagic.Magic(no_check_compress=True,
                      mime_encoding=False,
                      mime_type=True)
cmagic.load()

USEAGE = """Usage: ducmagic [options] [args]

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

Use 'ducmagic help --all' for a complete list of all options for all subcommands."""


def get_file_type(file_path) -> str:
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
        return magic_out, magic_bytes


def get_duc_info(file_path: str) -> str:
    # cmd = f'/usr/bin/duc ls -a -b -R --full-path {file_path}'
    cmd = f"{DUC_BINARY} {DUC_PARAMS} {file_path}"
    proc = subprocess.Popen(
        cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE, shell=True
    )
    output, err = proc.communicate()

    if err:
        if err.decode().startswith(PATH_NOT_IN_INDEX):
            sys.stdout.write(PATH_NOT_IN_INDEX + "\n")
            sys.exit(-1)
        else:
            sys.stdout.write(err.decode())
            sys.exit(-1)

    return output.decode()


def remove_small_files(duc_info: str, base_path: str) -> (set, set):
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
    with multiprocessing.Pool(5) as pool:
        file_types = pool.map(get_file_type, wanted)
    return file_types


def cli() -> any:
    cmd_list = ["-h", "--help", "index", "ls"]

    if len(sys.argv) == 1:  # No cmd g:
        sys.exit(-1)

    if not sys.argv[1] in cmd_list:
        print(USEAGE)
        sys.exit(-1)

    if sys.argv[1] == "index":
        if len(sys.argv) >= 2:
            do_index(sys.argv[2:])
        else:
            do_index()

    if sys.argv[1] == "ls":
        if len(sys.argv) >= 2:
            do_ls(sys.argv[2:])
        else:
            do_ls()


def do_ls(path: str) -> any:
    if not os.path.isfile(DUC_MAGIC_STORE):
        sys.stdout.write(
            f"Unable to read ducmagic db {DUC_MAGIC_STORE}\n Could not ls, no data no ls."
        )

    log.debug(f"Trying to read {DUC_MAGIC_STORE}..")
    if log.level == logging.DEBUG:
        st = time.time()
    try:
        with open(DUC_MAGIC_STORE, "rb") as fh:
            with bz2.open(fh) as d:
                res = pickle.load(d)
    except Exception as error:
        log.error(f"{error.strerror}")
        sys.exit(-1)

    if log.level == logger.DEBUG:
        log.debug(f"Done reading {DUC_MAGIC_STORE} in {time.time() - st} seconds.")

    if not res.get(path):
        res[path] = {}

        duc_info = get_duc_info(path)
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
    else:
        print("Noting todo magic is there!!")


def do_index(path: str) -> any:
    if os.path.isfile(DUC_MAGIC_STORE):
        log.debug(f"Trying to read {DUC_MAGIC_STORE}..")
        if log.level == logger.DEBUG:
            st = time.time()
        try:
            with open(DUC_MAGIC_STORE, "rb") as fh:
                with bz2.open(fh) as d:
                    res = pickle.load(d)
        except Exception as error:
            log.error(f"{error.strerror}")
            sys.exit(-1)
        if log.level == logger.DEBUG:
            log.debug(f"Reading {DUC_MAGIC_STORE} in {time.time() - st} seconds.")
    else:
        log.debug(f"No ducmagic db found at {DUC_MAGIC_STORE}")
        res = {}

    if not res.get(path):
        res[path] = {}

        duc_info = get_duc_info(path)
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
    else:
        print("Noting todo magic is there!!")


if __name__ == "__main__":
    cli()
