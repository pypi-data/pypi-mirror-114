"""A setuptools based setup module.
See:
https://packaging.python.org/guides/distributing-packages-using-setuptools/
https://github.com/pypa/sampleproject
"""

# Always prefer setuptools over distutils
from setuptools import setup, find_packages, Extension
import pathlib

here = pathlib.Path(__file__).parent.resolve()

# Get the long description from the README file
long_description = (here / 'README.md').read_text(encoding='utf-8')

setup(
    name='rwpm',  # Required
    version='0.0.0.1-3',  # Required
    description='A sample Python project',  # Optional
    long_description=long_description,  # Optional
    long_description_content_type='text/markdown',  
    url='https://github.com/rewq/rwpm',  # Optional
    author='rewq',  # Optional
    #author_email='x@cmail.nu',  # Optional
    classifiers=[  # Optional
        # How mature is this project? Common values are
        #   3 - Alpha
        #   4 - Beta
        #   5 - Production/Stable
        'Development Status :: 2 - Pre-Alpha',

        # Indicate who your project is intended for
        'Intended Audience :: Developers',
        'Topic :: Software Development :: Disassemblers',
        'Topic :: Software Development :: Debuggers',
        'Topic :: System :: Operating System Kernels :: Linux',
        'Operating System :: POSIX :: Linux',

        # Pick your license as you wish
        #'License :: OSI Approved :: MIT License',

        # Specify the Python versions you support here. In particular, ensure
        # that you indicate you support Python 3. These classifiers are *not*
        # checked by 'pip install'. See instead 'python_requires' below.
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.6',
        'Programming Language :: Python :: 3.7',
        'Programming Language :: Python :: 3.8',
        'Programming Language :: Python :: 3.9',
        'Programming Language :: Python :: 3 :: Only',
    ],
    keywords='sample, setuptools, development',  # Optional
    #package_dir={'': 'src'},  # Optional
    packages=find_packages(where='src'),  # Required
    python_requires='>=3.6, <4',
    ext_modules = [Extension("rwpm", ["src/rwpm/rwpm.c"],include_dirs=['src/rwpm'])],
    #install_requires=[],  # Optional
    #package_data={},  # Optional
    #data_files=[],  # Optional

    # To provide executable scripts, use entry points in preference to the
    # "scripts" keyword. Entry points provide cross-platform support and allow
    # `pip` to create the appropriate form of executable for the target
    # platform.
    #
    # For example, the following would provide a command called `sample` which
    # executes the function `main` from this package when invoked:
    #entry_points={  # Optional
    #    'console_scripts': [
    #        'sample=sample:main',
    #    ],
    #},

    project_urls={  # Optional
        'Bug Reports': 'https://github.com/rewq/rwpm/issues',
        'Source': 'https://github.com/rewq/rwpm',
    },
)