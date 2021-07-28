from setuptools import setup, find_packages, Extension


try:
    from pybind11.setup_helpers import Pybind11Extension, build_ext as build_ext_orig

except ImportError:
    from setuptools import Extension as Pybind11Extension
    from distutils.command.build_ext import build_ext as build_ext_orig



from glob import glob

import sys
import os
import re

import pathlib


def find_pybind_cmake_dir():
    result = None
    for dirname, dirnames, filenames in os.walk(os.environ['VIRTUAL_ENV']):
        for subdirname in dirnames:
            if(subdirname=='pybind11'):
                result = os.path.join(dirname, subdirname)
                if re.search("share/cmake", result) is not None:
                    return result
    if(result == None):
        log.write("Could not find pybind11 in venv")
    else:
        log.write("Could not find cmake files in pybind11")
    exit()



class CMakeExtension(Extension):

    def __init__(self, name):
        # don't invoke the original build_ext for this special extension
        super().__init__(name, sources=[])   


class build_ext(build_ext_orig):

    def run(self):
        for ext in self.extensions:
            self.build_cmake(ext)
        super().run()

    def build_cmake(self, ext):
        
        cwd = pathlib.Path().absolute()
        cwd = cwd.parent /  (cwd.name + "/minimal") 
        
        build_temp = pathlib.Path(self.build_temp)
        build_temp.mkdir(parents=True, exist_ok=True)
        
        extdir = pathlib.Path(self.get_ext_fullpath(ext.name))

        
        log = open('set_up_log', 'w')
        path = find_pybind_cmake_dir()

        log.write("Cmake pybind files found at:\n")
        log.write(path + "\n")
        log.write(str(extdir.absolute()) +'/build')

        log.close()
        
        # cmake args
        config = 'Debug' if self.debug else 'Release'
        cmake_args = [
            '-DCMAKE_BUILD_TYPE=' + config,
            '-Dpybind11_DIR=' + path
        ]

        build_args = [
            '--config', config,
            '--', '-j4'
        ]

        os.chdir(str(build_temp))
        self.spawn(['cmake', str(cwd)] + cmake_args)
        if not self.dry_run:
            self.spawn(['cmake', '--build', '.'] + build_args)
        # Troubleshooting: if fail on line above then delete all possible 
        # temporary CMake files including "CMakeCache.txt" in top level dir.
        os.chdir(str(cwd))

setup(
    name="minimal",
    version='0.1.0',
    packages=find_packages(),
    ext_modules=[CMakeExtension('moduleCPP')],
    setup_requires=["pybind11>=2.6.2"],
    install_requires=[
        'pybind11>=2.6.2',
    ],
    extras_require={
        
    },

    cmdclass={
        'build_ext': build_ext,
    },
)