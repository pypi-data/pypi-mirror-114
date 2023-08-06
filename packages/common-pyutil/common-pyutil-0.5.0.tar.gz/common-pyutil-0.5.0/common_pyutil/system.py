from typing import Union, List
import os
import sys
import importlib.machinery
import importlib.util
from typing import List


class Semver:
    def __init__(self, version_string: str):
        self._version: List[int] = [*map(int, version_string.split("."))]

    def greater_than(self, other: Union["Semver", str]):
        if isinstance(other, str):
            other = Semver(other)
            return self.greater_than(other)
        elif isinstance(other, Semver):
            greater = False
            nolesser = True
            for x, y in zip(self._version, other._version):
                if x > y:
                    greater = True
                    break
                if y > x:
                    nolesser = False
            if len(other) < len(self):
                return nolesser or greater
            else:
                return nolesser and greater

    def equal_to(self, other: Union["Semver", str]):
        if isinstance(other, str):
            other = Semver(other)
            return self.equal_to(other)
        else:
            return len(self) == len(other) and\
                all([x == y for x, y in zip(self._version, other._version)])

    def smaller_than(self, other: Union["Semver", str]):
        if isinstance(other, str):
            other = Semver(other)
            return self.smaller_than(other)
        else:
            return not self.greater_than(other) and not self.equal_to(other)

    def __len__(self):
        return len(self._version)

    def __repr__(self):
        return ".".join(map(str, self._version))


def which(program: str):
    """
    This function is taken from
    http://stackoverflow.com/questions/377017/test-if-executable-exists-in-python
    """
    def is_exe(fpath):
        return os.path.isfile(fpath) and os.access(fpath, os.X_OK)
    fpath, fname = os.path.split(program)
    if fpath:
        if is_exe(program):
            return program
    else:
        for path in os.environ["PATH"].split(os.pathsep):
            path = path.strip('"')
            exe_file = os.path.join(path, program)
            if is_exe(exe_file):
                return exe_file
    return None


def load_user_module(modname: str, search_path: List[str] = None):
    """`search_paths` is a list of paths. Defaults to `sys.path`"""
    if search_path is not None:
        spec = importlib.machinery.PathFinder.find_spec(modname, search_path)
    else:
        if modname.endswith(".py"):
            modname = modname[:-3]
        spec = importlib.machinery.PathFinder.find_spec(modname)
    if spec is None:
        print(f"Could not find module {modname}")
        return None
    mod = importlib.util.module_from_spec(spec)
    sys.modules[modname] = mod
    spec.loader.exec_module(mod)
    return mod
