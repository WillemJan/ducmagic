#!/usr/bin/env python3

import os
import sys

import gc
import pickle

import stat
import mmap

import json

import multiprocessing
import subprocess

import bz2
import cmagic

import argparse


MIN_INSPECT = 30 # Nr of bytes to use for magic fingerprinting.
PATH_NOT_IN_INDEX = 'Requested path not found' # Duc's friendly error msg.
DUC_MAGIC_STORE = os.path.expanduser("~/.duc_magic.db") # Store output here for now, no questions asked.

cmagic = cmagic.Magic(no_check_compress=True,
                      mime_encoding=False,
                      mime_type=True)
cmagic.load()

def get_file_type(file_path) -> str:
    global cmagic

    file_path = file_path[0]

    st = os.lstat(file_path)
    ftype = stat.S_IFMT(st.st_mode)

    if ftype == stat.S_IFLNK:
        return 'Link', ""
    if ftype == stat.S_IFDIR:
        return 'Dir', ""

    with open(file_path, "rb") as f:
        mm = mmap.mmap(f.fileno(), 0, access=mmap.ACCESS_READ)
        magic_bytes = mm.read(MIN_INSPECT)
        magic_out = cmagic.guess_bytes(magic_bytes)
        return magic_out, magic_bytes

def get_duc_info(file_path: str) -> str:
    cmd = f'/usr/bin/duc ls -a -b -R --full-path {file_path}'
    proc = subprocess.Popen(cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE, shell=True)
    output, err = proc.communicate()

    if err:
        if err.decode().startswith(PATH_NOT_IN_INDEX):
            sys.stdout.write(PATH_NOT_IN_INDEX + '\n')
            sys.exit(-1)
        else:
            sys.stdout.write(err.decode())
            sys.exit(-1)

    return output.decode()

def remove_small_files(duc_info: str, base_path: str) -> (set, set):
    wanted, unwanted = set(), set()

    for line in duc_info.splitlines():
        line = line.strip()
        fsize = int(line.split(' ')[0])
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
    parser = argparse.ArgumentParser(description="A command line tool for managing Ducmagic indexes")

    subparsers = parser.add_subparsers(title="Commands", dest="cmd")

    # Help subcommand
    help_parser = subparsers.add_parser("help", help="Show help")

    # Index subcommand
    index_parser = subparsers.add_parser("index", help="Scan the filesystem and generate the Ducmagic index")

    # Info subcommand
    info_parser = subparsers.add_parser("info", help="Dump database info")

    # Ls subcommand
    ls_parser = subparsers.add_parser("ls", help="List sizes and magic of directory")

    # XML subcommand
    xml_parser = subparsers.add_parser("xml", help="Dump XML output")

    # Global options
    parser.add_argument("--debug", action="store_true", help="increase verbosity to debug level")
    parser.add_argument("-q", "--quiet", action="store_true", help="quiet mode, do not print any warning")
    parser.add_argument("-v", "--verbose", action="store_true", help="increase verbosity")
    parser.add_argument("--version", action="store_true", help="output version information and exit")

    args = parser.parse_args()

    if args.cmd is None:
        parser.print_help()
        exit(1)

    if args.cmd == "help":
        if args.subcommand is None:
            parser.print_help()
            exit(1)

        getattr(parser.subparsers, args.subcommand).print_help()
        exit(0)



def main() -> any:
    print(args)
    path = '/home/aloha/code/'

    with open(DUC_MAGIC_STORE, 'rb') as fh:
        with bz2.open(fh) as d:
            res = pickle.load(d)

    if not res.get(path):
        res = {}
        res[path] = {}

        duc_info = get_duc_info(path)
        wanted, unwanted = remove_small_files(duc_info, path)
        file_types = get_file_types(wanted)

        for file_path, file_type in zip(wanted, file_types):
            ftype = file_type[0]
            if not ftype in res[path]:
                res[path][ftype] = [file_path]
            else:
                res[path][ftype].append(file_path)


        gc.disable()
        try:
            gc.collect()
            with bz2.open(DUC_MAGIC_STORE, "wb") as fh:
                pickle.dump(res, fh)
        finally:
            gc.enable()

    #from pprint import pprint
    #pprint(len(res.get(path)))

if __name__ == "__main__":
    main()
