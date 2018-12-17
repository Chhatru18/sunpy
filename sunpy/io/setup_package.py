import os
from distutils.core import Extension
from glob import glob

from astropy_helpers import setup_helpers
from astropy_helpers.distutils_helpers import get_distutils_build_option


def _get_ana_extension():
    cfg = setup_helpers.DistutilsExtensionArgs()
    cfg['include_dirs'].append('numpy')
    cfg['sources'].extend(sorted(glob(os.path.join(os.path.dirname(__file__), 'src', 'ana', '*.c'))))

    if get_distutils_build_option('debug'):
        if setup_helpers.get_compiler_option() == 'msvc':
            cfg['extra_compile_args'].extend(["/Wall"])
        else:
            cfg['extra_compile_args'].extend(["-Werror", "-Wall",
                                              "-Wno-nonnull"])
    else:
        if setup_helpers.get_compiler_option() == 'msvc':
            cfg['extra_compile_args'].extend(['/w'])
        else:
            cfg['extra_compile_args'].extend(['-w'])
    return Extension('sunpy.io._pyana', **cfg)


def get_extensions():
    return [_get_ana_extension()]
