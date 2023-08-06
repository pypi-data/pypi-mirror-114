#!/usr/bin/env python3
#coding:utf-8
import os
import sys
import argparse
import shutil

example_str = """Example:
# build the codes in given folder inside a new folder and ignore `run.py`
python %(prog)s.py --folder path/to/python/source/folder --ignore run.py
# build the codes in given folder inplace and ignore `run.py`
python %(prog)s.py --folder path/to/python/source/folder --inplace --ignore run.py
# build the codes in given folder inside a new folder using given python interpreter
python %(prog)s.py --folder path/to/python/source/folder --ignore run.py --python /path/to/custom/python
# build the codes in given folder inside a new folder, but ignore any prebuilt files
python %(prog)s.py --folder path/to/python/source/folder --ignore run.py --build_mode new
"""

template = """#coding:utf-8
import os
import glob
import time
import shutil
from distutils.core import setup
from Cython.Build import cythonize

folder_list = ["{build_path}"]
py_list = []

ignored_files = ["{build_path}/setup.py"]
for file in "{ignore}".strip().split(','):
    ignored_files.append(os.path.join("{build_path}", file))

if "{cache_file}":
    unmodified_files = []
    with open("{cache_file}", "r") as f:
        for line in f:
            filename, t = line.split(',')
            if int(t) == int(os.path.getmtime(filename)):
                unmodified_files.append(filename)
    ignored_files.extend(unmodified_files)

while len(folder_list) > 0:
    current_folder = folder_list.pop(0)
    py_files = glob.glob("%s/*.py"%(current_folder))
    py_list.extend(py_files)
    for f in glob.glob("%s/*"%(current_folder)):
        if os.path.isdir(f):
            folder_list.append(f)

# update modification time record
if "{cache_file}":
    with open("{cache_file}", 'w') as f:
        for py_file in py_list:
            f.write(py_file + "," + str(int(os.path.getmtime(py_file))) + "\\n")

# remove ignored file from pylist
py_list = set(py_list) - set(ignored_files)

# copy file to other folder
pyx_list = []
for py_file in py_list:
    dst = py_file + 'x'
    shutil.copyfile(py_file, dst)
    pyx_list.append(dst)

print("=" * 10 , "build `.so` files")
rename_list = []
for file in pyx_list:
    print('building ****************', file)
    setup(name="myprint",
          ext_modules=cythonize([file], language_level="3"))
    so_filename = os.path.basename(file).split('.')[0] + ".*.so"
    path = os.path.dirname(file)
    for so_file in glob.glob(so_filename):
        dst = os.path.join(path, so_file)
        so_file_path = os.path.join(os.getcwd(), so_file)
        if os.path.exists(dst) and dst != so_file_path:
            os.remove(dst)
        if dst != so_file_path:
            shutil.move(so_file, path)
        else:
            so_file_new = so_file+'_'
            shutil.move(so_file, so_file_new)
            rename_list.append(so_file_new)
        print('so_file_path:', so_file_path)

# name to original name
for so_file_new in rename_list:
    shutil.move(so_file_new, so_file_new[:-1])

print("=" * 10, "remove generated .pyx and .c files")
for file in py_list:
    c_file = '.'.join(file.split('.')[:-1]) + '.c'
    if os.path.exists(c_file):
        print(":: removing", c_file)
        os.remove(c_file)
    pyx_file = '.'.join(file.split('.')[:-1]) + '.pyx'
    if os.path.exists(pyx_file):
        print(":: removing", pyx_file)
        os.remove(pyx_file)
    keep_py = {keep_py}
    if not keep_py:
        print(":: removing", file)
        os.remove(file)
"""

def main():
    # parse data from folder
    parser = argparse.ArgumentParser(prog='package',
                                     description="Convert python code to dynamic library. Note that the filename should not include '.' excpet suffix",
                                     epilog=example_str,
                                     formatter_class=argparse.RawDescriptionHelpFormatter)
    parser.add_argument("--folder", type=str, help="the project folder needed to package")
    parser.add_argument("--inplace", action="store_true", help="Whether build the code in origin folder")
    parser.add_argument("--ignore", type=str, default="", help="The files will be ignored. Comma should be used to split them if there are more two files. It is related to the path given by `folder` option")
    parser.add_argument("--python", type=str, help="Python interpreter path")
    parser.add_argument("--keep_py", action="store_true", help="Whether to keep original python file")
    parser.add_argument("--build_mode", type=str, default="incremental", help="Build from scratch or start a new session, supported `incremental`(default) and `new`")

    args = parser.parse_args()
    if not args.folder:
        parser.error("`--folder` option must be given")

    # create a new folder
    if not args.inplace:
        build_path = os.path.join(os.path.dirname(args.folder), os.path.basename(args.folder) + '_build')
        if args.build_mode != "incremental":
            while os.path.exists(build_path):
                build_path += '_'
        print('build to {0}'.format(build_path))
        shutil.copytree(args.folder, build_path, dirs_exist_ok=True)
    else:
        build_path = args.folder

    if args.build_mode == "incremental":
        cache_path = os.path.join(args.folder, '.pycodepack')
        cache_file = os.path.join(cache_path, "modinfo.cache")
        if not os.path.exists(cache_path):
            os.mkdir(cache_path)
        if not os.path.exists(cache_file):
            f = open(cache_file, 'w')
            f.close()
    else:
        cache_file = None

    setup_code = template.format(build_path=build_path,
                                 ignore=args.ignore,
                                 keep_py=args.keep_py,
                                 cache_file=cache_file)

    # create setup.py file
    with open(os.path.join(build_path, "setup.py"), 'w') as f:
        f.write(setup_code)

    # build the `.pyx` files to dynamic library
    python_interpreter = args.python if args.python else 'python'
    current_path = os.getcwd()
    os.chdir(build_path)
    ret = os.system(python_interpreter + ( ' setup.py' ' build_ext' ' --inplace') )
    # remove setup.py
    os.remove(os.path.join(build_path, "setup.py"))
    if ret == 0:
        print('Succeed.')
    else:
        print('Failed.')

if __name__ == '__main__':
    main()
