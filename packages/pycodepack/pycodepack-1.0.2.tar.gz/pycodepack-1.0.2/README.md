# pycodepack
Compile python code to dynamic library using `Cython`.

## Installation

```shell
pip install pycodepack
```

## Usage

After installation, there is a runable module called `py2dylib`. Suppose your code is in `/home/code/test_project` and `run.py` is the entrypoint file, you can convert the python files in that folder to dynamic libraries by running

```shell
python -m py2dylib --folder /home/code/test_project --ignore run.py
```

If there is no `/home/code/test_project_build` here, it will copy the folder and compile the python code in that folder. Otherwise, it will try append `_` to the folder until it isn't exist. It's out-of-project building. You can specify `--inplace` option to build in original folder. 

Besides, the`pycodepack` is running under `incremental building` mode by default, which means it only builds those files that changed since last building. You can change it by specifying `--build_mode` option.

Run `python -m py2dylib --help` for more information.
